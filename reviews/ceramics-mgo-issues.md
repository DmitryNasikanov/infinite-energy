# Review: ceramics-mgo.qmd

## Issues Found

### 1. Enthalpy Notation Ambiguity (Line 77)

**Current text:**
```
2Mg + O₂ → 2MgO + тепло (∆H = -1203 кДж/моль)
```

**Problem:** The value -1203 kJ is for the entire reaction (producing 2 moles of MgO), not per mole. The standard enthalpy of formation for MgO is approximately -601.6 kJ/mol.

**Suggested fix:**
```
2Mg + O₂ → 2MgO + тепло (∆H = -601.6 кДж/моль MgO)
```
or
```
2Mg + O₂ → 2MgO + тепло (∆Hреакции = -1203 кДж)
```

---

### 2. Thermal Conductivity Contradiction (Line 212)

**Current text:**
```
| Теплопроводность | 40-60 Вт/(м·К) | Высокая → хорошая теплоизоляция |
```

**Problem:** High thermal conductivity (40-60 W/m·K) means POOR thermal insulation, not good. Good insulators have low thermal conductivity (<1 W/m·K for porous ceramics).

**Suggested fix:**
```
| Теплопроводность | 40-60 Вт/(м·К) | Высокая → быстрый теплоотвод (не изолятор) |
```

**Note:** For actual thermal insulation (line 142, 181), porous MgO felt/foam is used, which has much lower thermal conductivity than dense MgO ceramics. This distinction should be clarified.

---

### 3. Energy Consumption Inconsistency (TL;DR vs Detailed Table)

**TL;DR (line 11):**
```
Энергопотребление: ~150 кВт
```

**Detailed table (lines 199-200):**
```
ИТОГО (электрика): ~120 кВт
ИТОГО (с учётом солнца): ~160 кВт эквивалент
```

**Suggested fix:** Update TL;DR to match detailed breakdown:
```
Энергопотребление: ~120 кВт (электрика) + солнечное тепло
```

---

## Verified Correct

- Stoichiometric calculations: Mg (48 t/day) + O2 (32 t/day) → MgO (79.6 t/day theoretical, ~70 t/day actual with 88% yield) - all correct
- MgO melting point: 2852°C - correct
- Al2O3 melting point: 2072°C - correct
- Sintering temperatures: 1500-1800°C - appropriate for MgO ceramics
- Molar masses: Mg (24.3), O2 (32), MgO (40.3) - all correct
- All internal links exist and are valid

## Recommendation

Fix issues #1, #2, #3 before translation. Issue #2 is the most significant as it states the opposite of physical reality.
