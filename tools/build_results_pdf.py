#!/usr/bin/env python3
"""Build docs/8051_Results_Sheet.pdf - the two page A4 result sheet a reviewer
holds while the board is demonstrated.

Page 1 - what was built, the headline numbers with a blank Measured column.
Page 2 - the thirteen programs, the twenty tests, and a sign off block.

Run:  python3 tools/build_results_pdf.py
Deps: reportlab
"""

import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "8051_Results_Sheet.pdf")

# deck tokens
INK = colors.HexColor("#1E293B")
PAPER = colors.HexColor("#F1F5F9")
BLUE = colors.HexColor("#2563EB")
EMERALD = colors.HexColor("#10B981")
MUTED = colors.HexColor("#64748B")
LINE = colors.HexColor("#CBD5E1")

PAGE_W, PAGE_H = A4
M = 16 * mm

ss = getSampleStyleSheet()

S = {
    "eyebrow": ParagraphStyle(
        "eyebrow", parent=ss["Normal"], fontName="Courier-Bold", fontSize=7.2,
        textColor=BLUE, leading=9, spaceAfter=3),
    "h1": ParagraphStyle(
        "h1", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=19,
        textColor=INK, leading=22, spaceAfter=2),
    "sub": ParagraphStyle(
        "sub", parent=ss["Normal"], fontName="Helvetica", fontSize=10,
        textColor=MUTED, leading=13, spaceAfter=0),
    "meta": ParagraphStyle(
        "meta", parent=ss["Normal"], fontName="Helvetica", fontSize=7.6,
        textColor=INK, leading=10),
    "h2": ParagraphStyle(
        "h2", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=10.5,
        textColor=INK, leading=13, spaceBefore=7, spaceAfter=3),
    "body": ParagraphStyle(
        "body", parent=ss["Normal"], fontName="Helvetica", fontSize=8.2,
        textColor=INK, leading=11, alignment=TA_LEFT),
    "cell": ParagraphStyle(
        "cell", parent=ss["Normal"], fontName="Helvetica", fontSize=7.4,
        textColor=INK, leading=9),
    "cellb": ParagraphStyle(
        "cellb", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=7.4,
        textColor=INK, leading=9),
    "mono": ParagraphStyle(
        "mono", parent=ss["Normal"], fontName="Courier", fontSize=7.2,
        textColor=INK, leading=9),
    "note": ParagraphStyle(
        "note", parent=ss["Normal"], fontName="Helvetica-Oblique", fontSize=7,
        textColor=MUTED, leading=9),
}


def P(t, st="cell"):
    return Paragraph(t, S[st])


def rule(width, colour=BLUE, thick=1.4):
    t = Table([[""]], colWidths=[width], rowHeights=[thick])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colour),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t


def data_table(header, rows, widths, blank_rows=0, align_right=(), size=None):
    """A statistics-table style grid with an emerald header band."""
    body = [[P(h, "cellb") for h in header]]
    for r in rows:
        body.append([c if isinstance(c, Paragraph) else P(str(c)) for c in r])
    for _ in range(blank_rows):
        body.append(["" for _ in header])

    t = Table(body, colWidths=widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), PAPER),
        ("LINEBELOW", (0, 0), (-1, 0), 1.0, EMERALD),
        ("LINEBELOW", (0, 1), (-1, -1), 0.25, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
    ]
    for c in align_right:
        style.append(("ALIGN", (c, 0), (c, -1), "RIGHT"))
    t.setStyle(TableStyle(style))
    return t


# ------------------------------------------------------------------ page 1

def page_one():
    W = PAGE_W - 2 * M
    out = [
        rule(W, BLUE, 3),
        Spacer(1, 5 * mm),
        P("MINI PROJECT / MICROPROCESSORS AND MICROCONTROLLERS", "eyebrow"),
        P("8051 Hardware Lab", "h1"),
        P("Real-time embedded monitoring on the AT89S52 - result sheet", "sub"),
        Spacer(1, 4 * mm),
        P("ATHARVA (24BEL0082) &nbsp;&middot;&nbsp; ADITYA (24BEL0087) &nbsp;&middot;&nbsp; "
          "Electronics and Communication Engineering &nbsp;&middot;&nbsp; 2025-26", "meta"),
        Spacer(1, 1.5 * mm),
        P("Target AT89S52-24PU &nbsp;&middot;&nbsp; 11.0592 MHz &nbsp;&middot;&nbsp; "
          "8 KB flash &nbsp;&middot;&nbsp; 13 Keil C51 programs &nbsp;&middot;&nbsp; "
          "20 bench tests &nbsp;&middot;&nbsp; INR 985 per board", "meta"),
        Spacer(1, 4 * mm),
    ]

    out.append(P("What was built", "h2"))
    out.append(P(
        "A complete 8051 board: eight LEDs through a latch, an eight way DIP switch bank, a two "
        "digit seven segment display, a 16x2 HD44780 LCD, an LM35 through an ADC0804, a MAX232 "
        "serial link at 9600 8N1, a relay and a buzzer, and two interrupt buttons. The eight data "
        "lines of the LCD, the ADC and both output latches share one bidirectional bus on port 0, "
        "each device gated by its own strobe on port 2. <b>The peripherals require 54 I/O signals; "
        "the chip provides 32.</b> The 22 pin deficit is closed by architecture, with no port "
        "expander IC.", "body"))
    out.append(Spacer(1, 2 * mm))

    out.append(P("Headline results", "h2"))
    rows = [
        ["I/O pins utilised", "32 of 32", "&#160;", "no headroom"],
        ["Supply rail, U1 pin 40", "5.00 V", "&#160;", "4.85 - 5.15 V"],
        ["UART baud error", "0.00 %, TH1 = FDH", "&#160;", "no framing errors"],
        ["Display refresh", "100 Hz per digit", "&#160;", "95 - 105 Hz"],
        ["Timer output, P3.4", "1.00 kHz, FE34H", "&#160;", "980 - 1020 Hz"],
        ["One second tick", "1.000 s, timer 0", "&#160;", "+/- 0.2 s in 10 s"],
        ["ADC step", "7.8125 mV, Vref/2 = 1.000 V", "&#160;", "reference 0.99 - 1.01 V"],
        ["Temperature agreement", "0.78 C per step", "&#160;", "within 1.5 C, 25-60 C"],
        ["Zone trip points", "40.0 C and 70.0 C", "&#160;", "+0 / - 0.5 C"],
        ["Supply current", "157 mA typ, 274 peak", "&#160;", "under 200 mA"],
        ["Largest program", "13_selftest, 3.4 KB of 8 KB", "&#160;", "fits AT89S52 flash"],
    ]
    out.append(data_table(
        ["Quantity", "Designed value", "Measured", "Acceptance"],
        rows,
        [W * 0.24, W * 0.32, W * 0.14, W * 0.30],
        align_right=()))
    out.append(Spacer(1, 1.5 * mm))
    out.append(P("The Measured column is to be completed at the bench, in ink, during the review. "
                 "Every tolerance above is the one stated in hardware/TESTING.md.", "note"))

    out.append(Spacer(1, 3.5 * mm))
    out.append(P("Constraints and how each was closed", "h2"))
    cons = [
        ["C1", "32 pins for 54 signals",
         "peripherals dropped, or an expander IC added",
         "one 8-bit bus on P0, per-device strobes on P2"],
        ["C2", "P0 is open drain, cannot source",
         "the bus never reaches a valid logic 1",
         "RN1, a 10 k x 9 SIP network, pulls the bus up"],
        ["C3", "output latches cannot be read back",
         "a stale byte is latched into the wrong device",
         "bus_shadow variable, interrupts gated per transfer"],
        ["C4", "P1.5-P1.7 shared with the ISP lines",
         "in-circuit programming fails or is corrupted",
         "1 k series resistors, SW6-SW8 documented OFF"],
        ["C5", "8-bit ADC, 5 V default reference",
         "1.95 C per step, most of the range wasted",
         "Vref/2 trimmed to 1.000 V, giving 0.78 C"],
        ["C6", "no hardware debounce on the buttons",
         "one press registers as several interrupts",
         "5 ms resampling, edge triggered INT0 and INT1"],
    ]
    out.append(data_table(
        ["ID", "Constraint", "Consequence if ignored", "Mitigation implemented"],
        cons,
        [W * 0.05, W * 0.26, W * 0.32, W * 0.37]))

    out.append(Spacer(1, 3.5 * mm))
    out.append(P("Operating behaviour", "h2"))
    out.append(P(
        "On power-up the board runs its program from flash with no host attached. The full system "
        "program monitors temperature against three zones - green below 40.0 C, yellow 40.0 to "
        "69.9 C, red at 70.0 C and above - drives the zone LEDs, energises the relay at the trip "
        "point, sounds the buzzer, updates the LCD and display, and transmits one telemetry line "
        "per second at 9600 8N1. The emergency input removes the relay and forces the alarm state; "
        "the second input restores normal control. The relay is a low voltage demonstration load "
        "and is never connected to mains.", "body"))

    return out


# ------------------------------------------------------------------ page 2

def page_two():
    W = PAGE_W - 2 * M
    out = [
        rule(W, EMERALD, 3),
        Spacer(1, 4 * mm),
        P("VERIFICATION / ALL THIRTEEN PROGRAMS", "eyebrow"),
        P("What each program demonstrates", "h1"),
        Spacer(1, 2 * mm),
    ]

    programs = [
        ["01", "led_blink", "8 LEDs blink at 1 Hz; the board runs with no PC attached", "T3"],
        ["02", "led_patterns", "sweep, then AA/55 alternation, then binary count", "T3"],
        ["03", "switch_led", "each DIP switch lights its own LED, debounced", "T4"],
        ["04", "seg7_counter", "two digit display counts 00 to 99, no ghosting", "T5"],
        ["05", "timer0_second", "one count per second from the timer interrupt", "T6"],
        ["06", "square_wave", "1.00 kHz on P3.4, 50 % duty, JP1 removed", "T7"],
        ["07", "ext_interrupt", "PB1 alternates the pattern, one press one change", "T8"],
        ["08", "uart_echo", "every byte typed on the terminal is echoed", "T9"],
        ["09", "uart_commands", "HLP, LED FF, SEG NN, RLY 1, BUZ 1, TMP all respond", "T10"],
        ["10", "adc_7seg", "LM35 temperature in degrees C on the display", "T11"],
        ["11", "adc_lcd", "LCD shows temperature and a bar graph that tracks it", "T12"],
        ["12", "industrial_monitor", "zones, relay, buzzer, LCD, emergency, telemetry", "T13-17"],
        ["13", "selftest", "walks every subsystem, prints SELF TEST: PASS or FAIL", "T1, T17"],
    ]
    rows = [[a, "&#160;" + b, c, d, "PASS / FAIL"] for a, b, c, d in programs]
    out.append(data_table(
        ["#", "Program", "Result observed", "Test", "Verdict"],
        rows,
        [W * 0.05, W * 0.17, W * 0.52, W * 0.10, W * 0.16],
        align_right=()))
    out.append(Spacer(1, 1.5 * mm))
    out.append(P("All thirteen sources compile with 0 errors under Keil C51. The AT89S52 variants "
                 "of the projects are the flashable ones; the AT89C51 has no ISP interface.", "note"))

    out.append(Spacer(1, 3 * mm))
    out.append(P("Bench test summary", "h2"))
    tests = [
        ("T1", "power on self test", "PASS"),
        ("T2", "supply rails", "5.00 +/-0.15 V"),
        ("T3", "LED bank timing", "20 half cycles / 10 s"),
        ("T4", "DIP switch input", "LED lights, no retrigger"),
        ("T5", "7 segment counter", "50 +/-2 s for 00-99"),
        ("T6", "one second timing", "10 in 10.0 +/-0.2 s"),
        ("T7", "square wave", "1.00 kHz +/-20 Hz"),
        ("T8", "external interrupts", "no double triggering"),
        ("T9", "serial echo", "byte exact, no framing"),
        ("T10", "command shell", "HLP, LED FF, RLY 1"),
        ("T11", "ADC and LM35", "within 1.5 C"),
        ("T12", "LCD bar graph", "monotonic, tracks"),
        ("T13", "zone thresholds", "40.0 / 70.0 C"),
        ("T14", "relay control", "trips at 40.0 C"),
        ("T15", "emergency stop", "relay off, buzzer"),
        ("T16", "emergency reset", "normal control"),
        ("T17", "telemetry rate", "10 lines in 10 s"),
        ("T18", "current draw", "under 200 mA"),
        ("T19", "regulator thermals", "below 60 C"),
        ("T20", "supply rejection", "7-12 V in, 5 V out"),
    ]
    half = 10
    body = [["#", "Test", "Acceptance", "Result", "#", "Test", "Acceptance", "Result"]]
    for i in range(half):
        a = tests[i]
        b = tests[i + half]
        body.append([a[0], a[1], a[2], "&#160;", b[0], b[1], b[2], "&#160;"])
    t = Table([[P(c, "cellb") if r == 0 else P(str(c)) for c in row] for r, row in enumerate(body)],
              colWidths=[W * 0.045, W * 0.16, W * 0.16, W * 0.09,
                         W * 0.045, W * 0.16, W * 0.16, W * 0.18],
              repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PAPER),
        ("LINEBELOW", (0, 0), (-1, 0), 1.0, EMERALD),
        ("LINEBELOW", (0, 1), (-1, -1), 0.25, LINE),
        ("LINEAFTER", (3, 0), (3, -1), 0.75, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
    ]))
    out.append(t)

    out.append(Spacer(1, 4 * mm))
    out.append(P("Demonstration sequence", "h2"))
    out.append(P(
        "1. Cold power-up with no host attached: program 01, eight LEDs at 1 Hz, showing the "
        "program is resident in flash. &nbsp; 2. Power-on self test, program 13, all subsystems "
        "reported on the terminal. &nbsp; 3. Full system, program 12: temperature raised and then "
        "lowered across the 40.0 C threshold, so the relay energises and releases. &nbsp; "
        "4. Emergency input pressed and released, then normal control restored. &nbsp; "
        "5. Telemetry observed at one line per second.", "body"))

    out.append(Spacer(1, 4 * mm))
    out.append(P("Stated limits", "h2"))
    lim = [
        ["Bus", "shared P0 caps throughput to a few hundred kHz"],
        ["ADC", "one channel, 8-bit, about 114 us per sample"],
        ["Memory", "256 B RAM, no external data memory wired"],
        ["Interrupts", "two external sources, no priority nesting"],
        ["Relay", "demonstration load only, never mains connected"],
    ]
    out.append(data_table(
        ["Area", "Limit"],
        lim,
        [W * 0.14, W * 0.86]))

    out.append(Spacer(1, 5 * mm))
    sign = Table(
        [[P("Reviewed by", "cellb"), P("&#160;", "cell"), P("Signature / date", "cellb"), P("&#160;", "cell")],
         ["", "", "", ""]],
        colWidths=[W * 0.16, W * 0.40, W * 0.20, W * 0.24],
        rowHeights=[4.5 * mm, 9 * mm])
    sign.setStyle(TableStyle([
        ("LINEBELOW", (1, 1), (1, 1), 0.75, MUTED),
        ("LINEBELOW", (3, 1), (3, 1), 0.75, MUTED),
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ]))
    out.append(sign)
    out.append(Spacer(1, 2 * mm))
    out.append(rule(W, INK, 0.75))
    out.append(Spacer(1, 1.5 * mm))
    out.append(P("8051 Hardware Lab &nbsp;&middot;&nbsp; AT89S52 &nbsp;&middot;&nbsp; "
                 "13 programs &nbsp;&middot;&nbsp; 20 tests &nbsp;&middot;&nbsp; "
                 "github.com/AdityaRezan/8051-hardware-lab", "note"))
    return out


# ------------------------------------------------------------------ document

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Courier", 6.8)
    canvas.setFillColor(MUTED)
    canvas.drawString(M, 9 * mm,
                      "8051 HARDWARE LAB  /  RESULT SHEET  /  AT89S52")
    canvas.drawRightString(PAGE_W - M, 9 * mm, "PAGE %d OF 2" % doc.page)
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.4)
    canvas.line(M, 12.5 * mm, PAGE_W - M, 12.5 * mm)
    canvas.restoreState()


def build():
    doc = BaseDocTemplate(
        OUT, pagesize=A4,
        leftMargin=M, rightMargin=M, topMargin=M, bottomMargin=18 * mm,
        title="8051 Hardware Lab - Result Sheet",
        author="ATHARVA 24BEL0082, ADITYA 24BEL0087",
        subject="Results and verification, AT89S52 embedded monitoring board")
    frame = Frame(M, 18 * mm, PAGE_W - 2 * M, PAGE_H - M - 18 * mm, id="main",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="sheet", frames=[frame], onPage=footer)])

    story = page_one() + [PageBreak()] + page_two()
    doc.build(story)
    print("wrote", os.path.relpath(OUT, ROOT))


if __name__ == "__main__":
    build()
