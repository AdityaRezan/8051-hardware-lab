# Smart Industrial Automation & Monitoring System

**8051 AT89S52 (Master) + ARM Cortex-M STM32 (Slave) — Python GUI Simulator**

A desktop GUI simulation of the dual-processor Smart Industrial Automation System. The 8051 node senses real-time temperature through LM35 + ADC0804, displays it on a 7-segment display, raises zone alerts, and transmits data over UART to the ARM Cortex-M node, which controls a DC motor using TIM2 PWM, drives an analog output through DAC0808, and triggers an instant emergency shutdown through the NVIC interrupt.

**Team:** ATHARV (24BEL0082) & ADITYA (24BEL0087) — Microprocessors & Microcontrollers Project

---

## Features

- **LM35 + ADC0804 sensing** — analog temperature to 8-bit digital conversion (P2 data bus with live bit-level view)
- **8051 temperature calculation** — `T = ADC × 2 / 5` (MUL / DIV instruction behaviour)
- **2-digit 7-segment display** — driven from the SEG7 lookup table (`3F 06 5B 4F 66 6D 7D 07 7F 6F`)
- **Alert zone LEDs (Port 1)** — GREEN / YELLOW / RED with CJNE / JC threshold comparison at 40 °C and 70 °C
- **UART link @ 9600 baud** — 8051 P3.1 TX → ARM PA0 RX (TH1 = 0xFD, Mode 1) with animated packet transfer and serial monitor log
- **TIM2 PWM motor control** — duty cycle with live gauge, CCR register value out of ARR = 999, spinning DC motor + L293D driver animation
- **DAC0808 analog output** — 8-bit PB0-7 data bus and 0–5 V output gauge
- **NVIC emergency interrupt** — INT0 (8051) / EXTI0 (ARM) push button → ISR → motor stop, buzzer ON, all outputs cleared, 0xFF shutdown frame on UART
- **AUTO simulation mode** — automatic temperature sweep through all zones, or MANUAL slider control

## Temperature Zones & System Actions

| Zone | Temperature | LED | Motor Speed | DAC Output | Buzzer |
|---|---|---|---|---|---|
| SAFE | < 40 °C | GREEN | 30 % (LOW) | 1.5 V | OFF |
| WARNING | 40 – 70 °C | YELLOW | 60 % (MEDIUM) | 3.0 V | OFF |
| DANGER | > 70 °C | RED | 99 % (HIGH) | 5.0 V | ON |
| EMERGENCY | Button (ALL) | OFF | STOP (0 %) | 0.0 V | ON |

## How to Run

**Requirements:** Python 3.8+ with tkinter (included by default with Python on Windows and macOS). No external libraries needed.

**Windows:**
```
python smart_industrial_automation.py
```

**Linux:**
```
python3 smart_industrial_automation.py
```
If tkinter is missing on Linux, install it first:
```
sudo apt-get install python3-tk
```

**macOS:**
```
python3 smart_industrial_automation.py
```

## Controls

| Control | Action |
|---|---|
| **AUTO SIM** | Temperature drifts automatically through all zones |
| **MANUAL** | Drag the LM35 slider (0–102 °C) to set any temperature |
| **EMERGENCY STOP** | Fires INT0 / EXTI0 → NVIC ISR → motor stop, buzzer ON, outputs cleared |
| **RESET SYSTEM** | Clears the emergency state and resumes normal operation |

## System Pipeline

1. **SENSE** — LM35 outputs analog voltage (10 mV/°C)
2. **CONVERT** — ADC0804 produces the 8-bit digital value
3. **CALCULATE** — 8051 computes `T = ADC × 2 / 5` in °C
4. **DISPLAY** — 7-segment shows tens and units digits
5. **ALERT** — Port 1 LEDs switch by zone (40 °C / 70 °C thresholds)
6. **TRANSMIT** — 8051 sends the ADC byte over UART at 9600 baud
7. **CONTROL** — ARM computes PWM duty (30 / 60 / 99 %) and DAC level
8. **ACTUATE** — TIM2 PWM drives the motor, DAC0808 drives the analog output

**EMERGENCY:** Button → INT0/EXTI0 → NVIC ISR → Motor STOP + Buzzer ON + 0xFF to ARM → all outputs cleared.

## Syllabus Coverage

| Module | Covered By |
|---|---|
| M1 — 8051 Architecture | SFRs, ports, pin configuration of AT89S52 |
| M2 — 8051 Instruction Set | MOV, MUL, DIV, CJNE, JC, DJNZ, SETB, CLR, MOVC, SBUF/TI |
| M3 — ARM Processor | 32-bit RISC pipeline, modes, PSR |
| M4 — ARM Cortex-M | STM32 NVIC, AMBA bus, TIM2, registers |
| M5 — ARM Instruction Set | LDR, STR, BL, CMP, BEQ, ORR, BIC, BX, MOV |
| M6 — GPIO & Circuits | LED interface, 7-segment, switch port circuitry |
| M7 — Peripherals | ADC, DAC, PWM, timer, UART, interrupts |
| M8 — Contemporary Issues | Real-time industrial automation application |

## Repository Structure

```
smart-industrial-automation-system/
├── smart_industrial_automation.py   # Main GUI application (Python + tkinter)
├── hardware/                        # Phase 2: real AT89S52 board
│   ├── SCHEMATIC.md                 # pin allocation, wiring tables, design calculations
│   ├── BOM.md  BOM.csv              # bill of materials with indicative pricing
│   ├── ASSEMBLY.md                  # ten stage build procedure with pass measurements
│   ├── TESTING.md                   # twenty test cases and calibration procedure
│   └── min-system.svg               # schematic of the minimum system
├── firmware/                        # Phase 2: Keil C51 sources
│   ├── inc/board.h                  # pin definitions and peripheral drivers
│   ├── src/01..13_*.c               # thirteen standalone programs
│   └── keil/*.uvprojx               # uVision 5 projects for AT89S52 and AT89C51
├── docs/
│   └── 8051_Hardware_Implementation.pptx
├── tools/                           # generators for the BOM, schematic and deck
└── README.md
```

## Reference Hardware

- 8051 node: AT89S52, ADC0804, LM35, 2-digit common-cathode 7-segment, alert LEDs, 11.0592 MHz crystal
- ARM node: STM32F103C8T6 (Blue Pill), DAC0808, L293D + 12 V DC motor, piezo buzzer, MAX232
- Tools: Keil uVision 5, Proteus 8 Professional, Flash Magic, STM32CubeProgrammer

---

# Phase 2 - Hardware Implementation on a Real AT89S52

The Python GUI simulates the system. This phase builds it. A single AT89S52 drives eight LEDs, an
eight way DIP switch, a two digit seven segment display, a 16x2 character LCD, an ADC0804 reading an
LM35 temperature sensor, a MAX232 serial link at 9600 baud, a relay, a buzzer and two interrupt push
buttons using all 32 of its I/O pins.

## Why a shared data bus

The peripherals need 54 I/O lines and the 8051 has 32. The eight data lines of the LCD, the ADC and
the two output latches are merged into one bidirectional bus on port 0, with each device keeping its
own enable strobe on port 2. That brings the requirement down to exactly 32 pins.

| Peripheral | Dedicated pins | After bus sharing |
|---|---:|---:|
| LED latch, segment latch, LCD, ADC data | 32 | 8 |
| DIP switch bank | 8 | 8 |
| Control strobes | 0 | 8 |
| UART, interrupts, relay, buzzer, digit selects | 14 | 8 |
| **Total** | **54** | **32** |

## Pin allocation

| Port | Function |
|---|---|
| P0.0-P0.7 | shared data bus BD0-BD7 with 10 kOhm pull-ups |
| P1.0-P1.7 | eight way DIP switch input |
| P2.0 | LED latch enable |
| P2.1 | seven segment latch enable |
| P2.2-P2.4 | LCD E, RS, RW |
| P2.5-P2.7 | ADC0804 WR, RD, INTR |
| P3.0-P3.1 | RxD and TxD through the MAX232 |
| P3.2-P3.3 | INT0 emergency button, INT1 mode button |
| P3.4-P3.5 | relay driver, buzzer driver |
| P3.6-P3.7 | seven segment digit selects |

## Key design numbers

| Quantity | Value |
|---|---|
| Machine cycle at 11.0592 MHz | 1.0851 microseconds |
| TH1 for 9600 baud | FDH, zero percent error |
| Timer 0 reload for the 5 ms display tick | EE00H |
| Timer 0 reload for a 50 ms tick | 4C00H |
| Timer 0 reload for 1 kHz output | FE34H |
| ADC step with Vref/2 at 1.000 V | 7.8125 mV, 0.78 degrees C |
| Temperature transfer function | T = raw x 25 / 32 |
| ADC clock from 10 kOhm and 150 pF | 606 kHz, about 114 microseconds per conversion |
| Typical board current | 157 mA |
| Component cost for one board | about INR 985 |

## Firmware

Thirteen Keil C51 programs in `firmware/src`, each a single file that includes `inc/board.h`. They
were written without comments and use only the C51 subset: `sbit`, `code`, `interrupt N`, and C89
declarations. All thirteen compile clean.

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
| 13_selftest | power on self test with PASS or FAIL report |

## Build and test

See `hardware/ASSEMBLY.md` for the ten stage build with a pass measurement at each stage,
`hardware/TESTING.md` for the twenty test cases, and `hardware/BOM.md` for the parts. The schematic
is in `hardware/min-system.svg` with full wiring tables in `hardware/SCHEMATIC.md`.

`tools/gen_min_system_svg.py` regenerates the schematic, `tools/gen_bom.py` regenerates the bill of
materials from `hardware/BOM.csv`, and `tools/build_deck.py` regenerates the presentation deck.

## Safety

The relay on J4 is never connected to mains during laboratory demonstration. The 7805 runs at about
1 W and needs its heatsink. DIP switches 6, 7 and 8 must be OFF during every programming cycle
because they share P1.5, P1.6 and P1.7 with the SPI programming lines.
