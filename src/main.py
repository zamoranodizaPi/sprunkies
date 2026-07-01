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
    if config.SOUND_PLAYER == "aplay":
        print(f"audio: using aplay device={config.APLAY_DEVICE}")
        return

    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=1024)
    device = os.environ.get("SPRUNKIES_AUDIO_DEVICE")
    try:
        if device and not device.startswith(("hw:", "plughw:", "default")):
            pygame.mixer.init(devicename=device)
        else:
            pygame.mixer.init()
        print(f"audio: pygame mixer initialized {pygame.mixer.get_init()} device={device or 'default'}")
    except pygame.error as exc:
        print(f"warning: audio disabled for {device or 'default'}: {exc}")
        if device:
            try:
                pygame.mixer.init()
                print(f"audio: fallback pygame mixer initialized {pygame.mixer.get_init()} device=default")
            except pygame.error as fallback_exc:
                print(f"warning: fallback audio disabled: {fallback_exc}")


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
