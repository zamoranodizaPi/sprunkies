"""Simon Touch Pet scene for the lightweight sprunkies demo."""

from __future__ import annotations

import math
import random
import subprocess
import time
import wave
from pathlib import Path

import pygame

import config
from action_controller import ActionController
from asset_loader import Assets
from command_watcher import CommandWatcher
from effects import Effects
from simon_pet import SimonPet


ACTION_BAR_TOP = 270
SIMON_BOTTOM = ACTION_BAR_TOP - 4
ACTION_BUTTONS = (
    ("soccer", "1 Futbol"),
    ("dance", "2 Baila"),
    ("joke", "3 Chiste"),
    ("wave", "4 Hola"),
    ("sleep", "5 Dormir"),
)


class SimonFieldScene:
    def __init__(self, screen: pygame.Surface, assets: Assets) -> None:
        self.screen = screen
        self.assets = assets
        self.running = True
        self.started_at = time.monotonic()
        self.next_blink = self._schedule_blink()
        self.pet = SimonPet()
        self.actions = ActionController()
        self.command_watcher = CommandWatcher(config.COMMAND_FILE)
        self.effects = Effects(self.assets.notes)
        self.sound_processes: list[subprocess.Popen[bytes]] = []
        self.message = ""
        self.message_until = 0.0
        self.cloud_highlight_until = 0.0
        self.clouds = [
            {"x": 36.0, "y": 48.0, "speed": 8.0, "scale": 1.0, "asset": 0},
            {"x": 300.0, "y": 76.0, "speed": 5.0, "scale": 0.78, "asset": 1},
        ]
        self.font = pygame.font.Font(None, 34)
        self.small_font = pygame.font.Font(None, 28)
        self.button_font = pygame.font.Font(None, 22)
        self.action_buttons = self._build_action_buttons()
        self.simon_rect = self.assets.simon_frames["idle"][0].get_rect()
        self.simon_rect.midbottom = (config.WIDTH // 2, SIMON_BOTTOM)

    def run(self) -> None:
        clock = pygame.time.Clock()
        while self.running:
            dt = clock.tick(config.FPS) / 1000.0
            self._handle_events()
            self._update(dt)
            self._draw()
            pygame.display.flip()
        self._cleanup_sound_processes(stop=True)

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self._handle_key(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_touch(event.pos)
            elif event.type == pygame.FINGERDOWN:
                pos = (int(event.x * config.WIDTH), int(event.y * config.HEIGHT))
                self._handle_touch(pos)

    def _handle_key(self, key: int) -> None:
        now = time.monotonic()
        if key == pygame.K_ESCAPE:
            self.running = False
        elif key == pygame.K_s:
            self._start_singing((self.simon_rect.centerx, self.simon_rect.top + 46))
        elif key in (pygame.K_1, pygame.K_KP1):
            self._start_action("soccer", now)
        elif key in (pygame.K_2, pygame.K_KP2):
            self._start_action("dance", now)
        elif key in (pygame.K_3, pygame.K_KP3):
            self._start_action("joke", now)
        elif key in (pygame.K_4, pygame.K_KP4):
            self._start_action("wave", now)
        elif key in (pygame.K_5, pygame.K_KP5):
            self._start_action("sleep", now)
        elif key == pygame.K_h:
            self._happy_head(now)
        elif key == pygame.K_d:
            self._dance_body(now)
        elif key == pygame.K_z:
            self.pet.set_state("sleepy", now)
            self._set_message("zzz", now, 1.5)

    def _handle_touch(self, pos: tuple[int, int]) -> None:
        now = time.monotonic()
        action = self._action_at(pos)
        if action is not None:
            self._start_action(action, now)
            return
        if self.actions.active():
            return

        info = self.pet.touch(pos, self.simon_rect, now)
        if info.was_sleepy and info.zone in {"head", "body", "simon"}:
            self.pet.set_state("wake", now, 0.9)
            self.effects.spawn_stars(self.simon_rect.centerx, self.simon_rect.top + 42, 7)
            self._set_message("Hola!", now, 1.0)
            self._play_sound("wake")
            return

        if info.zone == "head":
            self._happy_head(now)
        elif info.zone == "body":
            self._dance_body(now)
        elif info.zone == "sky":
            self.pet.set_state("happy", now, 1.2)
            self.cloud_highlight_until = now + 1.2
            self.effects.spawn_stars(pos[0], pos[1], 4)
            self.effects.spawn_notes(pos[0], pos[1], 2)
            self._set_message("Yupi!", now, 0.9)
            self._play_sound("sky")
        elif info.zone == "grass":
            self.pet.set_state("happy", now, 1.2)
            self.effects.spawn_flowers(pos[0], min(config.HEIGHT - 20, pos[1]), 7)
            self._set_message("Yupi!", now, 0.9)
            self._play_sound("grass")
        else:
            self._start_singing(pos)

    def _happy_head(self, now: float) -> None:
        self.pet.set_state("happy", now, 1.5)
        self.effects.spawn_hearts(self.simon_rect.centerx, self.simon_rect.top + 42, 5)
        self.effects.spawn_stars(self.simon_rect.centerx, self.simon_rect.top + 54, 3)
        self._set_message("Hola!", now, 1.0)
        self._play_sound("head")

    def _dance_body(self, now: float) -> None:
        self.pet.set_state("dance", now, 2.0)
        self.effects.spawn_stars(self.simon_rect.centerx, self.simon_rect.centery + 25, 6)
        self._set_message("Yupi!", now, 1.0)
        self._play_sound("body")

    def _start_singing(self, pos: tuple[int, int] | None = None) -> None:
        now = time.monotonic()
        if self.actions.active():
            self.actions.stop()
        duration = max(1.8, min(5.0, self._play_sound("main")))
        self.pet.set_state("sing", now, duration)
        note_x, note_y = pos if pos is not None else (self.simon_rect.centerx, self.simon_rect.top + 40)
        self.effects.spawn_notes(note_x, note_y, count=7)
        self._set_message("Canta!", now, 1.0)

    def _start_action(self, action: str, now: float) -> None:
        if not self.actions.start(action, now):
            return
        self.pet.set_state("idle", now)
        self.message = ""
        self.message_until = 0.0
        self._cleanup_sound_processes(stop=True)
        self._play_action_sound(action)

    def _play_sound(self, sound_name: str) -> float:
        path = self._sound_path(sound_name)
        if path is None:
            return 1.8

        if config.SOUND_PLAYER == "aplay":
            try:
                self._cleanup_sound_processes(stop=True)
                process = subprocess.Popen(
                    ["aplay", "-q", "-D", config.APLAY_DEVICE, str(path)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                self.sound_processes.append(process)
                return self._wav_length(path)
            except OSError as exc:
                print(f"warning: could not play sound with aplay: {exc}")
                return 1.8

        sound = self.assets.main_sound if sound_name == "main" else self.assets.effect_sounds.get(sound_name)
        if sound is None:
            return 1.8
        try:
            sound.set_volume(1.0)
            sound.play()
            return sound.get_length()
        except pygame.error as exc:
            print(f"warning: could not play sound {sound_name}: {exc}")
            return 1.8

    def _play_action_sound(self, action: str) -> float:
        path = self.assets.action_sound_paths.get(action)
        if path is None:
            return 1.8

        if config.SOUND_PLAYER == "aplay":
            try:
                process = subprocess.Popen(
                    ["aplay", "-q", "-D", config.APLAY_DEVICE, str(path)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                self.sound_processes.append(process)
                return self._wav_length(path)
            except OSError as exc:
                print(f"warning: could not play action sound with aplay: {exc}")
                return 1.8

        sound = self.assets.action_sounds.get(action)
        if sound is None:
            return 1.8
        try:
            sound.set_volume(1.0)
            sound.play()
            return sound.get_length()
        except pygame.error as exc:
            print(f"warning: could not play action sound {action}: {exc}")
            return 1.8

    def _sound_path(self, sound_name: str) -> Path | None:
        if sound_name == "main":
            return self.assets.main_sound_path
        if sound_name == "wake" and self.assets.effect_sound_paths.get("wake") is None:
            return self.assets.main_sound_path
        return self.assets.effect_sound_paths.get(sound_name)

    @staticmethod
    def _wav_length(path: Path) -> float:
        try:
            with wave.open(str(path), "rb") as handle:
                return handle.getnframes() / float(handle.getframerate())
        except (OSError, wave.Error, ZeroDivisionError):
            return 1.8

    def _update(self, dt: float) -> None:
        self._cleanup_sound_processes()
        now = time.monotonic()
        command = self.command_watcher.poll(now)
        if command is not None:
            self._start_action(command, now)

        self.actions.update(now)
        if self.actions.active():
            self.effects.update(dt)
            for cloud in self.clouds:
                cloud["x"] += cloud["speed"] * dt
                if cloud["x"] > config.WIDTH + 80:
                    cloud["x"] = -90.0
            return

        self.pet.update(now)

        if self.pet.state == "idle" and now >= self.next_blink:
            self.pet.set_state("blink", now, 0.14)
            self.next_blink = self._schedule_blink()

        if self.pet.state == "sing" and random.random() < 0.18:
            self.effects.spawn_notes(self.simon_rect.centerx + random.randint(-30, 30), self.simon_rect.top + 46, 1)

        for cloud in self.clouds:
            speed = cloud["speed"] * (2.2 if now < self.cloud_highlight_until else 1.0)
            cloud["x"] += speed * dt
            if cloud["x"] > config.WIDTH + 80:
                cloud["x"] = -90.0

        self.effects.update(dt)

    def _draw(self) -> None:
        self.screen.blit(self.assets.background, (0, 0))
        now = time.monotonic()
        for cloud in self.clouds:
            self._draw_cloud(
                int(cloud["x"]),
                int(cloud["y"]),
                float(cloud["scale"]),
                int(cloud["asset"]),
                now < self.cloud_highlight_until,
            )

        frame = self._current_simon_frame()
        bounce = self._bounce(now)
        self.simon_rect = frame.get_rect()
        self.simon_rect.midbottom = (config.WIDTH // 2, SIMON_BOTTOM + bounce)
        self.screen.blit(frame, self.simon_rect)

        if self.pet.state == "sleepy":
            self._draw_sleepy(now)

        self.effects.draw(self.screen)
        self._draw_action_message(now)
        self._draw_message(now)
        self._draw_action_bar()

    def _current_simon_frame(self) -> pygame.Surface:
        if self.actions.active():
            frames = self.assets.action_frames.get(self.actions.current, [])
            if frames:
                return frames[self.actions.frame_index(time.monotonic(), len(frames))]

        now = time.monotonic()
        state = self.pet.state
        if state in {"blink", "sleepy"}:
            return self._animated_frame("blink", now, 4)
        if state in {"happy", "wake"}:
            return self._animated_frame("happy", now, 6)
        if state == "sing":
            phase = int(now * 8) % 2
            return self._animated_frame("sing1" if phase == 0 else "sing2", now, 8)
        if state == "dance":
            key = "happy" if int(now * 6) % 2 == 0 else "idle"
            return self._animated_frame(key, now, 6)
        return self._animated_frame("idle", now, 3)

    def _animated_frame(self, key: str, now: float, fps: int) -> pygame.Surface:
        frames = self.assets.simon_frames[key]
        return frames[int(now * fps) % len(frames)]

    def _bounce(self, now: float) -> int:
        elapsed = now - self.started_at
        if self.pet.state == "dance":
            return int(math.sin(elapsed * 10.0) * 12)
        if self.pet.state == "sleepy":
            return int(math.sin(elapsed * 1.2) * 1)
        if self.pet.state == "wake":
            return int(math.sin(elapsed * 8.0) * 7)
        return int(math.sin(elapsed * 4.2) * 4)

    def _draw_cloud(self, x: int, y: int, scale: float, asset_index: int, highlighted: bool) -> None:
        if self.assets.clouds:
            cloud = self.assets.clouds[asset_index % len(self.assets.clouds)]
            if scale != 1.0:
                size = cloud.get_size()
                cloud = pygame.transform.smoothscale(cloud, (int(size[0] * scale), int(size[1] * scale)))
            self.screen.blit(cloud, (x, y))
            if highlighted:
                rect = cloud.get_rect(topleft=(x, y)).inflate(8, 5)
                pygame.draw.ellipse(self.screen, (255, 242, 132), rect, 3)
            return

        shade = (255, 242, 132) if highlighted else (224, 242, 250)
        for px, py, w, h in ((0, 16, 34, 18), (24, 6, 40, 26), (58, 14, 34, 18)):
            rect = pygame.Rect(x + int(px * scale), y + int(py * scale), int(w * scale), int(h * scale))
            pygame.draw.ellipse(self.screen, shade, rect.move(0, 3))
            pygame.draw.ellipse(self.screen, (255, 255, 255), rect)

    def _draw_sleepy(self, now: float) -> None:
        if int(now * 2) % 2 == 0:
            text = self.small_font.render("zzz", True, (80, 82, 120))
            self.screen.blit(text, (self.simon_rect.right - 16, max(18, self.simon_rect.top - 14)))

    def _set_message(self, text: str, now: float, duration: float) -> None:
        self.message = text
        self.message_until = now + duration

    def _draw_message(self, now: float) -> None:
        if not self.message or now >= self.message_until:
            return
        text = self.font.render(self.message, True, (36, 62, 92))
        shadow = self.font.render(self.message, True, (255, 255, 255))
        rect = text.get_rect(center=(config.WIDTH // 2, 32))
        self.screen.blit(shadow, rect.move(2, 2))
        self.screen.blit(text, rect)

    def _draw_action_message(self, now: float) -> None:
        if not self.actions.active():
            return
        message = self.actions.message(now)
        if not message:
            return
        lines = [message[i : i + 28] for i in range(0, len(message), 28)]
        for index, line in enumerate(lines[:2]):
            text = self.small_font.render(line, True, (36, 62, 92))
            shadow = self.small_font.render(line, True, (255, 255, 255))
            rect = text.get_rect(center=(config.WIDTH // 2, 28 + index * 24))
            self.screen.blit(shadow, rect.move(2, 2))
            self.screen.blit(text, rect)

    def _build_action_buttons(self) -> list[tuple[str, pygame.Rect, str]]:
        width = config.WIDTH // len(ACTION_BUTTONS)
        buttons: list[tuple[str, pygame.Rect, str]] = []
        for index, (action, label) in enumerate(ACTION_BUTTONS):
            rect = pygame.Rect(index * width, ACTION_BAR_TOP, width, config.HEIGHT - ACTION_BAR_TOP)
            if index == len(ACTION_BUTTONS) - 1:
                rect.width = config.WIDTH - rect.x
            buttons.append((action, rect, label))
        return buttons

    def _action_at(self, pos: tuple[int, int]) -> str | None:
        for action, rect, _label in self.action_buttons:
            if rect.collidepoint(pos):
                return action
        return None

    def _draw_action_bar(self) -> None:
        colors = {
            "soccer": (68, 170, 92),
            "dance": (232, 181, 64),
            "joke": (232, 105, 98),
            "wave": (82, 157, 218),
            "sleep": (126, 120, 188),
        }
        for action, rect, label in self.action_buttons:
            selected = self.actions.current == action
            color = colors[action]
            fill = tuple(min(255, c + 35) for c in color) if selected else color
            pygame.draw.rect(self.screen, fill, rect)
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 2)
            text = self.button_font.render(label, True, (20, 35, 42))
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

    @staticmethod
    def _schedule_blink() -> float:
        return time.monotonic() + random.uniform(2.5, 5.0)

    def _cleanup_sound_processes(self, stop: bool = False) -> None:
        alive: list[subprocess.Popen[bytes]] = []
        for process in self.sound_processes:
            if stop and process.poll() is None:
                process.terminate()
            if process.poll() is None:
                alive.append(process)
            else:
                process.wait()
        self.sound_processes = alive
