# Review: ru/science/detailed/production/railguns/overview.qmd

## Critical Issues

### 1. Physics Inconsistency: Track Length vs Acceleration vs Time

The document states:
- Target velocity: 5 km/s (5000 m/s)
- Track length: 2-3 km
- Acceleration: ~420 m/s^2 (43g)
- Acceleration time: ~12 sec

**Problem:** These values are internally inconsistent.

Calculation 1: If a = 420 m/s^2 and v = 5000 m/s:
- Time: t = v/a = 5000/420 = 11.9 sec (matches stated ~12 sec)
- Distance: s = v^2/(2a) = 25,000,000/840 = 29,761 m = **~30 km** (NOT 2-3 km!)

Calculation 2: If track length = 3 km and v = 5000 m/s:
- Acceleration: a = v^2/(2s) = 25,000,000/6000 = 4167 m/s^2 = **425g** (NOT 43g!)
- Time: t = v/a = 5000/4167 = 1.2 sec (NOT ~12 sec!)

**Conclusion:** Either:
- Track length should be ~30 km for 43g acceleration
- OR acceleration should be ~425g for a 3 km track

This same error appears in constants.qmd and theory.qmd - it's a project-wide inconsistency.

**Recommendation:** Decide which parameter is the design constraint:
- If 43g is the max acceptable acceleration (for payload survival), track must be ~30 km
- If 3 km is the max feasible track length, acceleration must be ~425g

## Minor Issues

### 2. Heat Dissipation Calculation

Line 274 mentions:
- Average power: 33 MW
- Heat dissipation: ~40 MW

At 40% efficiency, if 33 MW is average input, heat would be 33 * 0.6 = 19.8 MW.
If 40 MW thermal is correct, average input would be 40/0.6 = 67 MW.

Minor inconsistency, but should be clarified.

## Verified Correct

- Mercury escape velocity: 4.3 km/s (matches NASA/constants.qmd)
- Mercury gravity: 3.7 m/s^2 (0.38g) (matches NASA/constants.qmd)
- Mirror mass: 116 kg (matches constants.qmd)
- Kinetic energy calculation: E = 0.5 * 116 * 5000^2 = 1.45 GJ (correct)
- Energy with 40% efficiency: 1.45/0.40 = 3.6 GJ (correct)
- All internal links exist and are valid

## Materials on Mercury

The document correctly identifies:
- Local: Steel Fe-6%Mn, Aluminum (cryo-cooled)
- Import: Electronics (~7 tons)
- Localization: 99.5% by mass (consistent with project data)
