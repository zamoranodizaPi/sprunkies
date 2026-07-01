#!/bin/sh
set -eu

PROJECT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
SERVICE_NAME=sprunkies-demo.service
SERVICE_SOURCE="$PROJECT_DIR/config/$SERVICE_NAME"
SERVICE_TARGET="/etc/systemd/system/$SERVICE_NAME"
VENV_DIR="$PROJECT_DIR/.venv"

if [ "$(id -u)" -ne 0 ]; then
  printf 'Run with sudo:\n  sudo %s\n' "$0" >&2
  exit 1
fi

if [ ! -f "$SERVICE_SOURCE" ]; then
  printf 'Service file not found: %s\n' "$SERVICE_SOURCE" >&2
  exit 1
fi

if [ ! -x "$VENV_DIR/bin/python" ]; then
  sudo -u pi python3 -m venv "$VENV_DIR"
fi

sudo -u pi "$VENV_DIR/bin/pip" install -r "$PROJECT_DIR/requirements.txt"

install -m 0644 "$SERVICE_SOURCE" "$SERVICE_TARGET"
systemctl daemon-reload
systemctl enable "$SERVICE_NAME"
systemctl restart "$SERVICE_NAME"

systemctl --no-pager --lines=20 status "$SERVICE_NAME"
