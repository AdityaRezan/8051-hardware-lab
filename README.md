# 8051 Hardware Lab

**Real-time embedded monitoring on the AT89S52 - from browser simulator to measured silicon.**

A complete, buildable 8051 board: shared-bus architecture, Keil C51 firmware, schematic with
derived design constants, bill of materials, a ten stage assembly procedure and twenty bench tests.

**Authors:** ATHARVA (24BEL0082) and ADITYA (24BEL0087)
**Department:** Electronics and Communication Engineering
**Academic year:** 2025-26

---

## The problem this project solves

The peripherals need **54 I/O lines**. The 8051 provides **32**.

| Peripheral | Dedicated pins | After bus sharing |
|---|---:|---:|
| LED latch, segment latch, LCD, ADC data | 32 | 8 |
| DIP switch bank | 8 | 8 |
| Control strobes | 0 | 8 |
| UART, interrupts, relay, buzzer, digit selects | 14 | 8 |
| **Total** | **54** | **32** |

The eight data lines of the LCD, the ADC and the two output latches are merged into one
bidirectional bus on port 0. Each device keeps its own enable strobe on port 2, so a transfer only
affects the device whose strobe is pulsed. No port expander IC is used.

---

## What the board does

| Function | Hardware | Firmware entry point |
|---|---|---|
| Eight LED output bank | 74HC573 latch plus 470 Ohm resistors | `led_write` |
| Eight bit digital input | 8-way DIP switch on port 1 | `switch_read` |
| Two digit numeric display | second latch, two BC547 digit drivers | `seg_tick` from timer 0 |
| Text output | 16x2 HD44780, 8-bit mode | `lcd_string`, `lcd_number` |
| Analog temperature | LM35 into ADC0804, Vref/2 at 1.000 V | `adc_read`, `adc_to_celsius` |
| Serial link | MAX232 and DB9 at 9600 8N1 | `uart_string`, `uart_number` |
| Interrupts | PB1 on INT0, PB2 on INT1, falling edge | `int0_isr`, `int1_isr` |
| Actuators | 5 V SPDT relay and buzzer on BC547 drivers | `RELAY`, `BUZZER` |
| Zone control | green, yellow, red LEDs plus relay and buzzer | `12_industrial_monitor.c` |

---

## Specification

| Parameter | Value |
|---|---|
| Microcontroller | AT89S52-24PU, 40-pin DIP (AT89C51 fallback, pin compatible) |
| Crystal | 11.0592 MHz |
| Machine cycle | 1.0851 microseconds |
| Supply | 7-12 V in, 5.00 V regulated by a 7805 with heatsink |
| Current | 157 mA typical, 274 mA peak |
| Digital I/O | 32 of 32 pins used |
| Serial | 9600 8N1, TH1 = FDH, zero percent error |
| ADC | 8-bit, Vref/2 = 1.000 V, 7.8125 mV per LSB |
| Temperature | 0 to 199.2 C at 0.78 C resolution |
| Display refresh | 100 Hz per digit from a 5 ms timer 0 interrupt |
| Cost | about INR 985 per board, INR 1,715 for a full setup |

---

## Repository layout

```
8051-hardware-lab/
├── hardware/
│   ├── SCHEMATIC.md      pin budget, pin allocation, wiring tables, design calculations
│   ├── BOM.md  BOM.csv   bill of materials with indicative Indian pricing
│   ├── ASSEMBLY.md       ten stage build procedure with a pass measurement per stage
│   ├── TESTING.md        twenty test cases, calibration, sample telemetry
│   └── min-system.svg    schematic of the minimum system
├── firmware/
│   ├── inc/board.h       pin definitions and all peripheral drivers
│   ├── src/01..13_*.c    thirteen standalone Keil C51 programs
│   ├── keil/*.uvprojx    uVision 5 projects for AT89S52 and AT89C51
│   └── README.md         Keil setup, flashing, program reference
├── docs/
│   ├── 8051_Hardware_Lab_Review_Deck.pptx   7 slide technical review deck
│   ├── 8051_Hardware_Implementation.pptx    28 slide detailed deck
│   ├── DECK_OUTLINE.md  wireframes, content spec and visual asset manifest
│   └── wireframes.svg   layout blueprints for all seven slides
├── tools/                generators for the decks, the BOM and the schematic
└── smart_industrial_automation.py    phase 1 simulation model
```

---

## Firmware

Thirteen Keil C51 programs. Each is a single translation unit that includes `inc/board.h`, so every
program builds as its own target.

| Program | Demonstrates |
|---|---|
| 01_led_blink | port expansion through a latch |
| 02_led_patterns | rotate and pattern sequences |
| 03_switch_led | debounced digital input |
| 04_seg7_counter | lookup table and multiplexed display |
| 05_timer0_second | timer interrupt timing |
| 06_square_wave | timer generated frequency |
| 07_ext_interrupt | INT0 and INT1 edge triggered ISRs |
| 08_uart_echo | 9600 baud serial link |
| 09_uart_commands | serial command shell |
| 10_adc_7seg | LM35 and ADC0804 |
| 11_adc_lcd | HD44780 8-bit interface |
| 12_industrial_monitor | complete system: zones, relay, buzzer, telemetry |
| 13_selftest | power on self test with a PASS or FAIL report |

Sources contain no comments and use only the C51 subset: `sbit`, `code`, `interrupt N`, C89
declarations. All thirteen compile clean. See `firmware/README.md` for the Keil setup and the
flashing procedure.

---

## Key design constants

Every value below derives from the 1.0851 microsecond machine cycle.

| Quantity | Value | Derivation |
|---|---|---|
| TH1 for 9600 baud | FDH | `256 - 11059200 / (384 x 9600) = 253` |
| Timer 0, 5 ms display tick | EE00H | `65536 - 5000 / 1.0851 = 60928` |
| Timer 0, 50 ms tick | 4C00H | `65536 - 50000 / 1.0851 = 19456` |
| Timer 0, 1 kHz output | FE34H | `65536 - 500 / 1.0851 = 65076` |
| ADC step | 7.8125 mV | `2.000 V / 256` |
| Temperature transfer | `T = raw x 25 / 32` | `raw x 7.8125 mV / 10 mV` |
| ADC clock | 606 kHz | `1 / (1.1 x 10 kOhm x 150 pF)` |
| LED resistor | 470 Ohm | keeps the latch package at 53 mA, under its 70 mA limit |

---

## Build and test

1. Read `hardware/SCHEMATIC.md` for the pin allocation and wiring tables.
2. Order parts from `hardware/BOM.csv`.
3. Follow `hardware/ASSEMBLY.md`, ten stages, measuring at the end of each.
4. Flash a program from `firmware/src` with a USBasp.
5. Run the twenty tests in `hardware/TESTING.md` and record the measured column.

---

## Presentation decks

| Deck | Slides | Use |
|---|---:|---|
| `docs/8051_Hardware_Lab_Review_Deck.pptx` | 7 | technical review committee, executive summary |
| `docs/8051_Hardware_Implementation.pptx` | 28 | detailed walkthrough, full subsystem coverage |

The seven slide deck is built to an explicit design system: charcoal `#1E293B`, off-white
`#F1F5F9`, Electric Blue `#2563EB` and Emerald `#10B981`, on a 12 column grid. Its layout
wireframes, per-slide content specification and visual asset manifest are in
`docs/DECK_OUTLINE.md`, and `docs/wireframes.svg` is the blueprint contact sheet.

Rebuild either deck with:

```
pip install python-pptx
python3 tools/build_exec_deck.py      # 7 slide review deck
python3 tools/build_deck.py           # 28 slide detailed deck
python3 tools/gen_wireframes.py       # docs/wireframes.svg
python3 tools/gen_bom.py              # hardware/BOM.md
python3 tools/gen_min_system_svg.py   # hardware/min-system.svg
```

---

## Safety

- The relay is mains rated but must never be connected to mains during laboratory demonstration.
  Use a 5 V or 12 V lamp on J4, or leave the contacts open.
- The 7805 dissipates about 1 W at 9 V and 250 mA. Fit the heatsink.
- Disconnect power before inserting or removing the microcontroller.
- Set DIP switches 6, 7 and 8 to OFF before every programming cycle; they share P1.5 to P1.7 with
  the SPI programming lines.
