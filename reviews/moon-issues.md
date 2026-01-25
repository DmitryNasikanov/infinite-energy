# Review: ru/science/summaries/moon.qmd

## Critical Issue

### Lunar Mass Driver Length Inconsistency

**Location:** Lines 168-172

**Current text:**
```
- Длина: 1-1.5 км (vs 2-3 км на Меркурии)
- Скорость: 2.5 км/с
- Энергия: 3-4 ГДж/т (в 3× экономичнее)
```

**Problem:** The lunar mass driver length (1-1.5 km) and Mercury mass driver length (2-3 km) are inconsistent with the detailed calculations in `ru/science/detailed/production/railguns/theory.qmd`:

| Parameter | moon.qmd (incorrect) | theory.qmd (correct) |
|-----------|---------------------|---------------------|
| Lunar MD length | 1-1.5 km | ~15 km |
| Mercury MD length | 2-3 km | ~30 km |

**Physics verification:**
- Lunar escape velocity: 2.4 km/s (from constants.qmd)
- Target velocity: 2.5 km/s (16% margin)
- Acceleration: 20-25g = ~245 m/s²
- Track length: v²/(2a) = 2500²/(2×245) = **12.76 km ≈ 15 km**

The same inconsistency exists in `ru/science/reference/glossary.qmd` (line 183).

**Recommendation:** Update to match theory.qmd values:
```
- Длина: ~15 км (vs ~30 км на Меркурии)
- Скорость: 2.5 км/с
- Энергия: 3-4 ГДж/т (в 3-4× экономичнее)
```

---

## Verified (No Issues)

### Efficiency Calculation
- Formula: η = 0.90 × 0.72 × 0.90 × 0.45 × 0.90 × 0.95 × 0.95 × 0.85 = **0.18 (18%)**
- **CORRECT** - matches detailed calculation

### Physical Constants
- Lunar tidal lock (приливный захват) - **CORRECT**
- Lunar month: 29.5 days - **CORRECT**
- Microwave frequency: 2.45 GHz - **CORRECT** (N₂ and O₂ transparent at this frequency)
- Rectenna intensity: 230 W/m² vs sun 1000 W/m² - **CORRECT**
- Atmospheric transmission: 95% - **CORRECT**

### Internal Links (All Valid)
- `../reference/technology-readiness.qmd#микроволновая-передача-энергии` - EXISTS
- `../detailed/hub.qmd` - EXISTS
- `../detailed/hub.qmd#альтернативные-архитектуры` - EXISTS
- `../detailed/production.qmd` - EXISTS
- `../detailed/production/railguns/theory.qmd` - EXISTS
- `roadmap.qmd` - EXISTS
- `comparison.qmd` - EXISTS

### Mercury Materials Reference
- Criswell reference is valid and correctly cited

---

## Status

- [x] Fix lunar mass driver length inconsistency (CRITICAL) - FIXED in moon.qmd
- [x] Physics calculations verified
- [x] Internal links verified
- [x] Constants verified against reference

## Note

The glossary.qmd file still contains outdated lunar mass driver length values (1-1.5 km). Consider updating ru/science/reference/glossary.qmd to match.
