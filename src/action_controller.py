"""Action state controller for v0.3 Simon interactions."""

from __future__ import annotations

from dataclasses import dataclass

import config


@dataclass(frozen=True)
class ActionSpec:
    name: str
    duration: float
    fps: int


class ActionController:
    def __init__(self) -> None:
        self.current = "idle"
        self.started_at = 0.0
        self.ends_at = 0.0
        self.specs = {
            name: ActionSpec(name, float(spec["duration"]), int(spec["fps"]))
            for name, spec in config.ACTION_SPECS.items()
        }

    def start(self, name: str, now: float) -> bool:
        if name not in self.specs:
            return False
        spec = self.specs[name]
        self.current = name
        self.started_at = now
        self.ends_at = now + spec.duration
        return True

    def stop(self) -> None:
        self.current = "idle"
        self.started_at = 0.0
        self.ends_at = 0.0

    def update(self, now: float) -> None:
        if self.current != "idle" and now >= self.ends_at:
            self.stop()

    def active(self) -> bool:
        return self.current != "idle"

    def elapsed(self, now: float) -> float:
        return max(0.0, now - self.started_at)

    def frame_index(self, now: float, frame_count: int) -> int:
        if frame_count <= 0:
            return 0
        spec = self.specs.get(self.current)
        fps = spec.fps if spec else 8
        return int(self.elapsed(now) * fps) % frame_count

    def message(self, now: float) -> str:
        elapsed = self.elapsed(now)
        if self.current == "joke":
            if elapsed < 2.0:
                return "\u00bfQu\u00e9 le dijo un foco a otro?"
            if elapsed < 4.0:
                return "\u00a1T\u00fa s\u00ed que brillas!"
            return "\u00a1Ja ja ja!"
        if self.current == "wave":
            return "\u00a1Hola!"
        if self.current == "sleep":
            if elapsed < 4.0:
                return "zzz..."
            return "\u00a1Buenos d\u00edas!"
        return ""
