# Issues: ru/science/detailed/production/materials/overview.qmd

## Broken Links

### 1. OJS Widget Link (Line 146)
**Current:** `data/nomenclature.html?unit=${unitId}`
**Problem:** No `data/` folder exists relative to the rendered HTML location
**Correct:** `../../../reference/nomenclature.html?unit=${unitId}`

### 2. Appendix Links (Lines 578-579)
**Current:** `../../../../reference/nomenclature.html?unit=EQU-021`
**Problem:** Path goes 4 levels up (to `ru/`), but `reference/` is under `science/`
**Correct:** `../../../reference/nomenclature.html?unit=EQU-021`

Same issue for EQU-004 link on line 579.

## Data Consistency

- All referenced unit IDs (EQU-034, EQU-005, EQU-022, EQU-023, CMP-011, EQU-021, EQU-004) exist in data.json
- All internal .qmd links verified to exist:
  - silicate-fabric.qmd
  - mre.qmd
  - distillation.qmd
  - titanium.qmd
  - technology-readiness.qmd
  - production.qmd
  - energy.qmd
  - batteries.qmd

## Recommended Fixes

```qmd
# Line 146: Change
<a href="data/nomenclature.html?unit=${unitId}">
# To:
<a href="../../../reference/nomenclature.html?unit=${unitId}">

# Lines 578-579: Change
(../../../../reference/nomenclature.html?unit=EQU-021)
(../../../../reference/nomenclature.html?unit=EQU-004)
# To:
(../../../reference/nomenclature.html?unit=EQU-021)
(../../../reference/nomenclature.html?unit=EQU-004)
```

## Translation Status

**COMPLETED** - English translation created at `en/science/detailed/production/materials/overview.qmd`

The English version has corrected nomenclature links (`../../../reference/nomenclature.html?unit=...`).

Note: Quarto warnings about unresolved links to production.qmd, energy.qmd, and batteries.qmd are expected - those English pages have not been translated yet.

## Still Needed for Russian Version

The Russian source file at `ru/science/detailed/production/materials/overview.qmd` still needs the link fixes described above.
