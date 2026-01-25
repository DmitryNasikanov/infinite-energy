# Review: ru/science/detailed/hub.qmd

## ✅ RESOLVED (2026-01-26)

The rectenna power density issue has been fixed:
- Intensity corrected from 230 W/m² to **10,000 W/m²** (matches 1 TW / 100 km²)
- Updated safety section with ICNIRP standards
- Added 4-zone territory zoning (center/middle/periphery/border)
- Added sources from NASA, JAXA, Caltech, PMC

**Research basis:**
- NASA 1978: 5 GW / 10 km ⌀ ≈ 64,000 W/m²
- JAXA: 114 mW/cm² = 1,140 W/m² (peak)
- Modern SBSP concepts: 10,000-100,000 W/m²

**Files updated:**
- `ru/science/detailed/hub.qmd`
- `en/science/detailed/hub.qmd`

---

## ~~Critical Issues~~ (FIXED)

### ~~1. Rectenna Power Density Calculation Error~~

**Location:** Line 311

**Problem:** The document states "Интенсивность на rectenna | 230 Вт/м²" but this is inconsistent with the given parameters:
- Power per rectenna: ~1 TW (line 275)
- Area per rectenna: ~100 km² = 10×10 km = 10⁸ m² (line 275)
- Calculated intensity: 10¹² W / 10⁸ m² = 10,000 W/m²

The stated 230 W/m² is ~43× lower than the actual calculation.

**Impact:** This affects safety claims comparing to US workplace standards (100 W/m²) and solar intensity (1000 W/m²).

**Possible resolutions:**
1. If 230 W/m² is the target, rectenna area should be ~4,350 km² each (66×66 km), not 100 km²
2. If 100 km² is correct, the intensity would be 10,000 W/m² (10× solar), requiring different safety discussion
3. The 230 W/m² might refer to edge intensity (Gaussian beam profile), not average

**Recommendation:** Clarify which parameter is the design driver. For now, left as-is pending author review.

## Minor Issues

### 2. PV Efficiency Inconsistency

**Location:** Lines 229 and 421

**Problem:**
- Line 229: "КПД PV (концентрация) | ~50%"
- Line 421: "PV на лунных станциях | 45%"

**Recommendation:** Use consistent value (45% is more conservative and used in final efficiency calculation).

## Verified Items

- Overall efficiency calculation (18%): Correct
  - 0.90 × 0.72 × 0.90 × 0.45 × 0.90 × 0.95 × 0.95 × 0.85 = 0.181 ≈ 18%

- Radiator area calculation (7,900 km²): Correct
  - Stefan-Boltzmann at 1000K: 5.67×10⁻⁸ × 10¹² = 56,700 W/m² ≈ 57 kW/m²
  - For 0.45 PW: 0.45×10¹⁵ / 5.7×10⁴ = 7.9×10⁹ m² ≈ 7,900 km²

- Physics constants match ru/science/reference/constants.qmd:
  - Stefan-Boltzmann constant: 5.67×10⁻⁸ W/(m²·K⁴)
  - Lunar gravity: 0.16g (1.62 m/s²)
  - Aluminum reflectivity: 90%

- All internal links verified to exist:
  - mirrors.qmd
  - ../summaries/moon.qmd
  - production/railguns/theory.qmd
  - production/robots/overview.qmd
  - ../executive-summary.qmd
  - energy.qmd
  - ../summaries/budget.qmd
  - ../summaries/roadmap.qmd

## Translation Notes

- "Хаб приёма энергии" → "Hub Station" (per terminology)
- "Рой Дайсона" → "Dyson Swarm"
- "Масс-драйвер" → "Mass Driver"
- "Крот" → "Mole"
- "Краб" → "Crab"
- "Кентавр" → "Centaur"
- "Завод «Точка Ноль»" → "Ground Zero Factory"
- "Витамины" → "Vitamins"
