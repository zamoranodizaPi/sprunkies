"""Simon in a field: the first lightweight sprunkies visual demo."""

from __future__ import annotations

import math
import random
import time
from dataclasses import dataclass

import pygame

import config
from asset_loader import Assets


@dataclass
class Note:
    x: float
    y: float
    speed: float
    life: float
    glyph: str
    image: pygame.Surface | None = None


class SimonFieldScene:
    def __init__(self, screen: pygame.Surface, assets: Assets) -> None:
        self.screen = screen
        self.assets = assets
        self.running = True
        self.started_at = time.monotonic()
        self.mode = "idle"
        self.mode_until = 0.0
        self.next_blink = self._schedule_blink()
        self.next_auto_song = time.monotonic() + 4.0
        self.notes: list[Note] = []
        self.clouds = [
            {"x": 36.0, "y": 48.0, "speed": 8.0, "scale": 1.0, "asset": 0},
            {"x": 300.0, "y": 76.0, "speed": 5.0, "scale": 0.78, "asset": 1},
        ]
        self.font = pygame.font.Font(None, 30)
        self.simon_rect = self.assets.simon_frames["idle"][0].get_rect()
        self.simon_rect.midbottom = (config.WIDTH // 2, config.HEIGHT - 18)

    def run(self) -> None:
        clock = pygame.time.Clock()
        while self.running:
            dt = clock.tick(config.FPS) / 1000.0
            self._handle_events()
            self._update(dt)
            self._draw()
            pygame.display.flip()

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_touch(event.pos)

    def _handle_touch(self, pos: tuple[int, int]) -> None:
        if self.simon_rect.collidepoint(pos):
            self._start_singing()
        else:
            self.mode = "happy"
            self.mode_until = time.monotonic() + 0.9
            self._spawn_notes(pos[0], pos[1], count=2)

    def _start_singing(self) -> None:
        now = time.monotonic()
        self.mode = "sing"
        self.mode_until = now + 1.8
        if self.assets.sing_sound is not None:
            try:
                self.assets.sing_sound.set_volume(1.0)
                self.assets.sing_sound.play()
                self.mode_until = now + max(1.2, self.assets.sing_sound.get_length())
            except pygame.error as exc:
                print(f"warning: could not play Simon sound: {exc}")
        self.next_auto_song = self.mode_until + random.uniform(5.0, 8.0)
        self._spawn_notes(self.simon_rect.centerx, self.simon_rect.top + 40, count=6)

    def _update(self, dt: float) -> None:
        now = time.monotonic()
        if self.mode in ("sing", "happy") and now >= self.mode_until:
            self.mode = "idle"

        if self.mode == "idle" and now >= self.next_blink:
            self.mode = "blink"
            self.mode_until = now + 0.14
            self.next_blink = self._schedule_blink()
        elif self.mode == "blink" and now >= self.mode_until:
            self.mode = "idle"

        if self.mode == "sing" and random.random() < 0.18:
            self._spawn_notes(self.simon_rect.centerx + random.randint(-28, 28), self.simon_rect.top + 44, count=1)
        elif self.mode == "idle" and now >= self.next_auto_song:
            self._start_singing()

        for cloud in self.clouds:
            cloud["x"] += cloud["speed"] * dt
            if cloud["x"] > config.WIDTH + 80:
                cloud["x"] = -90.0

        for note in self.notes:
            note.y -= note.speed * dt
            note.life -= dt
        self.notes = [note for note in self.notes if note.life > 0 and note.y > -20]

    def _draw(self) -> None:
        self.screen.blit(self.assets.background, (0, 0))
        for cloud in self.clouds:
            self._draw_cloud(int(cloud["x"]), int(cloud["y"]), cloud["scale"], int(cloud["asset"]))

        frame = self._current_simon_frame()
        bounce = int(math.sin((time.monotonic() - self.started_at) * 4.2) * 4)
        self.simon_rect = frame.get_rect()
        self.simon_rect.midbottom = (config.WIDTH // 2, config.HEIGHT - 18 + bounce)
        self.screen.blit(frame, self.simon_rect)

        for note in self.notes:
            alpha = max(40, min(255, int(note.life * 180)))
            if note.image is not None:
                image = note.image.copy()
                image.set_alpha(alpha)
                self.screen.blit(image, (int(note.x), int(note.y)))
            else:
                text = self.font.render(note.glyph, True, (120, 55, 190))
                text.set_alpha(alpha)
                self.screen.blit(text, (int(note.x), int(note.y)))

    def _current_simon_frame(self) -> pygame.Surface:
        now = time.monotonic()
        if self.mode == "blink":
            return self._animated_frame("blink", now, 8)
        if self.mode == "happy":
            return self._animated_frame("happy", now, 6)
        if self.mode == "sing":
            phase = int(time.monotonic() * 8) % 2
            return self._animated_frame("sing1" if phase == 0 else "sing2", now, 8)
        return self._animated_frame("idle", now, 3)

    def _animated_frame(self, key: str, now: float, fps: int) -> pygame.Surface:
        frames = self.assets.simon_frames[key]
        return frames[int(now * fps) % len(frames)]

    def _draw_cloud(self, x: int, y: int, scale: float, asset_index: int) -> None:
        if self.assets.clouds:
            cloud = self.assets.clouds[asset_index % len(self.assets.clouds)]
            if scale != 1.0:
                size = cloud.get_size()
                cloud = pygame.transform.smoothscale(cloud, (int(size[0] * scale), int(size[1] * scale)))
            self.screen.blit(cloud, (x, y))
            return

        color = (255, 255, 255)
        shade = (224, 242, 250)
        parts = [
            (0, 16, 34, 18),
            (24, 6, 40, 26),
            (58, 14, 34, 18),
        ]
        for px, py, w, h in parts:
            rect = pygame.Rect(x + int(px * scale), y + int(py * scale), int(w * scale), int(h * scale))
            pygame.draw.ellipse(self.screen, shade, rect.move(0, 3))
            pygame.draw.ellipse(self.screen, color, rect)

    def _spawn_notes(self, x: int, y: int, count: int) -> None:
        glyphs = ["♪", "♫"]
        for index in range(count):
            self.notes.append(
                Note(
                    x=x + random.randint(-36, 36),
                    y=y + index * 4,
                    speed=random.uniform(28, 52),
                    life=random.uniform(1.0, 1.8),
                    glyph=random.choice(glyphs),
                    image=random.choice(self.assets.notes) if self.assets.notes else None,
                )
            )

    @staticmethod
    def _schedule_blink() -> float:
        return time.monotonic() + random.uniform(2.5, 5.0)
