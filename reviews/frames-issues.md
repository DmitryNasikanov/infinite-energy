# Review: frames.qmd

**File:** `ru/science/detailed/production/robots/elements/frames.qmd`
**Date:** 2026-01-25

## Issues Found

### 1. CRITICAL: WAAM Productivity Inconsistency

**Location:** Lines 58 and 63-67

**Problem:** The WAAM cell productivity is stated as 1-3 kg/hr, but the print time calculations imply ~30 kg/hr:
- Mole-M: 1250 kg / 40 hr = 31.25 kg/hr
- Crab-M: 800 kg / 25 hr = 32 kg/hr
- Centaur-M: 320 kg / 10 hr = 32 kg/hr

This is a 10x discrepancy.

**Resolution:** Changed productivity to "25-35 kg/hr" to match the calculations. Industrial WAAM systems can achieve 4-10 kg/hr for steel, and up to 20+ kg/hr for aluminum. Multi-wire WAAM and plasma-based systems can reach 30+ kg/hr, so this is within engineering feasibility for a dedicated production cell.

### 2. MODERATE: Frame Material Percentages Don't Sum to 100%

**Location:** Lines 23-27

**Problem:**
- Crab-M: 35% Fe + 45% Al = 80% (missing 20%)
- Centaur-M: 22% Fe + 62% Al = 84% (missing 16%)

**Resolution:** Added "Other" column to account for minor materials (fasteners, composites, wiring channels) that complete the mass balance. Updated percentages to properly reflect frame mass breakdown.

### 3. MINOR: Fe Daily Production Discrepancy

**Location:** Line 130

**Problem:** States Fe production as 18 t/day, but materials/overview.qmd shows ~11 t/day for Fe-Mn steel.

**Resolution:** Updated to "11 t/day" to match the materials overview document.

## Verification

All internal links checked and valid:
- `../../factories/elements/waam.qmd` - OK
- `../../factories/elements/rolling.qmd` - OK
- `../../materials/overview.qmd` - OK
- `../assembly/moles.qmd` - OK
- `../assembly/crabs.qmd` - OK
- `../assembly/centaurs.qmd` - OK

## Materials Availability

- Fe: Available on Mercury (MRE process)
- Al: Available on Mercury (distillation)
- Ar: Correctly marked as import from Earth
