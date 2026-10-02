#!/usr/bin/env python3
"""Draw the shmupfan avatar: an original pixel-art fighter in a bullet curtain.

    python3 branding/make_logo.py

Writes logo_512.png (GitHub avatar) and logo_32.png (1:1 pixels).
The ship is drawn as its left half and mirrored, so it stays symmetric.
"""
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent

PAL = {
    ".": None,             # background
    "K": (16, 12, 28),     # outline
    "W": (250, 250, 255),  # highlight
    "S": (190, 196, 214),  # silver hull
    "G": (112, 120, 148),  # hull shade
    "R": (232, 44, 60),    # red wing
    "D": (140, 18, 40),    # dark red
    "C": (120, 236, 255),  # cockpit glass
    "B": (30, 110, 200),   # cockpit dark
    "Y": (255, 236, 120),  # flame core
    "O": (255, 150, 30),   # flame
    "F": (230, 60, 20),    # flame tail
}

# Left half of the ship, 16 columns; column 15 sits beside the centre line.
SHIP = """
................
................
................
...............K
..............KW
..............KS
.............KWC
.............KSC
.............KSB
............KWSB
............KSSS
............KRSS
.......K....KRSS
......KR...KRRSS
......KR..KRRSSG
.....KRR.KRRSSSG
.....KRRKRRSSSGS
....KRRRRRRSSSGS
...KDRRRRRSSSSGS
..KDDRRRRSSSSGGS
..KDDDRRSSSSGGKS
..KKKDDDSSSGGK.K
.....KKKSSGGK..K
........KGGK..KO
.........KK...KY
..............OY
..............FO
...............F
................
................
................
................
"""

# Pink bullets: (x, y) on the 32x32 grid, ringed for a danmaku look.
BULLETS = [(3, 2), (8, 1), (23, 1), (28, 2), (1, 7), (30, 7), (5, 10), (26, 10),
           (2, 15), (29, 15), (6, 26), (25, 26), (3, 30), (28, 30), (10, 29), (21, 29)]
BG_TOP, BG_BOT = (36, 14, 70), (8, 6, 24)
BULLET, BULLET_CORE = (255, 90, 190), (255, 230, 250)


def draw():
    rows = [r for r in SHIP.strip("\n").split("\n")]
    assert len(rows) == 32 and all(len(r) == 16 for r in rows), "ship grid must be 32x16"
    img = Image.new("RGB", (32, 32))
    for y in range(32):
        t = y / 31
        bg = tuple(round(a + (b - a) * t) for a, b in zip(BG_TOP, BG_BOT))
        for x in range(32):
            img.putpixel((x, y), bg)
    for x, y in BULLETS:
        img.putpixel((x, y), BULLET_CORE)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if 0 <= x + dx < 32 and 0 <= y + dy < 32:
                img.putpixel((x + dx, y + dy), BULLET)
    for y, row in enumerate(rows):
        for x, ch in enumerate(row + row[::-1]):
            if PAL[ch]:
                img.putpixel((x, y), PAL[ch])
    img.save(HERE / "logo_32.png")
    img.resize((512, 512), Image.NEAREST).save(HERE / "logo_512.png")


if __name__ == "__main__":
    draw()
