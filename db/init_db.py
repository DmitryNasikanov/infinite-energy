#!/usr/bin/env python3
"""
Инициализация базы данных номенклатуры проекта «Гелиос»

Схема v3:
- planets: +has_atmosphere, +references (JSON)
- entities → units: +is_assembly, +production_planet_id
- entity_materials → unit_materials: quantity_kg → fraction_pct
"""

import json
import duckdb
from pathlib import Path

DB_PATH = Path(__file__).parent / "helios.duckdb"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"


def create_tables(con):
    """Создание таблиц из schema.sql"""
    schema_sql = SCHEMA_PATH.read_text()
    con.execute(schema_sql)


def seed_planets(con):
    """Планеты солнечной системы"""
    planets = [
        # id, name, gravity, solar_constant, escape_velocity, has_atmosphere, sources (JSON)
        ("earth", "Земля", 9.81, 1361, 11.2, True,
         json.dumps(["https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html"])),

        ("mercury", "Меркурий", 3.7, 10343, 4.25, False,
         json.dumps([
             "https://messenger.jhuapl.edu/",
             "Nittler et al. 2011 - Surface composition",
             "Peplowski et al. 2015 - Elemental abundances"
         ])),

        ("moon", "Луна", 1.62, 1361, 2.38, False,
         json.dumps([
             "https://www.lpi.usra.edu/lunar/samples/",
             "Taylor 1982 - Planetary Science",
             "LROC - Lunar Reconnaissance Orbiter Camera"
         ])),

        ("mars", "Марс", 3.71, 589, 5.03, True,
         json.dumps([
             "https://mars.nasa.gov/",
             "Rieder et al. 2004 - Mars Pathfinder soil composition",
             "ESA Mars Express data"
         ])),
    ]
    con.executemany(
        """INSERT OR REPLACE INTO planets
           (id, name, gravity_m_s2, solar_constant_w_m2, escape_velocity_km_s, has_atmosphere, sources)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        planets
    )


def seed_categories(con):
    """Категории единиц"""
    categories = [
        ("robots", "Роботы"),
        ("facilities", "Объекты/Заводы"),
        ("equipment", "Оборудование"),
        ("products", "Продукция"),
        ("transport", "Транспорт/Контейнеры"),
    ]
    con.executemany(
        "INSERT OR REPLACE INTO categories (id, name) VALUES (?, ?)",
        categories
    )


def seed_materials(con):
    """Материалы с иерархией"""
    materials = [
        # id, parent_id, name, symbol, description, criticality

        # Корневые категории
        ("MAT-METAL", None, "Металлы", None, "Металлы и сплавы", None),
        ("MAT-NONMETAL", None, "Неметаллы", None, "Неметаллические элементы и соединения", None),

        # Металлы
        ("MAT-AL", "MAT-METAL", "Алюминий", "Al", "Зеркала, корпуса, радиаторы, фольга для куполов", "critical"),
        ("MAT-FE", "MAT-METAL", "Железо", "Fe", "Рамы, шасси, конструкции", "critical"),
        ("MAT-FE-MN", "MAT-FE", "Сталь Fe-6%Mn", None, "Прочная сталь без углерода, легированная марганцем", "high"),
        ("MAT-MG", "MAT-METAL", "Магний", "Mg", "Лёгкие сплавы, пиротехника", "high"),
        ("MAT-TI", "MAT-METAL", "Титан", "Ti", "Электрохромика зеркал, прочные узлы", "medium"),
        ("MAT-NA", "MAT-METAL", "Натрий", "Na", "Батареи NaS (анод)", "high"),
        ("MAT-MN", "MAT-METAL", "Марганец", "Mn", "Легирование стали Fe-6%Mn", "medium"),
        ("MAT-IR", "MAT-METAL", "Иридий", "Ir", "Аноды MRE-ячеек (устойчивость к расплаву)", "medium"),
        ("MAT-PT", "MAT-METAL", "Платина", "Pt", "Фильеры для волочения стекловолокна", "medium"),
        ("MAT-W", "MAT-METAL", "Вольфрам", "W", "Фрезы CNC, инструмент", "medium"),

        # Неметаллы
        ("MAT-O2", "MAT-NONMETAL", "Кислород", "O₂", "Главный продукт MRE, побочный продукт", "critical"),
        ("MAT-SI", "MAT-NONMETAL", "Кремний", "Si", "Стекловолокно, электроника, солнечные панели", "critical"),
        ("MAT-S", "MAT-NONMETAL", "Сера", "S", "Батареи NaS (катод)", "high"),
        ("MAT-C", "MAT-NONMETAL", "Углерод/Графит", "C", "Композиты, восстановитель Ti, термозащита", "high"),
        ("MAT-K", "MAT-NONMETAL", "Калий", "K", "Удобрения, химические процессы", "low"),
    ]
    con.executemany(
        "INSERT OR REPLACE INTO materials (id, parent_id, name, symbol, description, criticality) VALUES (?, ?, ?, ?, ?, ?)",
        materials
    )


def seed_planet_materials(con):
    """Связь материалов с планетами"""
    planet_materials = [
        # planet_id, material_id, concentration_pct, notes

        # Меркурий (основная база)
        ("mercury", "MAT-O2", 42, "главный продукт MRE"),
        ("mercury", "MAT-MG", 8, None),
        ("mercury", "MAT-AL", 7, None),
        ("mercury", "MAT-SI", 4.2, None),
        ("mercury", "MAT-NA", 3.3, None),
        ("mercury", "MAT-S", 3, None),
        ("mercury", "MAT-FE", 1.7, None),
        ("mercury", "MAT-K", 0.5, None),
        ("mercury", "MAT-TI", 0.5, "из ильменита TiO₂"),
        ("mercury", "MAT-MN", 0.1, None),
        ("mercury", "MAT-C", 2, "только LRM-зоны (полярные кратеры)"),

        # Луна
        ("moon", "MAT-O2", 45, None),
        ("moon", "MAT-SI", 21, None),
        ("moon", "MAT-AL", 10, "в анортозите"),
        ("moon", "MAT-FE", 8, "в базальтах"),
        ("moon", "MAT-TI", 1.5, "в ильмените"),
        ("moon", "MAT-MG", 5, None),

        # Марс
        ("mars", "MAT-O2", 45, None),
        ("mars", "MAT-SI", 21, None),
        ("mars", "MAT-FE", 14, "в оксидах (красный цвет)"),
        ("mars", "MAT-MG", 3, None),

        # Земля (импорт — concentration = NULL)
        ("earth", "MAT-IR", None, "импорт, аноды MRE"),
        ("earth", "MAT-PT", None, "импорт, фильеры стекловолокна"),
        ("earth", "MAT-W", None, "импорт, фрезы CNC"),
    ]
    con.executemany(
        "INSERT OR REPLACE INTO planet_materials (planet_id, material_id, concentration_pct, notes) VALUES (?, ?, ?, ?)",
        planet_materials
    )


def seed_units(con):
    """Единицы проекта (бывш. entities)"""
    units = [
        # id, category_id, name, description, mass_kg, power_kw, parent_id, is_assembly, production_planet_id

        # Роботы (все — сборки, производятся на Меркурии)
        ("ROB-001", "robots", "Кракен", "Тяжёлый транспортный робот, 8 ног, 5 т груз", 2000, 50, None, True, "mercury"),
        ("ROB-002", "robots", "Кентавр", "Сборочный робот-манипулятор", 500, 15, None, True, "mercury"),
        ("ROB-003", "robots", "Краб", "Логистический робот, 6 ног", 200, 10, None, True, "mercury"),
        ("ROB-004", "robots", "Крот", "Бурильный робот", 800, 30, None, True, "mercury"),
        ("ROB-005", "robots", "Паук", "Сервисный робот, высотные работы", 150, 5, None, True, "mercury"),

        # Заводы (сборки)
        ("FAC-001", "facilities", "Точка Ноль", "Основной завод на северном полюсе Меркурия", None, 55000, None, True, "mercury"),
        ("FAC-002", "facilities", "Комплекс Карбон-Север", "Мини-завод по добыче графита (LRM)", None, 5000, None, True, "mercury"),
        ("FAC-003", "facilities", "Комплекс Карбон-Юг", "Мини-завод по добыче графита (LRM)", None, 5000, None, True, "mercury"),

        # Оборудование (вложено в FAC-001, сборки)
        ("EQU-001", "equipment", "Масс-драйвер", "Электромагнитная катапульта, 3 км", 1300000, 33000, "FAC-001", True, "mercury"),
        ("EQU-002", "equipment", "MRE-ячейка", "Электролиз расплава реголита", 5000, 500, "FAC-001", True, "mercury"),
        ("EQU-003", "equipment", "Солнечная печь", "Концентратор для плавки реголита", 2000, 0, "FAC-001", True, "mercury"),
        ("EQU-004", "equipment", "Щековая дробилка", "Дробление реголита <10мм", 3000, 50, "FAC-001", True, "mercury"),
        ("EQU-005", "equipment", "Магнитный сепаратор", "Разделение магнитной/немагнитной фракций", 500, 20, "FAC-001", True, "mercury"),
        ("EQU-006", "equipment", "МНЛЗ-Al", "Машина непрерывного литья алюминия", 8000, 100, "FAC-001", True, "mercury"),
        ("EQU-007", "equipment", "МНЛЗ-Fe", "Машина непрерывного литья стали", 10000, 150, "FAC-001", True, "mercury"),
        ("EQU-008", "equipment", "Прокатный стан", "6-клетьевой стан для проката профиля", 15000, 200, "FAC-001", True, "mercury"),
        ("EQU-009", "equipment", "WAAM-ячейка", "3D-печать дуговой наплавкой", 2000, 50, "FAC-001", True, "mercury"),
        ("EQU-010", "equipment", "CNC 5-осевой", "Фрезерный станок для чистовой обработки", 3000, 30, "FAC-001", True, "mercury"),
        ("EQU-011", "equipment", "Мини масс-драйвер", "МД для комплексов Карбон, 500м-1км", 330000, 500, None, True, "mercury"),

        # Импортное оборудование (простые единицы, с Земли)
        ("EQU-012", "equipment", "Электроника сенсоров", "Микроконтроллеры, датчики, камеры", 20, 0, None, False, "earth"),
        ("EQU-013", "equipment", "Фильеры платиновые", "Фильеры для волочения стекловолокна", 0.5, 0, None, False, "earth"),
        ("EQU-014", "equipment", "Аноды иридиевые", "Аноды для MRE-ячеек", 2, 0, None, False, "earth"),

        # Продукция
        ("PRD-001", "products", "Зеркало Роя", "Алюминиевое зеркало 30×30м с электрохромикой", 116, 0, None, True, "mercury"),
        ("PRD-002", "products", "Робот Gen-2", "Робот второго поколения (местное производство)", 320, 15, None, True, "mercury"),
        ("PRD-003", "products", "Купол", "Силикатный купол для завода", 8000, 0, None, True, "mercury"),

        # Транспорт
        ("TRN-001", "transport", "Контейнер графита", "Баллистический контейнер 100кг", 20, 0, None, True, "mercury"),
    ]
    con.executemany(
        """INSERT OR REPLACE INTO units
           (id, category_id, name, description, mass_kg, power_kw, parent_id, is_assembly, production_planet_id)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        units
    )


def seed_unit_components(con):
    """Компоненты сборок (unit → unit, M:N)"""
    components = [
        # assembly_id, component_id, quantity

        # Роботы содержат электронику
        ("ROB-001", "EQU-012", 8),   # Кракен — 8 блоков электроники
        ("ROB-002", "EQU-012", 5),   # Кентавр — 5 блоков
        ("ROB-003", "EQU-012", 4),   # Краб — 4 блока
        ("ROB-004", "EQU-012", 6),   # Крот — 6 блоков
        ("ROB-005", "EQU-012", 3),   # Паук — 3 блока
        ("PRD-002", "EQU-012", 3),   # Робот Gen-2 — 3 блока

        # MRE-ячейка содержит иридиевые аноды
        ("EQU-002", "EQU-014", 4),   # 4 анода на ячейку

        # Завод Точка Ноль содержит оборудование (уже связано через parent_id)
        # но для полноты добавим количество MRE-ячеек и проч.
        ("FAC-001", "EQU-002", 20),  # 20 MRE-ячеек
        ("FAC-001", "EQU-003", 5),   # 5 солнечных печей
        ("FAC-001", "EQU-004", 3),   # 3 дробилки
        ("FAC-001", "EQU-005", 2),   # 2 магнитных сепаратора

        # Масс-драйвер содержит электронику
        ("EQU-001", "EQU-012", 100), # 100 блоков управления
    ]
    con.executemany(
        "INSERT OR REPLACE INTO unit_components (assembly_id, component_id, quantity) VALUES (?, ?, ?)",
        components
    )


def seed_unit_materials(con):
    """BOM — состав единиц (fraction_pct вместо quantity_kg)"""
    # Пересчитаем из старых данных:
    # PRD-002 (320 кг): FE=150кг→46.9%, AL=50кг→15.6%, NA=50кг→15.6%, S=50кг→15.6%
    # PRD-001 (116 кг): AL=100кг→86.2%, TI=5кг→4.3%
    # EQU-001 (1300000 кг): FE=800000кг→61.5%, AL=300000кг→23.1%, SI=50000кг→3.8%
    # PRD-003 (8000 кг): SI=7500кг→93.75%, AL=500кг→6.25%

    bom = [
        # unit_id, material_id, fraction_pct

        # Робот Gen-2 (PRD-002, 320 кг)
        ("PRD-002", "MAT-FE", 46.9),    # 150 кг рама, шасси
        ("PRD-002", "MAT-AL", 15.6),    # 50 кг корпус, радиаторы
        ("PRD-002", "MAT-NA", 15.6),    # 50 кг батарея NaS (Na)
        ("PRD-002", "MAT-S", 15.6),     # 50 кг батарея NaS (S)
        # Итого: 93.7% (остальное — электроника с Земли)

        # Зеркало Роя (PRD-001, 116 кг)
        ("PRD-001", "MAT-AL", 86.2),    # 100 кг фольга + каркас
        ("PRD-001", "MAT-TI", 4.3),     # 5 кг электрохромика TiO₂
        # Итого: 90.5%

        # Масс-драйвер (EQU-001, 1300000 кг = 1300 т)
        ("EQU-001", "MAT-FE", 61.5),    # 800 т каркас тоннеля
        ("EQU-001", "MAT-AL", 23.1),    # 300 т рельсы, обмотки
        ("EQU-001", "MAT-SI", 3.8),     # 50 т электроника
        # Итого: 88.4%

        # Купол (PRD-003, 8000 кг)
        ("PRD-003", "MAT-SI", 93.75),   # 7500 кг силикатная ткань
        ("PRD-003", "MAT-AL", 6.25),    # 500 кг газонепроницаемая мембрана
        # Итого: 100%
    ]
    con.executemany(
        "INSERT OR REPLACE INTO unit_materials (unit_id, material_id, fraction_pct) VALUES (?, ?, ?)",
        bom
    )


def main():
    print(f"Инициализация базы данных v3: {DB_PATH}")

    # Удаляем старую БД если есть
    if DB_PATH.exists():
        DB_PATH.unlink()
        print("  Удалена старая БД")

    con = duckdb.connect(str(DB_PATH))

    print("  Создание таблиц...")
    create_tables(con)

    print("  Добавление планет...")
    seed_planets(con)

    print("  Добавление категорий...")
    seed_categories(con)

    print("  Добавление материалов...")
    seed_materials(con)

    print("  Добавление связей планета-материал...")
    seed_planet_materials(con)

    print("  Добавление единиц...")
    seed_units(con)

    print("  Добавление BOM...")
    seed_unit_materials(con)

    print("  Добавление компонентов сборок...")
    seed_unit_components(con)

    con.close()
    print(f"\nГотово! База данных: {DB_PATH}")
    print(f"Размер: {DB_PATH.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
