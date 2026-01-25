# Review: replication.qmd

## Issues Found

### 1. Broken Link (Fixed)

**Location:** Line 96, Line 322
**File:** `ru/science/detailed/production/factories/assembly/replication.qmd`

**Issue:** Incorrect relative path to scaling.qmd

**Original:**
```
../../../production/railguns/scaling.qmd
```

**Fixed:**
```
../../railguns/scaling.qmd
```

**Explanation:** From `assembly/` directory, `../../` navigates to `production/`, then `railguns/scaling.qmd` correctly reaches the target file. The original path had an extra `../` and redundant `production/` segment.

---

### 2. Table Inconsistency (Warning)

**Location:** Line 86-92 (Replication time calculation table)

**Warning:** The table shows replication progression but the week numbers don't follow a consistent exponential doubling pattern:

| Week | Factories | Expected (doubling every 3 weeks) |
|------|-----------|-----------------------------------|
| 0    | 1         | 1 (correct)                       |
| 6    | 2         | 4 (if doubling at weeks 3, 6)     |
| 9    | 4         | 8 (if doubling at weeks 3, 6, 9)  |
| 12   | 16        | 16 (matches)                      |
| 16   | ~1000     | ~32 (at week 15)                  |

**Note:** The jump from 16 to ~1000 factories between weeks 12 and 16 seems inconsistent with the stated 3-week doubling time. This may be intentional (representing acceleration or different allocation strategies) but should be verified for accuracy.

---

## Summary

- **Critical:** 1 broken link (fixed in 2 locations)
- **Warning:** 1 table with potentially inconsistent progression values
