#!/bin/sh
set -eu

PROJECT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PNG_PATH="$PROJECT_DIR/assets/images/simon-start.png"
FRAMEBUFFER="${1:-/dev/fb1}"
DISPLAY_VALUE="${DISPLAY:-:0}"
XAUTHORITY_VALUE="${XAUTHORITY:-$HOME/.Xauthority}"

python3 "$PROJECT_DIR/src/simon_start.py" --framebuffer "$FRAMEBUFFER" --png "$PNG_PATH"

if command -v pcmanfm >/dev/null 2>&1; then
  DISPLAY="$DISPLAY_VALUE" XAUTHORITY="$XAUTHORITY_VALUE" \
    pcmanfm --set-wallpaper "$PNG_PATH" --wallpaper-mode=fit
else
  printf 'pcmanfm not found; Simon was written to %s and saved to %s\n' "$FRAMEBUFFER" "$PNG_PATH"
fi
