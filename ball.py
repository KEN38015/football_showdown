"""
soccer_ball.py — prints a round ASCII soccer ball to the terminal.

The key fix: terminal characters are ~2x taller than wide, so a naive
circle looks oval. We compensate by stretching the horizontal mapping
by the character aspect ratio (CA ≈ 2.05), giving a true circle.

Run:  python3 soccer_ball.py
"""
import math


def normalize(v):
    l = math.sqrt(sum(x * x for x in v))
    return tuple(x / l for x in v)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def rot_x(v, a):
    x, y, z = v
    return (x, y * math.cos(a) - z * math.sin(a),
               y * math.sin(a) + z * math.cos(a))


def rot_y(v, a):
    x, y, z = v
    return (x * math.cos(a) + z * math.sin(a),
            y,
           -x * math.sin(a) + z * math.cos(a))


# ── Pentagon centres (12 vertices of an icosahedron = classic soccer-ball patches) ──
PHI = (1 + math.sqrt(5)) / 2
_ICOSA = [
    (0, 1, PHI), (0, -1, PHI), (0, 1, -PHI), (0, -1, -PHI),
    (1, PHI, 0), (-1, PHI, 0), (1, -PHI, 0), (-1, -PHI, 0),
    (PHI, 0, 1), (-PHI, 0, 1), (PHI, 0, -1), (-PHI, 0, -1),
]
PENTS = [
    normalize(rot_x(rot_y(v, math.radians(18)), math.radians(22)))
    for v in _ICOSA
]

# ── Shading ramps ────────────────────────────────────────────────────────────
DARK  = ' .,:ioIB#'   # pentagon (black) patches
LIGHT = ' .-:+oO0@'   # hexagon  (white) patches
LIGHT_SRC = normalize((-0.4, 0.7, 0.5))

# ── Geometry ─────────────────────────────────────────────────────────────────
RADIUS = 18          # ball radius in terminal rows
CA     = 2.05        # character aspect ratio (height / width) — fixes the oval


def draw_ball():
    rows = RADIUS * 2 + 1
    cols = int(RADIUS * 2 * CA) + 3
    cx   = cols / 2.0
    cy   = float(RADIUS)

    lines = []
    for row in range(rows):
        chars = []
        for col in range(cols):
            sx = (col - cx) / (RADIUS * CA)   # compensate aspect ratio here
            sy = (cy - row) / RADIUS
            r2 = sx * sx + sy * sy

            if r2 > 1.0:
                chars.append(' ')
                continue

            sz  = math.sqrt(1.0 - r2)
            bri = max(0.05, dot((sx, sy, sz), LIGHT_SRC))
            nd  = max(dot((sx, sy, sz), p) for p in PENTS)

            if nd > 0.932:                          # black pentagon patch
                idx = int(bri * 0.50 * (len(DARK) - 1))
                ch  = DARK[max(0, min(idx, len(DARK) - 1))]
            elif nd > 0.885:                        # seam between patches
                ch = '+' if bri > 0.50 else '.'
            else:                                   # white hexagon patch
                idx = int(bri * (len(LIGHT) - 1))
                ch  = LIGHT[max(0, min(idx, len(LIGHT) - 1))]

            chars.append(ch)
        lines.append(''.join(chars))
    return lines







def display_ball():
    print()
    for line in draw_ball():
        print(line)
    print()

