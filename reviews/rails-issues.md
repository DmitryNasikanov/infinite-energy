# Review: rails.qmd

## ✅ RESOLVED (2026-01-26)

The rail mass calculation has been fixed:
- Profile changed from solid to **hollow** (15 mm wall thickness)
- Baseline track length changed from 3 km to **1 km**
- Mass corrected: ~70 t per 1 km (was 200 t for claimed 3 km)

**Files updated:**
- `ru/science/detailed/production/railguns/elements/rails.qmd`
- `en/science/detailed/production/railguns/elements/rails.qmd`
- `frame.qmd` (ru/en): 200 t → 210 t for 3 km
- `track.qmd` (ru/en): 200 t → 210 t for 3 km

---

## ~~Potential Issue: Rail Mass Calculation~~ (FIXED)

**File:** `ru/science/detailed/production/railguns/elements/rails.qmd`

**Stated values:**
- Profile: 200x300 mm rectangular
- Cooling channel: 50 mm diameter
- Length: 3 km (300 segments x 10 m)
- Mass: ~200 t for pair of rails

**Calculation check:**
- Cross-section area: 0.2 x 0.3 = 0.06 m^2
- Cooling channel area: pi x 0.025^2 = ~0.002 m^2
- Net cross-section: ~0.058 m^2 per rail
- For 2 rails x 3000 m x 0.058 m^2 = 348 m^3
- With Al density 2700 kg/m^3: 348 x 2700 = 939,600 kg = ~940 t

**Discrepancy:** Stated 200 t vs calculated ~940 t

**Possible explanations:**
1. The cooling channel may be larger than Ø50 mm (could be hollow rectangular)
2. The profile dimensions may include spacing/air gaps not specified
3. The table may show approximate values for initial design

**Recommendation:** Verify intended rail cross-section and update mass estimate, or add clarifying note about why mass is lower than solid calculation.

## Physics Constants: VERIFIED

- Aluminum conductivity at room temp: 60% IACS (correct)
- Conductivity increase at -180°C: ~6x for Al (plausible, based on RRR)
- Copper comparison at cryo temps: consistent
- Acceleration 43g: matches constants.qmd (420 m/s^2)

## Internal Links: ALL VALID

- `../../factories/elements/rolling.qmd` - EXISTS
- `../../factories/elements/waam.qmd` - EXISTS
- `coils.qmd` - EXISTS
- `frame.qmd` - EXISTS
- `../assembly/track.qmd` - EXISTS

## Materials on Mercury: CONSISTENT

- Aluminum: Available via MRE (Molten Regolith Electrolysis)
- NaK coolant: Can be synthesized locally (Na and K in regolith)
- Referenced materials match project resource assumptions

## Overall Assessment: MINOR ISSUES

The document is internally consistent and physics is reasonable. The only concern is the mass calculation that may need clarification. Not blocking for translation.
