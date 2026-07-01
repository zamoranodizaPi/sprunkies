#!/bin/sh
set -eu

SERVICE_NAME=sprunkies-demo.service

if [ "$(id -u)" -ne 0 ]; then
  printf 'Run with sudo:\n  sudo %s\n' "$0" >&2
  exit 1
fi

systemctl disable --now "$SERVICE_NAME" || true
systemctl --no-pager --lines=20 status "$SERVICE_NAME" || true
