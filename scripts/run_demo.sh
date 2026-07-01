#!/bin/sh
set -eu

PROJECT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
VENV_DIR="$PROJECT_DIR/.venv"

if [ ! -x "$VENV_DIR/bin/python" ]; then
  printf 'Virtualenv not found. Create it with:\n'
  printf '  python3 -m venv .venv\n'
  printf '  . .venv/bin/activate\n'
  printf '  pip install -r requirements.txt\n'
  exit 1
fi

. "$VENV_DIR/bin/activate"
cd "$PROJECT_DIR"

if [ -z "${DISPLAY:-}" ] && [ -e "$HOME/.Xauthority" ]; then
  export DISPLAY=:0
  export XAUTHORITY="$HOME/.Xauthority"
fi

exec python src/main.py
