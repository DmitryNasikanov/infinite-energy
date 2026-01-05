# База данных номенклатуры проекта «Гелиос» v3

DuckDB база для управления единицами проекта.

## Установка

```bash
./venv/bin/pip install duckdb
```

## Инициализация

```bash
./venv/bin/python db/init_db.py
```

## Изменения v3

- `planets`: +`has_atmosphere`, +`sources` (JSON-массив ссылок)
- `entities` → `units`: +`is_assembly`, +`production_planet_id`
- `entity_materials` → `unit_materials`: `quantity_kg` → `fraction_pct`
- **NEW**: `unit_components` — связь unit → unit (M:N), состав сборок

## Схема

```
planets ─────────────┬──── planet_materials (M:N)
                     │
materials ───────────┤
    │ parent_id      │
    ▼                │
materials            │
                     │
                     └──── units
                              │ production_planet_id
categories ──────────────────│
                              │ parent_id (локация)
                              ▼
                          units
                              │
                              ├── unit_materials (BOM, %)
                              │
                              └── unit_components (M:N, qty)
                                     │
                                     ▼
                                  units
```

## Таблицы

| Таблица | Описание |
|---------|----------|
| `planets` | Планеты с `has_atmosphere`, `sources` (JSON) |
| `materials` | Материалы с иерархией |
| `planet_materials` | Связь материал↔планета |
| `categories` | Категории единиц |
| `units` | Единицы с `is_assembly`, `production_planet_id` |
| `unit_materials` | BOM в % от массы (`fraction_pct`) |
| `unit_components` | Состав сборок (unit → unit, quantity) |

## Логика

### planet_materials
- `concentration_pct` число → добывается из реголита
- `concentration_pct = NULL` → импорт (связь с `earth`)

### units
- `is_assembly = true` → сборка из компонентов
- `is_assembly = false` → простая единица (импорт)
- `production_planet_id` → проверка доступности материалов

### unit_materials
- `fraction_pct` — процент от массы единицы
- Масса = `units.mass_kg * fraction_pct / 100`

### unit_components
- `assembly_id` → `component_id` + `quantity`
- Один компонент может быть в **нескольких** сборках (M:N)
- Пример: EQU-012 (электроника) входит в ROB-001, ROB-002, PRD-002...
- **Отличие от parent_id**: parent_id = локация (EQU в FAC), unit_components = физический состав

## Примеры запросов

```python
import duckdb

con = duckdb.connect('db/helios.duckdb')

# BOM с вычислением массы
con.execute("""
    SELECT
        m.name as material,
        um.fraction_pct,
        u.mass_kg * um.fraction_pct / 100 as mass_kg
    FROM unit_materials um
    JOIN units u ON um.unit_id = u.id
    JOIN materials m ON um.material_id = m.id
    WHERE um.unit_id = 'PRD-002'
""").fetchall()

# Проверка доступности материалов на планете производства
con.execute("""
    SELECT
        m.name,
        CASE WHEN plm.planet_id IS NOT NULL THEN 'OK' ELSE 'MISSING!' END
    FROM units u
    JOIN unit_materials um ON um.unit_id = u.id
    JOIN materials m ON um.material_id = m.id
    LEFT JOIN planet_materials plm
        ON plm.planet_id = u.production_planet_id
        AND plm.material_id = um.material_id
    WHERE u.id = 'PRD-002'
""").fetchall()

# Импортные единицы
con.execute("""
    SELECT id, name, mass_kg
    FROM units
    WHERE production_planet_id = 'earth'
""").fetchall()

# Источники по планете (JSON)
import json
row = con.execute("SELECT sources FROM planets WHERE id = 'mercury'").fetchone()
sources = json.loads(row[0])
```

## Структура ID

| Префикс | Категория |
|---------|-----------|
| `ROB-xxx` | Роботы |
| `FAC-xxx` | Заводы |
| `EQU-xxx` | Оборудование |
| `PRD-xxx` | Продукция |
| `MAT-xxx` | Материалы |
| `TRN-xxx` | Транспорт |
