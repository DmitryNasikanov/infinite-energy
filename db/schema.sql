-- Схема базы данных проекта «Гелиос» v4 (i18n)
-- DuckDB DDL

-- ============================================
-- 1. ПЛАНЕТЫ
-- ============================================
CREATE TABLE IF NOT EXISTS planets (
    id VARCHAR PRIMARY KEY,                    -- 'earth', 'mercury', 'moon', 'mars'
    name_ru VARCHAR NOT NULL,                  -- Название на русском
    name_en VARCHAR,                           -- Название на английском
    gravity_m_s2 DECIMAL,                      -- Ускорение свободного падения, м/с²
    solar_constant_w_m2 DECIMAL,               -- Солнечная постоянная на орбите, Вт/м²
    escape_velocity_km_s DECIMAL,              -- Вторая космическая скорость, км/с
    has_atmosphere BOOLEAN,                    -- Наличие атмосферы
    sources TEXT                               -- JSON-массив ссылок на источники
);

-- ============================================
-- 2. МАТЕРИАЛЫ (с иерархией)
-- ============================================
CREATE TABLE IF NOT EXISTS materials (
    id VARCHAR PRIMARY KEY,                    -- 'MAT-AL', 'MAT-FE-MN', ...
    parent_id VARCHAR,                         -- Иерархия: MAT-METAL → MAT-FE → MAT-FE-MN
    name_ru VARCHAR NOT NULL,                  -- Название на русском
    name_en VARCHAR,                           -- Название на английском
    symbol VARCHAR,                            -- Химический символ: 'Al', 'Fe', 'O₂'
    description_ru TEXT,                       -- Описание на русском
    description_en TEXT,                       -- Описание на английском
    criticality VARCHAR,                       -- 'critical' / 'high' / 'medium' / 'low'
    sources TEXT                               -- JSON-массив ссылок на источники
);

-- ============================================
-- 3. СВЯЗЬ ПЛАНЕТА-МАТЕРИАЛ (M:N)
-- ============================================
-- Логика:
--   - Есть запись → материал доступен на планете
--   - concentration_pct число → добывается из реголита
--   - concentration_pct = NULL → доступен, но не из реголита (импорт/покупка)
--   - Нет записи вообще → материал не используется в проекте
-- ============================================
CREATE TABLE IF NOT EXISTS planet_materials (
    planet_id VARCHAR REFERENCES planets(id),
    material_id VARCHAR REFERENCES materials(id),
    concentration_pct DECIMAL,                 -- % в реголите (NULL = не добывается)
    notes TEXT,                                -- 'только LRM-зоны', 'импорт' и т.д.
    PRIMARY KEY (planet_id, material_id)
);

-- ============================================
-- 4. КАТЕГОРИИ ЕДИНИЦ
-- ============================================
CREATE TABLE IF NOT EXISTS categories (
    id VARCHAR PRIMARY KEY,                    -- 'robots', 'facilities', ...
    name_ru VARCHAR NOT NULL,                  -- Название на русском
    name_en VARCHAR                            -- Название на английском
);

-- ============================================
-- 5. ЕДИНИЦЫ (роботы, заводы, оборудование, продукция)
-- ============================================
-- Бывш. entities → переименовано в units
-- ============================================
CREATE TABLE IF NOT EXISTS units (
    id VARCHAR PRIMARY KEY,                    -- 'ROB-001', 'FAC-001', 'EQU-001', ...
    category_id VARCHAR REFERENCES categories(id),
    name_ru VARCHAR NOT NULL,                  -- Название на русском
    name_en VARCHAR,                           -- Название на английском
    description_ru TEXT,                       -- Описание на русском
    description_en TEXT,                       -- Описание на английском
    mass_kg DECIMAL,                           -- Масса, кг
    power_kw DECIMAL,                          -- Потребляемая мощность, кВт
    parent_id VARCHAR,                         -- Родительская сборка (вложенность)
    is_assembly BOOLEAN,                       -- true = сборка, false = простая единица
    production_planet_id VARCHAR REFERENCES planets(id),  -- Где производится
    sources TEXT                               -- JSON-массив ссылок на источники
);

-- ============================================
-- 6. BOM — СОСТАВ ЕДИНИЦЫ (Bill of Materials)
-- ============================================
-- Бывш. entity_materials → переименовано в unit_materials
-- quantity_kg → fraction_pct (% от массы единицы)
-- ============================================
CREATE TABLE IF NOT EXISTS unit_materials (
    unit_id VARCHAR REFERENCES units(id),
    material_id VARCHAR REFERENCES materials(id),
    fraction_pct DECIMAL,                      -- % от массы единицы (НЕ кг!)
    PRIMARY KEY (unit_id, material_id)
);

-- ============================================
-- 7. КОМПОНЕНТЫ СБОРОК (M:N unit → unit)
-- ============================================
-- Связь сборка → компоненты (подшипник в роботе, электроника в фабрике)
-- Отличие от parent_id: parent_id = принадлежность объекту,
--                       unit_components = физический состав
-- ============================================
CREATE TABLE IF NOT EXISTS unit_components (
    assembly_id VARCHAR REFERENCES units(id),  -- сборка (родитель)
    component_id VARCHAR REFERENCES units(id), -- компонент (дочерний)
    quantity INTEGER DEFAULT 1,                -- сколько штук
    PRIMARY KEY (assembly_id, component_id)
);

-- ============================================
-- ПОЛЕЗНЫЕ ЗАПРОСЫ
-- ============================================

-- Вычисление массы материала для единицы:
-- SELECT
--     u.name_ru as unit,
--     m.name_ru as material,
--     um.fraction_pct,
--     u.mass_kg * um.fraction_pct / 100 as material_mass_kg
-- FROM unit_materials um
-- JOIN units u ON um.unit_id = u.id
-- JOIN materials m ON um.material_id = m.id;

-- Проверка доступности материалов на планете производства:
-- SELECT
--     u.name_ru as unit,
--     u.production_planet_id,
--     m.name_ru as material,
--     CASE WHEN plm.planet_id IS NOT NULL THEN 'OK' ELSE 'MISSING!' END as availability
-- FROM units u
-- JOIN unit_materials um ON um.unit_id = u.id
-- JOIN materials m ON um.material_id = m.id
-- LEFT JOIN planet_materials plm
--     ON plm.planet_id = u.production_planet_id
--     AND plm.material_id = um.material_id;
