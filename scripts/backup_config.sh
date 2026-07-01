#!/bin/sh
set -eu

PROJECT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
SOURCE_FILE=/boot/firmware/config.txt
BACKUP_DIR="$PROJECT_DIR/config/backups"
STAMP=$(date +%Y%m%d-%H%M%S)
BACKUP_FILE="$BACKUP_DIR/config.txt.$STAMP.bak"

if [ ! -r "$SOURCE_FILE" ]; then
  printf 'Cannot read %s\n' "$SOURCE_FILE" >&2
  exit 1
fi

mkdir -p "$BACKUP_DIR"
cp "$SOURCE_FILE" "$BACKUP_FILE"

printf 'Backup created:\n%s\n' "$BACKUP_FILE"
