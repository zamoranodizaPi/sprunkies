#!/bin/sh
set -u

section() {
  printf '\n== %s ==\n' "$1"
}

section "Input event devices"
ls -l /dev/input/event* 2>/dev/null || printf 'No /dev/input/event* devices found\n'

section "Input device descriptions"
if [ -r /proc/bus/input/devices ]; then
  cat /proc/bus/input/devices
else
  printf '/proc/bus/input/devices not readable\n'
fi

section "xinput"
if command -v xinput >/dev/null 2>&1; then
  DISPLAY="${DISPLAY:-:0}" xinput list 2>&1 || true
else
  printf 'xinput is not installed or not in PATH\n'
fi

section "libinput"
if command -v libinput >/dev/null 2>&1; then
  libinput list-devices 2>&1 || true
else
  printf 'libinput command is not installed or not in PATH\n'
fi

section "evtest"
if command -v evtest >/dev/null 2>&1; then
  printf 'evtest is installed. To test touch manually, run:\n'
  printf '  sudo evtest\n'
  printf 'Then select the touch device and tap the four screen corners.\n'
else
  printf 'evtest is not installed. If needed later, install it with:\n'
  printf '  sudo apt install evtest\n'
fi

section "Calibration notes"
printf 'If touch is rotated or inverted, record:\n'
printf '- screen orientation and resolution\n'
printf '- exact xinput device name\n'
printf '- evtest min/max X and Y values\n'
printf '- whether X/Y are swapped\n'
printf '- whether X or Y are inverted\n'
