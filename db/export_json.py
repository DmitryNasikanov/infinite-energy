#!/usr/bin/env python3
"""
Экспорт базы данных номенклатуры в JSON для веб-интерфейса

Поддержка i18n: экспорт для русского и английского языков
"""

import json
import duckdb
from pathlib import Path

DB_PATH = Path(__file__).parent / "helios.duckdb"
EXPORT_DIR = Path(__file__).parent / "export"


def export_planets(con, lang='ru'):
    """Экспорт планет"""
    name_field = 'name_ru' if lang == 'ru' else 'name_en'
    rows = con.execute(f"""
        SELECT id, {name_field}, gravity_m_s2, solar_constant_w_m2,
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


def export_materials(con, lang='ru'):
    """Экспорт материалов"""
    name_field = 'name_ru' if lang == 'ru' else 'name_en'
    desc_field = 'description_ru' if lang == 'ru' else 'description_en'
    rows = con.execute(f"""
        SELECT id, parent_id, {name_field}, symbol, {desc_field}, criticality, sources
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
            "criticality": row[5],
            "sources": json.loads(row[6]) if row[6] else []
        })
    return materials


def export_units(con, lang='ru'):
    """Экспорт единиц"""
    name_field = 'name_ru' if lang == 'ru' else 'name_en'
    desc_field = 'description_ru' if lang == 'ru' else 'description_en'
    rows = con.execute(f"""
        SELECT id, category_id, {name_field}, {desc_field}, mass_kg, power_kw,
               parent_id, is_assembly, production_planet_id, sources
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
            "production_planet_id": row[8],
            "sources": json.loads(row[9]) if row[9] else []
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


def export_categories(con, lang='ru'):
    """Экспорт категорий"""
    name_field = 'name_ru' if lang == 'ru' else 'name_en'
    rows = con.execute(f"""
        SELECT id, {name_field} FROM categories
    """).fetchall()

    categories = []
    for row in rows:
        categories.append({
            "id": row[0],
            "name": row[1]
        })
    return categories


def export_all_for_lang(con, lang='ru'):
    """Экспорт всех данных для указанного языка"""
    return {
        "planets": export_planets(con, lang),
        "materials": export_materials(con, lang),
        "categories": export_categories(con, lang),
        "units": export_units(con, lang),
        "planet_materials": export_planet_materials(con),
        "unit_materials": export_unit_materials(con),
        "unit_components": export_unit_components(con),
    }


def generate_data_json(all_data, output_path):
    """Генерация data.json для OJS виджетов"""
    ojs_data = {
        "planets": all_data["planets"],
        "materials": all_data["materials"],
        "categories": all_data["categories"],
        "units": all_data["units"],
        "planetMaterials": all_data["planet_materials"],
        "unitMaterials": all_data["unit_materials"],
        "unitComponents": all_data["unit_components"],
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(ojs_data, f, ensure_ascii=False, indent=2)


def generate_data_js(data_dict, output_path):
    """Генерация data.js для веб-интерфейса"""
    js_content = "const DATA = {\n"

    items = [
        ("planets", data_dict["planets"]),
        ("materials", data_dict["materials"]),
        ("categories", data_dict["categories"]),
        ("units", data_dict["units"]),
        ("planetMaterials", data_dict["planet_materials"]),
        ("unitMaterials", data_dict["unit_materials"]),
        ("unitComponents", data_dict["unit_components"]),
    ]

    for i, (key, data) in enumerate(items):
        json_str = json.dumps(data, ensure_ascii=False)
        comma = "," if i < len(items) - 1 else ""
        js_content += f"  {key}: {json_str}{comma}\n"

    js_content += "};\n"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(js_content)


def main():
    print(f"Экспорт базы данных: {DB_PATH}")

    if not DB_PATH.exists():
        print("ОШИБКА: База данных не найдена. Запустите init_db.py")
        return

    EXPORT_DIR.mkdir(exist_ok=True)

    con = duckdb.connect(str(DB_PATH), read_only=True)

    # Пути для экспорта
    base_path = Path(__file__).parent.parent

    # Экспорт для русского языка
    print("\n  Экспорт RU:")
    ru_data = export_all_for_lang(con, 'ru')
    ru_json_path = base_path / "ru" / "science" / "data" / "db" / "data.json"
    ru_js_path = base_path / "ru" / "science" / "data" / "db" / "data.js"
    generate_data_json(ru_data, ru_json_path)
    generate_data_js(ru_data, ru_js_path)
    print(f"    data.json: {ru_json_path}")
    print(f"    data.js: {ru_js_path}")

    # Экспорт для английского языка
    print("\n  Экспорт EN:")
    en_data = export_all_for_lang(con, 'en')
    en_json_path = base_path / "en" / "science" / "data" / "db" / "data.json"
    en_js_path = base_path / "en" / "science" / "data" / "db" / "data.js"
    generate_data_json(en_data, en_json_path)
    generate_data_js(en_data, en_js_path)
    print(f"    data.json: {en_json_path}")
    print(f"    data.js: {en_js_path}")

    # Также экспортируем отдельные JSON файлы в db/export/ (для совместимости)
    print("\n  Экспорт в db/export/ (RU):")
    exports = [
        ("planets.json", ru_data["planets"]),
        ("materials.json", ru_data["materials"]),
        ("categories.json", ru_data["categories"]),
        ("units.json", ru_data["units"]),
        ("planet_materials.json", ru_data["planet_materials"]),
        ("unit_materials.json", ru_data["unit_materials"]),
        ("unit_components.json", ru_data["unit_components"]),
    ]
    for filename, data in exports:
        filepath = EXPORT_DIR / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"    {filename}: {len(data)} записей")

    con.close()
    print(f"\nГотово!")


if __name__ == "__main__":
    main()
