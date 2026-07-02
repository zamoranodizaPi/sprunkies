"""Tiny file-command reader for SSH-triggered Simon actions."""

from __future__ import annotations

from pathlib import Path


COMMAND_ALIASES = {
    "1": "soccer",
    "soccer": "soccer",
    "2": "dance",
    "dance": "dance",
    "3": "joke",
    "joke": "joke",
    "4": "wave",
    "wave": "wave",
    "5": "sleep",
    "sleep": "sleep",
}


class CommandWatcher:
    def __init__(self, path: Path, interval: float = 0.2) -> None:
        self.path = path
        self.interval = interval
        self.next_check = 0.0

    def poll(self, now: float) -> str | None:
        if now < self.next_check:
            return None
        self.next_check = now + self.interval
        if not self.path.exists():
            return None

        try:
            raw = self.path.read_text(encoding="utf-8", errors="ignore").strip().lower()
            self.path.unlink(missing_ok=True)
        except OSError as exc:
            print(f"warning: could not read command file {self.path}: {exc}")
            return None

        return COMMAND_ALIASES.get(raw)
