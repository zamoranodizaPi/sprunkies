#!/bin/sh
set -eu

PROJECT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
FRAMEBUFFER="${1:-/dev/fb1}"

python3 "$PROJECT_DIR/src/simon_start.py" --framebuffer "$FRAMEBUFFER"
