#!/bin/bash
# Скрипт автоматической проверки и обновления индекса ugrep
# Использование: bash scripts/check-ugrep-index.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
TIMESTAMP_FILE="$PROJECT_ROOT/.ugrep-index-timestamp"
INDEX_MAX_AGE_HOURS=12

cd "$PROJECT_ROOT"

# Функция для вывода сообщений
log() {
    echo "[ugrep-index] $1"
}

# Проверяем, установлен ли ugrep-indexer
if ! command -v ugrep-indexer &> /dev/null; then
    log "ОШИБКА: ugrep-indexer не установлен"
    log "Установите: brew install ugrep"
    exit 1
fi

# Функция для построения индекса
build_index() {
    log "Строю индекс..."
    ugrep-indexer . --ignore-binary --hidden 2>/dev/null || ugrep-indexer .
    date +%s > "$TIMESTAMP_FILE"
    log "Индекс обновлён"
}

# Проверяем наличие timestamp файла
if [ ! -f "$TIMESTAMP_FILE" ]; then
    log "Файл timestamp не найден. Первичная индексация..."
    build_index
    exit 0
fi

# Читаем время последней индексации
LAST_INDEX=$(cat "$TIMESTAMP_FILE" 2>/dev/null || echo "0")
CURRENT_TIME=$(date +%s)
AGE_SECONDS=$((CURRENT_TIME - LAST_INDEX))
AGE_HOURS=$((AGE_SECONDS / 3600))

if [ $AGE_HOURS -ge $INDEX_MAX_AGE_HOURS ]; then
    log "Индекс устарел ($AGE_HOURS часов). Обновляю..."
    build_index
else
    log "Индекс актуален ($AGE_HOURS ч. из $INDEX_MAX_AGE_HOURS ч. макс.)"
fi
