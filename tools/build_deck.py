from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn

BG      = RGBColor(0x0F, 0x1B, 0x33)
PANEL   = RGBColor(0x1E, 0x2E, 0x4E)
PANEL2  = RGBColor(0x17, 0x24, 0x3E)
DARK    = RGBColor(0x0A, 0x12, 0x24)
ACCENT  = RGBColor(0x2F, 0xE0, 0xC0)
TEXT    = RGBColor(0xF2, 0xF6, 0xFF)
MUTED   = RGBColor(0xA9, 0xB8, 0xD6)
DIM     = RGBColor(0x6F, 0x81, 0xA5)
LIGHT   = RGBColor(0xCF, 0xE0, 0xFF)
AMBER   = RGBColor(0xFF, 0xB4, 0x54)
RED     = RGBColor(0xFF, 0x6B, 0x6B)
GREEN   = RGBColor(0x5C, 0xE0, 0x8A)
WHITE   = RGBColor(0xFF, 0xFF, 0xFF)

FONT  = "Calibri"
MONO  = "Consolas"

SW = 13.3333
SH = 7.5
ML = 0.62
CW = SW - 2 * ML

prs = Presentation()
prs.slide_width = Inches(SW)
prs.slide_height = Inches(SH)
BLANK = prs.slide_layouts[6]

_page = {"n": 0}


def new_slide():
    s = prs.slides.add_slide(BLANK)
    bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG
    bg.line.fill.background()
    bg.shadow.inherit = False
    _page["n"] += 1
    return s


def box(slide, x, y, w, h, fill=PANEL, line=None, shape=MSO_SHAPE.ROUNDED_RECTANGLE,
        adj=0.06, shadow=False):
    shp = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(1.0)
    shp.shadow.inherit = shadow
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        try:
            shp.adjustments[0] = adj
        except Exception:
            pass
    return shp


def text(slide, x, y, w, h, runs, size=14, color=TEXT, bold=False, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, space_after=4, line_spacing=1.0, font=FONT, italic=False):
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
            item = (item, size, color, bold, italic)
        item = tuple(item) + (None,) * (5 - len(item))
        t, sz, col, bd, it = item
        sz = size if sz is None else sz
        col = color if col is None else col
        bd = bold if bd is None else bd
        it = italic if it is None else it
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.text = t
        p.alignment = align
        p.space_after = Pt(space_after)
        p.line_spacing = line_spacing
        for r in p.runs:
            r.font.size = Pt(sz)
            r.font.bold = bd
            r.font.italic = it
            r.font.color.rgb = col
            r.font.name = font
    return tb


def rich(slide, x, y, w, h, parts, size=11.5, align=PP_ALIGN.LEFT, font=FONT, space_after=0):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    para = tf.paragraphs[0]
    para.alignment = align
    para.space_after = Pt(space_after)
    for item in parts:
        item = tuple(item) + (None,) * (4 - len(item))
        t, sz, col, bd = item[0], item[1], item[2], item[3]
        r = para.add_run()
        r.text = t
        r.font.size = Pt(sz if sz is not None else size)
        r.font.bold = bool(bd)
        r.font.color.rgb = col if col is not None else TEXT
        r.font.name = font
    return tb


def title_bar(slide, kicker, title, sub=None):
    bar = box(slide, 0, 0, SW, 0.10, ACCENT, shape=MSO_SHAPE.RECTANGLE)
    text(slide, ML, 0.40, CW, 0.28, [(kicker.upper(), 11, ACCENT, True)], space_after=0)
    text(slide, ML, 0.66, CW, 0.48, [(title, 27, TEXT, True)], space_after=0)
    if sub:
        text(slide, ML, 1.16, CW, 0.28, [(sub, 12.5, MUTED, False)], space_after=0)
    rule = box(slide, ML, 1.48, 1.5, 0.035, ACCENT, shape=MSO_SHAPE.RECTANGLE)
    return rule


def footer(slide, n):
    line = box(slide, ML, 6.98, CW, 0.012, RGBColor(0x25, 0x35, 0x57), shape=MSO_SHAPE.RECTANGLE)
    text(slide, ML, 7.06, 9.0, 0.26,
         [("8051 Microcontroller Hardware Lab  |  ATHARVA (24BEL0082) - ADITYA (24BEL0087)", 8.5, DIM)],
         space_after=0)
    text(slide, SW - ML - 1.2, 7.06, 1.2, 0.26, [(str(n), 8.5, DIM)], align=PP_ALIGN.RIGHT, space_after=0)


def content_slide(kicker, title, sub=None):
    s = new_slide()
    title_bar(s, kicker, title, sub)
    footer(s, _page["n"])
    return s


def card(slide, x, y, w, h, heading, body, accent=ACCENT, hsize=13, bsize=11, fill=PANEL):
    box(slide, x, y, w, h, fill=fill)
    bar = box(slide, x, y, 0.055, h, accent, shape=MSO_SHAPE.RECTANGLE)
    text(slide, x + 0.26, y + 0.18, w - 0.45, 0.3, [(heading, hsize, TEXT, True)], space_after=0)
    text(slide, x + 0.26, y + 0.60, w - 0.45, h - 0.75,
         [(body, bsize, MUTED)], line_spacing=1.18, space_after=0)


def num_card(slide, x, y, w, h, num, heading, body, accent=ACCENT):
    box(slide, x, y, w, h, fill=PANEL)
    box(slide, x, y, w, 0.045, accent, shape=MSO_SHAPE.RECTANGLE)
    text(slide, x + 0.22, y + 0.16, 0.7, 0.42, [(num, 22, accent, True)], space_after=0)
    text(slide, x + 0.22, y + 0.70, w - 0.42, 0.54, [(heading, 12.5, TEXT, True)], line_spacing=1.0, space_after=0)
    text(slide, x + 0.22, y + 1.26, w - 0.42, h - 1.40,
         [(body, 10.5, MUTED)], line_spacing=1.15, space_after=0)


def table(slide, x, y, w, h, data, col_w=None, fsize=9.5, hsize=9.5,
          header=True, align=None, fills=None, row_h=None):
    rows = len(data)
    cols = len(data[0])
    gf = slide.shapes.add_table(rows, cols, Inches(x), Inches(y), Inches(w), Inches(h))
    tbl = gf.table
    tbl.first_row = header
    tbl.horz_banding = False
    if row_h:
        for i, rh in enumerate(row_h):
            tbl.rows[i].height = Inches(rh)
    if col_w:
        total = float(sum(col_w))
        for i, cwv in enumerate(col_w):
            tbl.columns[i].width = Emu(int(Inches(w) * cwv / total))
    for r in range(rows):
        for c in range(cols):
            cell = tbl.cell(r, c)
            cell.margin_left = Inches(0.08)
            cell.margin_right = Inches(0.08)
            cell.margin_top = Inches(0.03)
            cell.margin_bottom = Inches(0.03)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            if fills and (r, c) in fills:
                cell.fill.fore_color.rgb = fills[(r, c)]
            elif header and r == 0:
                cell.fill.fore_color.rgb = ACCENT if False else RGBColor(0x2A, 0x3C, 0x63)
            else:
                cell.fill.fore_color.rgb = PANEL2 if r % 2 else PANEL
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            val = str(data[r][c])
            p.text = val
            if align and c < len(align) and align[c] == "c":
                p.alignment = PP_ALIGN.CENTER
            elif align and c < len(align) and align[c] == "r":
                p.alignment = PP_ALIGN.RIGHT
            else:
                p.alignment = PP_ALIGN.LEFT
            for run in p.runs:
                run.font.size = Pt(hsize if (header and r == 0) else fsize)
                run.font.bold = bool(header and r == 0)
                run.font.name = FONT
                if header and r == 0:
                    run.font.color.rgb = LIGHT
                else:
                    run.font.color.rgb = TEXT
    return tbl


def code_panel(slide, x, y, w, h, lines, size=10.5, title=None):
    box(slide, x, y, w, h, fill=DARK)
    yy = y + 0.14
    if title:
        text(slide, x + 0.22, yy, w - 0.4, 0.24, [(title, 9.5, DIM, True)], space_after=0)
        yy += 0.28
    runs = []
    for ln in lines:
        runs.append((ln, size, LIGHT))
    text(slide, x + 0.22, yy, w - 0.4, h - (yy - y) - 0.1, runs,
         font=MONO, line_spacing=1.14, space_after=0)


def arrow(slide, x1, y1, x2, y2, color=ACCENT, width=1.2, head=True):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = color
    c.line.width = Pt(width)
    if head:
        ln = c.line._get_or_add_ln()
        tail = ln.makeelement(qn('a:tailEnd'), {'type': 'triangle', 'w': 'sm', 'len': 'sm'})
        ln.append(tail)
    return c


def node(slide, x, y, w, h, label, sub=None, fill=PANEL, border=ACCENT, lsize=11, ssize=8.5):
    box(slide, x, y, w, h, fill=fill, line=border)
    tf_h = 0.30 if sub else h
    ty = y + (h / 2.0 - tf_h / 2.0) - (0.12 if sub else 0)
    text(slide, x + 0.08, ty, w - 0.16, 0.3, [(label, lsize, TEXT, True)],
         align=PP_ALIGN.CENTER, space_after=0)
    if sub:
        text(slide, x + 0.08, ty + 0.30, w - 0.16, 0.26, [(sub, ssize, MUTED)],
             align=PP_ALIGN.CENTER, space_after=0)
    return None


# ----------------------------------------------------------------- slide 1
s = new_slide()
box(s, 0, 0, SW, 0.16, ACCENT, shape=MSO_SHAPE.RECTANGLE)
box(s, 0, SH - 0.16, SW, 0.16, ACCENT, shape=MSO_SHAPE.RECTANGLE)

text(s, ML, 1.05, CW, 0.4, [("MINI PROJECT - MICROPROCESSORS AND MICROCONTROLLERS", 12, ACCENT, True)],
     space_after=0)
text(s, ML, 1.52, CW, 1.5,
     [("8051 Microcontroller:", 40, TEXT, True),
      ("Architecture Study, Assembly Programming and Simulation", 21, MUTED)],
     space_after=2)
text(s, ML, 3.10, CW, 0.5,
     [("Phase 2 - Hardware Implementation on a Real AT89S52", 19, LIGHT, True)], space_after=0)

box(s, ML, 3.78, 6.6, 0.045, ACCENT, shape=MSO_SHAPE.RECTANGLE)

for i, (lbl, val) in enumerate([
        ("Target device", "AT89S52-24PU, 40 pin DIP"),
        ("Clock", "11.0592 MHz, 1.0851 us machine cycle"),
        ("I/O used", "32 of 32 pins, shared 8-bit bus"),
        ("Cost", "about INR 985 per board")]):
    rich(s, ML, 4.02 + i * 0.32, 6.9, 0.28,
         [(lbl + ":  ", 11.5, DIM, False), (val, 11.5, TEXT, True)], size=11.5)

badge = box(s, 9.05, 3.72, 3.5, 1.62, fill=PANEL, line=ACCENT)
text(s, 9.05, 3.95, 3.5, 0.4, [("PHASE 2", 15, ACCENT, True)], align=PP_ALIGN.CENTER, space_after=0)
text(s, 9.22, 4.36, 3.16, 0.9,
     [("Simulator verified 14 assembly and 5 C programs.", 10.5, MUTED),
      ("This phase builds the board, writes Keil C51 firmware, and measures every signal.", 10.5, MUTED)],
     align=PP_ALIGN.CENTER, line_spacing=1.15, space_after=0)

box(s, ML, 5.62, CW, 0.012, RGBColor(0x25, 0x35, 0x57), shape=MSO_SHAPE.RECTANGLE)
text(s, ML, 5.80, 6.5, 0.9,
     [("SUBMITTED BY", 9.5, DIM, True),
      ("ATHARVA  (24BEL0082)      ADITYA  (24BEL0087)", 15, TEXT, True),
      ("Department of Electronics and Communication Engineering", 11, MUTED)],
     space_after=3)
text(s, 7.4, 5.80, SW - 7.4 - ML, 0.9,
     [("ACADEMIC YEAR", 9.5, DIM, True),
      ("2025 - 26", 15, TEXT, True),
      ("Microprocessors and Microcontrollers", 11, MUTED)],
     align=PP_ALIGN.RIGHT, space_after=3)

# ----------------------------------------------------------------- slide 2
s = content_slide("Overview", "From simulator to silicon",
                  "What phase 1 delivered and what phase 2 adds")

card(s, ML, 1.72, 5.85, 2.55, "PHASE 1 - DIGITAL MODEL (COMPLETE)",
     "A browser based 8051 trainer with a two pass assembler and an instruction level simulator.\n"
     "Fourteen assembly programs and five Embedded C programs were executed one instruction at a time "
     "and every register, flag and memory change was compared with hand calculation.\n"
     "All fourteen programs verified.",
     accent=DIM, bsize=10.5)

card(s, ML + 6.24, 1.72, 5.85, 2.55, "PHASE 2 - REAL HARDWARE (THIS DECK)",
     "The same ideas built on an AT89S52 with latches, a real ADC, a character LCD, a MAX232 serial "
     "link, a relay and a buzzer.\n"
     "Thirteen Keil C51 programs replace the assembly sources, the board is assembled in ten measured "
     "stages, and twenty tests verify it on the bench.",
     accent=ACCENT, bsize=10.5)

text(s, ML, 4.60, CW, 0.3, [("What changes when the machine becomes real", 15, TEXT, True)], space_after=0)

data = [["Aspect", "In the simulator", "On the hardware"],
        ["I/O", "Ports written directly", "Shared bus with latch strobes"],
        ["Timing", "Idealised machine cycles", "1.0851 us per cycle, measured on a scope"],
        ["Inputs", "Clicked switches, ideal", "Bounce, pull-ups, noise, debounce needed"],
        ["Analog", "Slider sets the temperature", "LM35 into ADC0804, reference must be calibrated"],
        ["Serial", "Terminal pane", "MAX232, DB9 wiring, 9600 8N1"],
        ["Failure", "Program stops", "Wrong Vref, reversed sensor, floating EA pin"],
        ["Verification", "Compare with hand calculation", "Compare with a multimeter and a scope"]]
table(s, ML, 4.98, CW, 1.85, data, col_w=[1.6, 3.6, 3.6], fsize=10, hsize=10)

# ----------------------------------------------------------------- slide 3
s = content_slide("Problem statement", "Why the hardware phase is needed")

box(s, ML, 1.72, CW, 1.52, fill=PANEL, line=ACCENT)
text(s, ML + 0.32, 1.92, CW - 0.64, 1.22,
     [("\"To transfer the verified 8051 programs from a software model to a physical AT89S52 trainer "
       "board, interfacing LEDs, a seven segment display, a DIP switch bank, a character LCD, an "
       "LM35 temperature sensor with an ADC0804, a MAX232 serial link, a relay and a buzzer, and to "
       "confirm on the bench that each output matches the value predicted by the simulator.\"",
       14.5, LIGHT, False, True)], line_spacing=1.2, space_after=0)

text(s, ML, 3.42, CW, 0.3, [("Difficulties the hardware phase has to solve", 15, TEXT, True)], space_after=0)

items = [
    ("Port shortage", "The peripherals need 54 I/O lines. The 8051 has 32. A shared 8-bit bus with "
                      "latches closes the gap."),
    ("Port 0 is open drain", "It cannot drive a logic 1 without pull-ups, and every bus transfer has "
                             "to respect the resulting rise time."),
    ("No zero flag, no read back", "Output states live in latches, so the firmware keeps a shadow byte "
                                   "for the bus and restores it after every transfer."),
    ("Analog accuracy", "An 8-bit ADC needs a deliberate reference. Vref/2 is trimmed to 1.000 V so "
                        "the LM35 range is used instead of wasted."),
    ("Programming", "P1.5, P1.6 and P1.7 serve both the DIP switches and the SPI programming header, "
                    "so the two must not fight."),
]
yy = 3.80
for i, (h, b) in enumerate(items):
    box(s, ML, yy, 0.30, 0.52, fill=ACCENT, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    text(s, ML, yy + 0.10, 0.30, 0.3, [(str(i + 1), 12, BG, True)], align=PP_ALIGN.CENTER, space_after=0)
    text(s, ML + 0.44, yy + 0.02, 2.6, 0.3, [(h, 12, TEXT, True)], space_after=0)
    text(s, ML + 3.10, yy + 0.02, CW - 3.10, 0.5, [(b, 10.5, MUTED)], line_spacing=1.12, space_after=0)
    yy += 0.62

# ----------------------------------------------------------------- slide 4
s = content_slide("Objectives", "What the hardware phase sets out to do")

objs = [
    ("01", "Build the minimum system",
     "AT89S52 with an 11.0592 MHz crystal, a reset circuit, the EA strap and a regulated 5 V supply, "
     "verified by a 1.843 MHz signal on ALE."),
    ("02", "Solve the port shortage",
     "Put the LCD, the ADC and two output latches on one 8-bit bus so all 32 pins cover every "
     "peripheral on the board."),
    ("03", "Interface real output hardware",
     "Eight LEDs behind a latch, a two digit multiplexed seven segment display, a 16x2 character LCD."),
    ("04", "Interface real input hardware",
     "An eight way DIP switch bank with pull-ups and debouncing, plus two interrupt push buttons on "
     "INT0 and INT1."),
    ("05", "Measure something real",
     "LM35 into an ADC0804 with a calibrated reference, converting raw codes to degrees Celsius and "
     "driving zone decisions."),
    ("06", "Verify against the simulator",
     "Twenty bench tests with acceptance limits, so each hardware result can be compared with the "
     "value the simulator produced."),
]
for i, (n, h, b) in enumerate(objs):
    x = ML + (i % 3) * 4.09
    y = 1.78 + (i // 3) * 2.52
    num_card(s, x, y, 3.85, 2.30, n, h, b)

# ----------------------------------------------------------------- slide 5
s = content_slide("System architecture", "How the board is organised",
                  "One 8-bit bus, four devices behind latches and strobes")

node(s, 5.30, 1.85, 2.72, 1.05, "AT89S52", "40 pin DIP, 11.0592 MHz", fill=RGBColor(0x24, 0x3A, 0x62),
     border=ACCENT, lsize=13)

node(s, 0.95, 1.85, 2.35, 0.72, "P1", "8 DIP switches", border=LIGHT, lsize=11)
node(s, 0.95, 2.78, 2.35, 0.72, "P3.2 / P3.3", "INT0 and INT1", border=LIGHT, lsize=11)
node(s, 0.95, 3.71, 2.35, 0.72, "P3.4 / P3.5", "relay and buzzer", border=LIGHT, lsize=11)
node(s, 0.95, 4.64, 2.35, 0.72, "P0", "shared data bus", border=ACCENT, lsize=11)

node(s, 10.05, 1.85, 2.35, 0.72, "P2.0 / P2.1", "latch enables", border=ACCENT, lsize=11)
node(s, 10.05, 2.78, 2.35, 0.72, "P2.2-P2.4", "LCD E, RS, RW", border=ACCENT, lsize=11)
node(s, 10.05, 3.71, 2.35, 0.72, "P2.5-P2.7", "ADC WR, RD, INTR", border=ACCENT, lsize=11)
node(s, 10.05, 4.64, 2.35, 0.72, "P3.0 / P3.1", "UART to MAX232", border=LIGHT, lsize=11)

box(s, 3.55, 5.40, 6.22, 0.56, fill=PANEL2, line=ACCENT)
text(s, 3.55, 5.50, 6.22, 0.4,
     [("8-bit data bus BD0-BD7, port 0, 10 kOhm pull-ups", 12, LIGHT, True)],
     align=PP_ALIGN.CENTER, space_after=0)

for yy in (2.21, 3.14, 4.07, 5.00):
    arrow(s, 3.30, yy, 5.30, 2.37, color=DIM, width=1.0)
    arrow(s, 5.30, 2.37, 3.30, yy, color=DIM, width=1.0)

arrow(s, 6.66, 2.90, 6.72, 5.40, color=ACCENT, width=1.6)
text(s, 6.80, 3.80, 2.6, 0.3, [("data bus", 9.5, MUTED)], space_after=0)

bus_targets = [
    (3.95, 6.08, "U2 74HC573", "8 LEDs"),
    (6.05, 6.08, "U3 74HC573", "7-segment"),
    (8.15, 6.08, "LCD1 16x2", "HD44780"),
    (10.25, 6.08, "U4 ADC0804", "LM35"),
]
for x, y, a, b in bus_targets:
    node(s, x, y, 1.95, 0.74, a, b, lsize=10.5, ssize=8.5, border=DIM)
    arrow(s, x + 0.97, 5.96, x + 0.97, 6.08, color=ACCENT, width=1.2)

arrow(s, 1.72, 2.57, 2.72, 2.57, color=LIGHT, width=1.0)
arrow(s, 2.72, 2.57, 1.72, 2.57, color=LIGHT, width=1.0)
arrow(s, 10.62, 2.57, 11.62, 2.57, color=LIGHT, width=1.0)
arrow(s, 11.62, 2.57, 10.62, 2.57, color=LIGHT, width=1.0)

# ----------------------------------------------------------------- slide 6
s = content_slide("Design problem", "The 8051 has 32 I/O pins and the board needs 54")

data = [["Peripheral", "Dedicated pins", "After bus sharing", "How the saving is made"],
        ["8 LED output bank", "8", "0", "moves behind latch U2 on the bus"],
        ["7-segment segment lines", "8", "0", "moves behind latch U3 on the bus"],
        ["16x2 LCD", "11", "3", "data lines move to the bus, RS RW E stay"],
        ["ADC0804", "11", "3", "data lines move to the bus, WR RD INTR stay"],
        ["8 way DIP switch", "8", "8", "stays on port 1"],
        ["Digit selects", "2", "2", "stays on P3.6 and P3.7"],
        ["UART", "2", "2", "stays on P3.0 and P3.1"],
        ["Interrupt buttons", "2", "2", "stays on P3.2 and P3.3"],
        ["Relay and buzzer", "2", "2", "stays on P3.4 and P3.5"],
        ["Control strobes", "0", "8", "new: enables on port 2, replace the per-device data pins"],
        ["TOTAL", "54", "32", "exactly the 32 pins the 8051 provides"]]
fills = {(11, 1): RGBColor(0x24, 0x3A, 0x62), (11, 2): RGBColor(0x24, 0x3A, 0x62),
         (11, 0): RGBColor(0x24, 0x3A, 0x62)}
table(s, ML, 1.78, 7.55, 3.9, data, col_w=[2.0, 1.15, 1.25, 3.15], fsize=9.5, hsize=9.5,
      align=["l", "c", "c", "l"], fills=fills)

card(s, ML + 7.85, 1.78, 4.24, 3.9, "Why this works",
     "The LCD, the ADC and the two latches only hold data. None of them needs to be driven "
     "continuously.\n\n"
     "Each one keeps its own enable line on port 2. A transfer writes a byte to port 0 and pulses "
     "exactly one enable, so only the addressed device captures the byte.\n\n"
     "The bus is driven by software rather than by MOVX, which keeps port 2 free for those eight "
     "strobes and keeps the code readable.",
     bsize=10.5, hsize=13)

box(s, ML, 5.88, CW, 0.97, fill=PANEL, line=ACCENT)
text(s, ML + 0.28, 6.02, CW - 0.56, 0.78,
     [("Bus rule used everywhere in the firmware:  ", 12, TEXT, True),
      ("place the byte on P0, pulse the enable, restore the shadow byte. Interrupts are disabled "
       "during LCD and ADC transfers so the 5 ms display refresh cannot corrupt a bus cycle.", 12, MUTED)],
     line_spacing=1.15, space_after=0)

# ----------------------------------------------------------------- slide 7
s = content_slide("Pin allocation", "All 32 pins accounted for",
                  "AT89S52, 40 pin plastic DIP, 11.0592 MHz")

left = [["Pin", "Signal", "Board net"],
        ["39-32", "P0.0-P0.7", "BD0-BD7 shared data bus"],
        ["1-5", "P1.0-P1.4", "SW1-SW5"],
        ["6-8", "P1.5-P1.7", "SW6-SW8 and MOSI, MISO, SCK"],
        ["21", "P2.0", "LED_LE"],
        ["22", "P2.1", "SEG_LE"],
        ["23", "P2.2", "LCD_E"],
        ["24", "P2.3", "LCD_RS"],
        ["25", "P2.4", "LCD_RW"],
        ["26", "P2.5", "ADC_WR"],
        ["27", "P2.6", "ADC_RD"],
        ["28", "P2.7", "ADC_INTR"]]
right = [["Pin", "Signal", "Board net"],
         ["10", "P3.0 RxD", "MAX232 R1OUT"],
         ["11", "P3.1 TxD", "MAX232 T1IN"],
         ["12", "P3.2 INT0", "PB1 emergency button"],
         ["13", "P3.3 INT1", "PB2 mode button"],
         ["14", "P3.4 T0", "relay driver via JP1"],
         ["15", "P3.5 T1", "buzzer driver"],
         ["16", "P3.6 WR", "DIG1 digit select"],
         ["17", "P3.7 RD", "DIG2 digit select"],
         ["9", "RST", "reset RC and PB3, ISP pin 5"],
         ["18", "XTAL2", "crystal and 30 pF"],
         ["19", "XTAL1", "crystal and 30 pF"],
         ["31", "EA/VPP", "tied to +5 V"]]
table(s, ML, 1.78, 5.95, 3.55, left, col_w=[0.85, 1.55, 3.55], fsize=9.5, hsize=9.5, align=["c", "l", "l"])
table(s, ML + 6.14, 1.78, 5.95, 3.55, right, col_w=[0.85, 1.55, 3.55], fsize=9.5, hsize=9.5, align=["c", "l", "l"])

box(s, ML, 5.62, CW, 1.14, fill=PANEL, line=RED)
text(s, ML + 0.28, 5.78, CW - 0.56, 0.9,
     [("Three traps that make a board look dead", 13, AMBER, True),
      ("EA/VPP (pin 31) floating - the device fetches code from external memory and never runs.\n"
       "P0 used without RN1 pull-ups - port 0 is open drain and cannot drive a logic 1.\n"
       "DIP switches 6, 7 and 8 closed while programming - they short the SPI lines on P1.5 to P1.7.",
       10.5, MUTED)], line_spacing=1.2, space_after=3)

# ----------------------------------------------------------------- slide 8
s = content_slide("Minimum system", "Clock, reset, EA strap and decoupling",
                  "Four parts decide whether the board runs at all")

node(s, 0.95, 2.05, 3.30, 3.05, "", fill=PANEL2, border=ACCENT)
text(s, 1.15, 2.22, 2.9, 0.3, [("AT89S52  (U1)", 13, TEXT, True)], align=PP_ALIGN.CENTER, space_after=0)
for i, ln in enumerate(["pin 40  VCC      5.00 V", "pin 20  GND", "pin 31  EA  ->  +5 V",
                        "pin 19  XTAL1", "pin 18  XTAL2", "pin  9  RST", "pin 30  ALE"]):
    text(s, 1.15, 2.66 + i * 0.31, 2.9, 0.28, [(ln, 11, LIGHT)], font=MONO, space_after=0)

data = [["Part", "Value", "Purpose", "Measured"],
        ["Y1 crystal", "11.0592 MHz", "clock; gives exact 9600 baud", "11.0592 MHz on pin 18"],
        ["C3a, C3b", "30 pF", "crystal load capacitors", "-"],
        ["R1", "10 kOhm", "holds RST low in steady state", "-"],
        ["C2", "10 uF", "holds RST high for about 100 ms at power up", "RST low when idle"],
        ["PB3", "tactile", "manual reset to +5 V", "RST above 4 V when held"],
        ["EA strap", "wire to +5 V", "selects internal flash", "5.00 V on pin 31"],
        ["C1", "0.1 uF", "decoupling across pins 40 and 20", "5.00 V, no ripple spike"],
        ["ALE", "output", "clock divided by 6", "1.843 MHz"]]
table(s, 4.65, 1.85, 7.44, 2.55, data, col_w=[1.1, 1.25, 2.85, 2.24], fsize=9.5, hsize=9.5,
      align=["l", "l", "l", "l"])

code_panel(s, 4.65, 4.60, 7.44, 1.28,
           ["machine cycle = 12 oscillator periods",
            "Tcy = 12 / 11.0592 MHz = 1.0851 microseconds",
            "ALE = fosc / 6 = 1.8432 MHz  (fastest proof the device is running)"],
           size=11, title="TIMING")

box(s, 0.95, 5.62, 3.30, 1.16, fill=PANEL, line=AMBER)
text(s, 1.15, 5.78, 2.9, 0.9,
     [("Reset rule", 12, AMBER, True),
      ("RST must stay above 1.2 V for at least two machine cycles, about 2.2 us.\n"
       "The RC gives about 100 ms.", 10, MUTED)], line_spacing=1.15, space_after=3)

# ----------------------------------------------------------------- slide 9
s = content_slide("Shared bus", "How one byte reaches one device",
                  "The four steps every transfer follows, and why the shadow byte exists")

steps = [
    ("1", "Place the byte", "BUS = value; the byte appears on P0.0 to P0.7 and is copied into "
                            "bus_shadow.", ACCENT),
    ("2", "Disable interrupts", "EA = 0, so the 5 ms display refresh cannot overwrite the bus "
                                "half way through.", AMBER),
    ("3", "Pulse the enable", "One strobe line on port 2 goes high for about 2.7 us. Only the device "
                              "wired to that strobe captures the byte.", ACCENT),
    ("4", "Restore the bus", "BUS = bus_shadow, then EA is restored. The other three devices never "
                             "saw a strobe, so they are unaffected.", ACCENT),
]
for i, (n, h, b, col) in enumerate(steps):
    x = ML + i * 3.09
    box(s, x, 1.80, 2.85, 2.30, fill=PANEL)
    box(s, x, 1.80, 2.85, 0.045, col, shape=MSO_SHAPE.RECTANGLE)
    text(s, x + 0.22, 2.00, 0.6, 0.4, [(n, 20, col, True)], space_after=0)
    text(s, x + 0.22, 2.46, 2.45, 0.3, [(h, 12.5, TEXT, True)], space_after=0)
    text(s, x + 0.22, 2.82, 2.45, 1.15, [(b, 10.5, MUTED)], line_spacing=1.15, space_after=0)

code_panel(s, ML, 4.30, 5.95, 2.48,
           ["void led_write(unsigned char v)",
            "{",
            "    unsigned char ea_state;",
            "    ea_state = EA;",
            "    EA = 0;",
            "    bus_put(v);",
            "    LED_LE = 1;",
            "    delay_short();",
            "    LED_LE = 0;",
            "    EA = ea_state;",
            "}"],
           size=9, title="firmware/inc/board.h")

card(s, ML + 6.14, 4.32, 5.95, 2.34, "Why the shadow byte is not optional",
     "Port 0 is quasi-bidirectional and open drain. Reading back a latch output is not possible, so "
     "the last value written is kept in a variable.\n\n"
     "The display refresh interrupt writes segment patterns to the same bus every 5 ms. Without "
     "saving, restoring and gating, an interrupt landing between the byte and the strobe would load "
     "the wrong value into the LED latch and produce visible glitches.\n\n"
     "The same pattern is used by seg_latch, lcd_write and adc_read.",
     bsize=10.5)

# ----------------------------------------------------------------- slide 10
s = content_slide("Output stage", "Eight LED bank behind a 74HC573 latch",
                  "Active high outputs, one current limiting resistor per LED")

node(s, 0.95, 2.20, 2.55, 0.86, "P0 bus", "BD0-BD7", border=ACCENT, lsize=11.5)
arrow(s, 3.50, 2.63, 4.35, 2.63, color=ACCENT, width=1.5)
node(s, 4.35, 1.98, 2.70, 1.30, "U2 74HC573", "LE <- P2.0, OE tied low", border=ACCENT, lsize=12)
arrow(s, 7.05, 2.63, 7.90, 2.63, color=ACCENT, width=1.5)
node(s, 7.90, 1.98, 2.20, 1.30, "RN3", "470 Ohm x 8", border=DIM, lsize=12)
arrow(s, 10.10, 2.63, 10.95, 2.63, color=ACCENT, width=1.5)
node(s, 10.95, 1.98, 1.75, 1.30, "8 LEDs", "to GND", border=DIM, lsize=12)

data = [["Parameter", "Value", "Reason"],
        ["Latch type", "74HC573", "transparent latch, CMOS inputs suit the port 0 pull-ups"],
        ["Latch enable", "P2.0", "rising edge captures the byte"],
        ["Output enable", "tied to GND", "outputs permanently valid"],
        ["Series resistor", "470 Ohm", "8 x 6.6 mA = 53 mA, inside the 70 mA package limit"],
        ["Resistor not used", "330 Ohm", "would give 75 mA and exceed the package rating"],
        ["LED polarity", "active high", "latch output high lights the LED"]]
table(s, 0.95, 3.62, 7.55, 2.10, data, col_w=[1.9, 1.6, 4.05], fsize=10, hsize=10, align=["l", "l", "l"])

card(s, ML + 7.85, 3.62, 4.24, 3.00, "Current arithmetic",
     "I per LED = (5.0 - 1.9) / 470 = 6.6 mA\n"
     "I per package = 8 x 6.6 = 53 mA\n"
     "74HC573 package limit = 70 mA\n\n"
     "Headroom = 17 mA, which is why 470 Ohm is specified instead of the more usual 330 Ohm. "
     "Brightness at 6.6 mA is ample for a modern high efficiency indicator.",
     bsize=10.5)

code_panel(s, 0.95, 5.92, 7.55, 0.96,
           ["led_write(0x0F);   /* lower four LEDs on   */",
            "led_write(0xF0);   /* upper four LEDs on   */"],
           size=10.5)

# ----------------------------------------------------------------- slide 11
s = content_slide("Display stage", "Two digit seven segment display",
                  "Latched segments, transistor switched digits, 100 Hz refresh")

node(s, 0.95, 1.95, 2.35, 0.80, "P0 bus", "BD0-BD7", border=ACCENT, lsize=11)
arrow(s, 3.30, 2.35, 4.05, 2.35, color=ACCENT, width=1.5)
node(s, 4.05, 1.75, 2.50, 1.20, "U3 74HC573", "LE <- P2.1", border=ACCENT, lsize=11.5)
arrow(s, 6.55, 2.35, 7.30, 2.35, color=ACCENT, width=1.5)
node(s, 7.30, 1.75, 2.10, 1.20, "RN4 470 Ohm", "a b c d e f g dp", border=DIM, lsize=11.5)
arrow(s, 9.40, 2.35, 10.10, 2.35, color=ACCENT, width=1.5)
node(s, 10.10, 1.75, 2.30, 1.20, "DSP1", "2 digit common cathode", border=DIM, lsize=11.5)

text(s, 0.95, 3.20, 6.0, 0.3, [("Digit cathodes", 13, TEXT, True)], space_after=0)
node(s, 0.95, 3.55, 1.85, 0.72, "Q1 BC547", "digit 1", border=LIGHT, lsize=10.5)
node(s, 3.05, 3.55, 1.85, 0.72, "Q2 BC547", "digit 2", border=LIGHT, lsize=10.5)
text(s, 0.95, 4.40, 6.0, 0.5,
     [("Bases via 4.7 kOhm from P3.6 and P3.7. Emitters to GND. A logic 1 on the base pulls the digit "
       "cathode to ground and lights that digit.", 10.5, MUTED)], line_spacing=1.15, space_after=0)

data = [["Digit", "Pattern", "Digit", "Pattern", "Note"],
        ["0", "3FH", "5", "6DH", "Q0 = a"],
        ["1", "06H", "6", "7DH", "Q1 = b"],
        ["2", "5BH", "7", "07H", "Q2 = c"],
        ["3", "4FH", "8", "7FH", "Q3 = d"],
        ["4", "66H", "9", "6FH", "Q4 = e"]]
table(s, 7.30, 3.20, 5.10, 2.05, data, col_w=[0.8, 0.9, 0.8, 0.9, 1.7], fsize=10, hsize=10,
      align=["c", "c", "c", "c", "c"])

box(s, 0.95, 5.30, 11.45, 1.50, fill=PANEL, line=ACCENT)
text(s, 1.18, 5.46, 11.0, 1.2,
     [("Multiplexing", 13, TEXT, True),
      ("Timer 0 interrupts every 5 ms. The service routine turns both digits off, latches the digit 1 "
       "pattern, raises P3.6, and on the next interrupt does the same for digit 2 with P3.7.", 11, MUTED),
      ("Refresh rate per digit = 1 / (2 x 5 ms) = 100 Hz, above the flicker fusion limit.", 11, ACCENT, True),
      ("Reload value: 65536 - 4608 = 60928 = EE00H, so TH0 = EEH and TL0 = 00H.", 11, LIGHT)],
     line_spacing=1.18, space_after=3)

# ----------------------------------------------------------------- slide 12
s = content_slide("Input stage", "DIP switches, pull-ups and interrupt buttons",
                  "Every input is active low, so a closed switch reads as zero")

card(s, ML, 1.80, 5.95, 2.55, "Eight way DIP switch on port 1",
     "Each contact pulls its pin to ground through the switch. RN2, a 10 kOhm x 9 SIP network, "
     "pulls every pin back to +5 V when the switch is open.\n\n"
     "Closed reads 0, open reads 1. Port 1 has internal pull-ups, so the board would work without "
     "RN2, but the external network makes the input immune to noise on long breadboard wires.\n\n"
     "P1.5, P1.6 and P1.7 have 1 kOhm series resistors so a closed switch cannot fight the ISP "
     "programmer during flashing.", bsize=10.5)

card(s, ML + 6.14, 1.80, 5.95, 2.55, "Interrupt push buttons",
     "PB1 on P3.2 (INT0) and PB2 on P3.3 (INT1), each pulled up by 4.7 kOhm and switching to ground.\n\n"
     "TCON is set with IT0 = 1 and IT1 = 1 so the 8051 detects the falling edge, giving one interrupt "
     "per press.\n\n"
     "The service routines only set a flag. All the work is done in the main loop, which keeps the "
     "interrupt short and makes the behaviour easy to reason about.", bsize=10.5)

text(s, ML, 4.56, CW, 0.3, [("Debouncing", 15, TEXT, True)], space_after=0)

code_panel(s, ML, 4.94, 5.95, 1.72,
           ["unsigned char switch_read(void)",
            "{",
            "    unsigned char a, b;",
            "    a = SWITCH;",
            "    do { delay_ms(5); b = SWITCH; } while (b != a);",
            "    return b;",
            "}"],
           size=10)

card(s, ML + 6.14, 4.94, 5.95, 1.72, "Why 5 ms",
     "A mechanical contact bounces for 1 to 10 ms. Sampling every 5 ms until two consecutive reads "
     "agree removes the bounce without slowing the response, because the whole loop finishes in one "
     "or two samples.", bsize=10.5)

# ----------------------------------------------------------------- slide 13
s = content_slide("Analog input", "LM35 temperature sensor with an ADC0804",
                  "Vref/2 trimmed to 1.000 V so the sensor range is used, not wasted")

node(s, 0.95, 2.05, 2.30, 0.92, "LM35", "10 mV per degree C", border=DIM, lsize=11.5)
arrow(s, 3.25, 2.51, 4.05, 2.51, color=ACCENT, width=1.5)
node(s, 4.05, 1.80, 2.55, 1.42, "ADC0804", "Vin+ pin 6, Vin- to GND", border=ACCENT, lsize=12)
arrow(s, 6.60, 2.51, 7.45, 2.51, color=ACCENT, width=1.5)
node(s, 7.45, 1.80, 2.30, 1.42, "P0 bus", "DB0-DB7", border=ACCENT, lsize=12)
arrow(s, 9.75, 2.51, 10.60, 2.51, color=ACCENT, width=1.5)
node(s, 10.60, 1.80, 1.80, 1.42, "8051", "adc_read()", border=ACCENT, lsize=12)

text(s, 0.95, 3.46, 2.30, 0.22, [("control", 10, MUTED, True)], align=PP_ALIGN.CENTER, space_after=0)
text(s, 0.95, 3.74, 2.30, 0.9,
     [("WR   P2.5", 10, LIGHT), ("RD   P2.6", 10, LIGHT), ("INTR P2.7", 10, LIGHT)],
     font=MONO, line_spacing=1.2, space_after=0)

data = [["Quantity", "Value", "Note"],
        ["Vref/2 (pin 9)", "1.000 V", "set with the R8 trimpot, not left open"],
        ["Full scale input", "2.000 V", "twice the reference voltage"],
        ["Step size", "7.8125 mV", "2.000 V / 256"],
        ["Temperature per step", "0.781 degree C", "7.8125 mV / (10 mV per degree C)"],
        ["Transfer function", "T = raw x 25 / 32", "integer arithmetic, no float library"],
        ["Range", "0 to 199.2 degree C", "well past anything the LM35 sees in a lab"],
        ["Clock", "606 kHz", "1 / (1.1 x 10 kOhm x 150 pF)"],
        ["Conversion time", "about 114 us", "66 to 73 clock periods"],
        ["LM35 output at 30 C", "300 mV", "raw code 38, displayed 29"]]
table(s, 3.55, 3.48, 8.85, 2.72, data, col_w=[2.3, 2.2, 4.35], fsize=10, hsize=10, align=["l", "l", "l"])

box(s, 0.95, 5.42, 5.35, 1.40, fill=PANEL, line=ACCENT)
text(s, 1.15, 5.58, 4.95, 1.1,
     [("Read sequence", 12.5, TEXT, True),
      ("Pulse WR low to start. Wait for INTR to go high, then low. Drive RD low, read the byte, "
       "release RD.", 10.5, MUTED)], line_spacing=1.15, space_after=3)

box(s, 6.65, 5.42, 5.75, 1.40, fill=PANEL, line=AMBER)
text(s, 6.85, 5.58, 5.35, 1.1,
     [("Why not leave Vref/2 open", 12.5, AMBER, True),
      ("An open pin selects the internal 2.5 V reference, giving 0 to 5 V full scale. The LM35 only "
       "reaches 1.5 V at 150 C, so more than two thirds of the range would be wasted and the "
       "resolution would be 1.95 degrees C instead of 0.78.", 10.5, MUTED)],
     line_spacing=1.15, space_after=3)

# ----------------------------------------------------------------- slide 14
s = content_slide("Text output", "16x2 character LCD on the shared bus",
                  "HD44780 compatible module in 8-bit mode, three control lines")

data = [["LCD pin", "Name", "Connected to", "Function"],
        ["1", "VSS", "GND", "ground"],
        ["2", "VDD", "+5 V", "logic supply, 0.1 uF to ground"],
        ["3", "VO", "R9 wiper", "contrast, about 0.5 to 1.0 V"],
        ["4", "RS", "P2.3", "0 = command, 1 = character data"],
        ["5", "RW", "P2.4", "0 = write, 1 = read"],
        ["6", "E", "P2.2", "enable, data taken on the falling edge"],
        ["7-14", "D0-D7", "BD0-BD7", "8-bit data on the shared bus"],
        ["15", "A", "+5 V via 220 Ohm", "backlight anode"],
        ["16", "K", "GND", "backlight cathode"]]
table(s, ML, 1.80, 7.35, 3.10, data, col_w=[0.9, 0.8, 1.9, 3.75], fsize=10, hsize=10,
      align=["c", "l", "l", "l"])

code_panel(s, ML + 7.55, 1.80, 4.54, 3.10,
           ["lcd_cmd(0x38);   /* 8-bit, 2 lines, 5x7  */",
            "lcd_cmd(0x0C);   /* display on, cursor off*/",
            "lcd_cmd(0x06);   /* increment on write    */",
            "lcd_cmd(0x01);   /* clear display         */",
            "lcd_gotoxy(0, 0);",
            "lcd_string(\"8051 HARDWARE\");"],
           size=10, title="INITIALISATION")

box(s, ML, 5.10, CW, 1.72, fill=PANEL, line=ACCENT)
text(s, ML + 0.28, 5.28, CW - 0.56, 1.4,
     [("Timing and the shared bus", 13, TEXT, True),
      ("The enable pulse stays high for about 8 machine cycles, roughly 8.7 us, far above the 450 ns "
       "minimum the HD44780 needs. Commands wait 2 ms afterwards so the clear and home instructions "
       "can complete.", 11, MUTED),
      ("Because the data pins sit on the shared bus, lcd_write brackets the transfer the same way as "
       "every other driver: save, write, strobe, restore, with interrupts disabled.", 11, MUTED),
      ("RW is driven from P2.4 so the busy flag can be polled. The shipped driver uses fixed delays "
       "instead, so RW may be tied to ground to free one pin.", 11, LIGHT)],
     line_spacing=1.18, space_after=3)

# ----------------------------------------------------------------- slide 15
s = content_slide("Serial link", "MAX232 and DB9 at 9600 baud",
                  "The reason the board uses 11.0592 MHz instead of 12 MHz")

data = [["MAX232 pin", "Name", "Connected to"],
        ["1, 3", "C1+ , C1-", "C7a, 1 uF"],
        ["4, 5", "C2+ , C2-", "C7b, 1 uF"],
        ["2", "V+", "C7c to +5 V, not to ground"],
        ["6", "V-", "C7d, positive leg to ground"],
        ["11", "T1IN", "P3.1 TxD"],
        ["12", "R1OUT", "P3.0 RxD"],
        ["13", "R1IN", "DB9 pin 3"],
        ["14", "T1OUT", "DB9 pin 2"],
        ["15, 16", "GND, VCC", "ground and +5 V"]]
table(s, ML, 1.80, 5.55, 3.00, data, col_w=[1.35, 1.5, 2.7], fsize=10, hsize=10, align=["l", "l", "l"])

code_panel(s, ML + 5.75, 1.80, 6.34, 1.34,
           ["TH1 = 256 - (11059200 / (384 x 9600))",
            "    = 256 - 3 = 253 = 0xFD",
            "SMOD = 0, timer 1 in mode 2"],
           size=10.5, title="BAUD RATE")

card(s, ML + 5.75, 3.30, 6.34, 1.56, "DB9 wiring",
     "The board connector is wired as DCE: T1OUT to pin 2 and R1IN to pin 3, so a straight through "
     "cable works with a USB to RS-232 adapter. If the terminal shows nothing, swap pins 2 and 3 "
     "first, then check that V+ is about +9 V and V- about -9 V.", bsize=10.5)

box(s, ML, 4.98, 5.55, 1.86, fill=PANEL, line=ACCENT)
text(s, ML + 0.26, 5.14, 5.05, 1.6,
     [("Configuration", 13, TEXT, True),
      ("SCON = 0x50   mode 1, 8 data bits, receive enabled", 10.5, LIGHT),
      ("TMOD         timer 1 in mode 2, 8-bit auto reload", 10.5, LIGHT),
      ("PCON         SMOD cleared", 10.5, LIGHT),
      ("Error        0.0 percent at 11.0592 MHz", 10.5, ACCENT, True),
      ("Error        8.5 percent at 12 MHz, which fails", 10.5, RED, True)],
     font=MONO, line_spacing=1.2, space_after=3)

code_panel(s, ML + 5.75, 4.98, 6.34, 1.86,
           ["T=28.1C ADC=36 ZONE=SAFE FAN=0 BUZ=0",
            "T=41.4C ADC=53 ZONE=WARNING FAN=1 BUZ=0",
            "T=72.6C ADC=93 ZONE=DANGER FAN=1 BUZ=1",
            "T=72.6C ADC=93 ZONE=EMERGENCY FAN=0 BUZ=1"],
           size=10.5, title="TELEMETRY AT 9600 8N1")

# ----------------------------------------------------------------- slide 16
s = content_slide("Power", "Regulated 5 V and the current budget",
                  "A 7805, its heatsink, and knowing how much current the board really draws")

data = [["Load", "Typical", "Maximum"],
        ["AT89S52 at 11.0592 MHz", "25 mA", "30 mA"],
        ["U2 latch plus 8 LEDs", "53 mA", "53 mA"],
        ["U3 latch plus one display digit", "53 mA", "53 mA"],
        ["16x2 LCD logic and backlight", "10 mA", "14 mA"],
        ["ADC0804", "3 mA", "5 mA"],
        ["MAX232", "10 mA", "15 mA"],
        ["LM35", "0.1 mA", "0.2 mA"],
        ["Transistor base currents", "3 mA", "4 mA"],
        ["Relay coil when energised", "0 mA", "70 mA"],
        ["Buzzer when sounding", "0 mA", "30 mA"],
        ["TOTAL", "157 mA", "274 mA"]]
fills = {(11, 0): RGBColor(0x24, 0x3A, 0x62), (11, 1): RGBColor(0x24, 0x3A, 0x62),
         (11, 2): RGBColor(0x24, 0x3A, 0x62)}
table(s, ML, 1.80, 6.55, 3.35, data, col_w=[3.6, 1.45, 1.5], fsize=10, hsize=10,
      align=["l", "r", "r"], fills=fills)

card(s, ML + 6.75, 1.80, 5.34, 1.62, "Regulator dissipation",
     "P = (Vin - Vout) x I = (9 - 5) x 0.25 = 1.0 W\n\n"
     "One watt in a TO-220 without a heatsink runs hot enough to drop out. HS1 is not optional.",
     bsize=10.5)

card(s, ML + 6.75, 3.56, 5.34, 1.59, "Decoupling",
     "C1 0.1 uF across pins 40 and 20 of the microcontroller, plus one 0.1 uF capacitor at each of "
     "U2, U3, U4, U5, the LCD and the ADC. Ceramic, short leads, physically close to the pins.",
     bsize=10.5)

box(s, ML, 5.34, CW, 1.48, fill=PANEL, line=ACCENT)
text(s, ML + 0.28, 5.50, CW - 0.56, 1.2,
     [("Supply chain", 13, TEXT, True),
      ("J1 barrel jack, 7 to 12 V in, centre positive   ->   1N4007 reverse protection   ->   "
       "C4 100 uF and 0.1 uF   ->   L7805 with heatsink   ->   C5 100 uF and 0.1 uF   ->   5 V rail",
       11, LIGHT),
      ("A 500 mA adapter is comfortable. Below 7 V input the 7805 drops out of regulation; above "
       "12 V the dissipation becomes the limiting factor, not the current.", 11, MUTED)],
     line_spacing=1.18, space_after=3)

# ----------------------------------------------------------------- slide 17
s = content_slide("Bill of materials", "Parts, quantities and cost",
                  "Indicative Indian retail rates, 2025-26 academic year")

data = [["Category", "Line items", "Cost (INR)"],
        ["Semiconductors and ICs", "AT89S52, two 74HC573, ADC0804, MAX232, LM35, 7805", "397"],
        ["Discretes", "four BC547, two 1N4007, nine LEDs", "21"],
        ["Displays, modules, actuators", "16x2 LCD, 2-digit display, 5 V relay, buzzer", "275"],
        ["Switches and buttons", "8-way DIP switch, three tactile buttons", "39"],
        ["Resistors and networks", "four SIP networks, nine resistors, trimpot, pot", "82"],
        ["Capacitors", "crystal loads, electrolytics, ceramics, 1 uF pump caps", "35"],
        ["Crystal", "11.0592 MHz", "12"],
        ["Sockets, connectors, jumpers", "IC sockets, DC jack, DB9, ISP header, terminals", "124"],
        ["Power, PCB, wire, programmers", "adapter, dot PCB, hookup wire, USBasp, USB-RS232", "730"],
        ["TOTAL, one complete setup", "", "1,715"],
        ["Recurring cost of a second board", "the adapter and programmers are reused", "985"]]
fills = {(9, 2): RGBColor(0x24, 0x3A, 0x62), (9, 0): RGBColor(0x24, 0x3A, 0x62),
         (10, 2): RGBColor(0x24, 0x3A, 0x62), (10, 0): RGBColor(0x24, 0x3A, 0x62)}
table(s, ML, 1.80, 8.30, 3.55, data, col_w=[3.5, 6.2, 1.5], fsize=10, hsize=10,
      align=["l", "l", "r"], fills=fills)

card(s, ML + 8.50, 1.80, 3.59, 3.55, "Sourcing notes",
     "AT89S52 over AT89C51: SPI programming with a 250 rupee USBasp instead of a parallel programmer "
     "costing several thousand.\n\n"
     "74HC573 over 74LS573: CMOS inputs suit port 0 pull-ups and load the bus less.\n\n"
     "MAX232A or MAX3232 may be substituted with 0.1 uF pump capacitors.\n\n"
     "The display must be common cathode; a common anode part inverts the whole design.",
     bsize=10)

box(s, ML, 5.55, CW, 1.27, fill=PANEL, line=ACCENT)
text(s, ML + 0.28, 5.72, CW - 0.56, 1.0,
     [("What is not on the bill", 13, TEXT, True),
      ("A digital multimeter and, ideally, a 20 MHz oscilloscope for the four tests that need one. "
       "Both are standard laboratory instruments and are shared across the batch.", 11, MUTED),
      ("A reference thermometer for calibrating the LM35 against a known temperature.", 11, MUTED)],
     line_spacing=1.18, space_after=3)

# ----------------------------------------------------------------- slide 18
s = content_slide("Firmware architecture", "One header, thirteen programs",
                  "firmware/inc/board.h holds every pin definition and driver")

node(s, 5.05, 1.85, 3.20, 0.85, "src/01 .. src/13", "one file per program", border=ACCENT, lsize=12)
arrow(s, 6.65, 2.70, 6.65, 3.20, color=ACCENT, width=1.5)
node(s, 3.35, 3.20, 6.60, 0.95, "inc/board.h", "pin definitions, bus and peripheral drivers",
     fill=RGBColor(0x24, 0x3A, 0x62), border=ACCENT, lsize=13)

layers = [
    ("Hardware layer", "bus_put, led_write, seg_latch, seg_tick", "moves bytes and strobes the enables"),
    ("Peripheral layer", "lcd_init, lcd_string, adc_read, uart_string", "device protocols and timing"),
    ("Conversion layer", "adc_to_celsius, seg_number, uart_number, lcd_number", "raw values to human units"),
    ("Application layer", "main and the interrupt service routines", "what each program actually does"),
]
yy = 4.28
for i, (h, b, note) in enumerate(layers):
    box(s, ML, yy, 3.05, 0.58, fill=PANEL)
    text(s, ML + 0.18, yy + 0.07, 2.75, 0.26, [(h, 11.5, TEXT, True)], space_after=0)
    text(s, ML + 0.18, yy + 0.31, 2.75, 0.24, [(note, 8.5, DIM)], space_after=0)
    box(s, ML + 3.25, yy, 8.84, 0.58, fill=PANEL2)
    text(s, ML + 3.45, yy + 0.18, 8.44, 0.3, [(b, 10.5, LIGHT)], font=MONO, space_after=0)
    yy += 0.65

text(s, ML, 1.95, 3.0, 0.3, [("Design rules", 13, TEXT, True)], space_after=0)
box(s, ML, 2.30, 2.85, 2.30, fill=PANEL, line=DIM)
text(s, ML + 0.20, 2.46, 2.45, 2.0,
     [("No comments in the sources", 10.5, TEXT),
      ("No emojis anywhere", 10.5, TEXT),
      ("C89 declarations only", 10.5, TEXT),
      ("Keil keywords: sbit, code, interrupt N", 10.5, TEXT),
      ("No printf, no floating point", 10.5, TEXT),
      ("Each program is one translation unit", 10.5, TEXT)],
     line_spacing=1.24, space_after=3)

# ----------------------------------------------------------------- slide 19
s = content_slide("Program library", "Thirteen Keil C51 programs",
                  "Each builds as its own target and fits inside the 8 KB flash of the AT89S52")

data = [["#", "Program", "Peripherals exercised", "What to observe", "Size"],
        ["01", "led_blink", "LED latch", "eight LEDs toggle every 500 ms", "1.1 KB"],
        ["02", "led_patterns", "LED latch", "running light, AAH, 55H, blink", "1.2 KB"],
        ["03", "switch_led", "DIP switches, LEDs", "LEDs follow switches, flash above 80H", "1.2 KB"],
        ["04", "seg7_counter", "7-segment, digits", "00 to 99 at two counts per second", "1.3 KB"],
        ["05", "timer0_second", "timer 0", "one second blink from the interrupt", "1.2 KB"],
        ["06", "square_wave", "timer 0, P3.4", "1.00 kHz on a scope, JP1 removed", "1.1 KB"],
        ["07", "ext_interrupt", "INT0, INT1", "PB1 alternates 0FH and F0H, PB2 counts", "1.3 KB"],
        ["08", "uart_echo", "UART, MAX232", "banner and character echo", "1.4 KB"],
        ["09", "uart_commands", "UART, relay, buzzer", "HLP, LED HH, SEG NN, RLY N, TMP", "3.0 KB"],
        ["10", "adc_7seg", "ADC0804, LM35", "temperature on the display", "1.5 KB"],
        ["11", "adc_lcd", "ADC, LCD", "temperature and bar graph", "2.0 KB"],
        ["12", "industrial_monitor", "everything", "zones, relay, buzzer, telemetry", "3.4 KB"],
        ["13", "selftest", "everything", "PASS or FAIL report on the terminal", "2.6 KB"]]
table(s, ML, 1.80, CW, 4.05, data, col_w=[0.5, 1.9, 2.4, 5.3, 0.9],
      fsize=9.5, hsize=9.5, align=["c", "l", "l", "l", "r"])

box(s, ML, 6.00, CW, 0.85, fill=PANEL, line=ACCENT)
text(s, ML + 0.28, 6.14, CW - 0.56, 0.66,
     [("Verification:  ", 11.5, TEXT, True),
      ("all thirteen compiled with zero errors and zero warnings. The largest, program 12, uses about "
       "40 percent of the flash and about 30 bytes of internal RAM.", 11.5, MUTED)],
     line_spacing=1.15, space_after=0)

# ----------------------------------------------------------------- slide 20
s = content_slide("Firmware timing", "Every constant the programs depend on",
                  "All derived from one number: the 1.0851 microsecond machine cycle")

data = [["Function", "Register setting", "Derivation", "Result"],
        ["UART 9600 baud", "TH1 = TL1 = FDH", "256 - 11059200 / (384 x 9600) = 253", "0.00 percent error"],
        ["Display refresh 5 ms", "TH0 = EEH, TL0 = 00H", "65536 - 5000 / 1.0851 = 60928", "100 Hz per digit"],
        ["50 ms tick", "TH0 = 4CH, TL0 = 00H", "65536 - 50000 / 1.0851 = 19456", "20 ticks = 1 s"],
        ["1 kHz output", "TH0 = FEH, TL0 = 34H", "65536 - 500 / 1.0851 = 65076", "1001.7 Hz"],
        ["Bus strobe width", "8 NOPs", "8 x 1.0851 us", "8.7 us, above all minimums"],
        ["LCD command wait", "delay_ms(2)", "calibrated DJNZ loop", "covers clear and home"],
        ["Switch debounce", "delay_ms(5)", "two consecutive equal samples", "1 to 10 ms bounce removed"],
        ["LM35 conversion", "T = raw x 25 / 32", "raw x 7.8125 mV / 10 mV", "0.78 degree C per step"]]
table(s, ML, 1.80, CW, 3.10, data, col_w=[2.1, 2.3, 4.0, 2.6], fsize=10, hsize=10,
      align=["l", "l", "l", "l"])

code_panel(s, ML, 4.98, 5.95, 1.90,
           ["void timer0_isr(void) interrupt 1",
            "{",
            "    TH0 = TH0_5MS;      /* EEH  */",
            "    TL0 = TL0_5MS;      /* 00H  */",
            "    seg_tick();",
            "    ms_ticks++;",
            "}"],
           size=10, title="DISPLAY REFRESH INTERRUPT")

card(s, ML + 6.14, 4.98, 5.95, 1.90, "Calibration note",
     "delay_ms is written for 11.0592 MHz and assumes the loop compiles to a DJNZ. Verify it once by "
     "timing program 05, which uses the hardware timer, against program 01, which uses delay_ms. If "
     "they disagree, trim the two literal 250 values in delay_1ms and leave the timer reloads alone.",
     bsize=10.5)

# ----------------------------------------------------------------- slide 21
s = content_slide("Build procedure", "Ten stages, each with a pass measurement",
                  "Nothing is wired on top of a stage that has not been measured")

data = [["Stage", "What is built", "Measurement that must pass"],
        ["1", "Power: jack, 1N4007, 7805, capacitors", "5.00 V plus or minus 0.15 V at the regulator output"],
        ["2", "Minimum system: socket, crystal, reset, EA", "1.843 MHz on ALE, RST below 0.5 V when idle"],
        ["3", "LED latch U2 and the eight LEDs", "all eight blink at 1 Hz, 6 to 7 mA each"],
        ["4", "DIP switch bank and pull-ups", "P1 reads FFH open, FEH with switch 1 closed"],
        ["5", "Segment latch, display, digit transistors", "counts 00 to 99 in about 50 s"],
        ["6", "MAX232, pump capacitors, DB9", "banner on the terminal, V+ about +9 V"],
        ["7", "ADC0804, LM35, reference trimpot", "pin 9 at 1.000 V, about 606 kHz on pin 4"],
        ["8", "16x2 LCD and contrast pot", "temperature text and a growing bar graph"],
        ["9", "Relay, buzzer, driver transistors, JP1", "relay clicks at 40 C, buzzer above 70 C"],
        ["10", "Final checkout with the self test", "every line OK, final line SELF TEST: PASS"]]
table(s, ML, 1.80, 8.10, 4.15, data, col_w=[0.7, 3.3, 4.1], fsize=10, hsize=10,
      align=["c", "l", "l"])

card(s, ML + 8.30, 1.80, 3.79, 4.15, "Order matters",
     "Power first and alone. If the regulator is wrong, everything downstream is wrong.\n\n"
     "The minimum system second, because ALE proves the device is running before any peripheral "
     "complicates the diagnosis.\n\n"
     "Outputs before inputs, because an LED is the quickest way to see a state.\n\n"
     "The ADC after the serial link, because the reference voltage is set and checked with the "
     "terminal connected.\n\n"
     "Transfer to a soldered dot PCB only after the breadboard passes every test.",
     bsize=10)

# ----------------------------------------------------------------- slide 22
s = content_slide("Verification", "Twenty bench tests with acceptance limits",
                  "A test passes only when the measured value is inside the stated limit")

data = [["#", "Test", "Expected", "#", "Test", "Expected"],
        ["T1", "Power on self test", "every line OK, PASS", "T11", "LM35 accuracy", "within 1.5 C, 25 to 60 C"],
        ["T2", "Supply rails", "5.00 V plus or minus 0.15 V", "T12", "LCD bar graph", "increases monotonically"],
        ["T3", "LED timing", "20 half cycles in 10.0 s", "T13", "Zone thresholds", "green, then 40 C, then 70 C"],
        ["T4", "DIP switch input", "correct LED within 10 ms", "T14", "Relay control", "energises at 40.0 C"],
        ["T5", "Counter 00 to 99", "50 s plus or minus 2 s", "T15", "Emergency stop", "relay off, buzzer on"],
        ["T6", "One second timing", "10 transitions in 10.0 s", "T16", "Emergency reset", "returns to zone control"],
        ["T7", "Square wave", "1.00 kHz plus or minus 20 Hz", "T17", "Telemetry rate", "10 lines in 10 s"],
        ["T8", "External interrupts", "no double triggering", "T18", "Current", "below 200 mA"],
        ["T9", "Serial loopback", "every byte echoed", "T19", "Regulator thermals", "below about 60 C"],
        ["T10", "Command shell", "HLP, LED FF, RLY 1 all work", "T20", "Supply rejection", "5 V holds, 7 V to 12 V"]]
table(s, ML, 1.80, CW, 3.35, data, col_w=[0.45, 1.75, 2.55, 0.45, 1.75, 2.55], fsize=9.5, hsize=9.5,
      align=["c", "l", "l", "c", "l", "l"])

box(s, ML, 5.32, 5.95, 1.52, fill=PANEL, line=ACCENT)
text(s, ML + 0.26, 5.48, 5.45, 1.25,
     [("Calibration of the reference", 12.5, TEXT, True),
      ("Adjust R8 until ADC0804 pin 9 reads exactly 1.000 V. Confirm the transfer function against "
       "two temperatures at least 20 degrees apart. If both readings are off by the same factor, R8 "
       "has drifted; if only one is off, the LM35 is picking up noise.", 10.5, MUTED)],
     line_spacing=1.16, space_after=3)

box(s, ML + 6.14, 5.32, 5.95, 1.52, fill=PANEL, line=AMBER)
text(s, ML + 6.40, 5.45, 5.45, 1.25,
     [("Known limitation", 12.5, AMBER, True),
      ("Resolution is 0.78 degree C and accuracy is about plus or minus 1.5 degree C. That is "
       "entirely adequate for switching zones at 40 and 70 degrees, and is not a metrology grade "
       "measurement. The limitation is the 8-bit converter, not the sensor.", 10.5, MUTED)],
     line_spacing=1.16, space_after=3)

# ----------------------------------------------------------------- slide 23
s = content_slide("Results", "What the board reports on the bench",
                  "Terminal capture at 9600 8N1, and the self test run")

code_panel(s, ML, 1.80, 6.55, 2.30,
           ["8051 ZONE MONITOR 9600 8N1",
            "T=28.1C ADC=36 ZONE=SAFE FAN=0 BUZ=0",
            "T=28.1C ADC=36 ZONE=SAFE FAN=0 BUZ=0",
            "T=41.4C ADC=53 ZONE=WARNING FAN=1 BUZ=0",
            "T=64.0C ADC=82 ZONE=WARNING FAN=1 BUZ=0",
            "T=72.6C ADC=93 ZONE=DANGER FAN=1 BUZ=1"],
           size=10.5, title="PROGRAM 12 TELEMETRY, ONE LINE PER SECOND")

code_panel(s, ML + 6.74, 1.80, 5.35, 2.30,
           ["8051 HARDWARE LAB",
            "POWER ON SELF TEST",
            "",
            "LED BANK      : OK",
            "7 SEGMENT     : OK",
            "RELAY DRIVER  : OK"],
           size=10.5, title="PROGRAM 13 SELF TEST")

data = [["Check", "Raw code", "T = raw x 25 / 32", "Zone", "Action"],
        ["Room temperature", "36", "28.1 C", "SAFE", "green LED, fan off"],
        ["Warmed by hand", "53", "41.4 C", "WARNING", "yellow LED, fan on"],
        ["Near a heat source", "82", "64.0 C", "WARNING", "yellow LED, fan on"],
        ["Above the threshold", "93", "72.6 C", "DANGER", "red LED, fan on, buzzer on"],
        ["PB1 pressed", "93", "72.6 C", "EMERGENCY", "fan off, buzzer on, latched"]]
table(s, ML, 4.30, CW, 1.85, data, col_w=[2.4, 1.2, 1.9, 2.2, 3.4], fsize=10, hsize=10,
      align=["l", "c", "c", "c", "l"])

box(s, ML, 6.32, CW, 0.52, fill=PANEL, line=ACCENT)
text(s, ML + 0.26, 6.42, CW - 0.52, 0.35,
     [("Every printed pair satisfies the transfer function, which is the arithmetic link between the "
       "analog hardware and the digital output.", 11, LIGHT)],
     line_spacing=1.15, space_after=0)

# ----------------------------------------------------------------- slide 24
s = content_slide("Design decisions", "Trade-offs made, and why")

data = [["Decision", "Alternative considered", "Why this one was chosen"],
        ["AT89S52 with ISP", "AT89C51 with a parallel programmer", "programmed with a 250 rupee USBasp; the C51 needs hardware costing several thousand"],
        ["Software driven bus", "MOVX with an address latch and decoder", "port 2 stays free for eight strobes and the code stays readable for teaching"],
        ["74HC573 latches", "74LS573 or 74HC373", "CMOS inputs suit the port 0 pull-ups and load the bus less"],
        ["470 Ohm LED resistors", "the usual 330 Ohm", "keeps the package current at 53 mA, inside the 70 mA limit"],
        ["Vref/2 at 1.000 V", "internal 2.5 V reference", "0.78 degree C per step instead of 1.95, using the LM35 range properly"],
        ["Software debounce", "RC filter or a Schmitt trigger", "no extra parts, and the pin count has no spares left"],
        ["Common cathode display", "common anode", "NPN transistors switching ground are the simpler driver"],
        ["Flags in the ISRs", "doing the work inside the ISR", "short service routines, predictable timing, behaviour easy to follow"],
        ["11.0592 MHz crystal", "12 MHz", "zero percent baud error instead of 8.5 percent"]]
table(s, ML, 1.80, CW, 4.30, data, col_w=[2.5, 3.3, 6.3], fsize=9.5, hsize=9.5,
      align=["l", "l", "l"])

box(s, ML, 6.28, CW, 0.56, fill=PANEL, line=DIM)
text(s, ML + 0.26, 6.38, CW - 0.52, 0.4,
     [("Every decision above keeps the board buildable with through-hole parts on a breadboard or dot "
       "PCB, which is the constraint a college laboratory actually has.", 11, MUTED)],
     line_spacing=1.15, space_after=0)

# ----------------------------------------------------------------- slide 25
s = content_slide("Safety and practice", "Rules that keep the board and the bench safe")

rules = [
    ("Never connect the relay to mains", "The relay is mains rated but the demonstration uses a 5 V or "
                                         "12 V lamp on J4, or leaves the contacts open entirely.", RED),
    ("Fit the 7805 heatsink", "About 1 W is dissipated at 9 V and 250 mA. Without the heatsink the "
                              "regulator shuts down thermally.", AMBER),
    ("Power off before handling the ICs", "Inserting or removing the microcontroller with power applied "
                                          "latches the outputs and can destroy the part.", AMBER),
    ("Switches 6, 7 and 8 OFF when flashing", "They share P1.5 to P1.7 with the SPI lines and will "
                                              "corrupt the programming transfer.", RED),
    ("Remove JP1 before probing P3.4", "The relay coil loads the square wave output and gives a false "
                                       "reading on the scope.", AMBER),
    ("Check the 5 V rail before anything else", "A wrong rail damages every IC on the board at once, "
                                                "so it is measured with nothing else connected.", RED),
]
for i, (h, b, col) in enumerate(rules):
    x = ML + (i % 3) * 4.09
    y = 1.85 + (i // 3) * 2.45
    box(s, x, y, 3.85, 2.18, fill=PANEL)
    box(s, x, y, 0.055, 2.18, col, shape=MSO_SHAPE.RECTANGLE)
    text(s, x + 0.26, y + 0.20, 3.35, 0.5, [(h, 12.5, TEXT, True)], line_spacing=1.05, space_after=0)
    text(s, x + 0.26, y + 0.92, 3.35, 1.1, [(b, 10.5, MUTED)], line_spacing=1.16, space_after=0)

# ----------------------------------------------------------------- slide 26
s = content_slide("Conclusion", "The 8051 now runs on real silicon")

concl = [
    ("The port shortage is solved",
     "A single 8-bit bus on port 0 with per-device strobes on port 2 puts eight LEDs, a two digit "
     "display, a 16x2 LCD, an ADC, a relay and a buzzer on a device with 32 pins."),
    ("Every number is derived, not guessed",
     "TH1 = FDH, TH0 = EE00H and 4C00H and FE34H, 470 Ohm resistors, 7.8125 mV per step and 606 kHz "
     "all follow from the 1.0851 microsecond machine cycle."),
    ("Thirteen programs, all compiling clean",
     "From a blinking LED to a complete zone monitor with telemetry, written without comments in the "
     "C51 subset and verified for zero errors and zero warnings."),
    ("The build is staged and measured",
     "Ten assembly stages each end with a measurement that must pass, and twenty tests with "
     "acceptance limits turn the demonstration into evidence."),
    ("The simulator and the hardware agree",
     "Each hardware result can be checked against the value the simulator produced in phase 1, which "
     "is the point of having built the model first."),
    ("It is affordable and repeatable",
     "About 985 rupees per board in through-hole parts, programmed with a 250 rupee USBasp, built on "
     "a breadboard or a dot PCB."),
]
for i, (h, b) in enumerate(concl):
    x = ML + (i % 3) * 4.09
    y = 1.85 + (i // 3) * 2.45
    num_card(s, x, y, 3.85, 2.18, "{0:02d}".format(i + 1), h, b, accent=ACCENT)

# ----------------------------------------------------------------- slide 27
s = content_slide("Future scope", "Where the board can go next")

data = [["Direction", "What it adds", "What it needs"],
        ["Complete instruction coverage", "the rarely used instructions and the 8052 extras: timer 2 "
                                          "and 256 bytes of RAM", "a second firmware pass, no new hardware"],
        ["Peripheral depth", "serial modes 0 and 2, the remaining timer modes, interrupt priority "
                             "nesting", "firmware only"],
        ["More sensors", "ADC0808 or ADC0809 for four or eight channels, an LDR, a potentiometer "
                         "setpoint", "one more ADC and a multiplexer"],
        ["Data logging", "an I2C EEPROM or an SD card so temperature history survives power down",
         "two I/O pins and a bit-banged I2C driver"],
        ["Real time clock", "a DS1307 so every telemetry line carries a timestamp", "the same I2C bus"],
        ["Wireless link", "an ESP-01 or a HC-05 module replacing the serial cable", "the existing UART at 3.3 V levels"],
        ["A proper PCB", "a two layer board with a ground plane, silk screen and mounting holes",
         "a KiCad layout from the net tables already written"],
        ["Mains rated enclosure", "an insulated box, a fused relay output and a proper terminal block",
         "safety review before any mains connection"]]
table(s, ML, 1.80, CW, 4.05, data, col_w=[2.6, 5.4, 4.1], fsize=9.5, hsize=9.5,
      align=["l", "l", "l"])

box(s, ML, 6.00, CW, 0.85, fill=PANEL, line=ACCENT)
text(s, ML + 0.28, 6.14, CW - 0.56, 0.66,
     [("The first four need no new hardware at all.  ", 11.5, TEXT, True),
      ("Two of the 32 pins are recoverable if the LCD is moved to a PCF8574 I2C backpack, which frees "
       "P2.3 and P2.4 for an I2C bus.", 11.5, MUTED)],
     line_spacing=1.15, space_after=0)

# ----------------------------------------------------------------- slide 28
s = content_slide("References", "Sources used for the design")

data = [["#", "Reference", "Used for"],
        ["1", "Intel, MCS-51 Microcontroller Family User's Manual, 1981", "architecture, SFRs, instruction timing"],
        ["2", "Atmel, AT89S52 and AT89C51 datasheets", "pinout, DC characteristics, ISP interface"],
        ["3", "Texas Instruments and Renesas, ADC0804 datasheet", "self clocking RC network, conversion timing, Vref/2"],
        ["4", "Texas Instruments, MAX232 datasheet", "charge pump capacitor connections, DB9 wiring"],
        ["5", "Texas Instruments, LM35 datasheet", "10 mV per degree C, output loading, decoupling"],
        ["6", "Hitachi HD44780 datasheet", "8-bit initialisation sequence and timing"],
        ["7", "Keil Software, C51 compiler and uVision documentation", "sbit, code and interrupt keywords, project options"],
        ["8", "M. A. Mazidi, J. G. Mazidi and R. D. McKinlay, The 8051 Microcontroller and Embedded Systems", "interfacing patterns and worked examples"],
        ["9", "K. J. Ayala, The 8051 Microcontroller: Architecture, Programming and Applications", "instruction set and addressing modes"],
        ["10", "Project files: hardware/SCHEMATIC.md, firmware/src, firmware/inc/board.h", "this implementation"]]
table(s, ML, 1.80, CW, 4.20, data, col_w=[0.4, 6.6, 5.1], fsize=10, hsize=10,
      align=["c", "l", "l"])

box(s, ML, 6.20, CW, 0.66, fill=PANEL, line=ACCENT)
text(s, ML + 0.28, 6.32, CW - 0.56, 0.45,
     [("Thank you - questions are welcome.", 13, LIGHT, True)], space_after=0)

import os
os.makedirs("docs", exist_ok=True)
prs.save("docs/8051_Hardware_Implementation.pptx")
print("saved docs/8051_Hardware_Implementation.pptx")
print("slides:", len(prs.slides.__iter__.__self__._sldIdLst))
