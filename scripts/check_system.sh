#!/bin/sh
set -u

section() {
  printf '\n== %s ==\n' "$1"
}

run_or_note() {
  label="$1"
  shift
  section "$label"
  if command -v "$1" >/dev/null 2>&1; then
    "$@" 2>&1 || true
  else
    printf 'Command not found: %s\n' "$1"
  fi
}

section "OS release"
if [ -r /etc/os-release ]; then
  cat /etc/os-release
else
  printf '/etc/os-release not found\n'
fi

run_or_note "Kernel and architecture" uname -a
run_or_note "Machine architecture" dpkg --print-architecture

section "Raspberry Pi model"
if [ -r /proc/device-tree/model ]; then
  tr -d '\0' </proc/device-tree/model
  printf '\n'
else
  printf '/proc/device-tree/model not found\n'
fi

section "SPI status"
if [ -e /dev/spidev0.0 ] || [ -e /dev/spidev0.1 ]; then
  ls -l /dev/spidev* 2>/dev/null || true
else
  printf 'No /dev/spidev* devices found\n'
fi
if [ -r /boot/firmware/config.txt ]; then
  printf '\nRelevant config.txt lines:\n'
  grep -nEi 'dtparam=spi|dtoverlay=.*(spi|35|waveshare|xpt|touch|ili|fb)' /boot/firmware/config.txt || true
else
  printf '/boot/firmware/config.txt not readable\n'
fi

section "Framebuffers"
ls -l /dev/fb* 2>/dev/null || printf 'No /dev/fb* devices found\n'

section "Input devices"
ls -l /dev/input/event* 2>/dev/null || printf 'No /dev/input/event* devices found\n'
if [ -r /proc/bus/input/devices ]; then
  printf '\n/proc/bus/input/devices:\n'
  cat /proc/bus/input/devices
fi

section "Displays"
if command -v xrandr >/dev/null 2>&1; then
  DISPLAY="${DISPLAY:-:0}" xrandr --query 2>&1 || true
else
  printf 'xrandr not installed\n'
fi

section "Graphical session and services"
printf 'DISPLAY=%s\n' "${DISPLAY:-not set}"
if command -v systemctl >/dev/null 2>&1; then
  systemctl get-default 2>&1 || true
  systemctl is-active display-manager 2>&1 || true
  systemctl status display-manager --no-pager --lines=12 2>&1 || true
else
  printf 'systemctl not available\n'
fi
