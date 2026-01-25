# Silicon Production Review Issues

**File:** `ru/science/detailed/production/materials/silicon.qmd`
**Reviewed:** 2026-01-25

## Critical Issue: Stoichiometry Error

### Problem

The byproduct calculation for Al₂O₃ (corundum) is incorrect.

**Current text (line 36-37):**
> - На 1 кг кремния: 1.3 кг алюминия
> - Побочно: 1.3 кг корунда (Al₂O₃)

### Correct Calculation

Reaction: `3SiO₂ + 4Al → 3Si + 2Al₂O₃`

**Molar masses:**
- Si: 28.09 g/mol
- Al: 26.98 g/mol
- Al₂O₃: 101.96 g/mol

**For 1 kg Si:**

1. Aluminum needed:
   - Ratio: 4 mol Al / 3 mol Si
   - Mass ratio: (4 × 26.98) / (3 × 28.09) = 107.92 / 84.27 = **1.28 kg Al**
   - Document says 1.3 kg - **OK (rounded)**

2. Al₂O₃ produced:
   - Ratio: 2 mol Al₂O₃ / 3 mol Si
   - Mass ratio: (2 × 101.96) / (3 × 28.09) = 203.92 / 84.27 = **2.42 kg Al₂O₃**
   - Document says 1.3 kg - **INCORRECT**

### Correction Needed

Change line 37 from:
```
- Побочно: 1.3 кг корунда (Al₂O₃)
```

To:
```
- Побочно: 2.4 кг корунда (Al₂O₃)
```

---

## Secondary Issue: Material Balance Inconsistency

### Problem

The material balance table (lines 62-68) doesn't match corrected stoichiometry.

**Current values for 70 tons Si:**
- Aluminum: 126 tons
- Corundum: 91 tons

**Correct values (using stoichiometry):**
- Aluminum: 70 × 1.28 = **90 tons**
- Corundum: 70 × 2.42 = **169 tons**

**OR** if 126 tons Al is the actual input:
- Silicon produced: 126 / 1.28 = **98.4 tons** (not 70)
- Corundum: 98.4 × 2.42 = **238 tons** (not 91)

### Recommendation

Review and reconcile material balance numbers. The values seem internally inconsistent.

---

## Minor Issues

None found.

---

## Verified Items

1. **Chemical equation** - Balanced correctly: `3SiO₂ + 4Al → 3Si + 2Al₂O₃`
2. **Internal links** - All three links verified to exist:
   - `distillation.qmd` - exists
   - `mre.qmd` - exists
   - `../../energy.qmd` - exists
3. **Temperature** - 2000°C for solar furnace aluminothermy is plausible
4. **Al/Si ratio** - 1.3 kg Al per 1 kg Si is correct (rounded from 1.28)

---

## Translation Status

**BLOCKED** - Cannot translate until stoichiometry issues are resolved.

Once corrected, translate to: `en/science/detailed/production/materials/silicon.qmd`
