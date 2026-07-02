"""Lightweight particles for Simon's touch reactions."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass

import pygame


@dataclass
class Particle:
    kind: str
    x: float
    y: float
    vx: float
    vy: float
    life: float
    max_life: float
    size: int
    color: tuple[int, int, int]
    image: pygame.Surface | None = None


class Effects:
    def __init__(self, notes: list[pygame.Surface]) -> None:
        self.notes = notes
        self.particles: list[Particle] = []
        self.note_font = pygame.font.Font(None, 30)

    def update(self, dt: float) -> None:
        for particle in self.particles:
            particle.x += particle.vx * dt
            particle.y += particle.vy * dt
            particle.vy += 7.0 * dt
            particle.life -= dt
        self.particles = [p for p in self.particles if p.life > 0 and p.y > -40]

    def draw(self, screen: pygame.Surface) -> None:
        for particle in self.particles:
            alpha = max(30, min(255, int(255 * (particle.life / particle.max_life))))
            if particle.kind == "note":
                self._draw_note(screen, particle, alpha)
            elif particle.kind == "star":
                self._draw_star(screen, particle, alpha)
            elif particle.kind == "heart":
                self._draw_heart(screen, particle, alpha)
            elif particle.kind == "flower":
                self._draw_flower(screen, particle, alpha)

    def spawn_notes(self, x: int, y: int, count: int = 5) -> None:
        for index in range(count):
            image = random.choice(self.notes) if self.notes else None
            self.particles.append(
                Particle(
                    "note",
                    x + random.randint(-34, 34),
                    y + index * 3,
                    random.uniform(-14, 14),
                    random.uniform(-58, -34),
                    random.uniform(1.1, 1.9),
                    1.9,
                    random.randint(18, 24),
                    random.choice([(92, 55, 178), (24, 114, 188), (238, 76, 111)]),
                    image,
                )
            )

    def spawn_stars(self, x: int, y: int, count: int = 5) -> None:
        for _ in range(count):
            self.particles.append(self._simple_particle("star", x, y, (255, 219, 60)))

    def spawn_hearts(self, x: int, y: int, count: int = 4) -> None:
        for _ in range(count):
            self.particles.append(self._simple_particle("heart", x, y, (244, 72, 112)))

    def spawn_flowers(self, x: int, y: int, count: int = 6) -> None:
        for _ in range(count):
            self.particles.append(
                Particle(
                    "flower",
                    x + random.randint(-60, 60),
                    y + random.randint(-5, 8),
                    random.uniform(-8, 8),
                    random.uniform(-36, -18),
                    random.uniform(1.0, 1.6),
                    1.6,
                    random.randint(8, 12),
                    random.choice([(255, 95, 148), (255, 220, 74), (166, 102, 230)]),
                )
            )

    def _simple_particle(self, kind: str, x: int, y: int, color: tuple[int, int, int]) -> Particle:
        return Particle(
            kind,
            x + random.randint(-34, 34),
            y + random.randint(-24, 12),
            random.uniform(-22, 22),
            random.uniform(-54, -28),
            random.uniform(1.0, 1.7),
            1.7,
            random.randint(9, 15),
            color,
        )

    def _draw_note(self, screen: pygame.Surface, particle: Particle, alpha: int) -> None:
        if particle.image is not None:
            image = particle.image.copy()
            image.set_alpha(alpha)
            screen.blit(image, (int(particle.x), int(particle.y)))
            return
        text = self.note_font.render(random.choice(("♪", "♫")), True, particle.color)
        text.set_alpha(alpha)
        screen.blit(text, (int(particle.x), int(particle.y)))

    @staticmethod
    def _draw_star(screen: pygame.Surface, particle: Particle, alpha: int) -> None:
        surface = pygame.Surface((particle.size * 3, particle.size * 3), pygame.SRCALPHA)
        cx = cy = particle.size * 1.5
        points = []
        for i in range(10):
            radius = particle.size if i % 2 == 0 else particle.size * 0.45
            angle = -math.pi / 2 + i * math.pi / 5
            points.append((cx + math.cos(angle) * radius, cy + math.sin(angle) * radius))
        pygame.draw.polygon(surface, (*particle.color, alpha), points)
        screen.blit(surface, (int(particle.x - cx), int(particle.y - cy)))

    @staticmethod
    def _draw_heart(screen: pygame.Surface, particle: Particle, alpha: int) -> None:
        surface = pygame.Surface((particle.size * 3, particle.size * 3), pygame.SRCALPHA)
        s = particle.size
        color = (*particle.color, alpha)
        pygame.draw.circle(surface, color, (s, s), s // 2)
        pygame.draw.circle(surface, color, (s * 2, s), s // 2)
        pygame.draw.polygon(surface, color, [(s // 2, s + 2), (s * 2 + s // 2, s + 2), (s * 3 // 2, s * 2 + 5)])
        screen.blit(surface, (int(particle.x - s), int(particle.y - s)))

    @staticmethod
    def _draw_flower(screen: pygame.Surface, particle: Particle, alpha: int) -> None:
        surface = pygame.Surface((34, 42), pygame.SRCALPHA)
        color = (*particle.color, alpha)
        stem = (59, 160, 72, alpha)
        pygame.draw.line(surface, stem, (17, 38), (17, 18), 2)
        for dx, dy in ((0, -7), (7, 0), (0, 7), (-7, 0)):
            pygame.draw.circle(surface, color, (17 + dx, 17 + dy), 5)
        pygame.draw.circle(surface, (255, 230, 82, alpha), (17, 17), 4)
        screen.blit(surface, (int(particle.x - 17), int(particle.y - 24)))
