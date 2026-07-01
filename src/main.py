#!/usr/bin/env python3
"""Entry point for the sprunkies Simon field demo."""

from __future__ import annotations

import os
import signal
import sys

import pygame

import config
from asset_loader import Assets
from scene_simon_field import SimonFieldScene


def init_audio() -> None:
    try:
        pygame.mixer.init()
    except pygame.error as exc:
        print(f"warning: audio disabled: {exc}")


def main() -> int:
    os.chdir(config.PROJECT_ROOT)
    pygame.init()
    init_audio()
    signal.signal(signal.SIGINT, lambda _sig, _frame: sys.exit(0))

    flags = pygame.FULLSCREEN if config.use_fullscreen() else 0
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT), flags)
    pygame.display.set_caption(config.WINDOW_TITLE)
    pygame.mouse.set_visible(not config.use_fullscreen())

    assets = Assets()
    scene = SimonFieldScene(screen, assets)
    try:
        scene.run()
    finally:
        pygame.quit()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
