#!/bin/bash
# Post-render script: copies data directories to subdirectories in _output
# Fixes OJS FileAttachment paths which are relative to the rendered document

set -e

echo "Copying data directories to _output subdirectories..."

# Source data directories
RU_DATA="ru/science/data"
EN_DATA="en/science/data"

# Target directories where OJS widgets are used
TARGETS=(
  "_output/ru/science/summaries"
  "_output/en/science/summaries"
  "_output/ru/science/detailed"
  "_output/en/science/detailed"
  "_output/ru/science/detailed/materials"
  "_output/ru/science/detailed/factories"
  "_output/ru/science/detailed/factories/assembly"
  "_output/ru/science/detailed/factories/elements"
  "_output/ru/science/detailed/railguns"
  "_output/ru/science/detailed/railguns/assembly"
  "_output/ru/science/detailed/railguns/elements"
  "_output/ru/science/detailed/robots"
  "_output/ru/science/detailed/robots/assembly"
  "_output/ru/science/detailed/robots/elements"
  "_output/en/science/detailed/materials"
  "_output/en/science/detailed/factories"
  "_output/en/science/detailed/factories/assembly"
  "_output/en/science/detailed/factories/elements"
  "_output/en/science/detailed/railguns"
  "_output/en/science/detailed/railguns/assembly"
  "_output/en/science/detailed/railguns/elements"
  "_output/en/science/detailed/robots"
  "_output/en/science/detailed/robots/assembly"
  "_output/en/science/detailed/robots/elements"
)

for target in "${TARGETS[@]}"; do
  if [[ -d "$target" ]]; then
    # Determine which data source to use based on language
    if [[ "$target" == *"/ru/"* ]]; then
      DATA_SRC="$RU_DATA"
    else
      DATA_SRC="$EN_DATA"
    fi

    # Remove existing data symlink/directory if it exists
    rm -rf "$target/data" 2>/dev/null || true

    # Copy data directory
    if [[ -d "$DATA_SRC" ]]; then
      cp -r "$DATA_SRC" "$target/data"
      echo "  Copied $DATA_SRC -> $target/data"
    fi
  fi
done

echo "Data copy complete!"
