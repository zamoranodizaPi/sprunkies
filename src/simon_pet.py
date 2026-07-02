"""Small state machine and touch-zone mapping for Simon."""

from __future__ import annotations

import time
from dataclasses import dataclass

import pygame

import config


@dataclass(frozen=True)
class TouchInfo:
    zone: str
    was_sleepy: bool


class SimonPet:
    def __init__(self) -> None:
        self.state = "idle"
        self.state_until = 0.0
        self.last_interaction = time.monotonic()

    def update(self, now: float) -> None:
        if self.state in {"sing", "happy", "dance", "wake", "blink"} and now >= self.state_until:
            self.state = "idle"

        if self.state == "idle" and now - self.last_interaction >= config.SLEEP_AFTER_SECONDS:
            self.state = "sleepy"
            self.state_until = 0.0

    def touch(self, pos: tuple[int, int], simon_rect: pygame.Rect, now: float) -> TouchInfo:
        was_sleepy = self.state == "sleepy"
        self.last_interaction = now
        return TouchInfo(self.zone_for(pos, simon_rect), was_sleepy)

    def set_state(self, state: str, now: float, duration: float = 0.0) -> None:
        self.state = state
        self.state_until = now + duration if duration > 0 else 0.0
        if state != "sleepy":
            self.last_interaction = now

    @staticmethod
    def zone_for(pos: tuple[int, int], simon_rect: pygame.Rect) -> str:
        x, y = pos
        if simon_rect.collidepoint(x, y):
            relative_y = (y - simon_rect.top) / max(1, simon_rect.height)
            if relative_y <= 0.52:
                return "head"
            if relative_y >= 0.66:
                return "body"
            return "simon"
        if y <= 150:
            return "sky"
        if y >= 235:
            return "grass"
        return "simon"
