# Silicon Production Review Issues

**File:** `ru/science/detailed/production/materials/silicon.qmd`
**Reviewed:** 2026-01-25

## ✅ RESOLVED (2026-01-26)

All stoichiometry issues have been fixed:

### Fixes Applied

1. **Corundum ratio** (line 37): 1.3 kg → **2.4 kg** Al₂O₃ per kg Si
2. **Material balance** (line 65): Al 126t → **90t** (for 70t Si)
3. **Corundum balance** (line 67): 91t → **170t** (matches 70t × 2.42)

### Verification

Reaction: `3SiO₂ + 4Al → 3Si + 2Al₂O₃`

**For 70 tons Si:**
- Al needed: 70 × 1.28 = **90t** ✓
- Al₂O₃ produced: 70 × 2.42 = **169t ≈ 170t** ✓

**Sources:**
- [ACS Sustainable Chemistry](https://pubs.acs.org/doi/10.1021/acssuschemeng.4c05326): "4 Al / 3 SiO₂"
- [NTNU Research](https://ntnuopen.ntnu.no/ntnu-xmlui/handle/11250/3153028): CaO-Al₂O₃ slag formation

**Files updated:**
- `ru/science/detailed/production/materials/silicon.qmd`
- `en/science/detailed/production/materials/silicon.qmd`

---

## ~~Critical Issue: Stoichiometry Error~~ (FIXED)

### ~~Problem~~

~~The byproduct calculation for Al₂O₃ (corundum) is incorrect.~~

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
   - Document says 1.3 kg - **OK (rounded)** ✓

2. Al₂O₃ produced:
   - Ratio: 2 mol Al₂O₃ / 3 mol Si
   - Mass ratio: (2 × 101.96) / (3 × 28.09) = 203.92 / 84.27 = **2.42 kg Al₂O₃**
   - Document now says 2.4 kg - **FIXED** ✓

---

## ~~Secondary Issue: Material Balance Inconsistency~~ (FIXED)

**Corrected values for 70 tons Si:**
- Aluminum: **90 tons** ✓
- Corundum: **170 tons** ✓

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

**COMPLETED** - Both ru and en versions updated and consistent.
