#!/usr/bin/env python3
"""Render Simon, the sprunkies starter character, to a Linux framebuffer."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw


BLACK = (0, 0, 0)
YELLOW = (255, 232, 0)
WHITE = (248, 248, 248)


def framebuffer_size(framebuffer: Path, fallback: tuple[int, int]) -> tuple[int, int]:
    size_file = Path("/sys/class/graphics") / framebuffer.name / "virtual_size"
    try:
        width, height = size_file.read_text(encoding="utf-8").strip().split(",", 1)
        return int(width), int(height)
    except (OSError, ValueError):
        return fallback


def rgb565(image: Image.Image) -> bytes:
    data = bytearray()
    for red, green, blue in image.convert("RGB").getdata():
        value = ((red & 0xF8) << 8) | ((green & 0xFC) << 3) | (blue >> 3)
        data.append(value & 0xFF)
        data.append((value >> 8) & 0xFF)
    return bytes(data)


def draw_simon(width: int, height: int) -> Image.Image:
    image = Image.new("RGB", (width, height), BLACK)
    draw = ImageDraw.Draw(image)

    scale = min(width / 320, height / 480)
    cx = width // 2
    head_r = int(78 * scale)
    head_cy = int(128 * scale)
    if height < 400:
        head_cy = int(height * 0.42)

    body_top = head_cy + int(58 * scale)
    body_bottom = height - int(10 * scale)
    body_half_top = int(28 * scale)
    body_half_bottom = int(56 * scale)

    def p(x: float, y: float) -> tuple[int, int]:
        return (int(cx + x * scale), int(y * scale))

    # Antennas and side points.
    antenna_y = head_cy - head_r - int(56 * scale)
    antenna_r = int(17 * scale)
    for side in (-1, 1):
        x = cx + side * int(78 * scale)
        draw.line((x, antenna_y, x, head_cy - int(58 * scale)), fill=YELLOW, width=max(3, int(6 * scale)))
        draw.ellipse((x - antenna_r, antenna_y - antenna_r, x + antenna_r, antenna_y + antenna_r), fill=YELLOW)

    side_y = head_cy
    draw.polygon([p(-150, side_y / scale), p(-82, side_y / scale - 30), p(-82, side_y / scale + 30)], fill=YELLOW)
    draw.polygon([p(150, side_y / scale), p(82, side_y / scale - 30), p(82, side_y / scale + 30)], fill=YELLOW)

    # Body.
    draw.polygon(
        [
            (cx - body_half_top, body_top),
            (cx + body_half_top, body_top),
            (cx + body_half_bottom, body_bottom),
            (cx - body_half_bottom, body_bottom),
        ],
        fill=YELLOW,
    )

    # Head.
    draw.ellipse((cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r), fill=YELLOW)

    # Hair spikes.
    spikes = [
        (-52, -70),
        (-18, -92),
        (-24, -62),
        (16, -92),
        (9, -59),
        (48, -82),
        (32, -50),
    ]
    for x, y in spikes:
        draw.polygon([p(x - 22, head_cy / scale - 45), p(x, head_cy / scale + y), p(x + 14, head_cy / scale - 45)], fill=BLACK)

    # Eyes.
    eye_y = head_cy - int(8 * scale)
    eye_outer = int(28 * scale)
    eye_inner = int(20 * scale)
    for side in (-1, 1):
        eye_x = cx + side * int(37 * scale)
        draw.ellipse((eye_x - eye_outer, eye_y - eye_outer, eye_x + eye_outer, eye_y + eye_outer), fill=WHITE)
        draw.ellipse((eye_x - eye_inner, eye_y - eye_inner, eye_x + eye_inner, eye_y + eye_inner), fill=BLACK)

    # Mouth and neck shadow.
    draw.polygon([p(-20, head_cy / scale + 36), p(20, head_cy / scale + 36), p(0, head_cy / scale + 76)], fill=BLACK)
    draw.arc(
        (cx - int(34 * scale), body_top - int(16 * scale), cx + int(34 * scale), body_top + int(18 * scale)),
        start=10,
        end=170,
        fill=(214, 190, 0),
        width=max(1, int(3 * scale)),
    )

    return image


def main() -> int:
    parser = argparse.ArgumentParser(description="Show Simon on the TFT framebuffer.")
    parser.add_argument("--framebuffer", default="/dev/fb1", help="Framebuffer path, default: /dev/fb1")
    parser.add_argument("--width", type=int, default=320, help="Fallback width when sysfs size is unavailable")
    parser.add_argument("--height", type=int, default=480, help="Fallback height when sysfs size is unavailable")
    parser.add_argument("--png", help="Optional path to save a PNG preview instead of writing only framebuffer")
    args = parser.parse_args()

    framebuffer = Path(args.framebuffer)
    width, height = framebuffer_size(framebuffer, (args.width, args.height))
    image = draw_simon(width, height)

    if args.png:
        Image.Image.save(image, args.png)

    if framebuffer.exists():
        framebuffer.write_bytes(rgb565(image))
    else:
        raise SystemExit(f"Framebuffer not found: {framebuffer}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
