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
        SELECT id, parent_id, name, symbol, description, criticality, sources
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


def export_units(con):
    """Экспорт единиц"""
    rows = con.execute("""
        SELECT id, category_id, name, description, mass_kg, power_kw,
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

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(js_content)


def generate_nomenclature_html(data_dict, output_path):
    """Генерация полной HTML страницы номенклатуры"""

    # Генерируем DATA объект
    data_items = [
        ("planets", data_dict["planets"]),
        ("materials", data_dict["materials"]),
        ("categories", data_dict["categories"]),
        ("units", data_dict["units"]),
        ("planetMaterials", data_dict["planet_materials"]),
        ("unitMaterials", data_dict["unit_materials"]),
        ("unitComponents", data_dict["unit_components"]),
    ]
    data_js = "const DATA = {\n"
    for i, (key, data) in enumerate(data_items):
        json_str = json.dumps(data, ensure_ascii=False)
        comma = "," if i < len(data_items) - 1 else ""
        data_js += f"  {key}: {json_str}{comma}\n"
    data_js += "};"

    html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Номенклатура — Проект Гелиос</title>
<style>
body {{
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
  line-height: 1.6;
}}
h1 {{ margin-bottom: 0.5rem; }}
.controls {{ margin-bottom: 1.5rem; }}
.controls select {{ padding: 0.5rem; font-size: 1rem; min-width: 300px; }}
.card {{
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1rem;
}}
.card.hidden {{ display: none; }}
.card h3 {{ margin-top: 0; margin-bottom: 0.5rem; }}
.card .meta {{ color: #6c757d; margin-bottom: 1rem; font-size: 0.9rem; }}
.badge {{
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  margin-right: 0.5rem;
}}
.badge.assembly {{ background: #d4edda; color: #155724; }}
.badge.simple {{ background: #f8d7da; color: #721c24; }}
.badge.critical {{ background: #f5c6cb; color: #721c24; }}
.badge.high {{ background: #ffeeba; color: #856404; }}
.badge.medium {{ background: #bee5eb; color: #0c5460; }}
.badge.low {{ background: #d6d8db; color: #383d41; }}
.card table {{ width: 100%; border-collapse: collapse; margin-top: 0.5rem; }}
.card th, .card td {{ padding: 0.5rem; text-align: left; border-bottom: 1px solid #dee2e6; }}
.card th {{ font-weight: 600; }}
.link {{ color: #0d6efd; cursor: pointer; text-decoration: underline; }}
.link:hover {{ color: #0a58ca; }}
.section {{ margin-top: 1rem; }}
.section h4 {{ margin-bottom: 0.5rem; font-size: 1rem; }}
#stats table {{ border-collapse: collapse; }}
#stats td {{ padding: 0.25rem 1rem 0.25rem 0; }}
#units-list h4 {{ margin-top: 1rem; margin-bottom: 0.5rem; }}
#units-list ul {{ margin: 0; padding-left: 1.5rem; }}
#units-list li {{ margin-bottom: 0.25rem; }}
hr {{ border: none; border-top: 1px solid #dee2e6; margin: 2rem 0; }}
</style>
<script>
{data_js}
</script>
</head>
<body>

<h1>Номенклатура</h1>
<p>Интерактивный браузер базы данных единиц проекта «Гелиос».</p>

<div id="app">
  <div class="controls">
    <label for="unit-select">Единица:</label>
    <select id="unit-select">
      <option value="">-- Выберите единицу --</option>
    </select>
  </div>
  <div id="unit-card" class="card hidden"></div>
</div>

<hr>
<h2>Статистика базы данных</h2>
<div id="stats"></div>

<hr>
<h2>Все единицы по категориям</h2>
<div id="units-list"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {{
  const planetsById = new Map(DATA.planets.map(p => [p.id, p]));
  const materialsById = new Map(DATA.materials.map(m => [m.id, m]));
  const categoriesById = new Map(DATA.categories.map(c => [c.id, c]));
  const unitsById = new Map(DATA.units.map(u => [u.id, u]));

  const select = document.getElementById('unit-select');
  DATA.units.forEach(u => {{
    const opt = document.createElement('option');
    opt.value = u.id;
    opt.textContent = u.id + ' — ' + u.name;
    select.appendChild(opt);
  }});

  function selectUnit(unitId) {{
    select.value = unitId;
    renderUnit(unitId);
  }}

  function renderUnit(unitId) {{
    const card = document.getElementById('unit-card');
    if (!unitId) {{ card.classList.add('hidden'); card.innerHTML = ''; return; }}
    const unit = unitsById.get(unitId);
    if (!unit) {{ card.classList.add('hidden'); return; }}

    const category = categoriesById.get(unit.category_id);
    const planet = planetsById.get(unit.production_planet_id);

    const bom = DATA.unitMaterials
      .filter(um => um.unit_id === unitId)
      .map(um => ({{
        ...um,
        material: materialsById.get(um.material_id),
        mass_kg: unit.mass_kg ? (unit.mass_kg * um.fraction_pct / 100).toFixed(1) : null
      }}));

    const components = DATA.unitComponents
      .filter(uc => uc.assembly_id === unitId)
      .map(uc => ({{ ...uc, component: unitsById.get(uc.component_id) }}));

    const usedIn = DATA.unitComponents
      .filter(uc => uc.component_id === unitId)
      .map(uc => ({{ ...uc, assembly: unitsById.get(uc.assembly_id) }}));

    let html = '<h3>' + unit.name + '</h3><div class="meta">' +
      '<span class="badge ' + (unit.is_assembly ? 'assembly' : 'simple') + '">' +
      (unit.is_assembly ? 'Сборка' : 'Простая единица') + '</span>' +
      (category ? '<span>' + category.name + '</span>' : '') +
      (unit.mass_kg ? ' | <strong>' + unit.mass_kg.toLocaleString() + '</strong> кг' : '') +
      (unit.power_kw ? ' | <strong>' + unit.power_kw.toLocaleString() + '</strong> кВт' : '') +
      '</div>';

    if (unit.description) html += '<p>' + unit.description + '</p>';
    if (planet) html += '<div class="section"><strong>Производство:</strong> ' + planet.name + (planet.id === 'earth' ? ' (импорт)' : '') + '</div>';

    if (components.length > 0) {{
      html += '<div class="section"><h4>Компоненты (' + components.length + '):</h4><table><thead><tr><th>Компонент</th><th>Кол-во</th></tr></thead><tbody>';
      components.forEach(c => {{
        html += '<tr><td><span class="link" data-unit="' + c.component_id + '">' + (c.component?.name || c.component_id) + '</span></td><td>' + c.quantity + ' шт</td></tr>';
      }});
      html += '</tbody></table></div>';
    }}

    if (usedIn.length > 0) {{
      html += '<div class="section"><h4>Используется в (' + usedIn.length + '):</h4><table><thead><tr><th>Сборка</th><th>Кол-во</th></tr></thead><tbody>';
      usedIn.forEach(u => {{
        html += '<tr><td><span class="link" data-unit="' + u.assembly_id + '">' + (u.assembly?.name || u.assembly_id) + '</span></td><td>' + u.quantity + ' шт</td></tr>';
      }});
      html += '</tbody></table></div>';
    }}

    if (bom.length > 0) {{
      html += '<div class="section"><h4>Состав (BOM):</h4><table><thead><tr><th>Материал</th><th>%</th><th>кг</th></tr></thead><tbody>';
      bom.forEach(b => {{
        html += '<tr><td>' + (b.material?.symbol ? '<strong>' + b.material.symbol + '</strong> ' : '') +
          (b.material?.name || b.material_id) +
          (b.material?.criticality ? ' <span class="badge ' + b.material.criticality + '">' + b.material.criticality + '</span>' : '') +
          '</td><td>' + b.fraction_pct + '%</td><td>' + (b.mass_kg || '—') + '</td></tr>';
      }});
      html += '</tbody></table></div>';
    }}

    card.innerHTML = html;
    card.classList.remove('hidden');
    card.querySelectorAll('.link[data-unit]').forEach(el => {{
      el.addEventListener('click', () => selectUnit(el.dataset.unit));
    }});
  }}

  select.addEventListener('change', () => renderUnit(select.value));

  document.getElementById('stats').innerHTML =
    '<table><tr><td>Планеты</td><td><strong>' + DATA.planets.length + '</strong></td></tr>' +
    '<tr><td>Материалы</td><td><strong>' + DATA.materials.length + '</strong></td></tr>' +
    '<tr><td>Единицы</td><td><strong>' + DATA.units.length + '</strong></td></tr>' +
    '<tr><td>Связей материал↔планета</td><td><strong>' + DATA.planetMaterials.length + '</strong></td></tr>' +
    '<tr><td>Записей BOM</td><td><strong>' + DATA.unitMaterials.length + '</strong></td></tr>' +
    '<tr><td>Связей компонентов</td><td><strong>' + DATA.unitComponents.length + '</strong></td></tr></table>';

  const byCategory = new Map();
  DATA.units.forEach(u => {{
    if (!byCategory.has(u.category_id)) byCategory.set(u.category_id, []);
    byCategory.get(u.category_id).push(u);
  }});

  let listHtml = '';
  byCategory.forEach((units, catId) => {{
    const cat = categoriesById.get(catId);
    listHtml += '<h4>' + (cat?.name || catId) + '</h4><ul>';
    units.forEach(u => {{
      listHtml += '<li><span class="link" data-unit="' + u.id + '"><strong>' + u.id + '</strong> ' + u.name + '</span>' +
        (u.mass_kg ? ' — ' + u.mass_kg.toLocaleString() + ' кг' : '') +
        (u.production_planet_id === 'earth' ? ' <em>(импорт)</em>' : '') + '</li>';
    }});
    listHtml += '</ul>';
  }});
  document.getElementById('units-list').innerHTML = listHtml;

  document.getElementById('units-list').querySelectorAll('.link[data-unit]').forEach(el => {{
    el.addEventListener('click', () => selectUnit(el.dataset.unit));
  }});

  // Автовыбор юнита из URL: ?unit=XXX
  const urlParams = new URLSearchParams(window.location.search);
  const unitFromUrl = urlParams.get('unit');
  if (unitFromUrl && unitsById.has(unitFromUrl)) {{
    selectUnit(unitFromUrl);
    document.getElementById('unit-card').scrollIntoView({{ behavior: 'smooth' }});
  }}
}});
</script>

</body>
</html>
'''

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)


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

    # Собираем данные и экспортируем JSON
    all_data = {}
    for filename, export_func in exports:
        data = export_func(con)
        # Ключ без .json
        key = filename.replace(".json", "").replace("-", "_")
        all_data[key] = data

        filepath = EXPORT_DIR / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  {filename}: {len(data)} записей")

    con.close()

    # Генерация data.js для веб-интерфейса
    data_js_path = Path(__file__).parent.parent / "ru" / "science" / "data" / "db" / "data.js"
    generate_data_js(all_data, data_js_path)
    print(f"  data.js: обновлён")

    # Генерация data.json для OJS виджетов
    data_json_path = Path(__file__).parent.parent / "ru" / "science" / "data" / "db" / "data.json"
    with open(data_json_path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    print(f"  data.json: обновлён")

    print(f"\nГотово! Файлы в: {EXPORT_DIR}")


if __name__ == "__main__":
    main()
