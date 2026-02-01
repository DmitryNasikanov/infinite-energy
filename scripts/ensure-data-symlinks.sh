#!/bin/bash
# Создает симлинки на data/ во всех вложенных директориях с OJS-виджетами
# Запускается автоматически перед quarto render (pre-render hook)

set -e

cd "$(dirname "$0")/.."

# Список директорий, которым нужен симлинк на data/
# Формат: "путь_к_директории:относительный_путь_к_data"
SYMLINKS=(
    # RU
    "ru/science/detailed:../data"
    "ru/science/detailed/materials:../../data"
    "ru/science/detailed/railguns:../../data"
    "ru/science/detailed/railguns/assembly:../../../data"
    "ru/science/detailed/railguns/elements:../../../data"
    "ru/science/detailed/robots:../../data"
    "ru/science/detailed/robots/assembly:../../../data"
    "ru/science/detailed/robots/elements:../../../data"
    "ru/science/detailed/factories:../../data"
    "ru/science/detailed/factories/assembly:../../../data"
    "ru/science/detailed/factories/elements:../../../data"
    "ru/science/summaries:../data"
    # EN
    "en/science/detailed:../data"
    "en/science/detailed/materials:../../data"
    "en/science/detailed/railguns:../../data"
    "en/science/detailed/railguns/assembly:../../../data"
    "en/science/detailed/railguns/elements:../../../data"
    "en/science/detailed/robots:../../data"
    "en/science/detailed/robots/assembly:../../../data"
    "en/science/detailed/robots/elements:../../../data"
    "en/science/detailed/factories:../../data"
    "en/science/detailed/factories/assembly:../../../data"
    "en/science/detailed/factories/elements:../../../data"
    "en/science/summaries:../data"
)

created=0
skipped=0
errors=0

for entry in "${SYMLINKS[@]}"; do
    dir="${entry%%:*}"
    target="${entry##*:}"
    link="$dir/data"

    # Пропускаем если директория не существует
    if [[ ! -d "$dir" ]]; then
        continue
    fi

    # Если симлинк уже существует и валиден - пропускаем
    if [[ -L "$link" ]] && [[ -d "$link" ]]; then
        skipped=$((skipped + 1))
        continue
    fi

    # Удаляем битый симлинк если есть
    if [[ -L "$link" ]]; then
        rm "$link"
    fi

    # Создаем симлинк
    if ln -s "$target" "$link" 2>/dev/null; then
        echo "Created: $link -> $target"
        created=$((created + 1))
    else
        echo "ERROR: Failed to create $link" >&2
        errors=$((errors + 1))
    fi
done

echo "Symlinks: $created created, $skipped already exist"

if [[ $errors -gt 0 ]]; then
    echo "ERRORS: $errors symlinks failed" >&2
    exit 1
fi
