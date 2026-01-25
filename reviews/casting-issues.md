# Review: casting.qmd

## File: ru/science/detailed/production/factories/elements/casting.qmd

### Issues Found

#### Critical (Fixed)

1. **Line 72 - Incorrect copper/steel thermal conductivity ratio**
   - **Original:** "Теплопроводность 400 Вт/(м·K) — в 2× быстрее отводит тепло, чем сталь"
   - **Problem:** Copper (401 W/m·K) vs Carbon Steel (~45-50 W/m·K) = approximately 8× difference, not 2×
   - **Sources:**
     - [Engineering Toolbox](https://www.engineeringtoolbox.com/thermal-conductivity-metals-d_858.html)
     - [Speciality Metals](https://www.smetals.co.uk/comparing-the-thermal-conductivity-of-different-metals/)
   - **Fix:** Changed to "~8× быстрее"

### Verified as Correct

1. **NaK temperature range:** -12°C to +785°C matches eutectic NaK-77 properties
   - Source: [Wikipedia - Sodium-potassium alloy](https://en.wikipedia.org/wiki/Sodium%E2%80%93potassium_alloy)

2. **Copper thermal conductivity:** 400 W/(m·K) - actual value is 401 W/(m·K)
   - Source: [Langley Alloys](https://www.langleyalloys.com/knowledge-advice/what-is-the-thermal-conductivity-of-copper/)

3. **Steel melting point:** 1500°C matches constants.qmd

4. **Energy calculation:** 195 kW total is arithmetically correct

5. **Material balance:** Losses of 1.2% (Al) and 1.5% (Fe) are reasonable for continuous casting

### Internal Links

All verified as valid:
- `melting.qmd` - exists
- `rolling.qmd` - exists
- `../../materials/overview.qmd` - exists
- `../../robots/overview.qmd` - exists

### Materials Availability

- Copper crystallizer: correctly marked as Earth import
- NaK: available from Mercury (Na+K from distillation)
- Steel rollers: available from Mercury (Fe-6%Mn)
- MgO refractory: available from Mercury

---
Reviewed: 2026-01-25
