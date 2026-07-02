"""Asset loading helpers with lightweight fallbacks for first-boot testing."""

from __future__ import annotations

import json
import math
from pathlib import Path

import pygame

import config


FRAME_KEYS = ("idle", "blink", "sing1", "sing2", "happy")


class Assets:
    def __init__(self) -> None:
        self.manifest = self._load_manifest()
        self.background = self._load_background()
        self.simon_frames = self._load_simon_frames()
        self.clouds = self._load_clouds()
        self.notes = self._load_notes()
        self.main_sound_path = self._first_existing(config.MAIN_SOUND_CANDIDATES)
        self.main_sound = self._load_sound(self.main_sound_path)
        self.effect_sound_paths = {
            name: self._first_existing(candidates)
            for name, candidates in config.EFFECT_SOUND_CANDIDATES.items()
        }
        self.effect_sounds = {
            name: self._load_sound(path)
            for name, path in self.effect_sound_paths.items()
            if path is not None
        }
        self.sing_sound = self.main_sound
        if self.main_sound_path is None:
            print("warning: no Simon main audio found; demo will continue without main sound")

    @staticmethod
    def _load_manifest() -> dict[str, object]:
        manifest_path = config.PROJECT_ROOT / "asset_manifest.json"
        try:
            return json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}

    @staticmethod
    def _load_image(path: Path) -> pygame.Surface | None:
        if not path.exists():
            return None
        try:
            return pygame.image.load(str(path)).convert_alpha()
        except pygame.error as exc:
            print(f"warning: could not load image {path}: {exc}")
            return None

    @staticmethod
    def _first_existing(paths: tuple[Path, ...]) -> Path | None:
        for path in paths:
            if path.exists():
                return path
        return None

    @staticmethod
    def _load_sound(path: Path | None) -> pygame.mixer.Sound | None:
        if path is None or not path.exists() or not pygame.mixer.get_init():
            return None
        try:
            return pygame.mixer.Sound(str(path))
        except pygame.error as exc:
            print(f"warning: could not load sound {path}: {exc}")
            return None

    def _load_background(self) -> pygame.Surface:
        image = self._load_image(config.FIELD_IMAGE)
        if image is not None:
            return pygame.transform.smoothscale(image, (config.WIDTH, config.HEIGHT))
        return self._fallback_background()

    def _load_simon_frames(self) -> dict[str, list[pygame.Surface]]:
        frames: dict[str, list[pygame.Surface]] = {}
        for key in FRAME_KEYS:
            found = self._find_simon_frames(key)
            frames[key] = found if found else [self._fallback_simon(key)]
        return frames

    def _find_simon_frames(self, key: str) -> list[pygame.Surface]:
        candidates = [
            config.SIMON_DIR / f"{key}.png",
            config.SIMON_DIR / f"simon_{key}.png",
            config.SIMON_DIR / f"{key}1.png",
            config.SIMON_DIR / f"simon_{key}1.png",
            config.SIMON_DIR / f"{key}2.png",
            config.SIMON_DIR / f"simon_{key}2.png",
        ]
        candidates.extend(sorted(config.SIMON_DIR.glob(f"{key}_*.png")))
        candidates.extend(sorted(config.SIMON_DIR.glob(f"simon_{key}_*.png")))
        frames: list[pygame.Surface] = []
        seen: set[Path] = set()
        for path in candidates:
            if path in seen:
                continue
            seen.add(path)
            image = self._load_image(path)
            if image is not None:
                frames.append(scale_sprite(image))
        return frames

    def _load_clouds(self) -> list[pygame.Surface]:
        clouds: list[pygame.Surface] = []
        for path in (config.IMAGES_DIR / "cloud_01.png", config.IMAGES_DIR / "cloud_02.png"):
            image = self._load_image(path)
            if image is not None:
                width, height = image.get_size()
                factor = min(1.0, 92 / max(1, width))
                clouds.append(pygame.transform.smoothscale(image, (int(width * factor), int(height * factor))))
        return clouds

    def _load_notes(self) -> list[pygame.Surface]:
        notes: list[pygame.Surface] = []
        for path in sorted(config.IMAGES_DIR.glob("music_note_*.png")):
            image = self._load_image(path)
            if image is not None:
                width, height = image.get_size()
                factor = min(1.0, 28 / max(1, height))
                notes.append(pygame.transform.smoothscale(image, (int(width * factor), int(height * factor))))
        return notes

    @staticmethod
    def _fallback_background() -> pygame.Surface:
        surface = pygame.Surface((config.WIDTH, config.HEIGHT)).convert()
        surface.fill((98, 190, 248))
        pygame.draw.circle(surface, (255, 236, 95), (410, 58), 28)
        pygame.draw.rect(surface, (67, 182, 75), (0, 210, config.WIDTH, 110))
        pygame.draw.ellipse(surface, (39, 143, 55), (-30, 224, 250, 80))
        pygame.draw.ellipse(surface, (48, 160, 60), (190, 220, 340, 88))
        for x in range(0, config.WIDTH, 18):
            pygame.draw.line(surface, (52, 148, 50), (x, 248), (x - 10, config.HEIGHT), 1)
        return surface

    @staticmethod
    def _fallback_simon(mood: str) -> pygame.Surface:
        surface = pygame.Surface((170, 220), pygame.SRCALPHA)
        cx = 85
        head_y = 70
        yellow = (255, 230, 0)

        pygame.draw.polygon(surface, yellow, [(54, 132), (116, 132), (130, 210), (40, 210)])
        pygame.draw.circle(surface, yellow, (cx, head_y), 66)
        pygame.draw.polygon(surface, yellow, [(20, 69), (0, 86), (20, 103)])
        pygame.draw.polygon(surface, yellow, [(150, 69), (170, 86), (150, 103)])

        for x in (35, 135):
            pygame.draw.line(surface, yellow, (x, 22), (x, 62), 5)
            pygame.draw.circle(surface, yellow, (x, 18), 16)

        hair = [(54, 20), (74, 5), (70, 27), (96, 4), (88, 29), (116, 17), (101, 36)]
        pygame.draw.polygon(surface, (0, 0, 0), hair)

        if mood == "blink":
            pygame.draw.line(surface, (0, 0, 0), (43, 71), (74, 71), 5)
            pygame.draw.line(surface, (0, 0, 0), (96, 71), (127, 71), 5)
        else:
            for eye_x in (58, 112):
                pygame.draw.circle(surface, (250, 250, 250), (eye_x, 73), 24)
                pygame.draw.circle(surface, (0, 0, 0), (eye_x, 73), 17)

        if mood in ("sing1", "sing2"):
            radius = 14 if mood == "sing1" else 19
            pygame.draw.ellipse(surface, (0, 0, 0), (cx - radius, 105, cx + radius, 105 + radius * 2))
        elif mood == "happy":
            pygame.draw.arc(surface, (0, 0, 0), (58, 97, 112, 137), 0, math.pi, 6)
        else:
            pygame.draw.polygon(surface, (0, 0, 0), [(68, 101), (102, 101), (85, 132)])

        return surface


def scale_sprite(image: pygame.Surface) -> pygame.Surface:
    max_width = 178
    max_height = 230
    width, height = image.get_size()
    factor = min(max_width / width, max_height / height, 1.5)
    size = (max(1, int(width * factor)), max(1, int(height * factor)))
    return pygame.transform.smoothscale(image, size)
