"""Configuration for the sprunkies visual demo."""

from __future__ import annotations

import os
import platform
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = PROJECT_ROOT / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
SPRITES_DIR = ASSETS_DIR / "sprites"
SOUNDS_DIR = ASSETS_DIR / "sounds"

WIDTH = 480
HEIGHT = 320
FPS = 30

FIELD_IMAGE = IMAGES_DIR / "field_day_480x320.png"
SIMON_DIR = SPRITES_DIR / "simon"
SIMON_ACTIONS_DIR = SPRITES_DIR / "simon_actions"
ACTIONS_SOUND_DIR = SOUNDS_DIR / "actions"
SIMON_SOUND = SOUNDS_DIR / "touch_demo.wav"
MAIN_SOUND_CANDIDATES = (
    SOUNDS_DIR / "simon_sing_theme.wav",
    SOUNDS_DIR / "simon_theme.wav",
    SOUNDS_DIR / "simon_signature_theme.wav",
    SOUNDS_DIR / "Square1_then_Square2_louder.wav",
    SOUNDS_DIR / "touch_demo.wav",
    SOUNDS_DIR / "simon_sing_lalala.wav",
)
EFFECT_SOUND_CANDIDATES = {
    "head": (
        SOUNDS_DIR / "success_jingle.wav",
        SOUNDS_DIR / "button_blue_bell.wav",
        SOUNDS_DIR / "button_yellow_la.wav",
    ),
    "body": (
        SOUNDS_DIR / "button_red_tom.wav",
        SOUNDS_DIR / "button_green_pop.wav",
        SOUNDS_DIR / "button_yellow_la.wav",
    ),
    "sky": (
        SOUNDS_DIR / "button_blue_bell.wav",
        SOUNDS_DIR / "oops_soft.wav",
    ),
    "grass": (
        SOUNDS_DIR / "button_green_pop.wav",
        SOUNDS_DIR / "button_yellow_la.wav",
    ),
    "wake": (
        SOUNDS_DIR / "simon_signature_motif.wav",
        SOUNDS_DIR / "success_jingle.wav",
    ),
}
SLEEP_AFTER_SECONDS = float(os.environ.get("SPRUNKIES_SLEEP_AFTER", "45"))
COMMAND_FILE = Path(os.environ.get("SPRUNKIES_COMMAND_FILE", "/tmp/sprunkies_command.txt"))
ACTION_SPECS = {
    "soccer": {
        "sheet": SIMON_ACTIONS_DIR / "simon_soccer_sheet.png",
        "sound": ACTIONS_SOUND_DIR / "action_1_soccer.wav",
        "duration": 4.0,
        "fps": 8,
    },
    "dance": {
        "sheet": SIMON_ACTIONS_DIR / "simon_dance_sheet.png",
        "sound": ACTIONS_SOUND_DIR / "action_2_dance_loop.wav",
        "duration": 5.0,
        "fps": 9,
    },
    "joke": {
        "sheet": SIMON_ACTIONS_DIR / "simon_joke_sheet.png",
        "sound": ACTIONS_SOUND_DIR / "action_3_joke_laugh.wav",
        "duration": 6.5,
        "fps": 7,
    },
    "wave": {
        "sheet": SIMON_ACTIONS_DIR / "simon_wave_sheet.png",
        "sound": ACTIONS_SOUND_DIR / "action_4_wave_hello.wav",
        "duration": 3.0,
        "fps": 8,
    },
    "sleep": {
        "sheet": SIMON_ACTIONS_DIR / "simon_sleep_wake_sheet.png",
        "sound": ACTIONS_SOUND_DIR / "action_5_sleep_wake.wav",
        "duration": 6.0,
        "fps": 7,
    },
}

WINDOW_TITLE = "sprunkies - Simon"
SOUND_PLAYER = os.environ.get("SPRUNKIES_SOUND_PLAYER", "pygame").lower()
APLAY_DEVICE = os.environ.get("SPRUNKIES_APLAY_DEVICE", "plughw:1,0")


def is_raspberry_pi() -> bool:
    model_path = Path("/proc/device-tree/model")
    try:
        return "raspberry pi" in model_path.read_text(errors="ignore").lower()
    except OSError:
        return platform.machine().startswith(("arm", "aarch"))


def use_fullscreen() -> bool:
    if os.environ.get("SPRUNKIES_WINDOWED") == "1":
        return False
    if os.environ.get("SPRUNKIES_FULLSCREEN") == "1":
        return True
    return is_raspberry_pi()
