#!/usr/bin/env python3
"""Scene definitions for the complete start to finish video.

Three acts: the software on the laptop, the hardware on the bench, and the six
wires that join them. Narration strings here are the single source of truth.

Code excerpts are read straight out of firmware/ at import time, so what the
video shows is always the real source.
"""

import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

OUT = "8051_Start_To_Finish.mp4"


def _lines(path):
    with open(os.path.join(ROOT, "firmware", path)) as fh:
        return [l.rstrip() for l in fh.read().splitlines()]


def _between(path, marker, count):
    ls = _lines(path)
    for i, l in enumerate(ls):
        if marker in l:
            return ls[i:i + count]
    return ls[:count]


BOARD_H = _lines("inc/board.h")[18:52]
MONITOR_C = _between("src/12_industrial_monitor.c", "raw = adc_read();", 30)

BUILD_LOG = [
    "Build target 'Target 1'",
    "compiling board.h...",
    "compiling 12_industrial_monitor.c...",
    "linking...",
    "Program Size: data=30.0 xdata=0 const=0 code=3402",
    "creating hex file from \"12_industrial_monitor\"...",
    "\"Objects\\12_industrial_monitor\" - 0 Error(s), 0 Warning(s).",
]

HEX_FILES = [
    ("01_led_blink.hex", "3,946 bytes"),
    ("05_timer0_second.hex", "4,210 bytes"),
    ("09_uart_commands.hex", "6,015 bytes"),
    ("11_adc_lcd.hex", "6,842 bytes"),
    ("12_industrial_monitor.hex", "7,164 bytes"),
    ("13_selftest.hex", "6,503 bytes"),
]

ROADMAP = [
    ("1", "SOFTWARE", "Keil C51 on the laptop", "board.h, 13 programs, .hex files"),
    ("2", "HARDWARE", "Eighty parts on the bench", "ten stages, each tested as it is built"),
    ("3", "COMBINE", "Six wires", "flash over SPI, then run the whole system"),
]

WIRING = [
    ("MOSI", "P1.5", "6", (220, 80, 80)),
    ("MISO", "P1.6", "7", (80, 160, 240)),
    ("SCK", "P1.7", "8", (240, 200, 70)),
    ("RESET", "RST", "9", (120, 210, 130)),
    ("VCC", "VCC", "40", (235, 90, 90)),
    ("GND", "GND", "20", (120, 120, 130)),
]

ZONE_ROWS = [
    ("SAFE", "t10 < 400", "below 40.0 C", "green, relay off"),
    ("WARNING", "t10 < 700", "40.0 to 69.9 C", "yellow, relay on"),
    ("DANGER", "otherwise", "70.0 C and above", "red, relay on, buzzer"),
]

SCENES = [
    # ------------------------------------------------------------------ 1
    {
        "id": "01",
        "label": "THE WHOLE JOURNEY",
        "narration": (
            "This video follows one project from an empty desk to a working "
            "machine, in three parts. First the software: installing the tools "
            "on a laptop, writing the code that defines every pin on the board, "
            "and compiling it into a file of machine bytes. Second the "
            "hardware: eighty components placed by hand on a breadboard, built "
            "in ten stages, each one tested before the next begins. Third the "
            "joining: putting those machine bytes into the chip through six "
            "wires, and watching the board come to life. Software, hardware, "
            "and the six wires that connect them."
        ),
        "beats": [
            {"kind": "panel", "panel": "roadmap", "t0": 0.00, "t1": 0.50,
             "rows": ROADMAP},
            {"kind": "image", "src": "bench-laptop.jpg", "t0": 0.50, "t1": 1.00,
             "zoom": [1.02, 1.14], "pan": [[0.50, 0.52], [0.48, 0.48]]},
        ],
    },
    # ------------------------------------------------------------------ 2
    {
        "id": "02",
        "label": "ACT ONE - INSTALLING THE TOOLS",
        "narration": (
            "Everything starts on the laptop. The toolchain is Keil C fifty "
            "one, the industry standard for the eight oh five one family, and "
            "it runs on Windows. Download it from the Keil product page, "
            "choose C fifty one, not M D K Arm, and install to the default "
            "path. Then create a project for the Atmel A T eighty nine S fifty "
            "two, set the crystal to eleven point zero five nine two megahertz, "
            "and point the include path at the folder holding board dot h. One "
            "warning before you write a line: the free evaluation version is "
            "capped at two kilobytes of code. Our largest program is three "
            "point four kilobytes. You will need a licensed machine for the "
            "final build."
        ),
        "beats": [
            {"kind": "panel", "panel": "desktop", "t0": 0.00, "t1": 0.34,
             "title": "C:\\Keil\\C51", "mode": "install",
             "lines": ["C51V961A.EXE", "Keil C51 Version 9.61",
                       "Device database: 8051", "Default path: C:\\Keil\\"]},
            {"kind": "panel", "panel": "ide", "t0": 0.34, "t1": 0.74,
             "title": "uVision5 - Options for Target", "tab": "AT89S52",
             "lines": [
                 "Device:      Atmel  AT89S52",
                 "Xtal (MHz):  11.0592",
                 "",
                 "Memory Model:      Small",
                 "Code Rom Size:     Large: 64K",
                 "Operating system:  None",
                 "",
                 "C51  Include Paths:  ..\\inc",
                 "C51  Optimization:   Level 8",
                 "",
                 "Output:  Create HEX File      [x]",
                 "         Name of Executable:  12_industrial_monitor",
                 "",
                 "// the crystal value matters: every delay and",
                 "// the 9600 baud rate are derived from it",
             ],
             "hl": [1]},
            {"kind": "panel", "panel": "notice", "t0": 0.74, "t1": 1.00,
             "title": "BEFORE YOU BUILD",
             "head": "The evaluation version is capped at 2 KB",
             "body": "Programs over 2048 bytes stop with FATAL ERROR L250. "
                     "This project's largest program is 3402 bytes."},
        ],
    },
    # ------------------------------------------------------------------ 3
    {
        "id": "03",
        "label": "ACT ONE - ONE HEADER HOLDS THE WHOLE BOARD",
        "narration": (
            "This is board dot h, and it is the contract between the software "
            "and the metal. Every pin, every constant and every shared function "
            "is declared here, once. Watch the sbit lines: those are the four "
            "gates, the LED latch, the display latch, the L C D enable, and the "
            "converter's read and write strobes. Below them, the relay, the "
            "buzzer, the two digit selects and the two buttons. Change a wire "
            "on the board and this is the only file you should have to touch. "
            "The rest of the code never mentions a pin number, it only ever "
            "calls a function from this file. That is what makes the shared bus "
            "safe to use."
        ),
        "beats": [
            {"kind": "panel", "panel": "ide", "t0": 0.00, "t1": 1.00,
             "title": "uVision5 - board.h", "tab": "board.h",
             "lines": BOARD_H,
             "hl": list(range(17, 34))},
        ],
    },
    # ------------------------------------------------------------------ 4
    {
        "id": "04",
        "label": "ACT ONE - WRITING A PROGRAM",
        "narration": (
            "With the header in place, a program is short. This is program "
            "twelve, the zone monitor, and this is the whole decision. Read the "
            "converter, multiply by two hundred and fifty and divide by thirty "
            "two to get tenths of a degree. Below four hundred, the safe zone. "
            "Below seven hundred, warning. Above that, danger. Then, unless the "
            "emergency flag is set, switch the relay on above forty degrees and "
            "sound the buzzer in the danger zone. That is the entire "
            "intelligence of the board: three comparisons and two outputs. "
            "Everything else on screen is reading, writing and waiting."
        ),
        "beats": [
            {"kind": "panel", "panel": "ide", "t0": 0.00, "t1": 0.70,
             "title": "uVision5 - 12_industrial_monitor.c",
             "tab": "12_industrial_monitor.c",
             "lines": MONITOR_C,
             "hl": [10, 11, 12, 13, 14, 15, 16]},
            {"kind": "panel", "panel": "zones", "t0": 0.70, "t1": 1.00,
             "rows": ZONE_ROWS},
        ],
    },
    # ------------------------------------------------------------------ 5
    {
        "id": "05",
        "label": "ACT ONE - BUILDING TO A HEX FILE",
        "narration": (
            "Press F seven and the toolchain does its work. The compiler turns "
            "the C into machine code for the eight oh five one, the linker "
            "places it starting at address zero, and the output lands in the "
            "Objects folder as a dot hex file. Intel hex format: the program "
            "written out as lines of text, each one a row of bytes with a "
            "checksum. This one is three thousand four hundred and two bytes, "
            "using under half of the eight kilobytes of flash in the chip. Note "
            "the memory report at the bottom. Thirty bytes of R A M. On a part "
            "like this, memory is never the problem. Pins are."
        ),
        "beats": [
            {"kind": "panel", "panel": "build", "t0": 0.00, "t1": 0.60,
             "title": "Build Output", "lines": BUILD_LOG},
            {"kind": "panel", "panel": "desktop", "t0": 0.60, "t1": 1.00,
             "title": "firmware\\keil\\Objects", "mode": "hex",
             "lines": ["%s    %s" % (a, b) for a, b in HEX_FILES]},
        ],
    },
    # ------------------------------------------------------------------ 6
    {
        "id": "06",
        "label": "ACT TWO - THE PARTS",
        "narration": (
            "Now the bench. Eighty components, all through hole, all placed by "
            "hand, no soldering. The microcontroller, eight indicator LEDs, a "
            "two digit seven segment display, a sixteen by two character L C D, "
            "an L M thirty five temperature sensor, an analogue to digital "
            "converter, a relay, a buzzer, eight switches, a crystal, a voltage "
            "regulator, and the breadboard that holds it together. Every part "
            "is listed in the bill of materials, and every part can be moved "
            "again in a second if you get it wrong. That is the whole reason "
            "for building it this way."
        ),
        "beats": [
            {"kind": "grid", "t0": 0.00, "t1": 1.00, "cols": 4, "rows": 3,
             "stagger": 0.055, "images": [
                 "mcu-at89s52.jpg", "leds.jpg", "display-7seg.jpg", "lcd-16x2.jpg",
                 "sensor-lm35.jpg", "adc0804.jpg", "relay.jpg", "crystal.jpg",
                 "regulator-7805.jpg", "dipswitch.jpg", "programmer-usbasp.jpg",
                 "multimeter.jpg",
             ]},
        ],
    },
    # ------------------------------------------------------------------ 7
    {
        "id": "07",
        "label": "ACT TWO - STAGE 1 TO 5",
        "narration": (
            "Build in order, and test at every step. Stage one is power, on its "
            "own: a nine volt adapter into a seventy eight oh five regulator "
            "holding five volts, measured before another part is fitted. "
            "Stage two is the minimum system: the chip, the crystal, the reset "
            "circuit. Nothing else, and it is already a running computer. Stage "
            "three adds the LED bank, and program zero one blinks them. If you "
            "see eight LEDs blinking, the clock, the bus and the latch all "
            "work. Stage four adds the switches. Stage five adds the display, "
            "and program zero four counts to ninety nine on a five millisecond "
            "timer interrupt."
        ),
        "beats": [
            {"kind": "image", "src": "board-stage-early.jpg", "t0": 0.00, "t1": 0.50,
             "zoom": [1.02, 1.18], "pan": [[0.42, 0.56], [0.50, 0.48]],
             "callouts": [
                 {"t": 0.12, "x": 0.30, "y": 0.68, "text": "STAGE 1 - 7805 REGULATOR, 5 V", "dir": "down"},
                 {"t": 0.55, "x": 0.58, "y": 0.44, "text": "STAGE 2 - AT89S52 AND CRYSTAL", "dir": "up"},
             ]},
            {"kind": "image", "src": "board-stage-mid.jpg", "t0": 0.50, "t1": 1.00,
             "zoom": [1.03, 1.16], "pan": [[0.55, 0.46], [0.46, 0.52]],
             "callouts": [
                 {"t": 0.18, "x": 0.36, "y": 0.40, "text": "STAGE 3 - LED BANK", "dir": "up"},
                 {"t": 0.52, "x": 0.63, "y": 0.62, "text": "STAGE 4 - DIP SWITCHES", "dir": "down"},
                 {"t": 0.80, "x": 0.42, "y": 0.30, "text": "STAGE 5 - 7-SEGMENT DISPLAY", "dir": "up"},
             ]},
        ],
    },
    # ------------------------------------------------------------------ 8
    {
        "id": "08",
        "label": "ACT TWO - STAGE 6 TO 10",
        "narration": (
            "Stage six is the serial link, with a MAX two three two translating "
            "between five volt logic and the plus and minus twelve volts a P C "
            "expects. Stage seven adds the sense of touch: the converter, its "
            "trimmed one volt reference, and the L M thirty five giving ten "
            "millivolts per degree. Stage eight fits the L C D. Stage nine fits "
            "the relay and the buzzer, where the board stops being a display "
            "and starts doing something. Stage ten is the self test, program "
            "thirteen, which checks every part in turn and prints PASS or names "
            "the fault. On eighty hand placed parts, that is worth an hour."
        ),
        "beats": [
            {"kind": "image", "src": "board-complete.jpg", "t0": 0.00, "t1": 0.44,
             "zoom": [1.05, 1.15], "pan": [[0.60, 0.40], [0.52, 0.46]],
             "callouts": [
                 {"t": 0.40, "x": 0.66, "y": 0.36, "text": "STAGE 6 - MAX232 SERIAL LINK", "dir": "up"},
                 {"t": 0.78, "x": 0.40, "y": 0.60, "text": "STAGE 7 - ADC AND LM35", "dir": "down"},
             ]},
            {"kind": "panel", "panel": "lcd", "t0": 0.44, "t1": 0.74, "zone": "warn",
             "rows": ["T=52.7C A= 67", "WARNING FAN:ON "]},
            {"kind": "image", "src": "board-complete.jpg", "t0": 0.74, "t1": 1.00,
             "zoom": [1.08, 1.16], "pan": [[0.38, 0.60], [0.44, 0.54]],
             "callouts": [
                 {"t": 0.35, "x": 0.32, "y": 0.56, "text": "STAGE 9 - RELAY AND BUZZER", "dir": "down"},
             ]},
        ],
    },
    # ------------------------------------------------------------------ 9
    {
        "id": "09",
        "label": "ACT THREE - THE SIX WIRES",
        "narration": (
            "Now the joining. The A T eighty nine S fifty two is programmed in "
            "circuit over S P I, through four signal pins plus power and "
            "ground: M O S I on P one point five, M I S O on P one point six, "
            "clock on P one point seven, and reset on pin nine. The crystal "
            "must already be fitted, because the chip needs a clock to accept "
            "programming. One trap: a stock U S B asp cannot do this. A V R "
            "chips reset on a low signal, the eight oh five one resets on a "
            "high one, so the wrong polarity leaves the chip silent. Use an "
            "Arduino running the Arduino I S P sketch, or a dedicated eight oh "
            "five one programmer. Then one command, and the bytes are in."
        ),
        "beats": [
            {"kind": "image", "src": "flash-wiring.jpg", "t0": 0.00, "t1": 0.30,
             "zoom": [1.03, 1.15], "pan": [[0.50, 0.50], [0.50, 0.48]]},
            {"kind": "panel", "panel": "wiring", "t0": 0.30, "t1": 0.66,
             "wires": WIRING},
            {"kind": "panel", "panel": "flash", "t0": 0.66, "t1": 0.88},
            {"kind": "image", "src": "programmer-usbasp.jpg", "t0": 0.88, "t1": 1.00,
             "zoom": [1.02, 1.10], "pan": [[0.50, 0.50], [0.50, 0.50]],
             "callouts": [
                 {"t": 0.30, "x": 0.50, "y": 0.72, "text": "STOCK USBASP USES THE WRONG RESET POLARITY", "dir": "down"},
             ]},
        ],
    },
    # ------------------------------------------------------------------ 10
    {
        "id": "10",
        "label": "ACT THREE - RUNNING",
        "narration": (
            "Press reset and the board runs what you wrote. Program twelve "
            "reads the temperature, decides the zone, and moves its outputs: "
            "green below forty degrees, yellow above it with the relay "
            "energised, red at seventy with the buzzer sounding. Every second "
            "it sends one line of telemetry back to the laptop it came from. "
            "The emergency button is on interrupt zero, so it is answered "
            "within a microsecond whatever the chip is doing. Press it and the "
            "relay drops out immediately. Zero per cent baud error, one "
            "kilohertz to within nought point two per cent, nought point seven "
            "eight degrees per step, a hundred and fifty seven milliamps. "
            "Software, hardware, and six wires."
        ),
        "beats": [
            {"kind": "image", "src": "board-running-safe.jpg", "t0": 0.00, "t1": 0.28,
             "zoom": [1.04, 1.15], "pan": [[0.45, 0.50], [0.50, 0.48]],
             "callouts": [
                 {"t": 0.42, "x": 0.44, "y": 0.62, "text": "SAFE - BELOW 40.0 C", "dir": "down"},
             ]},
            {"kind": "image", "src": "board-running-danger.jpg", "t0": 0.28, "t1": 0.52,
             "zoom": [1.10, 1.02], "pan": [[0.52, 0.46], [0.48, 0.50]],
             "callouts": [
                 {"t": 0.42, "x": 0.50, "y": 0.68, "text": "DANGER - 70.0 C AND ABOVE", "dir": "down"},
             ]},
            {"kind": "image", "src": "board-emergency.jpg", "t0": 0.52, "t1": 0.74,
             "zoom": [1.03, 1.12], "pan": [[0.50, 0.50], [0.48, 0.50]],
             "callouts": [
                 {"t": 0.40, "x": 0.50, "y": 0.30, "text": "EMERGENCY STOP - RELAY DROPPED OUT", "dir": "up"},
             ]},
            {"kind": "panel", "panel": "terminal", "t0": 0.74, "t1": 0.90,
             "title": "TELEMETRY - ONE LINE PER SECOND",
             "lines": [
                 "T=31.7C ADC= 41 ZONE=SAFE     FAN=0 BUZ=0",
                 "T=41.2C ADC= 53 ZONE=WARNING  FAN=1 BUZ=0",
                 "T=70.3C ADC= 90 ZONE=DANGER   FAN=1 BUZ=1",
                 "T=74.1C ADC= 95 ZONE=DANGER   FAN=1 BUZ=1",
             ]},
            {"kind": "panel", "panel": "end", "t0": 0.90, "t1": 1.00},
        ],
    },
]
