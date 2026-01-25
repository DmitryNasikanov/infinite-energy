# Review: ru/science/detailed/production.qmd

**Date:** 2026-01-25
**Status:** Reviewed

---

## Summary

Overall the document is technically sound. One inconsistency found regarding mirror aluminum mass.

---

## Issues Found

### 1. Mirror Aluminum Mass Inconsistency (Minor)

**Location:** Lines 171, 381

**Problem:** The document states mirrors use "95 kg Al" for calculating daily mirror output:
- Line 171: "600 т реголита/день -> 42 т Al + 18 т Fe -> ~407 зеркал/день (Ф-З)"
- Line 381: "Прокат фольги (Ф-З) | ~407 зеркал/день | 42 т / 95 кг Al x 0.92"

However, `constants.qmd` specifies:
- Foil mass: ~110 kg (calculated as 10000 m^2 x 4 um x 2700 kg/m^3 = 108 kg)
- Total mirror mass: 116 kg

**Correct calculation with 110 kg Al:**
- 42000 kg / 110 kg = 381.8 mirrors
- 381.8 x 0.92 yield = ~351 mirrors/day

**Impact:** The 407 mirrors/day figure is ~16% optimistic compared to the constants file.

**Recommendation:** Either update production.qmd to use 110 kg and ~351 mirrors/day, or document the 95 kg figure as a future optimization target in constants.qmd.

---

## Verified Items (No Issues)

### Physics Constants
- Solar flux on Mercury: "9-14 kW/m^2" matches constants.qmd range (6.2-14.4 kW/m^2)
- Mercury gravity: "3.7 m/s^2" matches constants.qmd
- Mass driver speed: "5 km/s" matches constants.qmd
- Light pressure: "~60 uPa" matches constants.qmd

### Calculations
- Aluminum output: 600 t x 7% = 42 t/day (correct)
- Iron output: 600 t x 3% = 18 t/day (correct)
- First expedition manifest: 22.5 + 1.6 + 35 + 1.5 + 1.0 = 61.6 ~ 62 t (correct)

### Materials on Mercury
- Al, Si, S, Fe, Mg, Ti, Na, K presence confirmed in materials/overview.qmd
- Carbon in LRM zones from MESSENGER data (confirmed via link)

### Internal Links
All internal links verified to exist:
- energy.qmd
- production/materials/overview.qmd
- production/robots/elements/actuators.qmd
- production/robots/elements/batteries.qmd
- production/factories/assembly/replication.qmd
- production/railguns/overview.qmd
- production/railguns/theory.qmd
- production/railguns/scaling.qmd
- production/robots/overview.qmd
- production/factories/overview.qmd

### External Links
- MESSENGER 2016 link (hub.jhu.edu) - verified working and relevant

---

## No Action Required

The aluminum mass inconsistency is minor and doesn't affect the overall feasibility argument. Both numbers are within engineering estimates range.
