import io

W, H = 1200, 880
X0, X1 = 470, 720
PY0, PITCH = 150, 26

LEFT = [
    (1, "P1.0", "SW1"), (2, "P1.1", "SW2"), (3, "P1.2", "SW3"), (4, "P1.3", "SW4"),
    (5, "P1.4", "SW5"), (6, "P1.5", "SW6 / MOSI"), (7, "P1.6", "SW7 / MISO"),
    (8, "P1.7", "SW8 / SCK"), (9, "RST", "reset"), (10, "P3.0", "RxD"),
    (11, "P3.1", "TxD"), (12, "P3.2", "INT0 / PB1"), (13, "P3.3", "INT1 / PB2"),
    (14, "P3.4", "T0 / RELAY"), (15, "P3.5", "T1 / BUZZER"), (16, "P3.6", "DIG1"),
    (17, "P3.7", "DIG2"), (18, "XTAL2", "clock out"), (19, "XTAL1", "clock in"),
    (20, "GND", "0 V"),
]

RIGHT = [
    (40, "VCC", "+5 V"), (39, "P0.7", "AD7"), (38, "P0.6", "AD6"), (37, "P0.5", "AD5"),
    (36, "P0.4", "AD4"), (35, "P0.3", "AD3"), (34, "P0.2", "AD2"), (33, "P0.1", "AD1"),
    (32, "P0.0", "AD0"), (31, "EA/VPP", "tie to +5 V"), (30, "ALE", "not connected"),
    (29, "PSEN", "not connected"), (28, "P2.7", "ADC_INTR"), (27, "P2.6", "ADC_RD"),
    (26, "P2.5", "ADC_WR"), (25, "P2.4", "LCD_RW"), (24, "P2.3", "LCD_RS"),
    (23, "P2.2", "LCD_E"), (22, "P2.1", "SEG_LE"), (21, "P2.0", "LED_LE"),
]

LY = {n: PY0 + (n - 1) * PITCH for n, _a, _b in LEFT}
RY = {n: PY0 + (40 - n) * PITCH for n, _a, _b in RIGHT}

VCC_Y = 96
GND_Y = 800

o = io.StringIO()
o.write('<?xml version="1.0" encoding="UTF-8"?>\n')
o.write('<svg xmlns="http://www.w3.org/2000/svg" width="{0}" height="{1}" viewBox="0 0 {0} {1}">\n'.format(W, H))
o.write('<rect width="{0}" height="{1}" fill="#ffffff"/>\n'.format(W, H))
o.write('<g font-family="DejaVu Sans, Helvetica, Arial, sans-serif" fill="#111827" '
        'stroke="#111827" stroke-width="1.6" stroke-linecap="round">\n')

def line(x1, y1, x2, y2, dash=None):
    d = ' stroke-dasharray="6,4"' if dash else ''
    o.write('<line x1="{0}" y1="{1}" x2="{2}" y2="{3}"{4}/>\n'.format(x1, y1, x2, y2, d))

def text(x, y, s, size=13, anchor="start", bold=False, fill="#111827"):
    w = ' font-weight="700"' if bold else ''
    o.write('<text x="{0}" y="{1}" font-size="{2}" text-anchor="{3}" fill="{4}" '
            'stroke="none"{5}>{6}</text>\n'.format(x, y, size, anchor, fill, w, s))

def dot(x, y):
    o.write('<circle cx="{0}" cy="{1}" r="3.4" fill="#111827" stroke="none"/>\n'.format(x, y))

def resistor_v(x, y1, y2, label, lx=None):
    mid = (y1 + y2) / 2.0
    h = 22.0
    line(x, y1, x, mid - h)
    o.write('<rect x="{0}" y="{1}" width="20" height="{2}" rx="2" fill="#ffffff"/>\n'.format(x - 10, mid - h, h * 2))
    line(x, mid + h, x, y2)
    text((lx if lx else x) + 16, mid + 5, label, 12)

def capacitor_v(x, ytop, label, lx=None):
    line(x, ytop, x, ytop + 26)
    line(x - 17, ytop + 26, x + 17, ytop + 26, dash=None)
    line(x - 17, ytop + 38, x + 17, ytop + 38)
    line(x, ytop + 38, x, ytop + 64)
    text((lx if lx else x) + 22, ytop + 40, label, 12)

def capacitor_h(y, xleft, label):
    line(xleft, y, xleft + 26, y)
    line(xleft + 26, y - 17, xleft + 26, y + 17)
    line(xleft + 38, y - 17, xleft + 38, y + 17)
    line(xleft + 38, y, xleft + 64, y)
    text(xleft + 6, y - 24, label, 12)

# power rails
line(90, VCC_Y, 1110, VCC_Y)
line(90, GND_Y, 1110, GND_Y)
text(90, VCC_Y - 12, "+5 V regulated supply", 14, bold=True)
text(90, GND_Y + 26, "0 V", 14, bold=True)
for gx in (280, 300, 405, 960):
    line(gx, GND_Y - 9, gx, GND_Y + 9)
    line(gx - 16, GND_Y + 9, gx + 16, GND_Y + 9)
    line(gx - 10, GND_Y + 16, gx + 10, GND_Y + 16)
    line(gx - 4, GND_Y + 23, gx + 4, GND_Y + 23)

# MCU body
o.write('<rect x="{0}" y="{1}" width="{2}" height="{3}" rx="6" fill="#f3f6fb"/>\n'.format(
    X0, PY0 - 34, X1 - X0, 19 * PITCH + 68))
text((X0 + X1) / 2, PY0 - 12, "AT89S52", 20, anchor="middle", bold=True)
text((X0 + X1) / 2, PY0 + 10, "40 pin plastic DIP", 13, anchor="middle", fill="#4b5563")
o.write('<path d="M {0} {1} a 14 14 0 0 1 14 -14" fill="none"/>\n'.format(X0 - 8, PY0 - 34 + 20))

# left pins
for n, name, note in LEFT:
    y = LY[n]
    line(X0 - 42, y, X0, y)
    text(X0 - 50, y + 4, "{0}".format(n), 11, anchor="end", fill="#6b7280")
    text(X0 - 96, y + 4, name, 13, anchor="end", bold=True)
    if note:
        text(X0 - 96 - 8 - 78, y + 4, note, 11, anchor="end", fill="#6b7280")

# right pins
for n, name, note in RIGHT:
    y = RY[n]
    line(X1, y, X1 + 42, y)
    text(X1 + 50, y + 4, "{0}".format(n), 11, fill="#6b7280")
    text(X1 + 96, y + 4, name, 13, bold=True)
    if note:
        text(X1 + 96 + 96, y + 4, note, 11, fill="#6b7280")

# P1 bus barrel
line(X0 - 120, LY[1], X0 - 120, LY[8])
for n in range(1, 9):
    line(X0 - 120, LY[n], X0 - 96, LY[n])
    dot(X0 - 120, LY[n])
text(X0 - 132, (LY[1] + LY[8]) / 2, "SW1 to SW8", 12, anchor="end", fill="#374151")

# P0 bus barrel
line(X1 + 150, RY[39], X1 + 150, RY[32])
for n in range(32, 40):
    line(X1 + 96 + 60, RY[n], X1 + 150, RY[n])
    dot(X1 + 150, RY[n])
text(X1 + 164, (RY[39] + RY[32]) / 2, "BD0 to BD7", 12, fill="#374151")
text(X1 + 164, (RY[39] + RY[32]) / 2 + 17, "data bus", 12, fill="#374151")

# P2 bus barrel
line(X1 + 150, RY[28], X1 + 150, RY[21])
for n in range(21, 29):
    line(X1 + 96 + 60, RY[n], X1 + 150, RY[n])
    dot(X1 + 150, RY[n])
text(X1 + 164, (RY[28] + RY[21]) / 2, "control", 12, fill="#374151")
text(X1 + 164, (RY[28] + RY[21]) / 2 + 17, "strobes", 12, fill="#374151")

# crystal network
y18, y19 = LY[18], LY[19]
line(X0 - 42, y18, 400, y18)
line(X0 - 42, y19, 400, y19)
line(400, y18, 400, y19)
o.write('<rect x="386" y="{0}" width="28" height="{1}" rx="2" fill="#ffffff"/>\n'.format(y18 + 12, (y19 - y18) - 24))
line(378, y18 + 12, 422, y18 + 12)
line(378, y19 - 12, 422, y19 - 12)
line(400, y18, 400, y18 + 12)
line(400, y19 - 12, 400, y19)
text(330, (y18 + y19) / 2 + 5, "Y1", 14, anchor="end", bold=True)
text(330, (y18 + y19) / 2 + 21, "11.0592 MHz", 11, anchor="end", fill="#6b7280")

line(400, y18, 280, y18)
line(280, y18, 280, y18 + 40)
capacitor_v(280, y18 + 40, "C3a  30 pF", lx=278)
line(280, y18 + 40 + 64, 280, GND_Y)

line(400, y19, 300, y19)
line(300, y19, 300, y19 + 40)
capacitor_v(300, y19 + 40, "C3b  30 pF", lx=298)
line(300, y19 + 40 + 64, 300, GND_Y)

# reset network
y9 = LY[9]
line(X0 - 96, y9, 330, y9)
dot(330, y9)
line(330, y9, 330, y9 + 72)
resistor_v(330, y9 + 72, y9 + 152, "R1  10 kOhm")
line(330, y9 + 152, 330, GND_Y)

line(330, y9, 240, y9)
line(240, y9, 240, y9 - 120)
line(240, y9 - 120, 240, y9 - 168)
line(224, y9 - 168, 256, y9 - 168)
line(240, y9 - 196, 240, y9 - 186)
line(196, y9 - 196, 256, y9 - 196)
line(240, y9 - 196, 240, VCC_Y)
text(268, y9 - 176, "PB3", 12, bold=True)
text(268, y9 - 160, "reset", 12)

line(330, VCC_Y, 330, y9 - 158)
capacitor_v(330, y9 - 158, "C2  10 uF", lx=352)
line(330, y9 - 158 + 64, 330, y9)

# EA strap
y31 = RY[31]
line(X1 + 42, y31, 940, y31)
line(940, y31, 940, VCC_Y)
dot(940, y31)
text(950, y31 - 10, "EA/VPP must be tied to +5 V", 12, bold=True, fill="#b91c1c")
text(950, y31 + 6, "otherwise the device fetches code", 11, fill="#b91c1c")
text(950, y31 + 22, "from external memory and looks dead", 11, fill="#b91c1c")

# VCC and GND pins of the MCU
line(X1 + 42, RY[40], 900, RY[40])
line(900, RY[40], 900, VCC_Y)
dot(900, RY[40])
text(908, RY[40] - 10, "decouple with C1 0.1 uF", 11, fill="#6b7280")

line(X0 - 42, LY[20], 405, LY[20])
line(405, LY[20], 405, GND_Y)
dot(405, LY[20])

# decoupling capacitor
line(960, VCC_Y, 960, 420)
capacitor_v(960, 420, "C1  0.1 uF", lx=1000)
line(960, 420 + 64, 960, GND_Y)
text(1000 + 22, 464, "mount within 5 mm", 11, fill="#6b7280")
text(1000 + 22, 480, "of pin 40 and pin 20", 11, fill="#6b7280")

# ALE proof note
text(X1 + 96 + 96, RY[30] + 4, "1.843 MHz when running", 11, fill="#6b7280")

# title and footer
text(90, 52, "8051 Hardware Lab Board - minimum system", 20, bold=True)
text(90, 74, "Crystal, reset, EA strap and decoupling. Peripheral wiring is given in SCHEMATIC.md section 4.", 12, fill="#4b5563")
text(90, H - 26, "One machine cycle = 12 oscillator periods = 1.0851 microseconds at 11.0592 MHz", 12, fill="#4b5563")
line(90, H - 52, 1110, H - 52, dash=True)

o.write('</g>\n</svg>\n')

with open("hardware/min-system.svg", "w", encoding="utf-8") as f:
    f.write(o.getvalue())
print("wrote hardware/min-system.svg")
