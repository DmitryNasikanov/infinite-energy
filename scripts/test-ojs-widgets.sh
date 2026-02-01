#!/bin/bash
# Automated test for OJS widgets in rendered output
# Verifies that OJS FileAttachment can find required data files

set -e

echo "=== OJS Widget Test Suite ==="
echo ""

ERRORS=0
WARNINGS=0

# Files with OJS widgets that need data
OJS_FILES=(
  "_output/ru/science/summaries/mirrors.html"
  "_output/en/science/summaries/mirrors.html"
  "_output/ru/science/detailed/hub.html"
  "_output/en/science/detailed/hub.html"
  "_output/ru/science/detailed/materials/mre.html"
  "_output/en/science/detailed/materials/mre.html"
  "_output/ru/science/detailed/materials/distillation.html"
  "_output/en/science/detailed/materials/distillation.html"
  "_output/ru/science/detailed/materials/carbon.html"
  "_output/en/science/detailed/materials/carbon.html"
  "_output/ru/science/detailed/materials/overview.html"
  "_output/en/science/detailed/materials/overview.html"
  "_output/ru/science/detailed/railguns/theory.html"
  "_output/en/science/detailed/railguns/theory.html"
  "_output/ru/science/detailed/railguns/overview.html"
  "_output/en/science/detailed/railguns/overview.html"
  "_output/ru/science/detailed/robots/elements/batteries.html"
  "_output/en/science/detailed/robots/elements/batteries.html"
)

echo "1. Checking rendered HTML for OJS errors..."
for file in "${OJS_FILES[@]}"; do
  if [[ ! -f "$file" ]]; then
    echo "  WARN: $file not found (skipping)"
    WARNINGS=$((WARNINGS + 1))
    continue
  fi

  # Check for OJS runtime errors embedded in HTML
  if grep -qi "OJS Runtime Error\|Unable to load file" "$file"; then
    echo "  FAIL: OJS error in $file"
    ERRORS=$((ERRORS + 1))
  else
    echo "  OK: $file"
  fi
done

echo ""
echo "2. Checking data file existence in _output..."

# Main data files at science level
DATA_FILES=(
  "_output/ru/science/data/db/data.json"
  "_output/en/science/data/db/data.json"
)

for data in "${DATA_FILES[@]}"; do
  if [[ ! -f "$data" ]]; then
    echo "  FAIL: Missing $data"
    ERRORS=$((ERRORS + 1))
  else
    echo "  OK: $data"
  fi
done

# Data directories in subdirectories (for FileAttachment relative paths)
SUBDIR_DATA=(
  "_output/ru/science/summaries/data/db/data.json"
  "_output/en/science/summaries/data/db/data.json"
  "_output/ru/science/detailed/data/db/data.json"
  "_output/en/science/detailed/data/db/data.json"
)

echo ""
echo "3. Checking data in subdirectories..."
for data in "${SUBDIR_DATA[@]}"; do
  if [[ ! -f "$data" ]]; then
    echo "  FAIL: Missing $data (OJS widgets will fail)"
    ERRORS=$((ERRORS + 1))
  else
    echo "  OK: $data"
  fi
done

echo ""
echo "=== Summary ==="
if [[ $ERRORS -gt 0 ]]; then
  echo "FAILED: $ERRORS error(s), $WARNINGS warning(s)"
  echo ""
  echo "To fix: run 'bash scripts/copy-data-to-output.sh' after render"
  exit 1
fi

if [[ $WARNINGS -gt 0 ]]; then
  echo "PASSED with $WARNINGS warning(s)"
else
  echo "PASSED: All OJS widget tests passed!"
fi
exit 0
