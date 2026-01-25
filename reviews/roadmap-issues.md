# roadmap.qmd Review Issues

## Critical Issues

### 1. Solar Flux Value Inconsistency
**Location:** Lines 559, 674, 1119
**Problem:** Document uses "9 kW/m²" for Mercury solar flux
**Reference:** `constants.qmd` states Mercury average solar flux is **10,343 W/m² (~10.3 kW/m²)**
**Impact:** Affects energy calculations for Ground Zero Factory startup
**Fix:** Replace "9 kVt/m²" with "10 kVt/m²" for consistency

### 2. Mass Driver Track Length Discrepancy
**Location:** Lines 284, 881
**Problem:** States "2-3 km" for Mercury Mass Driver track
**Reference:** `theory.qmd` specifies **~30 km** track length for 5 km/s launch velocity at 43g
**Impact:** Major underestimate of infrastructure requirements
**Fix:** Update to "2-3 km" -> should clarify this is for **testing** (Earth/Moon), not full Mercury MD

**Note:** Line 284 appears to mix test MD parameters with production MD. The 500-1000m (Earth), 1-1.5 km (Moon), and 2-3 km (Mercury) are inconsistent with theory.qmd which states 30 km for Mercury.

### 3. Dyson Swarm Area Unit Error
**Location:** Lines 908-909
**Problem:** States "Общая площадь: 1.1×10¹³ м² (~11 000 км²)"
**Calculation:** 1.1×10¹³ m² = 1.1×10⁷ km² = **11,000,000 km²** (11 million km²)
**Impact:** Off by factor of 1000
**Fix:** Change "~11 000 км²" to "~11 млн км²" or "~11 000 000 км²"

## Medium Issues

### 4. Swarm Mirror Power at Different Efficiencies
**Location:** Lines 823-824
**Problem:** States "205 TW reflected" and "47 TW to Earth (23% efficiency)"
**Reference:** `mirrors.qmd` and `hub.qmd` use 18% efficiency for LSP path
**Calculation check:** 205 TW × 0.23 = 47.15 TW (matches), but 23% vs 18% inconsistency
**Note:** The 23% might be intentional for Year 1 estimates with different efficiency assumptions. Should clarify.

### 5. Links Verification - All Internal Links Valid
**Verified links exist:**
- `../detailed/mirrors.qmd` - exists
- `../detailed/production/railguns/theory.qmd` - exists
- `budget.qmd` - exists
- `../reference/technology-readiness.qmd` - exists
- `../detailed/production/factories/overview.qmd` - exists
- `../detailed/production/robots/overview.qmd` - exists
- `../detailed/hub.qmd` - exists
- `../summaries/moon.qmd` - exists (referenced as `../summaries/moon.qmd`)

## Minor Issues

### 6. Moon Phase Timeline
**Location:** Lines 347-349
**Note:** Budget states "9-18 млрд" for Луна phase, roadmap states "9-18 млрд" - consistent

### 7. Mercury Materials Mentioned
**Verified:** Al, Fe, Si, Ti, S mentioned - all confirmed available on Mercury per documentation

## Physics Constants Verified

| Parameter | Roadmap Value | constants.qmd | Status |
|-----------|---------------|---------------|--------|
| Mercury escape velocity | 4.3 km/s (implied) | 4.3 km/s | OK |
| Launch velocity | 5 km/s | 5 km/s (with margin) | OK |
| Mirror area | 10,000 m² | 10,000 m² | OK |
| Mirror mass | 116 kg | 116 kg | OK |
| Mirror power | 93 MW | 93 MW | OK |
| LSP efficiency | 18% | 18% | OK |
| Lunar escape velocity | 2.4-2.5 km/s | 2.4 km/s | OK |

## Recommended Fixes

1. **Line 559:** Change "9 кВт/м²" to "10 кВт/м²" - **FIXED**
2. **Line 674:** Change "9 кВт/м²" to "10 кВт/м²" - **FIXED** (also updated calculation 54->60 МВт)
3. **Line 1119:** Change "9 кВт/м²" to "10 кВт/м²" - **FIXED**
4. **Line 284:** Clarify track lengths - add note that 2-3 km is simplified, actual production MD is 30 km - **DEFERRED** (requires deeper analysis of MD sections)
5. **Line 908-909:** Fix area unit: "~11 000 км²" -> "~11 млн км²" - **FIXED**
