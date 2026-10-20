"""Layout wireframes for the seven slide review deck."""

import io

CARD_W, CARD_H = 268.0, 150.75
PAD_X, PAD_Y = 26.0, 26.0
GAP_X, GAP_Y = 22.0, 30.0
COLS = 4

W = int(PAD_X * 2 + COLS * CARD_W + (COLS - 1) * GAP_X)
ROWS = 2
H = int(PAD_Y * 2 + 44 + ROWS * CARD_H + (ROWS - 1) * GAP_Y)

BG      = "#0F172A"
CARD    = "#1E293B"
GRID    = "#2A3A52"
REGION  = "#334155"
TEXT    = "#F1F5F9"
MUTED   = "#94A3B8"
BLUE    = "#2563EB"
BLUE_LT = "#60A5FA"
EMERALD = "#10B981"

# region spec: (x, y, w, h, label, colour) in normalised card coordinates
SLIDES = [
    ("01  TITLE & METADATA", [
        (0.055, 0.115, 0.615, 0.115, "EYEBROW  mono 9.5", BLUE_LT),
        (0.055, 0.245, 0.615, 0.115, "H1  40pt", TEXT),
        (0.055, 0.370, 0.615, 0.075, "SUB  18pt", MUTED),
        (0.055, 0.455, 0.615, 0.055, "DECK  12.5pt", MUTED),
        (0.055, 0.560, 0.615, 0.230, "METADATA  5 rows", REGION),
        (0.710, 0.130, 0.235, 0.235, "CHIP GLYPH", BLUE),
        (0.710, 0.420, 0.235, 0.185, "SYSTEM ID", REGION),
        (0.055, 0.815, 0.890, 0.145, "STAT STRIP  4 tiles", EMERALD),
    ]),
    ("02  PROBLEM & CONSTRAINTS", [
        (0.055, 0.125, 0.575, 0.110, "KICKER + H1", BLUE_LT),
        (0.055, 0.265, 0.575, 0.385, "PROBLEM STATEMENT", BLUE),
        (0.055, 0.665, 0.575, 0.165, "HARD CONSTRAINT", MUTED),
        (0.655, 0.265, 0.405, 0.565, "6 CONSTRAINTS", EMERALD),
        (0.055, 0.855, 1.005, 0.115, "CONSTRAINT TABLE C1-C6", REGION),
    ]),
    ("03  ARCHITECTURE", [
        (0.055, 0.125, 0.575, 0.110, "KICKER + H1", BLUE_LT),
        (0.355, 0.265, 0.355, 0.145, "MCU", BLUE),
        (0.055, 0.265, 0.275, 0.115, "IN 1", EMERALD),
        (0.055, 0.400, 0.275, 0.115, "IN 2", EMERALD),
        (0.055, 0.535, 0.275, 0.115, "IN 3", EMERALD),
        (0.735, 0.265, 0.275, 0.115, "OUT 1", BLUE_LT),
        (0.735, 0.400, 0.275, 0.115, "OUT 2", BLUE_LT),
        (0.735, 0.535, 0.275, 0.115, "OUT 3", BLUE_LT),
        (0.140, 0.690, 0.720, 0.090, "SHARED BUS BAR", BLUE),
        (0.055, 0.805, 0.240, 0.170, "DEV 1", BLUE_LT),
        (0.305, 0.805, 0.240, 0.170, "DEV 2", BLUE_LT),
        (0.555, 0.805, 0.240, 0.170, "DEV 3", EMERALD),
        (0.805, 0.805, 0.240, 0.170, "DEV 4", EMERALD),
    ]),
    ("04  HARDWARE / SOFTWARE STACK", [
        (0.055, 0.125, 0.575, 0.110, "KICKER + H1", BLUE_LT),
        (0.055, 0.265, 1.005, 0.105, "LAYER  APPLICATION", BLUE),
        (0.055, 0.380, 1.005, 0.105, "LAYER  DRIVER", BLUE_LT),
        (0.055, 0.495, 1.005, 0.105, "LAYER  INTERFACE", EMERALD),
        (0.055, 0.610, 1.005, 0.105, "LAYER  SILICON", EMERALD),
    ]),
    ("05  IMPLEMENTATION LOGIC", [
        (0.055, 0.125, 0.575, 0.110, "KICKER + H1", BLUE_LT),
        (0.075, 0.265, 0.230, 0.095, "board_init", BLUE_LT),
        (0.075, 0.375, 0.230, 0.095, "display_init", BLUE_LT),
        (0.075, 0.485, 0.230, 0.095, "adc_read", EMERALD),
        (0.075, 0.595, 0.230, 0.120, "zone?", BLUE_LT),
        (0.075, 0.730, 0.230, 0.095, "actuate", EMERALD),
        (0.075, 0.840, 0.230, 0.095, "publish", BLUE_LT),
        (0.345, 0.265, 0.330, 0.190, "TIMER 0 ISR", EMERALD),
        (0.345, 0.475, 0.330, 0.270, "BUS PRIMITIVE 6", BLUE),
        (0.345, 0.765, 0.330, 0.215, "INTERRUPTS", BLUE_LT),
        (0.715, 0.265, 0.345, 0.190, "STAGE TABLE", REGION),
        (0.715, 0.475, 0.345, 0.270, "TIMING TABLE", REGION),
        (0.715, 0.765, 0.345, 0.215, "RATIONALE", EMERALD),
    ]),
    ("06  RESULTS & TRADE-OFFS", [
        (0.055, 0.125, 0.575, 0.110, "KICKER + H1", BLUE_LT),
        (0.055, 0.265, 0.318, 0.185, "METRIC 1", EMERALD),
        (0.395, 0.265, 0.318, 0.185, "METRIC 2", EMERALD),
        (0.735, 0.265, 0.318, 0.185, "METRIC 3", BLUE_LT),
        (0.055, 0.470, 0.318, 0.185, "METRIC 4", BLUE_LT),
        (0.395, 0.470, 0.318, 0.185, "METRIC 5", BLUE_LT),
        (0.735, 0.470, 0.318, 0.185, "METRIC 6", EMERALD),
        (0.055, 0.685, 1.005, 0.270, "TRADE-OFF MATRIX  8 rows", REGION),
    ]),
    ("07  SCALE, SCOPE, CLOSE", [
        (0.055, 0.125, 0.575, 0.110, "KICKER + H1", BLUE_LT),
        (0.055, 0.265, 0.318, 0.330, "NOW", EMERALD),
        (0.395, 0.265, 0.318, 0.330, "NEXT", BLUE_LT),
        (0.735, 0.265, 0.318, 0.330, "LATER", BLUE_LT),
        (0.055, 0.625, 0.575, 0.330, "CONCLUSION  4", EMERALD),
        (0.655, 0.625, 0.405, 0.330, "LIMITS  5", BLUE_LT),
    ]),
]

def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


o = io.StringIO()
o.write('<?xml version="1.0" encoding="UTF-8"?>\n')
o.write('<svg xmlns="http://www.w3.org/2000/svg" width="{0}" height="{1}" '
        'viewBox="0 0 {0} {1}">\n'.format(W, H))
o.write('<rect width="{0}" height="{1}" fill="{2}"/>\n'.format(W, H, BG))
o.write('<g font-family="DejaVu Sans, Helvetica, Arial, sans-serif">\n')

o.write('<text x="{0}" y="{1}" font-size="17" font-weight="700" fill="{2}">'
        '{3}</text>\n'.format(
            PAD_X, PAD_Y + 2, TEXT,
            esc('8051 Hardware Lab - seven slide review deck - layout wireframes')))
o.write('<text x="{0}" y="{1}" font-size="11" fill="{2}">'
        '13.333 x 7.5 in  |  12 column grid  |  0.70 in margins  |  0.22 in gutters  |  '
        'all coordinates in inches from the top left of the slide</text>\n'.format(
            PAD_X, PAD_Y + 21, MUTED))

for idx, (title, regions) in enumerate(SLIDES):
    c = idx % COLS
    r = idx // COLS
    x = PAD_X + c * (CARD_W + GAP_X)
    y = PAD_Y + 44 + r * (CARD_H + GAP_Y)

    o.write('<rect x="{0:.1f}" y="{1:.1f}" width="{2:.1f}" height="{3:.1f}" fill="{4}" '
            'stroke="{5}" stroke-width="1"/>\n'.format(x, y, CARD_W, CARD_H, CARD, GRID))
    o.write('<text x="{0:.1f}" y="{1:.1f}" font-size="9.5" font-weight="700" fill="{2}">'
            '{3}</text>\n'.format(x + 7, y - 6, BLUE_LT, esc(title)))

    for gx in range(1, 12):
        gxx = x + CARD_W * gx / 12.0
        o.write('<line x1="{0:.1f}" y1="{1:.1f}" x2="{0:.1f}" y2="{2:.1f}" stroke="{3}" '
                'stroke-width="0.4" stroke-dasharray="2,3"/>\n'.format(gxx, y, y + CARD_H, GRID))

    for (rx, ry, rw, rh, label, col) in regions:
        px = x + rx * CARD_W
        py = y + ry * CARD_H
        pw = rw * CARD_W
        ph = rh * CARD_H
        o.write('<rect x="{0:.1f}" y="{1:.1f}" width="{2:.1f}" height="{3:.1f}" fill="none" '
                'stroke="{4}" stroke-width="1" stroke-dasharray="3,2"/>\n'.format(px, py, pw, ph, col))
        fs = 6.2 if len(label) > 16 else 7.2
        o.write('<text x="{0:.1f}" y="{1:.1f}" font-size="{2}" fill="{3}">{4}</text>\n'.format(
            px + 2.5, py + ph / 2 + 2.4, fs, col, esc(label)))

o.write('</g>\n</svg>\n')

with open("docs/wireframes.svg", "w", encoding="utf-8") as f:
    f.write(o.getvalue())
print("wrote docs/wireframes.svg", W, "x", H)
