#!/usr/bin/env python3
"""Scene definitions for the 8051 Hardware Lab assembly video.

Narration strings here are the single source of truth: they are spoken by
generate_speech and burned on screen as captions, so they can never drift.
"""

TITLE_MAIN = "8051 HARDWARE LAB"
TITLE_SUB = "Building and running an AT89S52 microcontroller board"

SCENES = [
    # ------------------------------------------------------------------ 1
    {
        "id": "01",
        "label": "THE PROBLEM",
        "narration": (
            "8051 Hardware Lab: building and running an AT89S52 microcontroller "
            "board, from loose parts to a working system. Before any part goes "
            "on the board, there is a problem to solve. The finished design "
            "needs fifty-four separate connections, and the chip has "
            "thirty-two pins to spare. That gap of twenty-two is the reason "
            "this project looks the way it does. Everything you are about to "
            "watch follows from it."
        ),
        "beats": [
            {"kind": "panel", "panel": "title", "t0": 0.00, "t1": 0.24},
            {"kind": "image", "src": "board-complete.jpg", "t0": 0.24, "t1": 0.58,
             "zoom": [1.03, 1.16], "pan": [[0.50, 0.52], [0.46, 0.44]]},
            {"kind": "panel", "panel": "problem", "t0": 0.58, "t1": 1.00},
        ],
    },
    # ------------------------------------------------------------------ 2
    {
        "id": "02",
        "label": "THE FIX",
        "narration": (
            "The answer is to stop giving every device its own wires. Eight "
            "pins of port zero become a single shared road. In front of each "
            "device sits a latch, and every latch has a gate pin. Open one "
            "gate, put a number on the road, close the gate. The device keeps "
            "that number even after the road moves on. Four devices, one road, "
            "four gates. That is the whole trick, and it cost nothing."
        ),
        "beats": [
            {"kind": "image", "src": "concept-shared-bus.png", "t0": 0.00, "t1": 1.00,
             "zoom": [1.04, 1.13], "pan": [[0.50, 0.50], [0.50, 0.50]],
             "callouts": [
                 {"t": 0.30, "x": 0.50, "y": 0.30, "text": "ONE SHARED BUS", "dir": "up"},
                 {"t": 0.62, "x": 0.50, "y": 0.74, "text": "ONE GATE OPEN AT A TIME", "dir": "down"},
             ]},
        ],
    },
    # ------------------------------------------------------------------ 3
    {
        "id": "03",
        "label": "THE PARTS",
        "narration": (
            "These are the parts. Eighty in total, all through-hole and "
            "hand-placeable: the microcontroller, eight indicator LEDs, a "
            "two-digit seven-segment display, a sixteen-by-two character LCD, "
            "an LM35 temperature sensor, an analogue-to-digital converter, a "
            "relay, a buzzer, eight switches, a crystal, a regulator, and a "
            "breadboard to hold it all. Every part is placed by hand and can "
            "be moved again in seconds."
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
    # ------------------------------------------------------------------ 4
    {
        "id": "04",
        "label": "STAGE 1 TO 2 - POWER AND MINIMUM SYSTEM",
        "narration": (
            "Stage one is power, built alone and tested before anything else "
            "is fitted. A nine volt adapter feeds a 7805 regulator on a "
            "heatsink, which holds a steady five volts. Measured with a meter "
            "it reads five point zero, plus or minus nought point one five. "
            "That rail is proven before a second part is added. Stage two is "
            "the minimum system: the chip, an eleven point zero five nine two "
            "megahertz crystal, the reset circuit and the EA strap. With "
            "nothing else fitted, this is already a running computer."
        ),
        "beats": [
            {"kind": "image", "src": "board-stage-early.jpg", "t0": 0.00, "t1": 1.00,
             "zoom": [1.02, 1.20], "pan": [[0.42, 0.55], [0.50, 0.48]],
             "callouts": [
                 {"t": 0.10, "x": 0.30, "y": 0.68, "text": "7805 REGULATOR, 5 V", "dir": "down"},
                 {"t": 0.42, "x": 0.57, "y": 0.44, "text": "AT89S52", "dir": "up"},
                 {"t": 0.70, "x": 0.74, "y": 0.34, "text": "11.0592 MHz CRYSTAL", "dir": "up"},
             ]},
        ],
    },
    # ------------------------------------------------------------------ 5
    {
        "id": "05",
        "label": "STAGE 3 TO 5 - OUTPUTS, INPUTS, DISPLAY",
        "narration": (
            "Stage three adds the LED bank: a latch, pull-ups, eight "
            "four-hundred-and-seventy ohm resistors, and eight LEDs. Program "
            "zero-one blinks them once a second, and if you see that, the "
            "clock, the bus and the latch all work. Stage four adds an "
            "eight-way DIP switch, and program zero-three closes the loop: "
            "move a switch, the matching LED lights within ten milliseconds. "
            "Stage five fits the seven-segment display, and program zero-four "
            "counts from zero-zero to ninety-nine on a five millisecond timer "
            "interrupt."
        ),
        "beats": [
            {"kind": "image", "src": "board-stage-mid.jpg", "t0": 0.00, "t1": 1.00,
             "zoom": [1.03, 1.17], "pan": [[0.55, 0.46], [0.46, 0.52]],
             "callouts": [
                 {"t": 0.10, "x": 0.36, "y": 0.40, "text": "LED BANK", "dir": "up"},
                 {"t": 0.42, "x": 0.62, "y": 0.62, "text": "DIP SWITCH INPUTS", "dir": "down"},
                 {"t": 0.72, "x": 0.42, "y": 0.30, "text": "7-SEGMENT DISPLAY", "dir": "up"},
             ]},
        ],
    },
    # ------------------------------------------------------------------ 6
    {
        "id": "06",
        "label": "STAGE 6 TO 7 - SERIAL LINK AND TEMPERATURE",
        "narration": (
            "Stage six is the serial link. The chip speaks zero and five "
            "volts, a PC serial port expects plus and minus twelve, and a "
            "MAX232 with four capacitors does the translating. Program "
            "zero-nine puts a command shell on the other end: type LED FF and "
            "all eight LEDs obey. Stage seven adds the sense of touch: an "
            "ADC0804 converter, a trimmed one volt reference, and an LM35 "
            "sensor giving ten millivolts per degree. Program ten reads it "
            "and shows the temperature on the display."
        ),
        "beats": [
            {"kind": "image", "src": "board-complete.jpg", "t0": 0.00, "t1": 0.44,
             "zoom": [1.05, 1.15], "pan": [[0.60, 0.40], [0.52, 0.46]],
             "callouts": [
                 {"t": 0.35, "x": 0.66, "y": 0.36, "text": "MAX232 SERIAL LINK", "dir": "up"},
             ]},
            {"kind": "panel", "panel": "terminal", "t0": 0.44, "t1": 0.76,
             "title": "TERMINAL - 9600 8N1 - PROGRAM 09",
             "lines": [
                 "> HLP",
                 "LED FF   RLY 0   RLY 1   SEG NN   TEMP",
                 "> LED FF",
                 "OK",
                 "> RLY 1",
                 "OK",
             ]},
            {"kind": "grid", "t0": 0.76, "t1": 1.00, "cols": 2, "rows": 1,
             "stagger": 0.10, "images": ["adc0804.jpg", "sensor-lm35.jpg"]},
        ],
    },
    # ------------------------------------------------------------------ 7
    {
        "id": "07",
        "label": "STAGE 8 TO 9 - LCD, RELAY, BUZZER",
        "narration": (
            "Stage eight fits the LCD on a removable header. Program eleven "
            "shows the temperature as a number on line one, and as a bar of "
            "blocks on line two that grows as things warm up. Now the board "
            "can be read with no PC attached. Stage nine is where it stops "
            "being a display and starts doing something: the driver "
            "transistor, the protection diode across the coil, the relay and "
            "the buzzer. That diode matters. When the coil switches off it "
            "throws a voltage spike large enough to destroy the transistor."
        ),
        "beats": [
            {"kind": "panel", "panel": "lcd", "t0": 0.00, "t1": 0.30, "zone": "safe",
             "rows": ["T=38.4C A= 49", "SAFE    FAN:OFF"]},
            {"kind": "panel", "panel": "lcd", "t0": 0.30, "t1": 0.52, "zone": "warn",
             "rows": ["T=52.7C A= 67", "WARNING FAN:ON "]},
            {"kind": "panel", "panel": "lcd", "t0": 0.52, "t1": 0.74, "zone": "danger",
             "rows": ["T=74.1C A= 95", "DANGER  FAN:ON "]},
            {"kind": "image", "src": "board-complete.jpg", "t0": 0.74, "t1": 1.00,
             "zoom": [1.06, 1.16], "pan": [[0.38, 0.60], [0.44, 0.54]],
             "callouts": [
                 {"t": 0.35, "x": 0.32, "y": 0.56, "text": "RELAY AND BUZZER", "dir": "down"},
             ]},
        ],
    },
    # ------------------------------------------------------------------ 8
    {
        "id": "08",
        "label": "STAGE 10 - SELF TEST",
        "narration": (
            "Stage ten is the final checkout. Program thirteen runs a "
            "self-test of every part in turn and prints PASS, or names the "
            "fault. On a board with eighty hand-placed parts and two hundred "
            "jumper wires, that turns an hour of fault finding into ten "
            "seconds. If every line reports OK, program twelve goes in and "
            "stays in."
        ),
        "beats": [
            {"kind": "panel", "panel": "terminal", "t0": 0.00, "t1": 1.00,
             "title": "TERMINAL - PROGRAM 13 SELF TEST",
             "lines": [
                 "8051 HARDWARE LAB SELF TEST",
                 "CRYSTAL ....... OK",
                 "LED BANK ...... OK",
                 "DIP SWITCH .... OK",
                 "7-SEGMENT ..... OK",
                 "LCD ........... OK",
                 "ADC + LM35 .... OK",
                 "UART LOOPBACK . OK",
                 "RELAY + BUZZER  OK",
                 "SELF TEST: PASS",
             ]},
        ],
    },
    # ------------------------------------------------------------------ 9
    {
        "id": "09",
        "label": "RUNNING - THE ZONE MONITOR",
        "narration": (
            "Program twelve is the finished system. Every pass of the loop it "
            "reads the temperature, converts it to tenths of a degree, decides "
            "which of three zones it is in, and moves its outputs. Below forty "
            "degrees: green, relay off. From forty to sixty-nine point nine: "
            "yellow, relay on. At seventy and above: red, relay on, buzzer "
            "sounding. Once every second it also sends one line of telemetry "
            "to the PC. Read, convert, decide, act, repeat."
        ),
        "beats": [
            {"kind": "image", "src": "board-running-safe.jpg", "t0": 0.00, "t1": 0.38,
             "zoom": [1.04, 1.15], "pan": [[0.45, 0.50], [0.50, 0.48]],
             "callouts": [
                 {"t": 0.40, "x": 0.44, "y": 0.62, "text": "SAFE ZONE - BELOW 40.0 C", "dir": "down"},
             ]},
            {"kind": "image", "src": "board-running-danger.jpg", "t0": 0.38, "t1": 0.72,
             "zoom": [1.10, 1.02], "pan": [[0.52, 0.46], [0.48, 0.50]],
             "callouts": [
                 {"t": 0.40, "x": 0.50, "y": 0.68, "text": "DANGER ZONE - 70.0 C AND ABOVE", "dir": "down"},
             ]},
            {"kind": "panel", "panel": "terminal", "t0": 0.72, "t1": 1.00,
             "title": "TELEMETRY - ONE LINE PER SECOND",
             "lines": [
                 "T=31.7C ADC= 41 ZONE=SAFE     FAN=0 BUZ=0",
                 "T=38.4C ADC= 49 ZONE=SAFE     FAN=0 BUZ=0",
                 "T=41.2C ADC= 53 ZONE=WARNING  FAN=1 BUZ=0",
                 "T=52.7C ADC= 67 ZONE=WARNING  FAN=1 BUZ=0",
                 "T=70.3C ADC= 90 ZONE=DANGER   FAN=1 BUZ=1",
                 "T=74.1C ADC= 95 ZONE=DANGER   FAN=1 BUZ=1",
             ]},
        ],
    },
    # ------------------------------------------------------------------ 10
    {
        "id": "10",
        "label": "EMERGENCY STOP AND RESULTS",
        "narration": (
            "The emergency button is wired to interrupt zero, so it is "
            "answered within a microsecond whatever the chip is doing. Press "
            "it and the relay drops out immediately, the buzzer sounds, the "
            "LCD reads EMERGENCY STOP, and the telemetry reports the zone as "
            "EMERGENCY. The second button clears it. The finished board: zero "
            "per cent baud error, one kilohertz to within nought point two per "
            "cent, nought point seven eight degrees per step, a hundred and "
            "fifty-seven milliamps, eighty parts, about nine hundred and "
            "eighty-five rupees. It was never short of memory. It was short of "
            "pins."
        ),
        "beats": [
            {"kind": "image", "src": "board-emergency.jpg", "t0": 0.00, "t1": 0.40,
             "zoom": [1.03, 1.14], "pan": [[0.50, 0.50], [0.48, 0.50]],
             "callouts": [
                 {"t": 0.35, "x": 0.50, "y": 0.30, "text": "EMERGENCY STOP - RELAY DROPPED OUT", "dir": "up"},
             ]},
            {"kind": "panel", "panel": "results", "t0": 0.40, "t1": 0.80},
            {"kind": "panel", "panel": "end", "t0": 0.80, "t1": 1.00},
        ],
    },
]

# ------------------------------------------------------------------ extras

RESULT_CARDS = [
    ("0.00 %", "BAUD ERROR"),
    ("1.00 kHz", "TIMER OUTPUT"),
    ("100 Hz", "DISPLAY REFRESH"),
    ("0.78 C", "ADC RESOLUTION"),
    ("157 mA", "BOARD CURRENT"),
    ("3.4 KB", "LARGEST PROGRAM"),
]

END_LINES = [
    "8051 HARDWARE LAB",
    "Atharva (24BEL0082)   Aditya (24BEL0087)",
    "Department of Electronics and Computer Engineering   AY 2025-26",
]

PROBLEM_ROWS = [
    ("Data lines for five devices", "40"),
    ("Control and strobe lines", "8"),
    ("Relay, buzzer, buttons, digit selects", "6"),
    ("TOTAL THE DESIGN NEEDS", "54"),
    ("FREE PINS ON THE CHIP", "32"),
    ("SHORTFALL", "22"),
]


def narration_list():
    return [(s["id"], s["narration"]) for s in SCENES]


if __name__ == "__main__":
    total = sum(len(s["narration"].split()) for s in SCENES)
    for sid, txt in narration_list():
        print("%s  %4d words" % (sid, len(txt.split())))
    print("total %d words  ~ %.1f min at 150 wpm" % (total, total / 150.0))
