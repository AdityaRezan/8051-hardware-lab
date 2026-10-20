#!/usr/bin/env python3
"""Build docs/guide/8051_How_It_Works.pdf - a plain English, photo led guide.

Run:  python3 tools/build_guide_pdf.py
Deps: weasyprint, pillow
"""

import os
import re
import html as htmllib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUIDE = os.path.join(ROOT, "docs", "guide")
IMG = os.path.join(GUIDE, "images")
OUT_PDF = os.path.join(GUIDE, "8051_How_It_Works.pdf")
OUT_HTML = os.path.join(GUIDE, "source.html")

# ------------------------------------------------------------------ helpers


def esc(s):
    return htmllib.escape(str(s), quote=False)


def uri(name):
    return "file://" + os.path.join(IMG, name)


def fig(name, caption=None, width=None, cls=""):
    w = (' style="width:%s"' % width) if width else ""
    out = ['<div class="fig %s">' % cls]
    out.append('<img src="%s"%s alt="">' % (uri(name), w))
    if caption:
        out.append('<div class="cap">%s</div>' % esc(caption))
    out.append("</div>")
    return "".join(out)


def card(name, title, body, tag=None):
    t = '<span class="tag">%s</span>' % esc(tag) if tag else ""
    return (
        '<td><div class="card">'
        '<div class="shot"><img src="%s" alt=""></div>'
        '<div class="ctitle">%s %s</div>'
        '<div class="cbody">%s</div>'
        "</div></td>" % (uri(name), esc(title), t, body)
    )


def grid(cells, n=3):
    rows = []
    for i in range(0, len(cells), n):
        chunk = cells[i:i + n]
        chunk = chunk + ["<td></td>"] * (n - len(chunk))
        rows.append("<tr>%s</tr>" % "".join(chunk))
    return '<table class="grid g%d">%s</table>' % (n, "".join(rows))


def table(headers, rows, cls="", widths=None):
    w = ""
    if widths:
        cols = "".join('<col style="width:%s">' % x for x in widths)
    else:
        cols = ""
    th = "".join("<th>%s</th>" % esc(h) for h in headers)
    trs = []
    for r in rows:
        trs.append("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r))
    return '<table class="tbl %s">%s<thead><tr>%s</tr></thead><tbody>%s</tbody></table>' % (
        cls, cols, th, "".join(trs))


def callout(title, body, tone="blue"):
    return ('<div class="callout %s"><div class="cotitle">%s</div>'
            '<div class="cobody">%s</div></div>' % (tone, esc(title), body))


def steps(items, cls=""):
    out = ['<ol class="steps %s">' % cls]
    for it in items:
        out.append("<li>%s</li>" % it)
    out.append("</ol>")
    return "".join(out)


def lead(text):
    return '<p class="lead">%s</p>' % text


def p(text):
    return "<p>%s</p>" % text


def h2(text):
    return '<h2>%s</h2>' % esc(text)


def page(title, kicker, body, wide=False):
    return (
        '<section class="page"><h1 class="pt">%s</h1>'
        '<div class="kick">%s</div>%s</section>'
        % (esc(title), esc(kicker), body)
    )


def stats(items):
    out = ['<table class="stats">']
    for i in range(0, len(items), 3):
        chunk = items[i:i + 3]
        chunk = chunk + [("", "")] * (3 - len(chunk))
        out.append("<tr>")
        for val, lab in chunk:
            out.append('<td><div class="sval">%s</div>'
                       '<div class="slab">%s</div></td>' % (esc(val), esc(lab)))
        out.append("</tr>")
    out.append("</table>")
    return "".join(out)


# ------------------------------------------------------------------ pull real code


def extract_board_fn(name):
    src = open(os.path.join(ROOT, "firmware", "inc", "board.h")).read()
    m = re.search(r"^%s\s*\n\{.*?^\}" % re.escape(name), src,
                  re.S | re.M)
    return m.group(0) if m else ""


LED_WRITE_SRC = extract_board_fn("void led_write(unsigned char v)")
BUS_PUT_SRC = extract_board_fn("void bus_put(unsigned char v)")

# ------------------------------------------------------------------ CSS

CSS = """
@page {
  size: A4;
  margin: 21mm 17mm 15mm 17mm;
  @top-left {
    content: "8051 HARDWARE LAB  -  PLAIN ENGLISH GUIDE";
    font-family: "DejaVu Sans", sans-serif;
    font-size: 6.6pt; color: #94A3B8; letter-spacing: 0.9pt;
  }
  @top-right {
    content: string(ptitle);
    font-family: "DejaVu Sans", sans-serif;
    font-size: 6.6pt; color: #2563EB; letter-spacing: 0.9pt;
    text-transform: uppercase;
  }
  @bottom-left {
    content: "Atharva (24BEL0082)  -  Aditya (24BEL0087)  -  Dept. of ECE, AY 2025-26";
    font-family: "DejaVu Sans", sans-serif;
    font-size: 6.2pt; color: #B4C0D0;
  }
  @bottom-right {
    content: "Page " counter(page) " of " counter(pages);
    font-family: "DejaVu Sans", sans-serif;
    font-size: 6.6pt; color: #64748B;
  }
}
@page cover {
  margin: 0;
  @top-left { content: normal; }
  @top-right { content: normal; }
  @bottom-left { content: normal; }
  @bottom-right { content: normal; }
}

* { box-sizing: border-box; }
html { font-family: "DejaVu Sans", sans-serif; }

body {
  margin: 0; padding: 0;
  font-family: "DejaVu Sans", sans-serif;
  font-size: 9.3pt; line-height: 1.5;
  color: #334155;
}

section.page { break-before: page; }
section.page:first-of-type { break-before: avoid; }

h1.pt {
  font-size: 19pt; line-height: 1.15; font-weight: bold;
  color: #0F172A; margin: 0 0 2.5mm 0; letter-spacing: -0.35pt;
  string-set: ptitle content();
}
.kick {
  font-size: 7pt; font-weight: bold; letter-spacing: 1.1pt;
  color: #2563EB; text-transform: uppercase;
  border-bottom: 1.6pt solid #2563EB;
  padding-bottom: 1.6mm; margin-bottom: 5mm;
}
h2 {
  font-size: 10.5pt; font-weight: bold; color: #1E293B;
  margin: 3.6mm 0 1.5mm 0; letter-spacing: -0.1pt;
}

p { margin: 0 0 2.6mm 0; text-align: justify; }
p.lead { font-size: 10.6pt; line-height: 1.52; color: #1E293B; margin-bottom: 3.5mm; }

b { color: #0F172A; }
code, .mono { font-family: "DejaVu Sans Mono", monospace; font-size: 8.4pt; }
code { background: #F1F5F9; padding: 0 1.2mm; border-radius: 0.8mm; color: #1E293B; }

/* figures */
div.fig { margin: 3mm 0; text-align: center; }
div.fig img { max-width: 100%; border: 0.4pt solid #E2E8F0; border-radius: 1mm; }
div.fig.strip img { border: none; }
div.cap {
  font-size: 7.4pt; color: #64748B; margin-top: 1.4mm;
  text-align: left; line-height: 1.4; padding: 0 1mm;
}

/* card grids */
table.grid { width: 100%; border-collapse: collapse; margin: 3mm 0; }
table.grid td { vertical-align: top; padding: 0 2mm 4mm 0; width: 50%; }
table.grid.g3 td { width: 33.33%; }
table.grid td:last-child { padding-right: 0; }
div.card {
  border: 0.4pt solid #E2E8F0; border-top: 1.6pt solid #2563EB;
  border-radius: 1mm; padding: 0 2.4mm 2.6mm 2.4mm;
  background: #FCFDFE; height: 100%;
}
div.shot { margin: 2.4mm -2.4mm 2mm -2.4mm; padding: 0 2.4mm; text-align: center; }
div.shot img { max-width: 88%; max-height: 30mm; }
div.ctitle {
  font-size: 8.6pt; font-weight: bold; color: #0F172A;
  margin-bottom: 1.1mm; line-height: 1.25;
}
span.tag {
  font-size: 6.2pt; font-weight: bold; color: #10B981;
  letter-spacing: 0.6pt; background: #ECFDF5;
  padding: 0.4mm 1.2mm; border-radius: 0.8mm;
  white-space: nowrap;
}
div.cbody { font-size: 7.9pt; line-height: 1.38; color: #475569; text-align: left; }

/* data tables */
table.tbl {
  width: 100%; border-collapse: collapse; margin: 3mm 0; font-size: 8pt;
}
table.tbl th {
  background: #1E293B; color: #F1F5F9; text-align: left;
  font-size: 7.2pt; font-weight: bold; letter-spacing: 0.4pt;
  padding: 1.5mm 2mm; border: none;
}
table.tbl td {
  padding: 1.35mm 2mm; border-bottom: 0.35pt solid #E2E8F0;
  vertical-align: top; line-height: 1.35;
}
table.tbl tr:nth-child(even) td { background: #F8FAFC; }
table.tbl td.n { font-family: "DejaVu Sans Mono", monospace; font-size: 7.6pt; color: #2563EB; }
table.tbl td.m { font-family: "DejaVu Sans Mono", monospace; font-size: 7.6pt; }
table.tbl.bar { border-left: 1.6pt solid #2563EB; }
table.tbl.gloss { font-size: 7.35pt; }
table.tbl.gloss td { padding: 0.92mm 2mm; line-height: 1.26; }
table.tbl.gloss th { padding: 1.2mm 2mm; }
table.tbl.files { font-size: 7.3pt; }
table.tbl.files td { padding: 1.05mm 2mm; line-height: 1.3; }
table.tbl.files th { padding: 1.2mm 2mm; }

/* callouts */
div.callout {
  border-left: 2.2pt solid #2563EB; background: #F4F8FF;
  padding: 2.6mm 3.2mm; margin: 3.5mm 0; border-radius: 0 1mm 1mm 0;
}
div.callout.green { border-left-color: #10B981; background: #F1FBF6; }
div.callout.amber { border-left-color: #F59E0B; background: #FFFAF0; }
div.cotitle {
  font-size: 7.4pt; font-weight: bold; letter-spacing: 0.8pt;
  color: #1E293B; text-transform: uppercase; margin-bottom: 1.2mm;
}
div.cobody { font-size: 8.4pt; line-height: 1.45; }

/* steps */
ol.steps { margin: 2.5mm 0 3mm 0; padding: 0; list-style: none; counter-reset: st; }
ol.steps li {
  counter-increment: st; position: relative;
  padding: 0 0 2.6mm 8.5mm; min-height: 6mm;
  font-size: 8.8pt; line-height: 1.42; text-align: justify;
}
ol.steps li::before {
  content: counter(st); position: absolute; left: 0; top: 0.1mm;
  width: 5.6mm; height: 5.6mm; line-height: 5.6mm; text-align: center;
  background: #1E293B; color: #FFFFFF; border-radius: 50%;
  font-size: 7.4pt; font-weight: bold;
}
ol.steps.tight li { padding-bottom: 1.8mm; font-size: 8.2pt; }
ol.steps.tighter li { padding-bottom: 1.2mm; font-size: 8.1pt; line-height: 1.36; }

/* stat blocks */
table.stats { width: 100%; border-collapse: collapse; margin: 3.5mm 0; }
table.stats td {
  width: 33.33%; padding: 0 2mm 3.5mm 0; vertical-align: top;
}
table.stats td:last-child { padding-right: 0; }
div.sval {
  font-size: 15pt; font-weight: bold; color: #2563EB; line-height: 1.05;
  letter-spacing: -0.5pt;
}
div.slab {
  font-size: 6.6pt; letter-spacing: 0.55pt; color: #64748B;
  text-transform: uppercase; margin-top: 0.8mm; line-height: 1.25;
}

/* code panel */
pre.code {
  background: #1E293B; color: #E2E8F0; border-radius: 1.2mm;
  padding: 3mm 3.4mm; margin: 3mm 0;
  font-family: "DejaVu Sans Mono", monospace; font-size: 7.9pt;
  line-height: 1.45; white-space: pre; overflow: hidden;
}
pre.code .kw { color: #7DD3FC; }
pre.code .cm { color: #94A3B8; }
pre.code .nb { color: #FBBF24; }

/* two column split */
table.split { width: 100%; border-collapse: collapse; margin: 3mm 0; }
table.split td { width: 50%; vertical-align: top; padding: 0; }
table.split td.l { padding-right: 3.5mm; }
table.split td.r { padding-left: 3.5mm; }
div.halfbox {
  border: 0.4pt solid #E2E8F0; border-top: 1.8pt solid #10B981;
  border-radius: 1mm; padding: 2.6mm 3mm; background: #FCFDFE;
}
div.halfbox.blue { border-top-color: #2563EB; }
div.halfbox h3 {
  margin: 0 0 1.4mm 0; font-size: 9pt; color: #0F172A;
}
div.halfbox p { font-size: 8.2pt; line-height: 1.42; margin-bottom: 1.6mm; }

/* cover */
section.cover { page: cover; }
div.cv {
  background: #1E293B; color: #F1F5F9;
  height: 297mm; width: 210mm; padding: 0; position: relative;
}
div.cvtop { padding: 20mm 18mm 0 18mm; }
div.cvkick {
  font-size: 8pt; font-weight: bold; letter-spacing: 2.4pt; color: #60A5FA;
  text-transform: uppercase;
}
div.cvtitle {
  font-size: 30pt; font-weight: bold; line-height: 1.1; color: #F8FAFC;
  margin: 5mm 0 3mm 0; letter-spacing: -0.9pt;
}
div.cvsub {
  font-size: 12pt; color: #94A3B8; line-height: 1.4; max-width: 150mm;
}
div.cvrule { height: 2.4pt; background: #2563EB; width: 42mm; margin: 7mm 0 0 0; }
div.cvimg { margin: 8mm 18mm 0 18mm; }
div.cvimg img {
  width: 174mm; border-radius: 1.5mm;
  border: 0.5pt solid #334155;
}
div.cvbot {
  position: absolute; left: 18mm; right: 18mm; bottom: 16mm;
}
table.cvmeta { width: 100%; border-collapse: collapse; }
table.cvmeta td {
  vertical-align: top; width: 33.33%; padding: 0 3mm 0 0;
  border-top: 0.5pt solid #334155; padding-top: 3mm;
}
div.cvlab {
  font-size: 6.4pt; letter-spacing: 1.1pt; color: #64748B;
  text-transform: uppercase; margin-bottom: 1.2mm;
}
div.cvval { font-size: 8.6pt; color: #CBD5E1; line-height: 1.4; }
div.cvval b { color: #F1F5F9; }
div.cvbar { height: 2.4pt; background: #10B981; width: 100%; margin-top: 6mm; }

div.avoid { break-inside: avoid; }
"""

# ------------------------------------------------------------------ pages

PAGES = []


def add(markup):
    PAGES.append(markup)


# ---------------------------------------------------------------- 1 cover
add(
    '<section class="cover"><div class="cv">'
    '<div class="cvtop">'
    '<div class="cvkick">8051 Hardware Lab &#183; Plain-English Guide</div>'
    '<div class="cvtitle">How the Software<br>and the Hardware<br>Work Together</div>'
    '<div class="cvsub">An AT89S52 microcontroller board, explained from the '
    'outside in: what the parts are, what the code says, where the two meet, '
    'and how to talk about it.</div>'
    '<div class="cvrule"></div>'
    "</div>"
    '<div class="cvimg"><img src="%s" alt=""></div>'
    '<div class="cvbot"><table class="cvmeta">'
    "<tr>"
    '<td><div class="cvlab">Built by</div><div class="cvval"><b>Atharva</b> '
    "(24BEL0082)<br><b>Aditya</b> (24BEL0087)</div></td>"
    '<td><div class="cvlab">Department</div><div class="cvval">Electronics '
    "and<br>Computer Engineering<br>AY 2025-26</div></td>"
    '<td><div class="cvlab">Inside</div><div class="cvval">18 pages &#183; '
    "real photographs<br>13 programs &#183; 80 parts<br>one shared data "
    "bus</div></td>"
    "</tr></table>"
    '<div class="cvbar"></div>'
    "</div></div></section>" % uri("breadboard.jpg")
)

# ---------------------------------------------------------------- 2 summary
add(page(
    "The whole project in one paragraph",
    "Start here",
    lead(
        "This is a small computer board that watches a room and reacts to it. "
        "At the centre sits a single chip, an Atmel <b>AT89S52</b> "
        "microcontroller, which is a complete computer no bigger than a thumb: "
        "a processor, 8 kilobytes of program memory and 256 bytes of working "
        "memory, all inside one black plastic block with forty metal legs. We "
        "wired real parts around it: eight indicator LEDs, a two-digit "
        "seven-segment display, a 16-character LCD, a temperature sensor, a "
        "relay, a buzzer, a bank of eight switches, and a cable that lets the "
        "board type lines of text onto a PC screen. Then we wrote thirteen "
        "small programs in Keil C51, compiled each one into a machine-code "
        "<code>.hex</code> file, and burned those files into the chip. The "
        "board now reads its switches and its sensor, works out what they "
        "mean, and moves its outputs: light an LED, print on the LCD, click "
        "the relay, send a line of telemetry upstairs. Everything it does is "
        "that same loop, over and over, hundreds of times a second."
    )
    + h2("If you remember only three things")
    + steps([
        "<b>The chip ran out of pins, and we did not add a chip to fix it.</b> "
        "The finished design needs 54 separate connections. The processor has "
        "32 to spare. Instead of buying an expander we made eight of those "
        "pins carry data for four different devices, one at a time, and used "
        "four more pins as gates that decide which device is listening.",

        "<b>Software is a list of instructions that change the voltage on a "
        "pin.</b> Nothing more mystical than that. When the code says the "
        "relay is on, five volts appear on pin 14 of the chip, and a "
        "millisecond later the relay clicks. The software never touches the "
        "world directly; it only ever moves pins.",

        "<b>Every program here runs the same four beats: read, convert, "
        "decide, act.</b> The largest and most complicated program on the "
        "board is that loop with a longer decide step. Once you can say those "
        "four beats out loud, you can explain all thirteen programs.",
    ])
    + callout(
        "How to read this guide",
        "Pages 3 to 6 explain the two halves separately, first the hardware "
        "you can touch and then the code you cannot. Pages 7 to 10 explain how "
        "they join and how we solved the shortage of pins. Pages 11 to 14 walk "
        "through the physical build and then follow two real events, a button "
        "press and a rise in temperature, all the way through the system. "
        "Pages 15 to 18 are reference: the tests, the numbers, a glossary, and "
        "a short script you can use when you are asked to present the work.",
        tone="green",
    )
))

# ---------------------------------------------------------------- 3 two halves
add(page(
    "Two halves of one machine",
    "Concept",
    lead(
        "Every embedded system has these two halves, and it is worth being "
        "blunt about the difference. One half you can drop on the floor. The "
        'other half you cannot hold at all: it is a pattern of electrical '
        "charges inside the chip. The entire job of this project is joining "
        "them."
    )
    + '<table class="split"><tr>'
    '<td class="l"><div class="halfbox">'
    "<h3>Hardware &#8212; the things you can touch</h3>"
    "<p>The black chip, the eight LEDs, the display, the LCD, the temperature "
    "sensor, the relay, the buzzer, the resistors, the wire. Hardware is "
    "physical and dumb. Left alone it does nothing at all: it is a collection "
    "of parts waiting for electricity to arrive in the right order.</p>"
    "<p>It also sets the limits. A pin can only supply so much current. A "
    "sensor can only measure so accurately. An LED needs a resistor or it "
    "burns out. Most of the engineering on this board was respecting those "
    "limits.</p>"
    "</div></td>"
    '<td class="r"><div class="halfbox blue">'
    "<h3>Software &#8212; the list of instructions</h3>"
    "<p>Thirteen programs written in C, typed into the Keil uVision editor and "
    "compiled into <code>.hex</code> files of bare machine bytes. Burn those "
    "bytes into the chip's flash memory and they survive with the power off. "
    "Switch on and the chip starts at the first instruction and obeys them one "
    "at a time, forever.</p>"
    "<p>Software has no physical form. Change one character and recompile and "
    "you have a completely different machine, with no change to the hardware "
    "at all. That is the whole reason these boards are useful.</p>"
    "</div></td></tr></table>"
    + fig(
        "concept-code-to-hardware.png",
        "The boundary between the two halves is a single pin. One line of code "
        "becomes one electrical signal on one pin, and that signal becomes "
        "light from one LED. Nothing else happens anywhere in the machine.",
        width="168mm",
    )
    + h2("Follow one instruction all the way out")
    + steps([
        "<b>In the code:</b> the program calls <code>led_write(0xFF)</code>. "
        "The compiler has already turned that line into three or four machine "
        "instructions stored in flash.",
        "<b>In the chip:</b> the processor fetches those instructions and "
        "executes them. Eight pins of port 0 are driven to 5 V at once, then a "
        "ninth pin, the LED latch gate, is pulsed high for a fraction of a "
        "microsecond.",
        "<b>In the hardware:</b> the latch chip captures that pattern and holds "
        "it. Current flows through a 470 ohm resistor into each LED, about "
        "7 milliamps each, and all eight light up. They stay lit after the bus "
        "has moved on to something else.",
    ], cls="tight")
))

# ---------------------------------------------------------------- 4 hardware 1
add(page(
    "The parts you can touch",
    "Hardware one",
    lead(
        "These are the six parts that do the visible work: they are what a "
        "person looking at the board actually notices. Each one is wired to "
        "the chip and each one is driven by a line of code somewhere in the "
        "thirteen programs."
    )
    + grid([
        card("mcu-at89s52.jpg", "AT89S52 microcontroller",
             "The brain. Forty pins, 8 KB of flash for the program, 256 bytes "
             "of RAM for working values, three timers and a serial port, all "
             "in one package. Runs at 11.0592 MHz.", tag="U1"),
        card("leds.jpg", "Eight indicator LEDs",
             "Six of them carry meaning: safe, warning, danger, relay, buzzer "
             "and a heartbeat that blinks once a second to prove the chip is "
             "alive. Each has its own 470 ohm resistor.", tag="D3-D10"),
        card("display-7seg.jpg", "Two-digit display",
             "Shows the temperature in whole degrees. Only one digit is ever "
             "lit at a time; the code swaps between them every 5 ms, which is "
             "fast enough that the eye sees both.", tag="DSP1"),
        card("lcd-16x2.jpg", "16x2 character LCD",
             "Two lines of sixteen characters. Line one carries the live "
             "reading, line two carries the state: SAFE, WARNING, DANGER, or "
             "EMERGENCY STOP.", tag="LCD1"),
        card("sensor-lm35.jpg", "LM35 temperature sensor",
             "The thermometer. It needs no calibration and puts out exactly "
             "10 millivolts per degree Celsius, so 0.31 V on its leg means 31 "
             "degrees. Three legs, looks like a small transistor.", tag="U6"),
        card("relay.jpg", "Relay",
             "An electrically operated switch. Five volts on one pin from the "
             "chip lets it switch a load a hundred times bigger, such as a "
             "fan or a pump. You hear it as a click.", tag="RLY1"),
    ], n=3)
    + callout(
        "A detail worth saying out loud",
        "Notice that five of these six parts need eight wires each. That "
        "single fact is what forced the design decision described on page 8. "
        "It is the only genuinely difficult thing about this board, and it is "
        "the part most worth understanding before a viva.",
        tone="amber",
    )
))

# ---------------------------------------------------------------- 5 hardware 2
add(page(
    "The parts that make the rest work",
    "Hardware two",
    lead(
        "None of these parts do anything a person would notice, and the board "
        "is dead without every one of them. This is the half of the hardware "
        "that students forget to explain, and examiners notice."
    )
    + grid([
        card("crystal.jpg", "11.0592 MHz crystal",
             "The metronome. Every instruction, every delay and the serial "
             "speed all come from this. The odd frequency is chosen on "
             "purpose: it divides exactly by 9600, so serial communication has "
             "zero timing error.", tag="Y1"),
        card("regulator-7805.jpg", "7805 voltage regulator",
             "Takes the 9 V from the adapter and holds a rock-steady 5 V no "
             "matter what the board is doing. Everything else on the board "
             "runs on that 5 V. It gets warm, so it wears a heatsink.",
             tag="U7"),
        card("adc0804.jpg", "ADC0804 converter",
             "The translator. The sensor speaks in voltages, but the chip only "
             "understands numbers. This chip measures a voltage and hands back "
             "a whole number from 0 to 255, about 114 microseconds per "
             "reading.", tag="U4"),
        card("programmer-usbasp.jpg", "USBasp programmer",
             "How the code gets in. It plugs into the PC's USB port and "
             "writes the compiled .hex file straight into the chip's flash "
             "memory. The board can be reprogrammed hundreds of times.",
             tag="P1"),
        card("breadboard.jpg", "Solderless breadboard",
             "The base. A plastic block full of spring contacts that lets "
             "parts be connected with push-in wire and no soldering at all, so "
             "a mistake costs ten seconds to undo.", tag="&#8212;"),
        card("dipswitch.jpg", "Eight-way DIP switch",
             "Eight tiny sliding switches standing in for real industrial "
             "inputs: a door sensor, a motor running, a tank level. Lets the "
             "board be tested without any real machinery attached.", tag="SW1"),
    ], n=3)
    + fig(
        "breadboard-2.jpg",
        "The board under construction on the breadboard. Every part is "
        "through-hole and hand-placeable: no reflow oven, no microscope, no "
        "printed circuit board.",
        width="52mm", cls="avoid",
    )
))

# ---------------------------------------------------------------- 6 software
add(page(
    "The code: thirteen small programs",
    "Software",
    lead(
        "The software is not one large program. It is thirteen small ones, "
        "each building on the one before, each small enough to read on a "
        "single screen. Write a program, compile it, burn it, watch the "
        "hardware prove it works, then move to the next. That order is why "
        "this project is easy to demonstrate: at every stage something on the "
        "board is doing something visible."
    )
    + table(
        ["#", "Program", "What it does, in plain English", "Hardware it drives"],
        [
            ["01", "led_blink", "Flashes the eight LEDs once a second. Proves the chip, the clock and the output wiring all work.", "LED bank"],
            ["02", "led_patterns", "Walks a lit LED left and right and counts up in binary, so a stuck bit would be obvious.", "LED bank"],
            ["03", "switch_led", "Reads the eight switches and lights the matching LED. The first program with a real input.", "LEDs, switches"],
            ["04", "seg7_counter", "Counts from 00 to 99 on the display, driven by a timer interrupt rather than a delay loop.", "7-segment"],
            ["05", "timer0_second", "Blinks one LED exactly once a second using the hardware timer, which is far more accurate than counting instructions.", "Timer 0, LEDs"],
            ["06", "square_wave", "Produces a 1.00 kHz square wave on a pin, checked on an oscilloscope against a calculated reload value.", "Timer 0, P3.4"],
            ["07", "ext_interrupt", "Press a button and the chip drops whatever it is doing immediately and responds. No waiting, no polling.", "INT0, INT1, LEDs"],
            ["08", "uart_echo", "Sends back every character the PC types. Proves the serial link in both directions.", "UART, MAX232"],
            ["09", "uart_commands", "A small command shell: type LED FF and all eight LEDs obey; type RLY 1 and the relay clicks.", "UART, LEDs, relay"],
            ["10", "adc_7seg", "Reads the temperature and shows it as two digits on the display.", "ADC, LM35, display"],
            ["11", "adc_lcd", "Shows the temperature on the LCD as a number and as a bar of solid blocks that grows with heat.", "ADC, LM35, LCD"],
            ["12", "industrial_monitor", "The finished system. Reads the temperature, colours the zone, drives relay and buzzer, and prints one line of telemetry every second.", "Everything"],
            ["13", "selftest", "Runs a check of every part on power-up and prints PASS or the name of the fault, so a dead board is diagnosed in seconds.", "Everything"],
        ],
        widths=["6%", "17%", "57%", "20%"],
    )
    + callout(
        "One line to remember",
        "The largest of these thirteen programs compiles to 3.4 kilobytes, "
        "which is well under half of the 8 KB of flash in the chip, and uses "
        "30 bytes of the 256 available. The constraint on this board was never "
        "memory. It was pins &#8212; see page 8.",
    )
))

# ---------------------------------------------------------------- 7 the pins
add(page(
    "Where the software touches the metal",
    "The join",
    lead(
        "The chip has forty legs. Thirty-two of them are general-purpose "
        "input/output pins, arranged in four groups of eight called "
        "<b>P0</b>, <b>P1</b>, <b>P2</b> and <b>P3</b>. Every single thing "
        "the software does to the outside world is done by driving one of "
        "those thirty-two pins to 5 V or to 0 V, or by reading which of the "
        "two it currently is."
    )
    + table(
        ["Pin", "Name in the code", "What happens when the code drives it"],
        [
            ["P0.0 &#8211; P0.7", "BUS", "The eight shared data lines. Whatever number is on the bus right now is visible to the LEDs, the display, the LCD and the ADC all at once."],
            ["P1.0 &#8211; P1.7", "SWITCH", "Reads the eight DIP switches. A closed switch pulls the pin to 0 V."],
            ["P2.0", "LED_LE", "Pulsed high to open the LED latch, which grabs the number on the bus and holds it."],
            ["P2.1", "SEG_LE", "Pulsed high to open the display latch, same idea for the seven-segment digits."],
            ["P2.2", "LCD_E", "Tells the LCD that the byte sitting on the bus is ready to be accepted."],
            ["P2.3", "LCD_RS", "Selects whether that byte is a command, such as clear the screen, or a character to print."],
            ["P2.5 / P2.6", "ADC_WR / ADC_RD", "Pulses that tell the converter to start a reading, then to hand the answer over."],
            ["P2.7", "ADC_INTR", "Read, not driven. The converter pulls this low when the answer is ready."],
            ["P3.2", "PB_EMERG", "The emergency stop button, wired to interrupt 0 so it is answered immediately."],
            ["P3.3", "PB_MODE", "The reset button, wired to interrupt 1, clears the emergency state."],
            ["P3.4", "RELAY", "5 V here energises the relay coil. The click is this pin changing state."],
            ["P3.5", "BUZZER", "5 V here sounds the buzzer."],
            ["P3.6 / P3.7", "DIG1 / DIG2", "Chooses which of the two digits is lit at this instant."],
        ],
        widths=["18%", "21%", "61%"],
    )
    + h2("And in the code itself, that is this")
    + '<pre class="code">'
    + htmllib.escape(BUS_PUT_SRC or "void bus_put(unsigned char v)\n{\n    bus_shadow = v;\n    BUS = v;\n}")
    + "</pre>"
    + p(
        "That is the whole trick. <code>bus_put()</code> remembers the number "
        "in a variable and pushes it out onto the eight pins of port 0. Then "
        "one more line pulses a gate pin, and whichever device owns that gate "
        "takes the number and keeps it. Everything else in the thirteen "
        "programs is built on those two moves."
    )
))

# ---------------------------------------------------------------- 8 the problem
add(page(
    "The problem: 54 wires, 32 pins",
    "Constraint",
    lead(
        "Here is the difficulty that shaped the entire design, and the one "
        "question worth being ready for. Count the connections the finished "
        "board needs, then count the pins the chip has."
    )
    + table(
        ["What needs connecting", "Wires it would want"],
        [
            ["LED bank, eight lights", "8"],
            ["Seven-segment display, seven segments plus the decimal point", "8"],
            ["Character LCD, its data lines", "8"],
            ["Analogue-to-digital converter, its data lines", "8"],
            ["DIP switch bank, eight inputs", "8"],
            ["Subtotal for data alone, with every device private", "40"],
            ["Control and strobe lines: two latch gates, three LCD lines, three converter lines", "8"],
            ["Relay, buzzer, two buttons, two digit selects", "6"],
            ["<b>Total the design needs</b>", "<b>54</b>"],
            ["<b>Free input/output pins on the chip, P0 to P3</b>", "<b>32</b>"],
            ["<b>Shortfall</b>", "<b>22</b>"],
        ],
        widths=["72%", "28%"], cls="bar",
    )
    + h2("Three ways out, and why we chose the third")
    + table(
        ["Option", "What it costs", "Verdict"],
        [
            ["Buy a bigger chip, such as one with 60 pins", "A new part, a new package, a printed circuit board, a reflow process, and it stops being a breadboard project.", "Rejected"],
            ["Add port expander chips on a serial bus", "Two extra ICs, roughly 250 rupees, and every output update becomes several slow serial transactions.", "Rejected"],
            ["Share one set of eight pins between the four data devices, with a gate per device", "Free. Costs a few microseconds per update and demands disciplined code.", "<b>Chosen</b>"],
        ],
        widths=["38%", "44%", "18%"], cls="bar",
    )
    + callout(
        "The one sentence",
        "The board could not afford 54 private wires, so the eight lines of "
        "port 0 became a single shared road, and four spare pins became the "
        "gates that decide who is listening. That decision is the project.",
        tone="green",
    )
))

# ---------------------------------------------------------------- 9 the fix
add(page(
    "The fix: one road, many gates",
    "Architecture",
    lead(
        "A latch is a chip that copies the eight numbers on its input and "
        "keeps holding them on its output until told to change. Put one latch "
        "in front of each device and a fascinating thing becomes possible: all "
        "four devices can watch the same eight wires, and only the one whose "
        "gate is opened takes any notice."
    )
    + fig(
        "concept-shared-bus.png",
        "One eight-line bus leaves the chip and runs past four devices. Each "
        "device has its own gate. Exactly one gate is open at any moment, "
        "shown here in green; the other three are closed and ignore whatever "
        "is on the road.",
        width="168mm",
    )
    + h2("Writing to a device takes four moves")
    + steps([
        "Put the number on the shared bus: <code>bus_put(0x55)</code>. All "
        "four devices see it, and all four ignore it, because their gates are "
        "shut.",
        "Pulse the gate of the device you actually want: <code>LED_LE = 1</code> "
        "then immediately <code>LED_LE = 0</code>.",
        "The latch behind that gate captures the number in that instant and "
        "goes back to ignoring the bus.",
        "Move on. The LEDs stay showing 0x55 while the bus runs off to update "
        "the display, the LCD or anything else.",
    ], cls="tight")
    + table(
        ["Device", "Its gate pin", "Called in the code"],
        [
            ["LED bank", "P2.0", "LED_LE"],
            ["Seven-segment display", "P2.1", "SEG_LE"],
            ["Character LCD", "P2.2", "LCD_E"],
            ["Analogue-to-digital converter", "P2.5 and P2.6", "ADC_WR and ADC_RD"],
        ],
        widths=["38%", "22%", "40%"], cls="bar",
    )
    + callout(
        "What sharing costs, honestly",
        "Two things. First, speed: four devices can no longer be updated at "
        "once, only one after another. At a microsecond per device that is "
        "irrelevant here. Second, discipline: the code must always know which "
        "device last had its gate open, and must never leave two gates open "
        "together. That is why every output goes through one small set of "
        "functions in <code>board.h</code> rather than being written "
        "directly.",
        tone="amber",
    )
))

# ---------------------------------------------------------------- 10 the loop
add(page(
    "The loop: read, convert, decide, act",
    "Behaviour",
    lead(
        "Once the wiring problem is solved, the behaviour is simple. Every "
        "program on this board, including the largest one, is the same four "
        "beats repeated forever. Program 12, the finished industrial monitor, "
        "is the clearest example."
    )
    + fig(
        "concept-control-loop.png",
        "The four beats, clockwise: the sensor measures, the converter turns "
        "the measurement into a number, the code decides what that number "
        "means, and the outputs move. Then it starts again.",
        width="118mm",
    )
    + steps([
        "<b>Read.</b> Every five milliseconds a timer interrupt fires and "
        "refreshes one digit of the display. Every time the main loop comes "
        "round, the code asks the converter for a temperature reading and the "
        "switches for their positions.",
        "<b>Convert.</b> The converter returns a whole number from 0 to 255. "
        "The code multiplies it by 250 and divides by 32, which turns it into "
        "tenths of a degree. So a reading of 128 means 40.0 degrees.",
        "<b>Decide.</b> Below 40.0 degrees is the safe zone. From 40.0 to "
        "69.9 is the warning zone. At 70.0 and above is the danger zone. The "
        "emergency button overrides all three.",
        "<b>Act.</b> Write the LED pattern, refresh a digit, update the two "
        "LCD lines, and once every second print a full line of telemetry to "
        "the PC. Then start again.",
    ])
    + table(
        ["Zone", "Temperature", "LEDs lit", "Relay", "Buzzer", "Second LCD line"],
        [
            ["SAFE", "below 40.0 &#176;C", "green", "off", "off", "SAFE &#160;&#160;&#160;&#160;FAN:OFF"],
            ["WARNING", "40.0 to 69.9 &#176;C", "yellow", "on", "off", "WARNING FAN:ON"],
            ["DANGER", "70.0 &#176;C and above", "red", "on", "on", "DANGER &#160;FAN:ON"],
            ["EMERGENCY", "any temperature", "red, flashing", "off", "on", "EMERGENCY STOP"],
        ],
        widths=["14%", "21%", "16%", "10%", "10%", "29%"], cls="bar",
    )
    + p(
        "The sixth LED, the heartbeat, toggles once per second independently "
        "of all of this. It is there so that anyone can tell at a glance that "
        "the program is still running and has not hung."
    )
))

# ---------------------------------------------------------------- 11 build 1
add(page(
    "Building it, part one: power to display",
    "Assembly 1 of 2",
    lead(
        "The board is built in stages, and the order matters: each stage is "
        "tested on its own before the next part is added, so a fault is always "
        "in the part you just fitted. Nothing here is soldered."
    )
    + steps([
        "<b>Stage 0 &#8212; the bench.</b> A clean, dry, non-conductive "
        "surface, a 9 V adapter, and the parts sorted and counted against the "
        "bill of materials first. Counting the parts first saves an hour later.",
        "<b>Stage 1 &#8212; power, alone.</b> The barrel jack, the protection "
        "diode, the 7805 regulator on its heatsink and its capacitors. This is "
        "built and measured before anything else is plugged in, because every "
        "other part depends on a clean 5 V.",
        "<b>Stage 2 &#8212; the minimum system.</b> The chip, the 11.0592 MHz "
        "crystal with its two 33 pF capacitors, the reset circuit and the EA "
        "strap tied high. With only these fitted and no program at all, the "
        "chip is already a running computer.",
        "<b>Stage 3 &#8212; the LED bank.</b> The latch, the pull-up resistor "
        "network, eight 470 ohm resistors and the eight LEDs. Program 01 is "
        "burned in at this point: if eight LEDs blink, the clock, the bus and "
        "the latch all work.",
        "<b>Stage 4 &#8212; the switches.</b> The eight-way DIP switch, its "
        "pull-up network and the interrupt buttons. Program 03 turns this into "
        "the first two-way conversation: read a switch, light an LED.",
        "<b>Stage 5 &#8212; the display.</b> The second latch, the digit "
        "driver transistors and the two-digit display. Program 04 counts 00 to "
        "99, which proves the 5 ms timer interrupt is running.",
    ])
    + grid([
        card("regulator-7805.jpg", "Stages 0 to 1",
             "Power first, on its own, measured with a meter before anything "
             "else is fitted."),
        card("mcu-at89s52.jpg", "Stage 2",
             "Chip, crystal and reset. With only these three things the board "
             "is a working computer."),
        card("dipswitch.jpg", "Stages 3 to 5",
             "Outputs, then inputs, then the display: each stage is proved "
             "with its own program before the next begins."),
    ], n=3)
))

# ---------------------------------------------------------------- 12 build 2
add(page(
    "Building it, part two: talking to the world",
    "Assembly 2 of 2",
    lead(
        "The second half of the build adds everything that lets the board "
        "communicate: with a person, through the display and the buzzer; with "
        "a PC, down a cable; and with the physical world, through the relay."
    )
    + steps([
        "<b>Stage 6 &#8212; the serial link.</b> The MAX232 level converter "
        "and its four capacitors, then the nine-pin connector. The chip's "
        "serial port speaks 5 V logic; a PC serial port expects plus and minus "
        "12 V. This chip does the translating, in both directions.",
        "<b>Stage 7 &#8212; the temperature input.</b> The ADC0804, its "
        "reference divider, its resistor and capacitor clock, and the LM35 "
        "sensor. Program 10 is burned in and the reading is compared against a "
        "real thermometer.",
        "<b>Stage 8 &#8212; the LCD.</b> The module on a removable header, its "
        "contrast potentiometer and its current-limiting resistor. Program 11 "
        "draws the temperature as a number and as a growing bar.",
        "<b>Stage 9 &#8212; the relay and buzzer.</b> The driver transistor, "
        "the back-EMF protection diode across the coil, the relay itself, the "
        "jumper that frees the pin for the square-wave test, and the buzzer.",
        "<b>Stage 10 &#8212; final checkout.</b> Program 13 is burned in and "
        "runs a self-test of every part in turn, printing PASS or naming the "
        "fault. Then program 12 goes in and stays in.",
    ])
    + grid([
        card("adc0804.jpg", "Stages 6 to 7",
             "The serial link to the PC, then the converter and the sensor "
             "that give the board something to think about."),
        card("lcd-16x2.jpg", "Stage 8",
             "The LCD turns numbers into something a person can read without "
             "a PC attached."),
        card("relay.jpg", "Stage 9",
             "The relay and buzzer: the point where the board stops being a "
             "display and starts doing something."),
    ], n=3)
    + callout(
        "Why build in this order",
        "Power, then the chip, then outputs, then inputs, then communication, "
        "then the load. Every stage can be tested with the parts already "
        "fitted, so a fault is always in the last thing you added. Building it "
        "all at once and testing at the end is the single most common reason "
        "student boards do not work.",
        tone="green",
    )
))

# ---------------------------------------------------------------- 13 press
add(page(
    "What happens when you press the button",
    "Walkthrough 1 of 2",
    lead(
        "This is the question to be ready for, because it tests whether you "
        "understand the machine rather than just the diagram. Here is the "
        "emergency stop button, from fingertip to buzzer, in order, with "
        "times."
    )
    + steps([
        "<b>You press PB1.</b> The button connects pin 12 of the chip, P3.2, "
        "straight to ground. The voltage on that pin falls from 5 V to 0 V.",
        "<b>The chip notices, within a microsecond.</b> That pin is wired to "
        "external interrupt 0, and the code has configured it to trigger on a "
        "falling edge. The processor finishes the instruction it is in the "
        "middle of, saves its place, and jumps straight to the interrupt "
        "routine. Nothing else has to be polled or waited for.",
        "<b>The routine does one thing.</b> It sets a flag called "
        "<code>emergency</code> to 1 and returns. Interrupt routines are kept "
        "this short on purpose; the actual work happens in the main loop.",
        "<b>The main loop picks the flag up</b> on its very next pass, which "
        "is within a few hundred microseconds. From here on the emergency "
        "state wins every decision.",
        "<b>The relay is dropped out.</b> Whatever the temperature is, the "
        "relay pin is driven low. The load it was switching is disconnected. "
        "This is the whole point of the button.",
        "<b>The buzzer is driven on</b> and the red alarm LED lights, "
        "overriding the green or yellow that was showing.",
        "<b>The LCD changes.</b> Line two is overwritten with EMERGENCY STOP. "
        "The temperature on line one keeps updating, so the reading is not "
        "lost.",
        "<b>The next telemetry line</b> to the PC reports the zone as "
        "EMERGENCY with the relay off and the buzzer on, so the log shows "
        "exactly what happened and when.",
        "<b>You press PB2.</b> That is interrupt 1. It clears the flag, the "
        "buzzer stops, and normal temperature control resumes immediately from "
        "the current reading.",
    ])
    + fig(
        "display-7seg-2.jpg",
        "Through all of this the two-digit display keeps showing the live "
        "temperature. The display is refreshed by a timer interrupt that the "
        "main loop can never block.",
        width="46mm", cls="avoid",
    )
))

# ---------------------------------------------------------------- 14 hot
add(page(
    "What happens when the room gets hot",
    "Walkthrough 2 of 2",
    lead(
        "The second question worth having ready. This one crosses from the "
        "physical world into numbers and back out again, which is exactly what "
        "an embedded system is for. Suppose the air around the sensor warms to "
        "45 degrees Celsius."
    )
    + steps([
        "<b>The sensor feels it.</b> The LM35 is built to produce 10 "
        "millivolts for every degree. At 45 degrees its output leg carries "
        "450 millivolts. That is a real, measurable voltage on a piece of "
        "wire.",
        "<b>The converter is given a reference.</b> A trimmed divider holds "
        "the converter's reference pin at exactly 1.000 volt, which makes each "
        "of its 256 steps worth 7.8125 millivolts. This was chosen "
        "deliberately: with the default 5 V reference each step would be "
        "1.95 degrees, and most of the scale would be wasted on temperatures "
        "the sensor can never see.",
        "<b>The chip asks for a reading.</b> It pulses the write pin, the "
        "converter takes about 114 microseconds, then pulls its interrupt pin "
        "low to say the answer is ready. The chip pulses the read pin and the "
        "answer appears on the shared bus: 450 divided by 7.8125 is roughly "
        "58.",
        "<b>The code turns 58 into degrees.</b> It multiplies by 250 and "
        "divides by 32, which gives 453, meaning 45.3 degrees, carried "
        "throughout as tenths so that no decimal arithmetic is ever needed on "
        "a chip with no floating-point unit.",
        "<b>The decision is three comparisons.</b> 453 is not below 400, so "
        "it is not the safe zone. It is below 700, so it is the warning zone. "
        "The relay is switched on, the buzzer stays off, the yellow LED "
        "lights.",
        "<b>The outputs move.</b> The LED pattern is assembled as a set of "
        "bits and pushed through the latch. The display is given the number "
        "45. The LCD prints T=45.3C on line one and WARNING FAN:ON on line "
        "two.",
        "<b>One line goes upstairs.</b> Every second the serial port sends "
        "T=45.3C ADC=58 ZONE=WARNING FAN=1 BUZ=0, which a terminal on the PC "
        "can log to a file.",
        "<b>And it starts again.</b> Cross 70 degrees and the red LED and the "
        "buzzer join in. This is why the heartbeat LED matters: it proves the "
        "loop is still turning even when nothing else changes.",
    ])
    + callout(
        "The sentence that answers both walkthroughs",
        "A voltage becomes a number, the number becomes a decision, and the "
        "decision becomes a voltage again. That is what an embedded system "
        "is, and this board does it in about a hundred microseconds.",
        tone="green",
    )
))

# ---------------------------------------------------------------- 15 testing
add(page(
    "How we checked it was right",
    "Verification",
    lead(
        "Building a board that lights up is not the same as building one that "
        "is correct. Every claim on this project is tied to a measurement with "
        "a number and a tolerance, taken with the two instruments below."
    )
    + '<table class="split"><tr>'
    '<td class="l">' + fig("multimeter.jpg",
                           "The multimeter answers: is the voltage what it "
                           "should be? Supply rails, the trimmed reference, "
                           "sensor output and current draw are all measured "
                           "with it.") + "</td>"
    '<td class="r">' + fig("oscilloscope.jpg",
                           "The oscilloscope answers: is the timing what it "
                           "should be? The 1.00 kHz square wave, the serial "
                           "bit width and the display refresh are all checked "
                           "on it.") + "</td></tr></table>"
    + table(
        ["#", "Check", "How it is done", "What should happen"],
        [
            ["T2", "Supply rails", "Meter on the regulator output, the chip's VCC pin and the converter's VCC pin", "5.00 V, plus or minus 0.15 V, at all three"],
            ["T3", "LED timing", "Burn program 01, time ten flashes with a stopwatch", "Ten flashes in 10.0 seconds, plus or minus 0.3 s"],
            ["T5", "Display count", "Burn program 04, time the count from 00 to 99", "50 seconds, plus or minus 2 s"],
            ["T6", "One second timing", "Burn program 05, time ten LED transitions", "Ten transitions in 10.0 seconds, plus or minus 0.2 s"],
            ["T7", "Square wave", "Scope on pin P3.4 with the relay jumper removed", "1.00 kHz, within 20 Hz, at 50 percent duty"],
            ["T9", "Serial link", "Short pins 2 and 3 of the connector and type characters", "Every character comes back, none corrupted"],
            ["T11", "Temperature accuracy", "Compare against a reference thermometer from 25 to 60 degrees", "Within 1.5 degrees at every point"],
            ["T13", "Zone thresholds", "Warm the sensor slowly and watch the LEDs", "Green below 40.0, yellow from 40.0, red at 70.0 and above"],
            ["T15", "Emergency stop", "Press PB1 while the board is running normally", "Relay drops out, buzzer sounds, LCD shows EMERGENCY STOP"],
            ["T18", "Current draw", "Ammeter in series with the 9 V supply, relay off", "Below 200 mA"],
            ["T19", "Regulator heat", "Run for fifteen minutes, then touch the heatsink", "Warm but holdable, under about 60 degrees"],
            ["T20", "Supply rejection", "Vary the input from 7 V to 12 V", "5 V rail stays between 4.90 and 5.10 V, no reset"],
        ],
        widths=["5%", "17%", "40%", "38%"], cls="bar",
    )
))

# ---------------------------------------------------------------- 16 numbers
add(page(
    "The numbers",
    "Results",
    lead(
        "These are the measured figures for the finished board. Each one is "
        "the answer to a test in the procedure, not an estimate, and each one "
        "comes with a short reason why it came out that way."
    )
    + stats([
        ("0.00 %", "Serial baud error at 9600"),
        ("1.00 kHz", "Timer output, +0.17 % error"),
        ("100 Hz", "Display refresh, per digit"),
        ("0.78 &#176;C", "Temperature resolution per step"),
        ("157 mA", "Board current, relay off"),
        ("3.4 KB", "Largest program of 8 KB flash"),
    ])
    + table(
        ["Measured", "Value", "Why it came out that way"],
        [
            ["Baud error", "0.00 %", "11.0592 MHz divides exactly by 384 and by 9600, so the timer reload is a whole number, 0xFD."],
            ["Square wave", "1.00 kHz, +0.17 %", "Reload value 0xFE34 with a 1.0851 microsecond machine cycle. The residual error is the interrupt response time."],
            ["Display refresh", "100 Hz", "A 5 ms timer interrupt refreshes one digit, so a full pair takes 10 ms. Fast enough that the eye sees both as solid."],
            ["ADC resolution", "7.8125 mV, 0.78 &#176;C", "The reference pin is trimmed to 1.000 V rather than left at 5 V, which spends the whole scale on 0 to 200 degrees."],
            ["Board current", "157 mA, 274 mA peak", "Eight LEDs at 7 mA, the display, the LCD and the logic. The peak is with the relay coil energised."],
            ["Program size", "3.4 KB, 30 B RAM", "Largest of the thirteen. Memory was never the constraint on this board; pins were."],
            ["Component count", "80 parts", "Through-hole, hand placeable, no printed circuit board and no surface-mount work."],
            ["Cost", "about INR 985", "Per board, at single-unit prices. A full setup with adapter and programmer is about INR 1,715."],
        ],
        widths=["19%", "18%", "63%"], cls="bar",
    )
    + callout(
        "If you are asked which number you are proudest of",
        "The baud error of 0.00 per cent. It is not luck: it is the direct "
        "result of choosing an 11.0592 MHz crystal instead of a rounder 12 MHz "
        "one, and it is the clearest example in the project of a hardware "
        "choice made in order to make the software simple.",
    )
))

# ---------------------------------------------------------------- 17 glossary
add(page(
    "Plain-English glossary",
    "Reference",
    lead(
        "Every technical term used in this guide, in the order it is likely to "
        "come up. If you can say each of these out loud in one plain sentence, "
        "you can present any part of this project."
    )
    + table(
        ["Term", "What it means here"],
        [
            ["Microcontroller", "A complete small computer in one chip: processor, program memory, working memory and input/output pins. This one is an Atmel AT89S52."],
            ["8051", "The family of chip design this belongs to, created in 1980 and still made today. Code written for one 8051 generally runs on another."],
            ["Pin", "One of the forty metal legs of the chip. Software affects the world only by setting a pin to 5 V or 0 V, or reading which it is. They are handled in four groups of eight, called ports P0 to P3, giving thirty-two in total, every one of them shared between several jobs."],
            [".hex file", "The compiled program, written as a text file of machine bytes in Intel hex format. This is the file the programmer burns into the chip."],
            ["Flash memory", "The 8 KB of memory inside the chip that holds the program. It keeps its contents with the power off and can be rewritten hundreds of times. Variables live in 256 bytes of RAM, which is wiped at every power-off."],
            ["Compiler", "The tool that turns the C you typed into machine bytes the chip can execute. Here it is the C51 compiler inside Keil uVision."],
            ["Programmer", "The small USB board that copies the .hex file from the PC into the chip's flash memory."],
            ["Crystal", "The 11.0592 MHz part that sets the chip's heartbeat. Every instruction and every delay is counted in these ticks."],
            ["Machine cycle", "1.0851 microseconds at this clock speed. Twelve crystal ticks make one machine cycle, and most instructions take one or two of them."],
            ["Bus", "A set of wires shared by several devices. Here, eight wires carry data to the LEDs, the display, the LCD and the converter in turn."],
            ["Latch", "A chip that copies the eight values on its input and keeps holding them on its output until told to change. This is what makes sharing a bus possible."],
            ["Strobe / gate", "A single pin that tells one latch to open and capture what is on the bus right now. Four gates, four devices, one bus."],
            ["Pull-up resistor", "A resistor that holds a pin gently at 5 V so that it never floats at an undefined voltage. The switches pull it down to 0 V against it."],
            ["Current-limiting resistor", "The 470 ohm resistor in series with each LED. Without it the LED would draw unlimited current and burn out."],
            ["ADC", "Analogue-to-digital converter. Measures a voltage and reports it as a whole number, here from 0 to 255."],
            ["Reference voltage", "The voltage the converter measures against. Trimmed to 1.000 V here, which sets the step size and therefore the accuracy."],
            ["Interrupt", "A signal that makes the chip stop what it is doing immediately and run a short routine, called an ISR. Kept short so the main loop is never delayed. Used here for the buttons and for the display refresh."],
            ["Timer", "A hardware counter inside the chip that can be set to interrupt after an exact number of microseconds. Used for the 5 ms display tick and the 1.00 kHz output."],
            ["UART", "The chip's built-in serial port. Sends and receives bytes one bit at a time down a single wire in each direction."],
            ["Baud rate", "How many bits per second the serial link sends. 9600 here, meaning one character every 1.04 milliseconds."],
            ["MAX232", "The chip that converts the 0 V and 5 V of the chip's serial port into the plus and minus 12 V a PC serial port expects."],
            ["Relay", "An electrically operated switch. 5 V on a chip pin lets it switch a mains-voltage load. It clicks audibly when it changes."],
            ["Back-EMF diode", "The diode across the relay coil. When the coil switches off it generates a large voltage spike, and this diode absorbs it before it can damage the driver."],
            ["Regulator", "The 7805, which turns the 9 V from the adapter into a steady 5 V. The extra 4 V leaves as heat, hence the heatsink."],
        ],
        widths=["20%", "80%"], cls="bar gloss",
    )
))

# ---------------------------------------------------------------- 18 present
add(page(
    "How to present this project",
    "Delivery",
    lead(
        "Keep a copy of this page in front of you during a viva. The "
        "difference between a good demonstration and a bad one is almost "
        "always having the short version ready."
    )
    + h2("The thirty-second version")
    + callout(
        "Say this first",
        "This board monitors temperature using an 8051 microcontroller and "
        "controls a relay and a buzzer based on three zones. The interesting "
        "part is that the design needed 54 connections and the chip only has "
        "32 pins available, so I shared one eight-bit bus between four devices "
        "using a latch and a gate pin for each. The software is thirteen small "
        "Keil C programs, the largest 3.4 kilobytes, and everything it does is "
        "read a sensor, convert it to a number, decide, and move an output. "
        "Shall I start the board?",
        tone="green",
    )
    + h2("Then the two-minute version, in four beats")
    + steps([
        "<b>Show the board, not the slides.</b> Point at the parts in order: "
        "chip, crystal, LEDs, display, LCD, sensor, relay. Say what each does "
        "in one sentence. Thirty seconds.",
        "<b>State the constraint.</b> 54 wires needed, 32 pins available. Name "
        "the two options you rejected and why. Thirty seconds.",
        "<b>Explain the fix.</b> One shared bus, four gates, one open at a "
        "time. Draw it on paper if you can. This is the part that earns the "
        "marks. Forty seconds.",
        "<b>Demonstrate.</b> Program 12 running. Warm the sensor with a finger "
        "and watch the zone change. Press the emergency button. Show the "
        "telemetry on the PC. Twenty seconds.",
    ], cls="tighter")
    + h2("Five questions you will be asked")
    + table(
        ["Question", "Answer in one or two sentences"],
        [
            ["Why not use a bigger chip?", "It would need a printed circuit board and surface-mount soldering, and it would stop being a breadboard project. The constraint was the point."],
            ["Why not add port expanders?", "Two more chips and about 250 rupees, and every update becomes a slow serial transaction. Sharing cost nothing but a few microseconds."],
            ["Why 11.0592 MHz and not 12?", "Because it divides exactly by 9600, so the serial baud rate has literally zero error. With 12 MHz the error is over 8 per cent and the link fails."],
            ["How accurate is the temperature?", "0.78 degrees per step, and within 1.5 degrees of a reference thermometer across 25 to 60 degrees. That comes from trimming the converter reference to 1.000 V."],
            ["What would you do differently?", "Move to a printed circuit board with a ground plane, and use a digital-output sensor to remove the converter and its reference entirely."],
        ],
        widths=["26%", "74%"], cls="bar",
    )
    + h2("Where every file lives")
    + table(
        ["Folder", "What is in it"],
        [
            ["firmware/src", "The thirteen C programs, 01 to 13"],
            ["firmware/inc/board.h", "Every pin, every constant and every shared function, in one place"],
            ["firmware/keil", "A ready-to-open Keil uVision project for each program, for both the AT89S52 and the AT89C51"],
            ["hardware/BOM.csv", "All 80 parts with quantities and prices"],
            ["hardware/SCHEMATIC.md", "Every connection, written out pin by pin"],
            ["hardware/ASSEMBLY.md", "The ten build stages in full detail"],
            ["hardware/TESTING.md", "All twenty tests with their expected results"],
            ["docs/", "The seven-slide review deck and this guide"],
        ],
        widths=["28%", "72%"], cls="bar files",
    )
))

# ------------------------------------------------------------------ build

def build():
    doc = (
        '<!DOCTYPE html><html><head><meta charset="utf-8">'
        "<title>8051 Hardware Lab - How It Works</title>"
        "<style>%s</style></head><body>%s</body></html>"
        % (CSS, "\n".join(PAGES))
    )
    if not os.path.isdir(GUIDE):
        os.makedirs(GUIDE)
    with open(OUT_HTML, "w") as fh:
        fh.write(doc)

    from weasyprint import HTML
    HTML(string=doc, base_url=ROOT).write_pdf(OUT_PDF)

    size = os.path.getsize(OUT_PDF)
    print("html: %s (%.1f KB)" % (OUT_HTML, len(doc) / 1024.0))
    print("pdf : %s (%.1f KB)" % (OUT_PDF, size / 1024.0))
    print("pages built: %d" % len(PAGES))


if __name__ == "__main__":
    build()
