#!/usr/bin/env python3
"""
Экспорт базы данных номенклатуры в JSON для веб-интерфейса

Выходные файлы (db/export/):
- planets.json
- materials.json
- units.json
- planet_materials.json
- unit_materials.json
- unit_components.json
"""

import json
import duckdb
from pathlib import Path

DB_PATH = Path(__file__).parent / "helios.duckdb"
EXPORT_DIR = Path(__file__).parent / "export"


def export_planets(con):
    """Экспорт планет"""
    rows = con.execute("""
        SELECT id, name, gravity_m_s2, solar_constant_w_m2,
               escape_velocity_km_s, has_atmosphere, sources
        FROM planets
    """).fetchall()

    planets = []
    for row in rows:
        planets.append({
            "id": row[0],
            "name": row[1],
            "gravity_m_s2": float(row[2]) if row[2] else None,
            "solar_constant_w_m2": float(row[3]) if row[3] else None,
            "escape_velocity_km_s": float(row[4]) if row[4] else None,
            "has_atmosphere": row[5],
            "sources": json.loads(row[6]) if row[6] else []
        })
    return planets


def export_materials(con):
    """Экспорт материалов"""
    rows = con.execute("""
        SELECT id, parent_id, name, symbol, description, criticality
        FROM materials
    """).fetchall()

    materials = []
    for row in rows:
        materials.append({
            "id": row[0],
            "parent_id": row[1],
            "name": row[2],
            "symbol": row[3],
            "description": row[4],
            "criticality": row[5]
        })
    return materials


def export_units(con):
    """Экспорт единиц"""
    rows = con.execute("""
        SELECT id, category_id, name, description, mass_kg, power_kw,
               parent_id, is_assembly, production_planet_id
        FROM units
    """).fetchall()

    units = []
    for row in rows:
        units.append({
            "id": row[0],
            "category_id": row[1],
            "name": row[2],
            "description": row[3],
            "mass_kg": float(row[4]) if row[4] else None,
            "power_kw": float(row[5]) if row[5] else None,
            "parent_id": row[6],
            "is_assembly": row[7],
            "production_planet_id": row[8]
        })
    return units


def export_planet_materials(con):
    """Экспорт связей планета-материал"""
    rows = con.execute("""
        SELECT planet_id, material_id, concentration_pct, notes
        FROM planet_materials
    """).fetchall()

    links = []
    for row in rows:
        links.append({
            "planet_id": row[0],
            "material_id": row[1],
            "concentration_pct": float(row[2]) if row[2] else None,
            "notes": row[3]
        })
    return links


def export_unit_materials(con):
    """Экспорт BOM (состав из материалов)"""
    rows = con.execute("""
        SELECT unit_id, material_id, fraction_pct
        FROM unit_materials
    """).fetchall()

    bom = []
    for row in rows:
        bom.append({
            "unit_id": row[0],
            "material_id": row[1],
            "fraction_pct": float(row[2]) if row[2] else None
        })
    return bom


def export_unit_components(con):
    """Экспорт состава сборок (unit → unit)"""
    rows = con.execute("""
        SELECT assembly_id, component_id, quantity
        FROM unit_components
    """).fetchall()

    components = []
    for row in rows:
        components.append({
            "assembly_id": row[0],
            "component_id": row[1],
            "quantity": row[2]
        })
    return components


def export_categories(con):
    """Экспорт категорий"""
    rows = con.execute("""
        SELECT id, name FROM categories
    """).fetchall()

    categories = []
    for row in rows:
        categories.append({
            "id": row[0],
            "name": row[1]
        })
    return categories


def main():
    print(f"Экспорт базы данных: {DB_PATH}")

    if not DB_PATH.exists():
        print("ОШИБКА: База данных не найдена. Запустите init_db.py")
        return

    EXPORT_DIR.mkdir(exist_ok=True)

    con = duckdb.connect(str(DB_PATH), read_only=True)

    exports = [
        ("planets.json", export_planets),
        ("materials.json", export_materials),
        ("categories.json", export_categories),
        ("units.json", export_units),
        ("planet_materials.json", export_planet_materials),
        ("unit_materials.json", export_unit_materials),
        ("unit_components.json", export_unit_components),
    ]

    for filename, export_func in exports:
        data = export_func(con)
        filepath = EXPORT_DIR / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  {filename}: {len(data)} записей")

    con.close()
    print(f"\nГотово! Файлы в: {EXPORT_DIR}")


if __name__ == "__main__":
    main()
