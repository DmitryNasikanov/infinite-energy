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
    """Материалы с иерархией и источниками"""
    materials = [
        # id, parent_id, name, symbol, description, criticality, sources (JSON)

        # Корневые категории
        ("MAT-METAL", None, "Металлы", None, "Металлы и сплавы", None, None),
        ("MAT-NONMETAL", None, "Неметаллы", None, "Неметаллические элементы и соединения", None, None),
        ("MAT-COMPOUND", None, "Соединения", None, "Сплавы и химические соединения", None, None),

        # Металлы
        ("MAT-AL", "MAT-METAL", "Алюминий", "Al", "Зеркала, корпуса, радиаторы, фольга для куполов", "critical",
         json.dumps(["CHALCO — фольга 4.5 мкм", "Novelis — промышленная фольга", "ALCOA — aerospace aluminium"])),
        ("MAT-FE", "MAT-METAL", "Железо", "Fe", "Рамы, шасси, конструкции", "critical",
         json.dumps(["ArcelorMittal — конструкционная сталь", "POSCO — автоматизированное производство"])),
        ("MAT-FE-MN", "MAT-FE", "Сталь Fe-6%Mn", None, "Прочная сталь без углерода, легированная марганцем", "high",
         json.dumps(["ASTM A128 — Hadfield steel standard", "Metso Outotec — износостойкие стали"])),
        ("MAT-MG", "MAT-METAL", "Магний", "Mg", "Лёгкие сплавы, пиротехника", "high",
         json.dumps(["US Magnesium — электролизное производство", "Magontec — сплавы"])),
        ("MAT-TI", "MAT-METAL", "Титан", "Ti", "Электрохромика зеркал, прочные узлы", "medium",
         json.dumps(["VSMPO-AVISMA — титановые сплавы", "ATI — aerospace titanium"])),
        ("MAT-NA", "MAT-METAL", "Натрий", "Na", "Батареи NaS (анод)", "high",
         json.dumps(["Chemours — промышленный натрий", "NGK Insulators — NaS технология"])),
        ("MAT-MN", "MAT-METAL", "Марганец", "Mn", "Легирование стали Fe-6%Mn", "medium",
         json.dumps(["South32 — добыча марганца", "ERAMET — ферросплавы"])),
        ("MAT-IR", "MAT-METAL", "Иридий", "Ir", "Аноды MRE-ячеек (устойчивость к расплаву)", "medium",
         json.dumps(["Johnson Matthey — платиновые металлы", "Heraeus — иридиевые аноды"])),
        ("MAT-PT", "MAT-METAL", "Платина", "Pt", "Фильеры для волочения стекловолокна", "medium",
         json.dumps(["Anglo American Platinum", "Impala Platinum"])),
        ("MAT-W", "MAT-METAL", "Вольфрам", "W", "Фрезы CNC, фильеры, инструмент", "medium",
         json.dumps(["Sandvik — вольфрамовые фрезы", "Kennametal — твёрдые сплавы W-Co"])),
        ("MAT-CU", "MAT-METAL", "Медь", "Cu", "Обмотки моторов Gen-1, кристаллизаторы МНЛЗ", "high",
         json.dumps(["Codelco — электролитическая медь", "Freeport-McMoRan"])),

        # Неметаллы
        ("MAT-O2", "MAT-NONMETAL", "Кислород", "O₂", "Главный продукт MRE, побочный продукт", "critical",
         json.dumps(["Linde — промышленный кислород", "Air Liquide — криогенное разделение"])),
        ("MAT-SI", "MAT-NONMETAL", "Кремний", "Si", "Стекловолокно, электроника, солнечные панели", "critical",
         json.dumps(["Wacker Chemie — поликремний", "LONGi — солнечный Si", "Owens Corning — стекловолокно"])),
        ("MAT-S", "MAT-NONMETAL", "Сера", "S", "Батареи NaS (катод)", "high",
         json.dumps(["BASF — промышленная сера", "Claus process — побочный продукт"])),
        ("MAT-C", "MAT-NONMETAL", "Углерод/Графит", "C", "Композиты, восстановитель Ti, термозащита", "high",
         json.dumps(["SGL Carbon — графитовые материалы", "Toray — углеродное волокно"])),
        ("MAT-K", "MAT-NONMETAL", "Калий", "K", "Удобрения, химические процессы", "low",
         json.dumps(["Nutrien — добыча калия", "K+S — хлорид калия"])),

        # Соединения и сплавы
        ("MAT-NAK", "MAT-COMPOUND", "Натрий-калий", "NaK", "Теплоноситель (-12°C...+785°C)", "high",
         json.dumps(["DOE — Sodium Technology Handbook", "ESA Bepi-Colombo — NaK cooling"])),
        ("MAT-MOS2", "MAT-COMPOUND", "Дисульфид молибдена", "MoS₂", "Смазка для вакуума", "medium",
         json.dumps(["Dow Corning — Molykote", "NASA — vacuum lubricants"])),
        ("MAT-GAAS", "MAT-COMPOUND", "Арсенид галлия", "GaAs", "Высокоэффективные фотоячейки (импорт)", "high",
         json.dumps(["Spectrolab — космические GaAs ячейки", "SolAero — multi-junction cells"])),
        ("MAT-AL2O3", "MAT-COMPOUND", "Оксид алюминия", "Al₂O₃", "Керамика, бета-глинозём для NaS", "medium",
         json.dumps(["NGK Insulators — beta-alumina для NaS", "CoorsTek — техническая керамика"])),
        ("MAT-MGO", "MAT-COMPOUND", "Оксид магния", "MgO", "Тугоплавкая керамика для тиглей (Tпл=2852°C)", "medium",
         json.dumps(["Magnesium oxide refractory", "Used in steelmaking furnaces"])),
        ("MAT-TIO2", "MAT-COMPOUND", "Диоксид титана", "TiO₂", "Электрохромика зеркал", "medium",
         json.dumps(["IKAROS (JAXA 2010) — TiO₂ электрохромика в космосе", "Gentex — автомобильная электрохромика"])),
        ("MAT-LI", "MAT-METAL", "Литий", "Li", "Li-ion батареи Gen-1 (импорт)", "high",
         json.dumps(["Albemarle — литиевые соединения", "CATL — Li-ion батареи", "Panasonic — Tesla cells"])),
        ("MAT-KEVLAR", "MAT-NONMETAL", "Кевлар", None, "Армирование конструкций Gen-1 (импорт)", "medium",
         json.dumps(["DuPont — Kevlar aramid fiber", "Teijin — Twaron"])),
        ("MAT-CFRP", "MAT-COMPOUND", "Углепластик", "CFRP", "Корпуса Gen-1 (импорт)", "medium",
         json.dumps(["Toray — T700/T800 carbon fiber", "Hexcel — aerospace CFRP", "SpaceX Dragon — CFRP capsule"])),
    ]
    con.executemany(
        "INSERT OR REPLACE INTO materials (id, parent_id, name, symbol, description, criticality, sources) VALUES (?, ?, ?, ?, ?, ?, ?)",
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
        ("mercury", "MAT-FE-MN", None, "производится (сплав Fe + Mn)"),
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
        ("earth", "MAT-CU", None, "импорт, кристаллизаторы, обмотки"),
        ("earth", "MAT-GAAS", None, "импорт, фотоячейки"),
        ("earth", "MAT-LI", None, "импорт, Li-ion батареи Gen-1"),
        ("earth", "MAT-KEVLAR", None, "импорт, армирование"),
        ("earth", "MAT-CFRP", None, "импорт, углепластик"),

        # Меркурий — дополнительные соединения
        ("mercury", "MAT-NAK", None, "производится из Na+K"),
        ("mercury", "MAT-MOS2", None, "производится (Mo — следы)"),
        ("mercury", "MAT-AL2O3", None, "производится из Al+O₂ (керамика, подшипники)"),
        ("mercury", "MAT-MGO", None, "производится из Mg+O₂"),
        ("mercury", "MAT-TIO2", None, "производится из Ti+O₂"),
    ]
    con.executemany(
        "INSERT OR REPLACE INTO planet_materials (planet_id, material_id, concentration_pct, notes) VALUES (?, ?, ?, ?)",
        planet_materials
    )


def seed_units(con):
    """Единицы проекта (бывш. entities) с источниками"""
    units = [
        # id, category_id, name, description, mass_kg, power_kw, parent_id, is_assembly, production_planet_id, sources

        # =====================================
        # РОБОТЫ GEN-1 (импорт с Земли)
        # =====================================
        ("ROB-011", "robots", "Паук-З (Spider-Z)", "Разведчик, альпинист, 4 ноги, камеры", 82, 3, None, True, "earth",
         json.dumps(["Boston Dynamics Spot — 4-leg robot", "NASA LEMUR — climbing robot"])),
        ("ROB-012", "robots", "Краб-З (Crab-Z)", "Тяжёлый грузчик, 6 ног, 2 т груз", 950, 25, None, True, "earth",
         json.dumps(["ANYbotics ANYmal — промышленный 4-leg", "Agility Robotics Digit — logistics robot"])),
        ("ROB-013", "robots", "Кентавр-З (Centaur-Z)", "Техник-манипулятор, 4 ноги + 2 руки", 150, 12, None, True, "earth",
         json.dumps(["NASA Robonaut — humanoid manipulator", "ABB YuMi — collaborative robot"])),
        ("ROB-014", "robots", "Крот-З (Mole-Z)", "Экскаватор, гусеницы, ковш", 800, 30, None, True, "earth",
         json.dumps(["Caterpillar 320F — compact excavator", "Komatsu PC200 — hydraulic excavator"])),
        ("ROB-015", "robots", "Манипулятор Ф-А1", "Стационарный манипулятор первого завода", 250, 8, "FAC-001", True, "earth",
         json.dumps(["FANUC M-2000iA — heavy payload robot", "KUKA KR 1000 titan — industrial manipulator"])),

        # =====================================
        # РОБОТЫ GEN-2 (местное производство)
        # =====================================
        ("ROB-021", "robots", "Краб-М (Crab-M)", "Логист Gen-2, 6 ног, 5 т груз, NaS батарея", 1000, 30, None, True, "mercury",
         json.dumps(["Caterpillar Command — autonomous mining", "Rio Tinto autonomous trucks"])),
        ("ROB-022", "robots", "Кентавр-М (Centaur-M)", "Сборщик Gen-2, 4 ноги + 2 руки, лёгкий", 370, 12, None, True, "mercury",
         json.dumps(["NASA Mars rovers — autonomous operation", "Boston Dynamics Stretch — warehouse robot"])),
        ("ROB-023", "robots", "Крот-М (Mole-M)", "Добытчик Gen-2, гусеницы, 600 т/день", 1500, 40, None, True, "mercury",
         json.dumps(["Komatsu autonomous haul trucks", "Sandvik AutoMine — underground mining"])),

        # =====================================
        # ЗАВОДЫ
        # =====================================
        ("FAC-001", "facilities", "Точка Ноль", "Основной завод на северном полюсе Меркурия, 1500 м²", None, 55000, None, True, "mercury",
         json.dumps(["SpaceX Starbase — automated factory concept", "Tesla Gigafactory — robotic manufacturing"])),
        ("FAC-002", "facilities", "Комплекс Карбон-Север", "Мини-завод по добыче графита (LRM, полярный кратер)", None, 5000, None, True, "mercury",
         json.dumps(["MESSENGER — Mercury LRM deposits data", "Apollo 17 — lunar graphite studies"])),
        ("FAC-003", "facilities", "Комплекс Карбон-Юг", "Мини-завод по добыче графита (LRM, полярный кратер)", None, 5000, None, True, "mercury",
         json.dumps(["MESSENGER — Mercury LRM deposits data", "Apollo 17 — lunar graphite studies"])),
        ("FAC-004", "facilities", "Гелио-башня", "Концентратор солнечной энергии на вершине кратера, 10 МВт", 50000, 0, None, True, "mercury",
         json.dumps(["Odeillo Solar Furnace (France) — 1 MW", "DLR Solar Tower Jülich — concentrated solar"])),

        # =====================================
        # ОБОРУДОВАНИЕ — ДОБЫЧА И ПОДГОТОВКА
        # =====================================
        ("EQU-021", "equipment", "Виброгрохот", "Грохочение реголита, разделение фракций", 500, 10, "FAC-001", True, "mercury",
         json.dumps(["Metso Outotec — vibrating screens", "Sandvik — mining equipment"])),
        ("EQU-004", "equipment", "Щековая дробилка", "Дробление реголита <10мм", 3000, 50, "FAC-001", True, "mercury",
         json.dumps(["Metso Lokotrack — mobile crusher", "Sandvik QJ341 — jaw crusher"])),
        ("EQU-005", "equipment", "Магнитный сепаратор", "Разделение магнитной/немагнитной фракций", 500, 20, "FAC-001", True, "mercury",
         json.dumps(["Eriez — magnetic separation", "STEINERT — sensor-based sorting"])),

        # =====================================
        # ОБОРУДОВАНИЕ — ПЛАВКА И ЭЛЕКТРОЛИЗ
        # =====================================
        ("EQU-003", "equipment", "Солнечная печь", "Концентратор для плавки реголита 1500°C", 2000, 0, "FAC-001", True, "mercury",
         json.dumps(["Odeillo (France) — 1 MW solar furnace", "DLR Cologne — high-flux solar furnace"])),
        ("EQU-002", "equipment", "MRE-ячейка", "Электролиз расплава реголита (Al, Fe, Si, O₂)", 5000, 500, "FAC-001", True, "mercury",
         json.dumps(["FFC Cambridge Process — molten salt electrolysis", "Metalysis — solid-state electrolysis"])),
        ("EQU-022", "equipment", "МГД-насос", "Перекачка расплава через магнитное поле", 200, 50, "FAC-001", True, "mercury",
         json.dumps(["ABB — electromagnetic pumps for metals", "Precimeter — MHD pumps"])),
        ("EQU-023", "equipment", "Промковш (тандиш)", "Разделение Al/Fe расплавов, 2 стопора", 1000, 0, "FAC-001", True, "mercury",
         json.dumps(["SMS Group — tundish technology", "Vesuvius — refractory systems"])),

        # =====================================
        # ОБОРУДОВАНИЕ — ДИСТИЛЛЯЦИЯ ШЛАКА
        # =====================================
        ("EQU-031", "equipment", "Конденсатор калия", "Фракционная конденсация K при 759°C", 500, 10, "FAC-001", True, "mercury",
         json.dumps(["Fractional distillation of metals", "Vacuum metallurgy"])),
        ("EQU-032", "equipment", "Конденсатор натрия", "Фракционная конденсация Na при 883°C", 800, 15, "FAC-001", True, "mercury",
         json.dumps(["Sodium production by Downs process", "Vacuum distillation"])),
        ("EQU-033", "equipment", "Конденсатор магния", "Фракционная конденсация Mg при 1091°C", 1500, 25, "FAC-001", True, "mercury",
         json.dumps(["Pidgeon process — magnesium distillation", "Vacuum metallurgy of Mg"])),

        # =====================================
        # ОБОРУДОВАНИЕ — ЛИТЬЁ
        # =====================================
        ("EQU-006", "equipment", "МНЛЗ-Al", "Машина непрерывного литья алюминия, 100×100 мм", 8000, 100, "FAC-001", True, "mercury",
         json.dumps(["SMS Group — aluminum casters", "Danieli — continuous casting"])),
        ("EQU-007", "equipment", "МНЛЗ-Fe", "Машина непрерывного литья стали, 100×100 мм", 10000, 150, "FAC-001", True, "mercury",
         json.dumps(["Danieli — steel continuous casters", "Primetals — billet casters"])),

        # =====================================
        # ОБОРУДОВАНИЕ — ФОРМОВКА
        # =====================================
        ("EQU-024", "equipment", "Индукционная печь", "Нагрев Fe заготовок до 1100°C в N₂", 3000, 100, "FAC-001", True, "mercury",
         json.dumps(["Inductotherm — induction heating", "ABP Induction — steel reheating"])),
        ("EQU-008", "equipment", "Прокатный стан", "6-клетьевой, вход 100×100 → выход Ø20 мм", 15000, 200, "FAC-001", True, "mercury",
         json.dumps(["SMS Meer — rolling mills", "Siemens VAI — long products"])),
        ("EQU-025", "equipment", "Волочильный стан", "Фильеры W, выход Ø1.6-2.0 мм проволока", 2000, 30, "FAC-001", True, "mercury",
         json.dumps(["Niehoff — wire drawing machines", "Samp — drawing equipment"])),
        ("EQU-026", "equipment", "Фольгопрокат", "Прокат Al фольги 4-50 мкм для зеркал", 5000, 50, "FAC-001", True, "mercury",
         json.dumps(["Achenbach — foil rolling mills", "Fata Hunter — aluminum rolling"])),
        ("EQU-009", "equipment", "WAAM-ячейка", "3D-печать дуговой наплавкой проволоки", 2000, 50, "FAC-001", True, "mercury",
         json.dumps(["Lincoln Electric — WAAM systems", "WAAM3D — wire arc additive manufacturing", "Cranfield University — WAAM research"])),
        ("EQU-010", "equipment", "CNC 5-осевой", "Фрезерный станок, твердосплавные фрезы W-Co", 3000, 30, "FAC-001", True, "mercury",
         json.dumps(["DMG MORI — 5-axis machining centers", "Mazak — multi-axis CNC", "Haas — vertical mills"])),

        # =====================================
        # ОБОРУДОВАНИЕ — СБОРКА
        # =====================================
        ("EQU-027", "equipment", "Сборочный стапель", "1 позиция сборки робота/оборудования", 500, 5, "FAC-001", True, "mercury",
         json.dumps(["Comau — assembly systems", "KUKA — robotic assembly cells"])),
        ("EQU-028", "equipment", "Мостовой кран", "Г/п 1 т, пролёт 10 м", 2000, 20, "FAC-001", True, "mercury",
         json.dumps(["Konecranes — overhead cranes", "Demag — industrial cranes"])),
        ("EQU-029", "equipment", "AGV-тележка", "Автоматическая логистическая тележка", 200, 5, "FAC-001", True, "mercury",
         json.dumps(["KUKA — mobile platforms", "MiR — autonomous mobile robots"])),

        # =====================================
        # ОБОРУДОВАНИЕ — ЭНЕРГЕТИКА
        # =====================================
        ("EQU-001", "equipment", "Масс-драйвер", "Электромагнитная катапульта, 3 км, 5 км/с", 1300000, 33000, "FAC-001", True, "mercury",
         json.dumps(["NASA Mass Driver Study 1992", "O'Neill 1974: The Colonization of Space", "NUDT maglev 700 km/h (China, 2025)"])),
        ("EQU-011", "equipment", "Мини масс-драйвер", "МД для комплексов Карбон, 500м-1км", 330000, 500, None, True, "mercury",
         json.dumps(["NASA Lunar Mass Driver concept", "EMF coilgun technology"])),
        ("EQU-030", "equipment", "ЛЭП криогенная", "Сверхпроводящая линия, 1 км участок", 1000, 0, None, True, "mercury",
         json.dumps(["AMSC — superconducting cables", "Nexans — HTS power cables"])),

        # =====================================
        # КОМПОНЕНТЫ — ИМПОРТ С ЗЕМЛИ
        # =====================================
        ("CMP-001", "equipment", "Блок электроники", "CPU, микроконтроллеры, связь", 5, 0, None, False, "earth",
         json.dumps(["ARM Cortex processors", "Intel Xeon — space-grade", "Xilinx — rad-hard FPGAs"])),
        ("CMP-002", "equipment", "Камера стерео", "Stereo vision, 2 камеры", 0.5, 0, None, False, "earth",
         json.dumps(["Intel RealSense", "ZED — stereo cameras", "Teledyne FLIR — industrial vision"])),
        ("CMP-003", "equipment", "Лидар", "3D сканер, дальность 50м", 2, 0, None, False, "earth",
         json.dumps(["Velodyne — lidar sensors", "Ouster — digital lidar", "Livox — compact lidar"])),
        ("CMP-004", "equipment", "BLDC мотор Cu", "Бесщёточный мотор, медные обмотки", 5, 0, None, False, "earth",
         json.dumps(["Maxon — precision motors", "FAULHABER — micro drives", "Kollmorgen — servomotors"])),
        ("CMP-005", "equipment", "Li-ion батарея", "Литий-ионная батарея 1 кВт·ч", 10, 0, None, False, "earth",
         json.dumps(["CATL — battery cells", "Panasonic — 2170 cells", "Samsung SDI — prismatic cells"])),
        ("EQU-014", "equipment", "Анод иридиевый", "Анод для MRE-ячеек, Ir", 2, 0, None, False, "earth",
         json.dumps(["Heraeus — precious metal anodes", "Johnson Matthey — Ir electrodes"])),
        ("EQU-013", "equipment", "Фильера Pt", "Фильера для стекловолокна, платина", 0.5, 0, None, False, "earth",
         json.dumps(["Heraeus — Pt bushings", "Johnson Matthey — glass fiber dies"])),
        ("CMP-006", "equipment", "Фильера W", "Фильера для волочения проволоки, вольфрам", 0.5, 0, None, False, "earth",
         json.dumps(["Sandvik — tungsten carbide dies", "Esteves — wire drawing dies"])),
        ("CMP-007", "equipment", "Фреза W-Co", "Твердосплавная фреза для CNC", 0.2, 0, None, False, "earth",
         json.dumps(["Sandvik Coromant — carbide cutters", "Kennametal — milling tools"])),
        ("CMP-008", "equipment", "Кристаллизатор Cu", "Медный кристаллизатор для МНЛЗ", 50, 0, None, False, "earth",
         json.dumps(["SMS Group — copper molds", "KME — crystallizers"])),
        ("CMP-009", "equipment", "GaAs панель", "Фотоячейка арсенид галлия, 1 м²", 5, 0, None, False, "earth",
         json.dumps(["Spectrolab — space solar cells", "SolAero — triple-junction GaAs"])),
        ("CMP-010", "equipment", "Чип управления", "Чип для зеркала Роя, 50 г", 0.05, 0, None, False, "earth",
         json.dumps(["Texas Instruments — rad-hard chips", "Microchip — space-grade MCUs"])),

        # =====================================
        # КОМПОНЕНТЫ — МЕСТНОЕ ПРОИЗВОДСТВО
        # =====================================
        ("CMP-011", "equipment", "BLDC мотор Al", "Бесщёточный мотор, алюминиевые обмотки", 5, 0, None, True, "mercury",
         json.dumps(["ABB — aluminum wound motors", "WEG — Al conductors in motors"])),
        ("CMP-012", "equipment", "NaS батарея 1кВт·ч", "Натрий-серная батарея, 1 кВт·ч", 8, 0, None, True, "mercury",
         json.dumps(["NGK Insulators — NaS batteries", "GE Durathon — Na-based storage"])),
        ("CMP-013", "equipment", "Подшипник Al₂O₃", "Корундовый подшипник, 100% местное производство", 0.5, 0, None, True, "mercury",
         json.dumps(["CoorsTek — alumina bearings", "Morgan Advanced Materials — Al₂O₃ ceramics"])),
        ("CMP-014", "equipment", "Редуктор", "Планетарный редуктор, Fe+Al", 3, 0, None, True, "mercury",
         json.dumps(["Harmonic Drive — precision gearboxes", "Nabtesco — planetary gears"])),

        # Старая электроника (для совместимости)
        ("EQU-012", "equipment", "Электроника сенсоров", "Микроконтроллеры, датчики, камеры (пакет)", 20, 0, None, False, "earth",
         json.dumps(["NXP — automotive MCUs", "STMicroelectronics — sensor hubs"])),

        # =====================================
        # ПРОДУКЦИЯ
        # =====================================
        ("PRD-001", "products", "Зеркало 100×100м", "Алюминиевое зеркало с электрохромикой TiO₂", 116, 0, None, True, "mercury",
         json.dumps(["IKAROS (JAXA 2010) — solar sail", "LightSail 2 (Planetary Society)", "NEA Scout — NASA solar sail"])),
        ("PRD-002", "products", "Робот Gen-2", "Робот второго поколения (усреднённый)", 320, 15, None, True, "mercury",
         json.dumps(["Caterpillar autonomous mining", "Rio Tinto autonomous trucks"])),
        ("PRD-003", "products", "Купол завода", "Силикатный купол 50×30м, 1500 м²", 8000, 0, None, True, "mercury",
         json.dumps(["Bigelow Aerospace — inflatable modules", "NASA TransHab — expandable habitats"])),
        ("PRD-004", "products", "NaS батарея 15кВт·ч", "Натрий-серная батарея для роботов", 100, 0, None, True, "mercury",
         json.dumps(["NGK Insulators — NaS grid storage", "GE Durathon — Na-based batteries"])),
        ("PRD-005", "products", "Si панель", "Кремниевая солнечная панель, 1 м²", 10, 0, None, True, "mercury",
         json.dumps(["LONGi — monocrystalline Si", "First Solar — thin film", "SunPower — high efficiency"])),
        ("PRD-006", "products", "Силикатная ткань", "Ткань SiO₂ для куполов, 1 м²", 0.3, 0, None, True, "mercury",
         json.dumps(["3M Nextel — ceramic fabric", "Saint-Gobain — silica cloth"])),

        # =====================================
        # ТРАНСПОРТ
        # =====================================
        ("TRN-001", "transport", "Контейнер графита", "Баллистический контейнер 100 кг", 20, 0, None, True, "mercury",
         json.dumps(["SpaceX Dragon cargo — reentry containers"])),
        ("TRN-002", "transport", "Капсула зеркала", "Защитная капсула для запуска зеркала", 10, 0, None, True, "mercury",
         json.dumps(["NASA — deployable structures", "JAXA IKAROS — sail deployment"])),
    ]
    con.executemany(
        """INSERT OR REPLACE INTO units
           (id, category_id, name, description, mass_kg, power_kw, parent_id, is_assembly, production_planet_id, sources)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        units
    )


def seed_unit_components(con):
    """Компоненты сборок (unit → unit, M:N)"""
    components = [
        # assembly_id, component_id, quantity

        # =====================================
        # РОБОТЫ GEN-1 — компоненты (импортные)
        # По robots.qmd
        # =====================================
        # Паук-З (82 кг): актуаторы 15 кг, Li-Ion 5 кг, электроника 2 кг
        ("ROB-011", "CMP-001", 1),   # 1 блок электроники (2-5 кг)
        ("ROB-011", "CMP-002", 2),   # 2 камеры стерео
        ("ROB-011", "CMP-004", 3),   # 3 мотора Cu (15 кг)
        ("ROB-011", "CMP-005", 1),   # 1 Li-ion батарея (5 кг)

        # Краб-З (950 кг): актуаторы 80 кг, Li-Ion 40 кг, электроника 30 кг
        ("ROB-012", "CMP-001", 6),   # 6 блоков электроники (30 кг)
        ("ROB-012", "CMP-002", 4),   # 4 камеры
        ("ROB-012", "CMP-003", 2),   # 2 лидара
        ("ROB-012", "CMP-004", 16),  # 16 моторов (80 кг)
        ("ROB-012", "CMP-005", 4),   # 4 Li-ion батареи (40 кг)

        # Кентавр-З (150 кг): моторы 50 кг, Li-Ion 30 кг, сенсоры 10 кг
        ("ROB-013", "CMP-001", 2),   # 2 блока электроники (10 кг)
        ("ROB-013", "CMP-002", 4),   # 4 камеры
        ("ROB-013", "CMP-004", 10),  # 10 моторов (50 кг)
        ("ROB-013", "CMP-005", 3),   # 3 Li-ion батареи (30 кг)

        # Крот-З (800 кг): моторы ~96 кг, Li-Ion ~104 кг
        ("ROB-014", "CMP-001", 2),   # 2 блока электроники
        ("ROB-014", "CMP-002", 2),   # 2 камеры
        ("ROB-014", "CMP-003", 1),   # 1 лидар
        ("ROB-014", "CMP-004", 19),  # 19 моторов (96 кг)
        ("ROB-014", "CMP-005", 10),  # 10 Li-ion батарей (104 кг → 100 кг)

        # =====================================
        # РОБОТЫ GEN-2 — компоненты (местные + импорт)
        # =====================================
        # Краб-М (1000 кг): 83% Fe, 13% Al, NaS батарея
        ("ROB-021", "CMP-001", 2),   # 2 блока электроники (импорт)
        ("ROB-021", "CMP-002", 4),   # 4 камеры (импорт)
        ("ROB-021", "CMP-011", 18),  # 18 моторов Al (местные)
        ("ROB-021", "CMP-012", 15),  # 15 кВт·ч NaS батарей (местные)
        ("ROB-021", "CMP-013", 36),  # 36 подшипников (местные)
        ("ROB-021", "CMP-014", 6),   # 6 редукторов (местные)

        # Кентавр-М (370 кг): 35% Fe, 62% Al
        ("ROB-022", "CMP-001", 2),   # 2 блока электроники
        ("ROB-022", "CMP-002", 4),   # 4 камеры
        ("ROB-022", "CMP-011", 14),  # 14 моторов Al
        ("ROB-022", "CMP-012", 8),   # 8 кВт·ч NaS
        ("ROB-022", "CMP-013", 28),  # 28 подшипников
        ("ROB-022", "CMP-014", 6),   # 6 редукторов

        # Крот-М (1500 кг): 78% Fe, 18% Al
        ("ROB-023", "CMP-001", 2),   # 2 блока электроники
        ("ROB-023", "CMP-002", 2),   # 2 камеры
        ("ROB-023", "CMP-011", 8),   # 8 моторов Al
        ("ROB-023", "CMP-012", 20),  # 20 кВт·ч NaS
        ("ROB-023", "CMP-013", 24),  # 24 подшипника
        ("ROB-023", "CMP-014", 4),   # 4 редуктора

        # =====================================
        # ОБОРУДОВАНИЕ — компоненты
        # =====================================
        # MRE-ячейка содержит иридиевые аноды
        ("EQU-002", "EQU-014", 4),   # 4 анода на ячейку

        # МНЛЗ содержат медные кристаллизаторы
        ("EQU-006", "CMP-008", 1),   # МНЛЗ-Al
        ("EQU-007", "CMP-008", 1),   # МНЛЗ-Fe

        # Волочильный стан содержит фильеры W
        ("EQU-025", "CMP-006", 10),  # 10 фильер

        # CNC содержит фрезы
        ("EQU-010", "CMP-007", 20),  # 20 фрез

        # =====================================
        # МАГНИТНЫЙ СЕПАРАТОР EQU-005
        # =====================================
        ("EQU-005", "CMP-011", 2),   # 2 мотора Al (барабан + виброжелоб)
        ("EQU-005", "CMP-013", 4),   # 4 подшипника Al₂O₃
        ("EQU-005", "CMP-014", 1),   # 1 редуктор

        # =====================================
        # ЗАВОД FAC-001 — полное оборудование
        # =====================================
        # Добыча и подготовка
        ("FAC-001", "EQU-004", 3),   # 3 дробилки
        ("FAC-001", "EQU-005", 2),   # 2 магнитных сепаратора
        ("FAC-001", "EQU-021", 2),   # 2 виброгрохота
        # Плавка и электролиз
        ("FAC-001", "EQU-002", 20),  # 20 MRE-ячеек
        ("FAC-001", "EQU-003", 5),   # 5 солнечных печей
        ("FAC-001", "EQU-022", 5),   # 5 МГД-насосов
        ("FAC-001", "EQU-023", 3),   # 3 промковша/тандиша
        # Литьё
        ("FAC-001", "EQU-006", 2),   # 2 МНЛЗ-Al
        ("FAC-001", "EQU-007", 2),   # 2 МНЛЗ-Fe
        # Формовка
        ("FAC-001", "EQU-024", 2),   # 2 индукционных печи
        ("FAC-001", "EQU-008", 2),   # 2 прокатных стана
        ("FAC-001", "EQU-025", 2),   # 2 волочильных стана
        ("FAC-001", "EQU-026", 1),   # 1 фольгопрокат
        ("FAC-001", "EQU-009", 5),   # 5 WAAM-ячеек
        ("FAC-001", "EQU-010", 3),   # 3 CNC 5-осевых
        # Сборка
        ("FAC-001", "EQU-027", 10),  # 10 сборочных стапелей
        ("FAC-001", "EQU-028", 2),   # 2 мостовых крана
        ("FAC-001", "EQU-029", 10),  # 10 AGV-тележек
        # Энергетика
        ("FAC-001", "EQU-001", 1),   # 1 масс-драйвер

        # =====================================
        # КОМПЛЕКС КАРБОН-СЕВЕР FAC-002
        # =====================================
        ("FAC-002", "EQU-011", 1),   # 1 мини масс-драйвер
        ("FAC-002", "EQU-004", 1),   # 1 дробилка
        ("FAC-002", "EQU-021", 1),   # 1 виброгрохот

        # =====================================
        # КОМПЛЕКС КАРБОН-ЮГ FAC-003
        # =====================================
        ("FAC-003", "EQU-011", 1),   # 1 мини масс-драйвер
        ("FAC-003", "EQU-004", 1),   # 1 дробилка
        ("FAC-003", "EQU-021", 1),   # 1 виброгрохот

        # =====================================
        # ГЕЛИО-БАШНЯ FAC-004
        # =====================================
        ("FAC-004", "PRD-005", 3500), # 35 000 м² Si панелей (3500 × 10 кг = 35 т)

        # =====================================
        # ПРОДУКЦИЯ — компоненты
        # =====================================
        # Зеркало 100×100м содержит чип управления
        ("PRD-001", "CMP-010", 1),   # 1 чип управления

        # Усреднённый робот Gen-2
        ("PRD-002", "CMP-001", 2),   # электроника
        ("PRD-002", "CMP-011", 12),  # моторы Al
        ("PRD-002", "CMP-012", 12),  # 12 кВт·ч NaS

        # Масс-драйвер — электроника
        ("EQU-001", "CMP-001", 50),  # 50 блоков управления
    ]
    con.executemany(
        "INSERT OR REPLACE INTO unit_components (assembly_id, component_id, quantity) VALUES (?, ?, ?)",
        components
    )


def seed_unit_materials(con):
    """BOM — состав единиц (fraction_pct вместо quantity_kg)"""

    bom = [
        # unit_id, material_id, fraction_pct

        # =====================================
        # РОБОТЫ GEN-1 (импорт с Земли)
        # Состав по robots.qmd
        # =====================================

        # Паук-З (82 кг)
        ("ROB-011", "MAT-TI", 49),      # 40 кг титановый сплав (3D-печать)
        ("ROB-011", "MAT-AL2O3", 24),   # 20 кг керамика Al₂O₃
        ("ROB-011", "MAT-CU", 18),      # 15 кг актуаторы/моторы
        ("ROB-011", "MAT-LI", 6),       # 5 кг Li-Ion батареи
        ("ROB-011", "MAT-SI", 3),       # 2.5 кг электроника/CPU
        # Итого: 100%

        # Краб-З (950 кг)
        ("ROB-012", "MAT-AL", 63),      # 600 кг Al-Li сплав
        ("ROB-012", "MAT-FE", 21),      # 200 кг пружинная сталь/Нитинол
        ("ROB-012", "MAT-CU", 8),       # 80 кг актуаторы
        ("ROB-012", "MAT-LI", 4),       # 40 кг Li-Ion батареи
        ("ROB-012", "MAT-SI", 4),       # 30 кг электроника/сенсоры
        # Итого: 100%

        # Кентавр-З (150 кг)
        ("ROB-013", "MAT-CFRP", 40),    # 60 кг карбоновый корпус
        ("ROB-013", "MAT-CU", 33),      # 50 кг точные моторы и руки
        ("ROB-013", "MAT-LI", 20),      # 30 кг Li-Ion батареи
        ("ROB-013", "MAT-SI", 7),       # 10 кг сенсоры/CPU
        # Итого: 100%

        # Крот-З (800 кг)
        ("ROB-014", "MAT-TI", 40),      # 320 кг титан (ковш, гусеницы)
        ("ROB-014", "MAT-FE", 30),      # 240 кг сталь (рама)
        ("ROB-014", "MAT-CU", 12),      # 96 кг моторы
        ("ROB-014", "MAT-LI", 13),      # 104 кг Li-Ion
        ("ROB-014", "MAT-SI", 5),       # 40 кг электроника/управление
        # Итого: 100%

        # Манипулятор Ф-А1 (250 кг)
        ("ROB-015", "MAT-AL", 40),      # 100 кг литое Al основание
        ("ROB-015", "MAT-CU", 40),      # 100 кг высокомоментные сервоприводы
        ("ROB-015", "MAT-SI", 20),      # 50 кг электроника/проводка
        # Итого: 100%

        # =====================================
        # РОБОТЫ GEN-2 (местное производство)
        # Состав по robots.qmd: гибрид Fe + Al, NaS батареи
        # =====================================

        # Краб-М (1000 кг): Al 45%, Fe 35%
        ("ROB-021", "MAT-AL", 45),      # 450 кг: рама 350 + радиаторы/панели 100
        ("ROB-021", "MAT-FE", 35),      # 350 кг: колёса 300 + подшипники 50
        ("ROB-021", "MAT-NA", 3.5),     # 35 кг Na в NaS батарее (70 кг / 2)
        ("ROB-021", "MAT-S", 3.5),      # 35 кг S в NaS батарее
        ("ROB-021", "MAT-CU", 10),      # 100 кг актуаторы/лебёдки
        ("ROB-021", "MAT-SI", 3),       # 30 кг импортная электроника
        # Итого: 100%

        # Кентавр-М (370 кг): Al 62%, Fe 22%
        ("ROB-022", "MAT-AL", 62),      # 230 кг: рама 100 + руки 80 + панели 50
        ("ROB-022", "MAT-FE", 22),      # 80 кг: колёса 60 + подшипники 20
        ("ROB-022", "MAT-NA", 6),       # 22 кг Na (NaS 45 кг)
        ("ROB-022", "MAT-S", 6),        # 22 кг S
        ("ROB-022", "MAT-SI", 4),       # 15 кг импорт электроника
        # Итого: 100%

        # Крот-М (1500 кг): Fe 83%, Al 7%
        ("ROB-023", "MAT-FE", 83),      # 1250 кг: гусеницы 400 + рама 400 + ковш 300 + приводы 150
        ("ROB-023", "MAT-AL", 7),       # 100 кг: панели/радиаторы
        ("ROB-023", "MAT-NA", 3.5),     # 50 кг Na (NaS 100 кг)
        ("ROB-023", "MAT-S", 3.5),      # 50 кг S
        ("ROB-023", "MAT-SI", 3),       # 45 кг импорт электроника
        # Итого: 100%

        # =====================================
        # ОБОРУДОВАНИЕ — ДОБЫЧА
        # =====================================

        # Виброгрохот (500 кг)
        ("EQU-021", "MAT-FE", 85),      # рама, сетки
        ("EQU-021", "MAT-AL", 10),      # корпус
        ("EQU-021", "MAT-SI", 5),       # электроника/датчики
        # Итого: 100%

        # Щековая дробилка (3000 кг)
        ("EQU-004", "MAT-FE-MN", 90),   # щёки из стали Fe-6%Mn
        ("EQU-004", "MAT-AL", 5),       # корпус
        ("EQU-004", "MAT-SI", 5),       # электроника/управление
        # Итого: 100%

        # Магнитный сепаратор (500 кг)
        ("EQU-005", "MAT-FE", 60),      # магнитопровод, рама, скребок
        ("EQU-005", "MAT-AL", 30),      # корпус, барабан, обмотки электромагнитов
        ("EQU-005", "MAT-AL2O3", 5),    # подшипники Al₂O₃ (местное производство)
        ("EQU-005", "MAT-SI", 5),       # электроника/датчики
        # Итого: 100%

        # =====================================
        # ОБОРУДОВАНИЕ — ПЛАВКА
        # =====================================

        # Солнечная печь (2000 кг)
        ("EQU-003", "MAT-AL", 70),      # зеркала 60%, каркас 10%
        ("EQU-003", "MAT-FE", 15),      # опорная конструкция
        ("EQU-003", "MAT-MGO", 10),     # тигель MgO (Tпл=2852°C, запас 852°C)
        ("EQU-003", "MAT-SI", 5),       # электроника/привода наведения
        # Итого: 100%

        # MRE-ячейка (5000 кг)
        ("EQU-002", "MAT-FE", 60),      # корпус, электроды
        ("EQU-002", "MAT-AL", 25),      # теплообменники
        ("EQU-002", "MAT-AL2O3", 10),   # футеровка
        ("EQU-002", "MAT-IR", 0.1),     # аноды (импорт, 5 кг)
        ("EQU-002", "MAT-SI", 4.9),     # электроника/управление
        # Итого: 100%

        # МГД-насос (200 кг)
        ("EQU-022", "MAT-FE", 50),      # магнитопровод
        ("EQU-022", "MAT-AL", 40),      # канал, обмотки
        ("EQU-022", "MAT-SI", 10),      # электроника/управление
        # Итого: 100%

        # Промковш/тандиш (1000 кг)
        ("EQU-023", "MAT-FE", 70),      # корпус
        ("EQU-023", "MAT-AL2O3", 25),   # футеровка
        ("EQU-023", "MAT-SI", 5),       # датчики уровня/температуры
        # Итого: 100%

        # =====================================
        # ОБОРУДОВАНИЕ — ЛИТЬЁ
        # =====================================

        # МНЛЗ-Al (8000 кг)
        ("EQU-006", "MAT-FE", 75),      # рама, механизмы
        ("EQU-006", "MAT-CU", 15),      # кристаллизатор (импорт)
        ("EQU-006", "MAT-AL", 5),       # охлаждение
        ("EQU-006", "MAT-SI", 5),       # электроника/датчики
        # Итого: 100%

        # МНЛЗ-Fe (10000 кг)
        ("EQU-007", "MAT-FE", 80),      # рама
        ("EQU-007", "MAT-CU", 12),      # кристаллизатор
        ("EQU-007", "MAT-AL", 3),       # охлаждение
        ("EQU-007", "MAT-SI", 5),       # электроника/датчики
        # Итого: 100%

        # =====================================
        # ОБОРУДОВАНИЕ — ФОРМОВКА
        # =====================================

        # Индукционная печь (3000 кг)
        ("EQU-024", "MAT-FE", 60),      # корпус
        ("EQU-024", "MAT-AL", 30),      # обмотки, охлаждение
        ("EQU-024", "MAT-AL2O3", 5),    # футеровка
        ("EQU-024", "MAT-SI", 5),       # электроника/управление
        # Итого: 100%

        # Прокатный стан (15000 кг)
        ("EQU-008", "MAT-FE-MN", 85),   # валки, станины
        ("EQU-008", "MAT-AL", 10),      # охлаждение, обмотки
        ("EQU-008", "MAT-SI", 5),       # электроника/привода
        # Итого: 100%

        # Волочильный стан (2000 кг)
        ("EQU-025", "MAT-FE", 80),      # рама
        ("EQU-025", "MAT-AL", 15),      # обмотки
        ("EQU-025", "MAT-W", 0.25),     # фильеры (импорт, 5 кг)
        ("EQU-025", "MAT-SI", 4.75),    # электроника/управление
        # Итого: 100%

        # Фольгопрокат (5000 кг)
        ("EQU-026", "MAT-FE", 85),      # валки, рама
        ("EQU-026", "MAT-AL", 10),      # обмотки
        ("EQU-026", "MAT-SI", 5),       # электроника/контроль толщины
        # Итого: 100%

        # WAAM-ячейка (2000 кг)
        ("EQU-009", "MAT-FE", 70),      # рама, механизмы
        ("EQU-009", "MAT-AL", 25),      # обмотки, сопла
        ("EQU-009", "MAT-SI", 5),       # электроника/ЧПУ
        # Итого: 100%

        # CNC 5-осевой (3000 кг)
        ("EQU-010", "MAT-FE", 80),      # станина, шпиндель
        ("EQU-010", "MAT-AL", 15),      # обмотки
        ("EQU-010", "MAT-W", 0.15),     # фрезы W-Co (импорт, 4 кг)
        ("EQU-010", "MAT-SI", 4.85),    # электроника/ЧПУ
        # Итого: 100%

        # =====================================
        # ОБОРУДОВАНИЕ — СБОРКА
        # =====================================

        # Сборочный стапель (500 кг)
        ("EQU-027", "MAT-FE", 70),      # рама
        ("EQU-027", "MAT-AL", 25),      # крепления
        ("EQU-027", "MAT-SI", 5),       # электроника/позиционирование
        # Итого: 100%

        # Мостовой кран (2000 кг)
        ("EQU-028", "MAT-FE", 85),      # балка, тельфер
        ("EQU-028", "MAT-AL", 10),      # обмотки
        ("EQU-028", "MAT-SI", 5),       # электроника/управление
        # Итого: 100%

        # AGV-тележка (200 кг)
        ("EQU-029", "MAT-FE", 50),      # рама
        ("EQU-029", "MAT-AL", 30),      # корпус, обмотки
        ("EQU-029", "MAT-NA", 5),       # NaS батарея
        ("EQU-029", "MAT-S", 5),        # NaS батарея
        ("EQU-029", "MAT-SI", 10),      # электроника/навигация
        # Итого: 100%

        # =====================================
        # ОБОРУДОВАНИЕ — ЭНЕРГЕТИКА
        # =====================================

        # Масс-драйвер (1300000 кг = 1300 т) — по railgun.qmd
        ("EQU-001", "MAT-FE", 62),      # 806 т: каркас 800 + платформа 5 + разное
        ("EQU-001", "MAT-AL", 38),      # 494 т: рельсы 200 + катушки 150 + конденсаторы 100 + охлаждение 44
        # Электроника (~7 т) учтена в unit_components (CMP-001 × 50)
        # Итого: 100%

        # Мини масс-драйвер (330000 кг)
        ("EQU-011", "MAT-FE", 65),      # каркас
        ("EQU-011", "MAT-AL", 30),      # обмотки
        ("EQU-011", "MAT-SI", 5),       # электроника
        # Итого: 100%

        # ЛЭП криогенная (1000 кг/км)
        ("EQU-030", "MAT-AL", 70),      # сверхпроводник Al
        ("EQU-030", "MAT-FE", 20),      # опоры
        ("EQU-030", "MAT-SI", 10),      # изоляция/электроника
        # Итого: 100%

        # =====================================
        # ОБОРУДОВАНИЕ — ДИСТИЛЛЯЦИЯ ШЛАКА
        # =====================================

        # Конденсатор калия (500 кг)
        ("EQU-031", "MAT-FE", 60),      # корпус, радиатор
        ("EQU-031", "MAT-MGO", 25),     # футеровка MgO (Tкип K = 759°C)
        ("EQU-031", "MAT-AL", 10),      # теплообменник
        ("EQU-031", "MAT-SI", 5),       # датчики/электроника
        # Итого: 100%

        # Конденсатор натрия (800 кг)
        ("EQU-032", "MAT-FE", 60),      # корпус, радиатор
        ("EQU-032", "MAT-MGO", 25),     # футеровка MgO (Tкип Na = 883°C)
        ("EQU-032", "MAT-AL", 10),      # теплообменник
        ("EQU-032", "MAT-SI", 5),       # датчики/электроника
        # Итого: 100%

        # Конденсатор магния (1500 кг)
        ("EQU-033", "MAT-FE", 55),      # корпус, радиатор
        ("EQU-033", "MAT-MGO", 30),     # больше футеровки (Tкип Mg = 1091°C)
        ("EQU-033", "MAT-AL", 10),      # теплообменник
        ("EQU-033", "MAT-SI", 5),       # датчики/электроника
        # Итого: 100%

        # =====================================
        # КОМПОНЕНТЫ — ИМПОРТ
        # =====================================

        # BLDC мотор Cu (5 кг)
        ("CMP-004", "MAT-CU", 60),      # медные обмотки
        ("CMP-004", "MAT-FE", 35),      # магниты, корпус
        ("CMP-004", "MAT-SI", 5),       # электроника/энкодер
        # Итого: 100%

        # Li-ion батарея (10 кг)
        ("CMP-005", "MAT-LI", 25),      # литий
        ("CMP-005", "MAT-AL", 40),      # корпус, фольга
        ("CMP-005", "MAT-C", 20),       # графит анода
        ("CMP-005", "MAT-CU", 10),      # контакты, BMS
        ("CMP-005", "MAT-SI", 5),       # электроника BMS
        # Итого: 100%

        # GaAs панель (5 кг/м²)
        ("CMP-009", "MAT-GAAS", 30),    # арсенид галлия
        ("CMP-009", "MAT-AL", 60),      # подложка, рама
        ("CMP-009", "MAT-SI", 10),      # электроника/bypass диоды
        # Итого: 100%

        # =====================================
        # КОМПОНЕНТЫ — МЕСТНЫЕ
        # =====================================

        # BLDC мотор Al (5 кг)
        ("CMP-011", "MAT-AL", 55),      # алюминиевые обмотки
        ("CMP-011", "MAT-FE", 40),      # магниты, корпус
        ("CMP-011", "MAT-SI", 3),       # электроника управления
        ("CMP-011", "MAT-MOS2", 2),     # сухая смазка подшипников
        # Итого: 100%

        # NaS батарея 1кВт·ч (8 кг)
        ("CMP-012", "MAT-NA", 30),      # натрий (анод)
        ("CMP-012", "MAT-S", 25),       # сера (катод)
        ("CMP-012", "MAT-AL2O3", 35),   # бета-глинозём (электролит)
        ("CMP-012", "MAT-AL", 5),       # корпус
        ("CMP-012", "MAT-FE", 5),       # контакты, термоизоляция
        # Итого: 100%

        # Подшипник Al₂O₃ (0.5 кг)
        ("CMP-013", "MAT-AL2O3", 95),   # корунд (местное производство)
        ("CMP-013", "MAT-FE", 5),       # обойма, сепаратор
        # Итого: 100%

        # Редуктор (3 кг)
        ("CMP-014", "MAT-FE", 80),      # шестерни
        ("CMP-014", "MAT-AL", 15),      # корпус
        ("CMP-014", "MAT-MOS2", 5),     # сухая смазка
        # Итого: 100%

        # =====================================
        # ПРОДУКЦИЯ
        # =====================================

        # Зеркало 100×100м (116 кг) — по mirrors.qmd
        ("PRD-001", "MAT-AL", 94.8),    # 110 кг: фольга 4 мкм
        ("PRD-001", "MAT-FE", 4.3),     # 5 кг: грузики 3 кг + тросы 2 кг
        ("PRD-001", "MAT-TIO2", 0.86),  # 1 кг: электрохромика TiO₂
        # Итого: 99.96% (~116 кг)

        # Робот Gen-2 усреднённый (320 кг)
        ("PRD-002", "MAT-FE", 46.9),    # 150 кг рама, шасси
        ("PRD-002", "MAT-AL", 15.6),    # 50 кг корпус, радиаторы
        ("PRD-002", "MAT-NA", 15.6),    # 50 кг батарея NaS (Na)
        ("PRD-002", "MAT-S", 15.6),     # 50 кг батарея NaS (S)
        ("PRD-002", "MAT-SI", 3.2),     # 10 кг электроника, датчики
        ("PRD-002", "MAT-CU", 1.6),     # 5 кг проводка
        ("PRD-002", "MAT-MOS2", 1.5),   # 5 кг смазка
        # Итого: 100%

        # Купол (8000 кг)
        ("PRD-003", "MAT-SI", 93.75),   # 7500 кг силикатная ткань
        ("PRD-003", "MAT-AL", 6.25),    # 500 кг газонепроницаемая мембрана
        # Итого: 100%

        # NaS батарея 15кВт·ч (100 кг)
        ("PRD-004", "MAT-NA", 30),      # 30 кг натрий
        ("PRD-004", "MAT-S", 25),       # 25 кг сера
        ("PRD-004", "MAT-AL2O3", 35),   # 35 кг бета-глинозём
        ("PRD-004", "MAT-AL", 5),       # 5 кг корпус
        ("PRD-004", "MAT-FE", 5),       # 5 кг контакты, термоизоляция
        # Итого: 100%

        # Si панель (10 кг/м²) — по railgun.qmd панели ~3.5 кг/м², но с защитой ~10 кг/м²
        ("PRD-005", "MAT-SI", 50),      # 5 кг: ячейки 3 кг + стекло/SiO₂ защита 2 кг
        ("PRD-005", "MAT-AL", 45),      # 4.5 кг: рама + подложка + кабели
        ("PRD-005", "MAT-CU", 5),       # 0.5 кг проводка, контакты
        # Итого: 100%

        # Силикатная ткань (0.3 кг/м²)
        ("PRD-006", "MAT-SI", 95),      # SiO₂ волокно
        ("PRD-006", "MAT-AL", 5),       # связующее покрытие
        # Итого: 100%

        # =====================================
        # ТРАНСПОРТ
        # =====================================

        # Контейнер графита (20 кг)
        ("TRN-001", "MAT-AL", 90),      # алюминиевый корпус
        ("TRN-001", "MAT-FE", 10),      # крепления, замки
        # Итого: 100%

        # Капсула зеркала (10 кг)
        ("TRN-002", "MAT-AL", 95),      # алюминий
        ("TRN-002", "MAT-FE", 5),       # крепления
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

    # Запуск валидации
    from validate import validate
    if not validate(DB_PATH):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
