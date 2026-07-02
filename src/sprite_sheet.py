"""Sprite-sheet helpers for Simon action animations."""

from __future__ import annotations

from pathlib import Path

import pygame


def load_sprite_sheet(
    path: Path,
    cols: int = 4,
    rows: int = 2,
    max_width: int = 210,
    max_height: int = 230,
) -> list[pygame.Surface]:
    if not path.exists():
        print(f"warning: missing sprite sheet {path}")
        return []

    try:
        sheet = pygame.image.load(str(path)).convert()
    except pygame.error as exc:
        print(f"warning: could not load sprite sheet {path}: {exc}")
        return []

    sheet.set_colorkey((255, 255, 255))
    frame_width = sheet.get_width() // cols
    frame_height = sheet.get_height() // rows
    frames: list[pygame.Surface] = []

    for row in range(rows):
        for col in range(cols):
            rect = pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height)
            frame = pygame.Surface((frame_width, frame_height)).convert()
            frame.set_colorkey((255, 255, 255))
            frame.blit(sheet, (0, 0), rect)
            frames.append(scale_frame(frame, max_width, max_height))

    return frames


def scale_frame(frame: pygame.Surface, max_width: int, max_height: int) -> pygame.Surface:
    width, height = frame.get_size()
    factor = min(max_width / max(1, width), max_height / max(1, height), 1.5)
    size = (max(1, int(width * factor)), max(1, int(height * factor)))
    scaled = pygame.transform.scale(frame, size)
    scaled.set_colorkey((255, 255, 255))
    return scaled
