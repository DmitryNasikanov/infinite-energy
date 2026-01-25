# Review: energy.qmd

## Critical Issues (FIXED)

### 1. Heat Dissipation Calculation Error [FIXED]
**Location:** Lines 437-443

**Problem:** Document stated continuous heat dissipation of "~40 MW" but calculation shows:
- 600 shots/day x 2.9 GJ heat per shot = 1740 GJ/day
- 1740 GJ / 86400 sec = **~20 MW**, not 40 MW

**Fix:** Corrected to ~20 MW throughout the document.

### 2. Energy per Launch Inconsistency [FIXED]
**Location:** Lines 367-370 vs 437-439

**Problem:**
- Section 2 (lines 367-370) uses "4.8 GJ per launch"
- Heat section (line 437) used "4.7 GJ"

**Fix:** Standardized to 4.8 GJ throughout.

## Minor Issues

### 3. Solar Flux Range
**Location:** Lines 149, 182-183

**Problem:** Document says "9-14 kW/m^2" but constants.qmd shows:
- Perihelion: 14.4 kW/m^2
- Aphelion: 6.2 kW/m^2

**Status:** Acceptable approximation, but could be more precise (6-14 or "average 10").

### 4. GaAs Panel Efficiency Confusion
**Location:** Lines 341-344

**Problem:** Panel output seems calculated with ~1.6 kW/m^2, but GaAs at 30% efficiency on Mercury (10 kW/m^2) should yield 3 kW/m^2.

**Analysis:** The document uses 35,000 m^2 = 56 MW, implying 1.6 kW/m^2. This may be accounting for thermal derating at Mercury temperatures or other losses, but should be clarified.

**Status:** Needs clarification in text.

## Physics Constants Verification

| Parameter | energy.qmd | constants.qmd | Status |
|-----------|------------|---------------|--------|
| Solar flux Earth | 1.3 kW/m^2 | 1.361 kW/m^2 | OK (rounded) |
| Solar flux Mercury | 9-14 kW/m^2 | 6.2-14.4 kW/m^2 | Minor diff |
| Mirror mass | 116 kg | ~116 kg | OK |
| Si efficiency | 18% | 18-22% | OK |
| Escape velocity Mercury | implicit 5 km/s | 4.3 km/s | OK (with margin) |

## Internal Links Check

| Link | Target | Status |
|------|--------|--------|
| production/railguns/scaling.qmd#энергобаланс-комплекса | Section exists | OK |
| production/overview.qmd | File exists | OK |
| production/railguns/theory.qmd | File exists | OK |
| production/materials/overview.qmd | File exists | OK |

## Recommendations

1. Fix heat dissipation calculation (40 MW -> 20 MW) or add explanation for additional heat sources
2. Standardize energy per launch value to 4.8 GJ throughout
3. Add note about GaAs thermal derating at Mercury temperatures if that's the reason for lower output
