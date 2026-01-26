#!/usr/bin/env python3
"""
Валидация базы данных Гелиос.
Проверяет целостность данных и предотвращает ошибки типа "BOM ≠ 100%".
"""

import sys
from pathlib import Path

import duckdb

DB_PATH = Path(__file__).parent / "helios.duckdb"


def validate_bom_percentages(con) -> list[str]:
    """Проверка: сумма BOM для каждого юнита = 100%"""
    errors = []

    result = con.execute("""
        SELECT
            um.unit_id,
            u.name_ru,
            ROUND(SUM(um.fraction_pct), 2) as total_pct
        FROM unit_materials um
        JOIN units u ON u.id = um.unit_id
        GROUP BY um.unit_id, u.name_ru
        HAVING ABS(100 - SUM(um.fraction_pct)) > 0.1
    """).fetchall()

    for unit_id, name, total in result:
        errors.append(f"  {unit_id} ({name}): {total}% вместо 100%")

    return errors


def validate_bom_references(con) -> list[str]:
    """Проверка: все material_id и unit_id в BOM существуют"""
    errors = []

    # Несуществующие материалы
    result = con.execute("""
        SELECT DISTINCT um.material_id
        FROM unit_materials um
        LEFT JOIN materials m ON m.id = um.material_id
        WHERE m.id IS NULL
    """).fetchall()
    for (mat_id,) in result:
        errors.append(f"  material_id '{mat_id}' не существует")

    # Несуществующие юниты
    result = con.execute("""
        SELECT DISTINCT um.unit_id
        FROM unit_materials um
        LEFT JOIN units u ON u.id = um.unit_id
        WHERE u.id IS NULL
    """).fetchall()
    for (unit_id,) in result:
        errors.append(f"  unit_id '{unit_id}' не существует")

    return errors


def validate_assembly_references(con) -> list[str]:
    """Проверка: ссылки в unit_components корректны"""
    errors = []

    # assembly_id должен быть сборкой
    result = con.execute("""
        SELECT DISTINCT uc.assembly_id, u.name_ru, u.is_assembly
        FROM unit_components uc
        JOIN units u ON u.id = uc.assembly_id
        WHERE u.is_assembly = false
    """).fetchall()
    for assembly_id, name, _ in result:
        errors.append(f"  {assembly_id} ({name}) — не сборка, но содержит компоненты")

    # component_id должен существовать
    result = con.execute("""
        SELECT DISTINCT uc.component_id
        FROM unit_components uc
        LEFT JOIN units u ON u.id = uc.component_id
        WHERE u.id IS NULL
    """).fetchall()
    for (comp_id,) in result:
        errors.append(f"  component_id '{comp_id}' не существует")

    return errors


def validate_circular_dependencies(con) -> list[str]:
    """Проверка: нет циклических зависимостей в сборках"""
    errors = []

    # Получаем все связи
    edges = con.execute("""
        SELECT assembly_id, component_id FROM unit_components
    """).fetchall()

    # Строим граф
    graph = {}
    for assembly, component in edges:
        if assembly not in graph:
            graph[assembly] = []
        graph[assembly].append(component)

    # DFS для поиска циклов
    def has_cycle(node, visited, rec_stack, path):
        visited.add(node)
        rec_stack.add(node)
        path.append(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                cycle = has_cycle(neighbor, visited, rec_stack, path)
                if cycle:
                    return cycle
            elif neighbor in rec_stack:
                # Нашли цикл
                cycle_start = path.index(neighbor)
                return path[cycle_start:] + [neighbor]

        path.pop()
        rec_stack.remove(node)
        return None

    visited = set()
    for node in graph:
        if node not in visited:
            cycle = has_cycle(node, visited, set(), [])
            if cycle:
                errors.append(f"  Цикл: {' → '.join(cycle)}")
                break

    return errors


def validate_planet_materials(con) -> list[str]:
    """Проверка: все материалы (кроме категорий) привязаны к планетам"""
    errors = []

    # Исключаем категории (parent_id IS NULL)
    result = con.execute("""
        SELECT m.id, m.name_ru
        FROM materials m
        LEFT JOIN planet_materials pm ON pm.material_id = m.id
        WHERE pm.material_id IS NULL
          AND m.parent_id IS NOT NULL
    """).fetchall()

    for mat_id, name in result:
        errors.append(f"  {mat_id} ({name}) — не привязан ни к одной планете")

    return errors


def validate_units_have_bom(con) -> list[str]:
    """Проверка: все местные простые юниты имеют BOM"""
    errors = []

    # Исключаем импортные юниты (production_planet_id = 'earth')
    # и сборки (is_assembly = true)
    result = con.execute("""
        SELECT u.id, u.name_ru
        FROM units u
        LEFT JOIN unit_materials um ON um.unit_id = u.id
        WHERE um.unit_id IS NULL
          AND u.is_assembly = false
          AND u.production_planet_id != 'earth'
    """).fetchall()

    for unit_id, name in result:
        errors.append(f"  {unit_id} ({name}) — нет BOM")

    return errors


def validate_unused_materials(con) -> list[str]:
    """Предупреждение: неиспользуемые материалы (кроме категорий)"""
    warnings = []

    # Исключаем категории (parent_id IS NULL)
    result = con.execute("""
        SELECT m.id, m.name_ru
        FROM materials m
        LEFT JOIN unit_materials um ON um.material_id = m.id
        WHERE um.material_id IS NULL
          AND m.parent_id IS NOT NULL
    """).fetchall()

    for mat_id, name in result:
        warnings.append(f"  {mat_id} ({name}) — не используется")

    return warnings


def validate(db_path: Path = DB_PATH, verbose: bool = True) -> bool:
    """
    Запуск всех проверок.
    Возвращает True если база валидна, False если есть ошибки.
    """
    if not db_path.exists():
        print(f"❌ База данных не найдена: {db_path}")
        return False

    con = duckdb.connect(str(db_path), read_only=True)

    if verbose:
        print("Валидация базы данных...")

    all_valid = True

    # Критические проверки (блокируют)
    checks = [
        ("BOM: суммы = 100%", validate_bom_percentages),
        ("BOM: ссылки на материалы/юниты", validate_bom_references),
        ("Сборки: ссылки на компоненты", validate_assembly_references),
        ("Сборки: циклические зависимости", validate_circular_dependencies),
        ("Материалы: привязка к планетам", validate_planet_materials),
        ("Юниты: наличие BOM", validate_units_have_bom),
    ]

    for name, check_fn in checks:
        errors = check_fn(con)
        if errors:
            print(f"❌ {name}")
            for err in errors:
                print(err)
            all_valid = False
        elif verbose:
            print(f"✓ {name}")

    # Предупреждения (не блокируют)
    warnings = validate_unused_materials(con)
    if warnings and verbose:
        print(f"⚠ Неиспользуемые материалы ({len(warnings)})")
        for w in warnings:
            print(w)

    con.close()

    if verbose:
        if all_valid:
            print("✅ База данных валидна")
        else:
            print("❌ Обнаружены ошибки")

    return all_valid


if __name__ == "__main__":
    valid = validate()
    sys.exit(0 if valid else 1)
