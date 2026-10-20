"""
Seven slide technical review deck for the 8051 Hardware Lab.

Design system
    Charcoal  #1E293B   background
    Off-white #F1F5F9   primary text
    Electric  #2563EB   primary accent (rules, fills, headers)
    Emerald   #10B981   secondary accent (verified, positive, results)

    Tints are used for accent *text* on dark surfaces so the mid tone of the
    requested accent stays legible: #60A5FA and #34D399.

Grid
    13.333 x 7.5 in, 12 columns, 0.70 in margins, 0.22 in gutters.
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn

BG        = RGBColor(0x1E, 0x29, 0x3B)
SURFACE   = RGBColor(0x24, 0x33, 0x4D)
SURFACE2  = RGBColor(0x1A, 0x26, 0x37)
BORDER    = RGBColor(0x33, 0x41, 0x55)
TEXT      = RGBColor(0xF1, 0xF5, 0xF9)
MUTED     = RGBColor(0x94, 0xA3, 0xB8)
DIM       = RGBColor(0x64, 0x74, 0x8B)
BLUE      = RGBColor(0x25, 0x63, 0xEB)
BLUE_LT   = RGBColor(0x60, 0xA5, 0xFA)
EMERALD   = RGBColor(0x10, 0xB9, 0x81)
EMERALD_LT= RGBColor(0x34, 0xD3, 0x99)
AMBER     = RGBColor(0xF5, 0x9E, 0x0B)
RED       = RGBColor(0xEF, 0x44, 0x44)
GRID      = RGBColor(0x28, 0x37, 0x4E)

FONT = "Calibri"
MONO = "Consolas"

SW, SH = 13.3333, 7.5
ML = 0.70
MR = 0.70
CW = SW - ML - MR
GUT = 0.22
COLW = (CW - 11 * GUT) / 12.0

prs = Presentation()
prs.slide_width = Inches(SW)
prs.slide_height = Inches(SH)
BLANKLAY = prs.slide_layouts[6]

_n = {"i": 0}


def cx(i):
    return ML + i * (COLW + GUT)


def cw(n):
    return n * COLW + (n - 1) * GUT


def new_slide():
    s = prs.slides.add_slide(BLANKLAY)
    bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG
    bg.line.fill.background()
    bg.shadow.inherit = False
    _n["i"] += 1
    return s


def grid_bg(slide, step=1.11):
    x = ML
    while x <= SW - MR + 0.01:
        ln = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), 0, Emu(9525), prs.slide_height)
        ln.fill.solid()
        ln.fill.fore_color.rgb = GRID
        ln.line.fill.background()
        ln.shadow.inherit = False
        x += step
    y = 0.0
    while y <= SH:
        ln = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(y), prs.slide_width, Emu(9525))
        ln.fill.solid()
        ln.fill.fore_color.rgb = GRID
        ln.line.fill.background()
        ln.shadow.inherit = False
        y += step


def rect(slide, x, y, w, h, fill=SURFACE, line=None, shape=MSO_SHAPE.RECTANGLE,
         lw=1.0, radius=None):
    shp = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(lw)
    shp.shadow.inherit = False
    if radius is not None and shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        try:
            shp.adjustments[0] = radius
        except Exception:
            pass
    return shp


def txt(slide, x, y, w, h, runs, size=12, color=TEXT, bold=False, align=PP_ALIGN.LEFT,
        anchor=MSO_ANCHOR.TOP, sa=3, ls=1.0, font=FONT, italic=False):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    first = True
    for item in runs:
        if isinstance(item, str):
            item = (item, None, None, None, None)
        item = tuple(item) + (None,) * (5 - len(item))
        t, sz, col, bd, it = item
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.text = t
        p.alignment = align
        p.space_after = Pt(sa)
        p.line_spacing = ls
        for r in p.runs:
            r.font.size = Pt(sz if sz is not None else size)
            r.font.bold = bd if bd is not None else bold
            r.font.italic = it if it is not None else italic
            r.font.color.rgb = col if col is not None else color
            r.font.name = font
    return tb


def rich(slide, x, y, w, h, parts, size=11, align=PP_ALIGN.LEFT, font=FONT):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = align
    p.space_after = Pt(0)
    for item in parts:
        item = tuple(item) + (None,) * (4 - len(item))
        t, sz, col, bd = item[0], item[1], item[2], item[3]
        r = p.add_run()
        r.text = t
        r.font.size = Pt(sz if sz is not None else size)
        r.font.bold = bool(bd)
        r.font.color.rgb = col if col is not None else TEXT
        r.font.name = font
    return tb


def kicker(slide, x, y, label, color=BLUE_LT, w=6.0):
    rect(slide, x, y + 0.055, 0.20, 0.075, fill=color)
    txt(slide, x + 0.30, y, w, 0.26, [(label.upper(), 9.5, color, True)],
        font=MONO, sa=0)
    return None


def panel(slide, x, y, w, h, title=None, accent=BLUE, fill=SURFACE, tsize=11.5):
    rect(slide, x, y, w, h, fill=fill, line=BORDER)
    rect(slide, x, y, 0.055, h, fill=accent)
    if title:
        txt(slide, x + 0.24, y + 0.16, w - 0.45, 0.30, [(title, tsize, TEXT, True)], sa=0)
        return y + 0.58
    return y + 0.22


def table(slide, x, y, w, h, data, colw, fsize=9.5, hsize=9.5, header=True,
          align=None, rowfills=None, rowh=None):
    rows, cols = len(data), len(data[0])
    gf = slide.shapes.add_table(rows, cols, Inches(x), Inches(y), Inches(w), Inches(h))
    tb = gf.table
    tb.first_row = header
    tb.horz_banding = False
    tot = float(sum(colw))
    for i, v in enumerate(colw):
        tb.columns[i].width = Emu(int(Inches(w) * v / tot))
    if rowh:
        for i, rh in enumerate(rowh):
            tb.rows[i].height = Inches(rh)
    for r in range(rows):
        for c in range(cols):
            cell = tb.cell(r, c)
            cell.margin_left = Inches(0.09)
            cell.margin_right = Inches(0.09)
            cell.margin_top = Inches(0.035)
            cell.margin_bottom = Inches(0.035)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            if rowfills and (r, c) in rowfills:
                cell.fill.fore_color.rgb = rowfills[(r, c)]
            elif header and r == 0:
                cell.fill.fore_color.rgb = RGBColor(0x2D, 0x3F, 0x5C)
            else:
                cell.fill.fore_color.rgb = SURFACE2 if r % 2 == 0 else SURFACE
            p = cell.text_frame.paragraphs[0]
            p.text = str(data[r][c])
            if align and c < len(align):
                p.alignment = {"c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}.get(align[c], PP_ALIGN.LEFT)
            for run in p.runs:
                run.font.size = Pt(hsize if (header and r == 0) else fsize)
                run.font.bold = bool(header and r == 0)
                run.font.name = FONT
                run.font.color.rgb = TEXT if not (header and r == 0) else RGBColor(0xCB, 0xD8, 0xE9)
    return tb


def arrow(slide, x1, y1, x2, y2, color=BLUE_LT, width=1.2, head=True, dash=False):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = color
    c.line.width = Pt(width)
    if dash:
        c.line.dash_style = 4
    if head:
        ln = c.line._get_or_add_ln()
        ln.append(ln.makeelement(qn('a:tailEnd'), {'type': 'triangle', 'w': 'sm', 'len': 'sm'}))
    return c


def node(slide, x, y, w, h, label, sub=None, fill=SURFACE, border=BLUE, lsize=11, ssize=8.5):
    rect(slide, x, y, w, h, fill=fill, line=border)
    ty = y + h / 2.0 - 0.15 - (0.14 if sub else 0.0)
    txt(slide, x + 0.06, ty, w - 0.12, 0.30, [(label, lsize, TEXT, True)],
        align=PP_ALIGN.CENTER, sa=0)
    if sub:
        txt(slide, x + 0.06, ty + 0.29, w - 0.12, 0.26, [(sub, ssize, MUTED)],
            align=PP_ALIGN.CENTER, sa=0)


def stat(slide, x, y, w, h, value, label, note=None, accent=BLUE_LT):
    rect(slide, x, y, w, h, fill=SURFACE, line=BORDER)
    rect(slide, x, y, w, 0.045, fill=accent)
    txt(slide, x + 0.18, y + 0.20, w - 0.32, 0.42, [(value, 20, TEXT, True)], sa=0)
    txt(slide, x + 0.18, y + 0.66, w - 0.32, 0.26, [(label, 9.5, MUTED, True)], font=MONO, sa=0)
    if note:
        txt(slide, x + 0.18, y + 0.92, w - 0.32, h - 1.0, [(note, 8.5, DIM)], ls=1.12, sa=0)


def header(slide, eyebrow, title, sub=None):
    txt(slide, ML, 0.38, CW, 0.26, [(eyebrow.upper(), 9.5, BLUE_LT, True)], font=MONO, sa=0)
    txt(slide, ML, 0.62, CW, 0.50, [(title, 25, TEXT, True)], sa=0)
    if sub:
        txt(slide, ML, 1.12, CW, 0.26, [(sub, 11.5, MUTED)], sa=0)
    rect(slide, ML, 1.48, 1.35, 0.035, fill=BLUE)
    rect(slide, ML + 1.45, 1.48, 0.30, 0.035, fill=EMERALD)
    return 1.72


def footer(slide, tag=None):
    n = _n["i"]
    rect(slide, ML, 6.94, CW, 0.010, fill=BORDER)
    txt(slide, ML, 7.04, 3.10, 0.24,
        [("8051 HARDWARE LAB  /  ECE 2025-26", 8, DIM, True)],
        font=MONO, sa=0)
    if tag:
        txt(slide, ML + 3.30, 7.04, 6.20, 0.24, [(tag, 8, DIM)], font=MONO, sa=0)
    txt(slide, SW - MR - 1.10, 7.04, 1.10, 0.24,
        [("%02d / 07" % n, 8, DIM, True)], font=MONO, align=PP_ALIGN.RIGHT, sa=0)


def chip_icon(slide, x, y, w, h):
    body_w = w * 0.52
    bx = x + (w - body_w) / 2.0
    by = y + 0.16
    bh = h - 0.32
    rect(slide, bx, by, body_w, bh, fill=SURFACE2, line=BLUE, lw=1.4)
    pins = 7
    step = bh / (pins + 1)
    for i in range(pins):
        py = by + step * (i + 1)
        rect(slide, bx - 0.16, py - 0.018, 0.16, 0.036, fill=BLUE_LT)
        rect(slide, bx + body_w, py - 0.018, 0.16, 0.036, fill=BLUE_LT)
    rect(slide, bx - 0.16, by + 0.10, 0.16, 0.10, fill=EMERALD)
    txt(slide, bx + 0.04, by + bh / 2 - 0.16, body_w - 0.08, 0.32,
        [("AT89S52", 8.5, TEXT, True)], align=PP_ALIGN.CENTER, font=MONO, sa=0)


# ============================================================ SLIDE 1
s = new_slide()
grid_bg(s)
rect(s, 0, 0, SW, 0.09, fill=BLUE)
rect(s, 0, SH - 0.09, SW, 0.09, fill=EMERALD)

txt(s, ML, 0.95, 8.6, 0.26,
    [("MINI PROJECT  /  MICROPROCESSORS AND MICROCONTROLLERS", 9.5, BLUE_LT, True)],
    font=MONO, sa=0)
txt(s, ML, 1.30, 8.6, 0.85, [("8051 Hardware Lab", 40, TEXT, True)], sa=0)
txt(s, ML, 2.18, 8.6, 0.55,
    [("Real-time embedded monitoring on the AT89S52", 18, TEXT)], sa=0)
txt(s, ML, 2.72, 8.6, 0.40,
    [("From browser simulator to measured silicon in one build cycle", 12.5, MUTED)], sa=0)
rect(s, ML, 3.32, 2.2, 0.045, fill=BLUE)
rect(s, ML + 2.30, 3.32, 0.45, 0.045, fill=EMERALD)

meta = [("Authors", "ATHARVA (24BEL0082)  -  ADITYA (24BEL0087)"),
        ("Department", "Electronics and Communication Engineering"),
        ("Academic year", "2025 - 26"),
        ("Review", "Technical Review Committee"),
        ("Artifacts", "Schematic, BOM, 13 Keil C51 programs, test report")]
yy = 3.70
for k, v in meta:
    rich(s, ML, yy, 8.6, 0.26, [(k.ljust(16), 10.5, DIM, True), (v, 10.5, TEXT)],
         size=10.5, font=MONO)
    yy += 0.30

chip_icon(s, 9.30, 1.20, 3.40, 2.10)
rect(s, 9.30, 3.45, 3.40, 1.55, fill=SURFACE, line=BORDER)
txt(s, 9.52, 3.62, 3.0, 0.26, [("SYSTEM ID", 9, BLUE_LT, True)], font=MONO, sa=0)
for i, (k, v) in enumerate([("Target", "AT89S52-24PU"), ("Clock", "11.0592 MHz"),
                            ("Bus", "8-bit shared, P0"), ("Firmware", "Keil C51, 13 programs")]):
    rich(s, 9.52, 3.92 + i * 0.26, 3.0, 0.24,
         [(k.ljust(10), 9, DIM), (v, 9, TEXT, True)], size=9, font=MONO)

stats = [("32 / 32", "I/O PINS UTILISED", "full allocation, no headroom", BLUE_LT),
         ("0.00 %", "UART BAUD ERROR", "TH1 = FDH at 11.0592 MHz", EMERALD_LT),
         ("0.78 C", "ADC RESOLUTION", "Vref/2 trimmed to 1.000 V", BLUE_LT),
         ("INR 985", "BOM PER BOARD", "through-hole, single unit", EMERALD_LT)]
for i, (v, l, n, c) in enumerate(stats):
    stat(s, ML + i * (cw(3) + GUT), 5.55, cw(3), 1.28, v, l, n, accent=c)

# ============================================================ SLIDE 2
s = new_slide()
grid_bg(s)
y0 = header(s, "Slide 02  /  Problem", "Problem statement and constraints",
            "What had to be solved before a single component was placed")

yb = panel(s, ML, y0, cw(7), 2.86, "PROBLEM STATEMENT", accent=BLUE)
txt(s, ML + 0.24, yb, cw(7) - 0.48, 1.32,
    [("Transfer the verified 8051 programs from a software model onto a physical AT89S52, interfacing "
      "eight LEDs, a two digit seven segment display, a 16x2 character LCD, an eight way DIP switch "
      "bank, an LM35 temperature sensor through an ADC0804, a MAX232 serial link, a relay and a "
      "buzzer, and confirm on the bench that every output matches the value the simulator predicted.",
      11.5, TEXT, False, True)], ls=1.22, sa=0)
txt(s, ML + 0.24, 3.62, cw(7) - 0.48, 0.86,
    [("Hard constraint:  ", 10.5, BLUE_LT, True),
     ("the peripherals require 54 I/O lines and the 8051 provides 32. The architecture must close a "
      "22 pin deficit without adding a port expander IC.", 10.5, MUTED)], ls=1.16, sa=0)

yb2 = panel(s, cx(7), y0, cw(5), 2.86, "DESIGN CONSTRAINTS", accent=EMERALD)
cons = [("I/O budget", "54 required, 32 available", BLUE_LT),
        ("Port 0 topology", "open drain, cannot source", AMBER),
        ("Latch read-back", "no read path to the latches", AMBER),
        ("ISP contention", "P1.5-P1.7 shared with SPI", RED),
        ("ADC resolution", "8 bits, reference is a choice", BLUE_LT),
        ("No HW debounce", "buttons bounce 1 to 10 ms", AMBER)]
for i, (k, v, c) in enumerate(cons):
    yy = yb2 + i * 0.355
    rect(s, cx(7) + 0.24, yy + 0.075, 0.075, 0.075, fill=c)
    rich(s, cx(7) + 0.42, yy, cw(5) - 0.66, 0.24,
         [(k, 10, TEXT, True), ("    " + v, 9.5, MUTED)], size=10)

data = [["ID", "Constraint", "Consequence if ignored", "Mitigation in this design"],
        ["C1", "32 I/O pins for 54 signals",
         "peripherals dropped, or an expander IC added",
         "single 8-bit bus on P0 with per-device strobes on P2"],
        ["C2", "P0 is open drain",
         "the bus never reaches a valid logic 1",
         "RN1, a 10 kOhm x 9 SIP network, pulls the bus up"],
        ["C3", "Output latches cannot be read",
         "a stale byte is latched into the wrong device",
         "bus_shadow variable plus interrupt gating on transfers"],
        ["C4", "SW6-SW8 share the ISP lines",
         "in-circuit programming fails or is corrupted",
         "1 kOhm series resistors and a documented OFF state"],
        ["C5", "8-bit ADC, 5 V default reference",
         "1.95 C per step, most of the range wasted",
         "Vref/2 trimmed to 1.000 V, giving 0.78 C per step"],
        ["C6", "No hardware debounce on the buttons",
         "one press registers as several interrupts",
         "5 ms resampling and edge triggered IT0 and IT1"]]
rowh = [0.275] + [0.305] * 6
table(s, ML, 4.72, CW, 2.10, data, colw=[0.55, 2.55, 3.6, 4.6], fsize=8.5, hsize=8.5,
      align=["c", "l", "l", "l"], rowh=rowh)
footer(s, "constraint register C1-C6")

# ============================================================ SLIDE 3
s = new_slide()
grid_bg(s)
y0 = header(s, "Slide 03  /  Architecture", "System block diagram",
            "One shared 8-bit bus resolves the 22 pin deficit")

mcu_w = cw(4)
mcu_x = (SW - mcu_w) / 2.0
node(s, mcu_x, 1.75, mcu_w, 0.95, "AT89S52-24PU", "40-pin DIP  /  11.0592 MHz",
     fill=RGBColor(0x2D, 0x3F, 0x5C), border=BLUE, lsize=12.5)

inputs = [("SW1 8-way DIP", "P1.0-P1.7"), ("PB1 / PB2", "P3.2 / P3.3"), ("LM35 sensor", "ADC Vin+")]
for i, (a, b) in enumerate(inputs):
    yy = 1.75 + i * 0.72
    node(s, ML, yy, cw(3), 0.62, a, b, border=EMERALD, lsize=10, ssize=8)
    arrow(s, ML + cw(3) + 0.02, yy + 0.31, mcu_x - 0.02, 2.22, color=EMERALD_LT, width=1.0)

outputs = [("Relay + buzzer", "P3.4 / P3.5"), ("Digit selects", "P3.6 / P3.7"),
           ("MAX232 / DB9", "P3.0 / P3.1")]
for i, (a, b) in enumerate(outputs):
    yy = 1.75 + i * 0.72
    ox = SW - MR - cw(3)
    node(s, ox, yy, cw(3), 0.62, a, b, border=BLUE_LT, lsize=10, ssize=8)
    arrow(s, mcu_x + mcu_w + 0.02, 2.22, ox - 0.02, yy + 0.31, color=BLUE_LT, width=1.0)

bw = cw(10)
bx = (SW - bw) / 2.0
rect(s, bx, 3.92, bw, 0.48, fill=RGBColor(0x2D, 0x3F, 0x5C), line=BLUE)
txt(s, bx, 4.01, bw, 0.32,
    [("BD0 - BD7      shared 8-bit data bus      port 0      10 kOhm pull-ups", 11, TEXT, True)],
    align=PP_ALIGN.CENTER, font=MONO, sa=0)
arrow(s, SW / 2.0, 2.70, SW / 2.0, 3.92, color=BLUE, width=1.8)

bus_devs = [("U2 74HC573", "8 LEDs", "P2.0 LED_LE", BLUE_LT),
            ("U3 74HC573", "7-segment x2", "P2.1 SEG_LE", BLUE_LT),
            ("LCD1 16x2", "HD44780 8-bit", "P2.2-P2.4 E RS RW", EMERALD_LT),
            ("U4 ADC0804", "LM35 8-bit", "P2.5-P2.7 WR RD INTR", EMERALD_LT)]
for i, (a, b, c, col) in enumerate(bus_devs):
    x = ML + i * (cw(3) + GUT)
    node(s, x, 4.62, cw(3), 0.78, a, b, border=col, lsize=10.5, ssize=8)
    arrow(s, x + cw(3) / 2, 4.40, x + cw(3) / 2, 4.62, color=col, width=1.3)
    txt(s, x, 5.42, cw(3), 0.22, [(c, 8, MUTED)], align=PP_ALIGN.CENTER, font=MONO, sa=0)

data = [["Interface", "Width", "Signals", "Direction", "Device"],
        ["Parallel bus", "8 bit", "BD0-BD7", "bidirectional", "U2 U3 LCD1 U4"],
        ["Latch strobe", "1 bit", "LED_LE SEG_LE", "output", "U2 U3"],
        ["LCD control", "3 bit", "E RS RW", "output", "LCD1"],
        ["ADC control", "3 bit", "WR RD INTR", "in / out", "U4"],
        ["Serial + GPIO", "6 bit", "TxD RxD P3.4-P3.7", "both", "MAX232 Q1-Q4"]]
table(s, ML, 5.70, cw(7), 1.14, data, colw=[1.5, 0.7, 2.3, 1.3, 1.9], fsize=8.5, hsize=8.5,
      align=["l", "c", "l", "c", "l"], rowh=[0.19] * 6)

yb = panel(s, cx(7), 5.70, cw(5), 1.14, "PIN ECONOMY", accent=EMERALD, tsize=9.5)
txt(s, cx(7) + 0.24, yb, cw(5) - 0.48, 0.50,
    [("54 pins required  ->  32 available", 9, MUTED),
     ("Three 8-bit data paths merged into one bus, saving 24 pins.", 9, TEXT),
     ("Eight of them pay for the strobes. Net saving: 16 pins.", 9, EMERALD_LT, True)],
    ls=1.14, sa=0)
footer(s, "single bus, four devices, eight strobes")

# ============================================================ SLIDE 4
s = new_slide()
grid_bg(s)
y0 = header(s, "Slide 04  /  Stack", "Hardware and software stack",
            "Four layers, one board, no operating system")

layers = [
    ("APPLICATION", "13 firmware programs  /  board.h  /  01 blink to 13 self test", "firmware/src", BLUE),
    ("DRIVER", "bus, LED, 7-segment, LCD, ADC, UART, switch debounce", "firmware/inc/board.h", BLUE_LT),
    ("INTERFACE", "8-bit parallel  /  HD44780 8-bit  /  ADC0804  /  UART 9600 8N1", "P0, P2, P3", EMERALD),
    ("SILICON", "AT89S52  2x 74HC573  ADC0804  LM35  MAX232  HD44780  BC547 x4  7805", "through-hole DIP", EMERALD_LT),
]
yy = y0
for name, body, tag, col in layers:
    rect(s, ML, yy, CW, 0.58, fill=SURFACE, line=BORDER)
    rect(s, ML, yy, 0.055, 0.58, fill=col)
    txt(s, ML + 0.24, yy + 0.07, 1.75, 0.24, [(name, 9, col, True)], font=MONO, sa=0)
    txt(s, ML + 2.10, yy + 0.07, CW - 4.10, 0.24, [(body, 10, TEXT)], font=MONO, sa=0)
    txt(s, ML + CW - 1.90, yy + 0.07, 1.70, 0.24, [(tag, 8.5, DIM)],
        align=PP_ALIGN.RIGHT, font=MONO, sa=0)
    txt(s, ML + 2.10, yy + 0.30, CW - 4.10, 0.22, [("", 8, DIM)], sa=0)
    yy += 0.64

comps = [("AT89S52-24PU", "MCU", "8 KB flash, 3 timers"),
         ("74HC573 x2", "latch", "LED bank, segment patterns"),
         ("ADC0804LCN", "ADC", "8-bit parallel, 606 kHz"),
         ("LM35DZ", "sensor", "10 mV per degree C"),
         ("MAX232N", "transceiver", "TTL to RS-232, 1 uF pump"),
         ("JHD162A", "display", "16x2 HD44780, 8-bit"),
         ("BC547 x4", "driver", "digits, relay, buzzer"),
         ("L7805CV", "regulator", "5.00 V, 1 W, heatsinked")]
for i, (a, b, c) in enumerate(comps):
    x = ML + (i % 4) * (cw(3) + GUT)
    y = 4.38 + (i // 4) * 0.80
    rect(s, x, y, cw(3), 0.72, fill=SURFACE, line=BORDER)
    rect(s, x, y, 0.045, 0.72, fill=EMERALD)
    txt(s, x + 0.20, y + 0.09, cw(3) - 0.34, 0.22, [(a, 10, TEXT, True)], font=MONO, sa=0)
    txt(s, x + 0.20, y + 0.31, cw(3) - 0.34, 0.20, [(b.upper(), 7.5, EMERALD_LT, True)], font=MONO, sa=0)
    txt(s, x + 0.20, y + 0.50, cw(3) - 0.34, 0.20, [(c, 8.5, MUTED)], sa=0)

data = [["Protocol", "Pins", "Used for"],
        ["8-bit parallel bus", "P0.0-P0.7", "latches, LCD, ADC"],
        ["UART 9600 8N1", "P3.0-P3.1", "telemetry and shell"],
        ["SPI (ISP only)", "P1.5-P1.7", "flash programming"]]
table(s, ML, 5.94, cw(6), 0.90, data, colw=[2.2, 1.6, 2.4], fsize=8.5, hsize=8.5,
      align=["l", "c", "l"], rowh=[0.225] * 4)

rect(s, cx(6), 5.94, cw(6), 0.90, fill=SURFACE, line=BORDER)
rect(s, cx(6), 5.94, 0.055, 0.90, fill=BLUE)
txt(s, cx(6) + 0.24, 6.04, cw(6) - 0.45, 0.24, [("TOOLCHAIN", 9.5, TEXT, True)], font=MONO, sa=0)
txt(s, cx(6) + 0.24, 6.30, cw(6) - 0.45, 0.48,
    [("Keil uVision 5, C51, level 8, small memory model", 8.5, TEXT),
     ("USBasp + avrdude -p 8052  USB-RS232  DMM  20 MHz scope", 8.5, MUTED)],
    ls=1.10, sa=0)
footer(s, "no RTOS, no external memory, one translation unit per program")

# ============================================================ SLIDE 5
s = new_slide()
grid_bg(s)
y0 = header(s, "Slide 05  /  Implementation", "Implementation logic and control flow",
            "Interrupt driven display refresh around a polling control loop")

steps = [
    ("board_init", "ports, latches, outputs off", BLUE_LT, 0.58),
    ("display_init", "timer 0 at 5 ms, EE00H", BLUE_LT, 0.58),
    ("adc_read", "start, wait INTR, read byte", EMERALD_LT, 0.58),
    ("zone decision", "T < 40 / < 70 / >= 70 C", AMBER, 0.72),
    ("actuate", "LEDs, relay, buzzer", EMERALD_LT, 0.58),
    ("publish", "LCD, 7-segment, UART 1 Hz", BLUE_LT, 0.58),
]
yy = y0
for i, (a, b, c, h) in enumerate(steps):
    shp = MSO_SHAPE.DIAMOND if i == 3 else MSO_SHAPE.ROUNDED_RECTANGLE
    rect(s, ML + 0.28, yy, cw(3) - 0.28, h, fill=SURFACE, line=c, shape=shp, radius=0.14, lw=1.3)
    ty = yy + h / 2.0 - 0.17
    txt(s, ML + 0.36, ty, cw(3) - 0.44, 0.22, [(a, 10, TEXT, True)], align=PP_ALIGN.CENTER, font=MONO, sa=0)
    txt(s, ML + 0.36, ty + 0.23, cw(3) - 0.44, 0.20, [(b, 8, MUTED)], align=PP_ALIGN.CENTER, sa=0)
    if i < len(steps) - 1:
        arrow(s, ML + cw(3) / 2 - 0.14, yy + h + 0.02, ML + cw(3) / 2 - 0.14, yy + h + 0.20,
              color=DIM, width=1.0)
    yy += h + 0.20

mx = cx(3)
mw = cw(4)
yb = panel(s, mx, y0, mw, 1.30, "TIMER 0 ISR  /  EVERY 5 ms", accent=EMERALD, tsize=9.5)
txt(s, mx + 0.24, yb, mw - 0.48, 0.62,
    [("TH0 = EEH   TL0 = 00H", 9.5, TEXT),
     ("seg_tick() alternates the two digits", 9, MUTED),
     ("saves and restores the bus shadow byte", 9, MUTED)], ls=1.14, sa=0, font=MONO)

yb = panel(s, mx, 3.14, mw, 1.86, "BUS TRANSFER PRIMITIVE", accent=BLUE, tsize=9.5)
seq = [("1  save", "ea = EA"), ("2  gate", "EA = 0"), ("3  place", "BUS = v"),
       ("4  strobe", "LE = 1"), ("5  release", "LE = 0"), ("6  restore", "BUS = shadow")]
for i, (a, b) in enumerate(seq):
    x = mx + 0.24 + (i % 2) * ((mw - 0.48) / 2.0)
    y = yb + (i // 2) * 0.44
    rect(s, x, y, (mw - 0.62) / 2.0, 0.38, fill=SURFACE2, line=BORDER)
    txt(s, x + 0.10, y + 0.04, (mw - 0.62) / 2.0 - 0.20, 0.20, [(a, 9, BLUE_LT, True)], font=MONO, sa=0)
    txt(s, x + 0.10, y + 0.21, (mw - 0.62) / 2.0 - 0.20, 0.18, [(b, 8, MUTED)], font=MONO, sa=0)

yb = panel(s, mx, 5.12, mw, 1.72, "EXTERNAL INTERRUPTS", accent=AMBER, tsize=9.5)
txt(s, mx + 0.24, yb, mw - 0.48, 1.0,
    [("INT0 falling edge  ->  emergency latch", 9.5, TEXT),
     ("INT1 falling edge  ->  clear the latch", 9, MUTED),
     ("Both ISRs set a flag only; the main loop", 9, MUTED),
     ("does the work, keeping service short.", 9, MUTED)], ls=1.14, sa=0, font=MONO)

rx = cx(7)
rw = cw(5)
data = [["Stage", "Operation", "Failure mode handled"],
        ["Acquire", "adc_read, INTR both edges", "guarded timeout returns"],
        ["Convert", "T = raw x 25 / 32 integer", "no float library needed"],
        ["Decide", "compare at 400 and 700", "emergency overrides all"],
        ["Actuate", "latch write, relay, buzzer", "interrupts gated"],
        ["Publish", "LCD, 7-segment, UART 1 Hz", "refresh runs in the ISR"]]
table(s, rx, y0, rw, 1.30, data, colw=[1.1, 2.5, 1.9], fsize=8.5, hsize=8.5,
      align=["l", "l", "l"], rowh=[0.20] + [0.22] * 5)

data = [["Operation", "Cycles", "Time"],
        ["machine cycle", "12 osc", "1.0851 us"],
        ["bus transfer", "~20", "21.7 us"],
        ["ADC conversion", "-", "114 us"],
        ["LCD write", "~30", "32.6 us"],
        ["display tick", "4608", "5.000 ms"],
        ["telemetry period", "-", "1.000 s"]]
table(s, rx, 3.18, rw, 1.74, data, colw=[2.0, 1.4, 1.6], fsize=8.5, hsize=8.5,
      align=["l", "c", "c"], rowh=[0.21] + [0.255] * 6)

yb = panel(s, rx, 5.12, rw, 1.72, "WHY POLL, WHY INTERRUPT", accent=EMERALD, tsize=9.5)
txt(s, rx + 0.24, yb, rw - 0.48, 1.0,
    [("The display must never flicker, so it runs", 9, MUTED),
     ("in the interrupt. Sensing and acting can", 9, MUTED),
     ("slip by milliseconds, so they poll. Each", 9, MUTED),
     ("mechanism is matched to its own deadline.", 9, TEXT, True)], ls=1.14, sa=0)
footer(s, "poll in the loop, refresh in the interrupt")

# ============================================================ SLIDE 6
s = new_slide()
grid_bg(s)
y0 = header(s, "Slide 06  /  Results", "Results, benchmarks and trade-offs",
            "Derived values, measured targets and the decisions behind them")

metrics = [("0.00 %", "BAUD ERROR", "TH1 = FDH at 11.0592 MHz", EMERALD_LT),
           ("1.00 kHz", "TIMER OUTPUT", "FE34H reload, +0.17 %", EMERALD_LT),
           ("100 Hz", "DISPLAY REFRESH", "EE00H reload, per digit", BLUE_LT),
           ("0.78 C", "ADC RESOLUTION", "7.8125 mV per step", BLUE_LT),
           ("157 mA", "BOARD CURRENT", "274 mA peak, relay on", AMBER),
           ("3.4 KB", "LARGEST PROGRAM", "of 8 KB flash, 30 B RAM", BLUE_LT)]
for i, (v, l, n, c) in enumerate(metrics):
    stat(s, ML + (i % 3) * (cw(4) + GUT), y0 + (i // 3) * 1.14, cw(4), 1.04, v, l, n, accent=c)

data = [["Decision", "Alternative rejected", "Trade-off accepted", "Outcome"],
        ["Shared 8-bit bus", "I2C or SPI port expander IC",
         "8 extra strobes and software arbitration", "54 pins fitted into 32, no extra IC"],
        ["AT89S52 with ISP", "AT89C51, parallel programmer",
         "slightly higher chip cost", "programmer cost falls to INR 250"],
        ["470 Ohm LED resistors", "the usual 330 Ohm",
         "about 15 % less brightness", "53 mA per package, inside the 70 mA limit"],
        ["Vref/2 at 1.000 V", "internal 2.5 V reference",
         "one trimpot and one calibration step", "0.78 C per step instead of 1.95 C"],
        ["Software driven bus", "MOVX with an address latch",
         "no hardware address decode", "port 2 stays free for eight strobes"],
        ["Flags inside the ISRs", "doing the work in the ISR",
         "one loop of latency", "short, predictable service routines"],
        ["Software debounce", "RC filter or Schmitt trigger",
         "5 ms of loop time", "no parts, no spare pins consumed"]]
table(s, ML, 4.36, CW, 2.48, data, colw=[2.0, 2.6, 2.9, 3.6], fsize=8.5, hsize=8.5,
      align=["l", "l", "l", "l"], rowh=[0.26] + [0.317] * 7)
footer(s, "20 bench tests, T1-T20, acceptance limits in hardware/TESTING.md")

# ============================================================ SLIDE 7
s = new_slide()
grid_bg(s)
y0 = header(s, "Slide 07  /  Outlook", "Scalability, future scope and conclusion",
            "Where the architecture has headroom and where it does not")

phases = [("NOW", "Single board, verified",
           ["13 programs, 20 tests", "INR 985 per board", "9600 baud telemetry"], EMERALD),
          ("NEXT", "Recover two pins",
           ["LCD on a PCF8574 backpack", "frees P2.3 and P2.4", "adds I2C: RTC, EEPROM"], BLUE_LT),
          ("LATER", "Multi-node and PCB",
           ["RS-485 or ESP-01 link", "KiCad two layer layout", "mains rated enclosure"], AMBER)]
for i, (tag, title, items, col) in enumerate(phases):
    x = ML + i * (cw(4) + GUT)
    rect(s, x, y0, cw(4), 2.24, fill=SURFACE, line=BORDER)
    rect(s, x, y0, cw(4), 0.045, fill=col)
    txt(s, x + 0.22, y0 + 0.19, 1.2, 0.24, [(tag, 10.5, col, True)], font=MONO, sa=0)
    txt(s, x + 0.22, y0 + 0.48, cw(4) - 0.44, 0.28, [(title, 12.5, TEXT, True)], sa=0)
    for j, it in enumerate(items):
        rect(s, x + 0.24, y0 + 0.92 + j * 0.39 + 0.07, 0.07, 0.07, fill=col)
        txt(s, x + 0.44, y0 + 0.92 + j * 0.39, cw(4) - 0.66, 0.30, [(it, 9.5, MUTED)], ls=1.1, sa=0)
    if i < 2:
        arrow(s, x + cw(4) + 0.02, y0 + 1.12, x + cw(4) + GUT - 0.02, y0 + 1.12,
              color=DIM, width=1.2)

yb = panel(s, ML, 4.24, cw(7), 2.56, "CONCLUSION", accent=EMERALD, tsize=12)
concl = [
    "A 22 pin deficit was closed by architecture, not by extra silicon.",
    "Every constant derives from the 1.0851 microsecond machine cycle.",
    "Thirteen programs compile clean; the build is staged and measured.",
    "Every hardware result reconciles with the phase 1 simulator.",
]
for i, c in enumerate(concl):
    rect(s, ML + 0.24, yb + 0.10 + i * 0.44 + 0.08, 0.07, 0.07, fill=EMERALD)
    txt(s, ML + 0.44, yb + 0.06 + i * 0.44, cw(7) - 0.68, 0.36, [(c, 10.5, TEXT)], ls=1.12, sa=0)

yb2 = panel(s, cx(7), 4.24, cw(5), 2.56, "SCALABILITY LIMITS", accent=AMBER, tsize=12)
lim = [("Bus", "shared P0 caps throughput, a few hundred kHz"),
       ("ADC", "one channel, 8-bit, about 114 us per sample"),
       ("Memory", "256 B RAM, no external data memory wired"),
       ("Interrupts", "two external sources, no priority nesting"),
       ("Relay", "demonstration only, never mains connected")]
for i, (k, v) in enumerate(lim):
    txt(s, cx(7) + 0.24, yb2 + i * 0.38, 1.10, 0.22, [(k, 9, AMBER, True)], font=MONO, sa=0)
    txt(s, cx(7) + 1.42, yb2 + i * 0.38, cw(5) - 1.66, 0.30, [(v, 9, MUTED)], ls=1.1, sa=0)

footer(s, "repository: AdityaRezan/8051-hardware-lab")

import os
os.makedirs("docs", exist_ok=True)
prs.save("docs/8051_Hardware_Lab_Review_Deck.pptx")
print("saved docs/8051_Hardware_Lab_Review_Deck.pptx")
print("slides:", len(prs.slides._sldIdLst))
