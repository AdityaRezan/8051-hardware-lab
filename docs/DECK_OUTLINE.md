# 8051 Hardware Lab - Seven Slide Technical Review Deck

**Deck outline, layout wireframes and visual asset specification.**

| Field | Value |
|---|---|
| Project title | 8051 Hardware Lab |
| Subtitle | Real-time embedded monitoring on the AT89S52 |
| Audience | Technical Review Committee / evaluators |
| Duration | 12 to 14 minutes, 7 slides |
| Format | 13.333 x 7.5 in, 16:9 |
| File | `docs/8051_Hardware_Lab_Review_Deck.pptx` |
| Build script | `tools/build_exec_deck.py` |
| Wireframes | `docs/wireframes.svg` |
| Tone | Precise, structured, engineering focused |

---

## 1. Design system

### 1.1 Colour tokens

| Token | Hex | Role |
|---|---|---|
| Charcoal | `#1E293B` | slide background |
| Surface | `#24334D` | panels, cards, table rows |
| Surface 2 | `#1A2637` | alternating table rows, recessed chips |
| Border | `#334155` | panel and card strokes |
| Grid | `#28374E` | background measurement grid, 1 px hairlines |
| Off-white | `#F1F5F9` | primary text |
| Muted | `#94A3B8` | secondary text, captions |
| Dim | `#64748B` | tertiary text, footers, labels |
| Electric Blue | `#2563EB` | primary accent: rules, fills, headers, structural elements |
| Electric Blue light | `#60A5FA` | accent text and strokes on dark surfaces |
| Emerald | `#10B981` | secondary accent: verified results, positive metrics, inputs |
| Emerald light | `#34D399` | emerald text on dark surfaces |
| Amber | `#F59E0B` | constraints, warnings, decision points |
| Red | `#EF4444` | critical constraints, faults |

Two tints are used for accent *text*. The requested accents are mid tones and lose contrast
against charcoal, so `#60A5FA` and `#34D399` carry text and thin strokes while `#2563EB` and
`#10B981` carry fills, bars and rules. The palette stays inside the specified system.

### 1.2 Typography

| Role | Font | Size | Weight | Colour |
|---|---|---:|---|---|
| Eyebrow / kicker | Consolas | 9.5 pt | Bold, uppercase | `#60A5FA` |
| Slide title (H1) | Calibri | 25 pt | Bold | `#F1F5F9` |
| Slide subtitle | Calibri | 11.5 pt | Regular | `#94A3B8` |
| Panel heading | Calibri | 11.5 pt | Bold | `#F1F5F9` |
| Body | Calibri | 9.5 - 11.5 pt | Regular | `#F1F5F9` / `#94A3B8` |
| Table header | Calibri | 8.5 - 9.5 pt | Bold | `#CBD8E9` |
| Table body | Calibri | 8.5 - 9.5 pt | Regular | `#F1F5F9` |
| Metric value | Calibri | 20 pt | Bold | `#F1F5F9` |
| Metric label | Consolas | 9.5 pt | Bold, uppercase | `#94A3B8` |
| Code / signals | Consolas | 8 - 10.5 pt | Regular | `#F1F5F9` |
| Footer | Consolas | 8 pt | Bold | `#64748B` |

### 1.3 Grid and spacing

| Parameter | Value |
|---|---|
| Slide | 13.333 x 7.5 in |
| Margins | 0.70 in left and right |
| Content width | 11.933 in |
| Columns | 12 |
| Gutter | 0.22 in |
| Column width | 0.793 in |
| Row rhythm | 0.22 in, steps of 0.11 in |
| Safe content band | y = 1.72 in to y = 6.84 in |
| Footer rule | y = 6.94 in |
| Footer text | y = 7.04 in |

Column helper: `x(n) = 0.70 + n x 1.013`, `width(n) = n x 0.793 + (n-1) x 0.22`.

---

## 2. Visual asset manifest

| ID | Asset | Slide | Type | Specification | Source |
|---|---|---:|---|---|---|
| A1 | System block diagram | 3 | vector diagram | MCU centre, 3 input nodes left, 3 output nodes right, bus bar, 4 device nodes | generated in deck |
| A2 | Chip glyph, DIP-40 outline | 1 | vector icon | 40-pin outline, 7 pins per side, notch, part label | generated in deck |
| A3 | Constraint matrix | 2 | table | 6 rows: ID, constraint, consequence, mitigation | `hardware/SCHEMATIC.md` section 1 |
| A4 | Stack diagram | 4 | layered bands | 4 horizontal layers, mono body text | generated in deck |
| A5 | Component breakdown grid | 4 | 4 x 2 card grid | 8 parts: name, category, one line spec | `hardware/BOM.md` |
| A6 | Control flow chart | 5 | flowchart | 6 nodes, 1 decision diamond, 5 connectors | `firmware/src/12_industrial_monitor.c` |
| A7 | Bus primitive sequence | 5 | 6 tile flow | save, gate, place, strobe, release, restore | `firmware/inc/board.h` `led_write` |
| A8 | Stage pipeline table | 5 | table | 5 stages, operation, failure mode handled | derived from firmware |
| A9 | Timing budget table | 5 | table | 6 operations, cycles, time | `hardware/SCHEMATIC.md` section 5 |
| A10 | Metrics grid | 6 | 3 x 2 tile grid | 6 headline numbers with derivation notes | `hardware/TESTING.md` |
| A11 | Trade-off matrix | 6 | table | 7 decisions, alternative, trade-off, outcome | `hardware/SCHEMATIC.md` section 6 |
| A12 | Roadmap | 7 | 3 phase timeline | Now, Next, Later with 3 items each | project plan |
| A13 | Minimum system schematic | appendix | SVG | crystal, reset, EA strap, decoupling | `hardware/min-system.svg` |
| A14 | Layout wireframes | all | SVG contact sheet | 7 labelled region maps | `docs/wireframes.svg` |

Recommended additions if the review allows extra evidence slides:

| ID | Asset | Type | Why |
|---|---|---|---|
| A15 | Oscilloscope capture | photo / PNG | ALE at 1.843 MHz proves the minimum system |
| A16 | Terminal capture | screenshot | 9600 8N1 telemetry frames from program 12 |
| A17 | Board photograph | photo | populated breadboard or dot PCB |
| A18 | ADC transfer plot | line chart | raw code against reference thermometer, 25 to 60 C |

---

## 3. Slide by slide specification

---

### Slide 1 - Title and author metadata

**Purpose.** Establish identity, ownership and scope in five seconds. Every claim on this slide is
a number the rest of the deck defends.

#### Wireframe

| Region | Columns | x | y | w | h | Content |
|---|---|---:|---:|---:|---:|---|
| Top rule | 0-12 | 0.00 | 0.00 | 13.333 | 0.09 | Electric Blue bar |
| Eyebrow | 0-7 | 0.70 | 0.95 | 8.60 | 0.26 | mono, uppercase |
| Title | 0-7 | 0.70 | 1.30 | 8.60 | 0.85 | H1, 40 pt |
| Subtitle | 0-7 | 0.70 | 2.18 | 8.60 | 0.55 | 18 pt |
| Deck line | 0-7 | 0.70 | 2.72 | 8.60 | 0.40 | 12.5 pt, muted |
| Accent rule | 0-2 | 0.70 | 3.32 | 2.20 | 0.045 | blue, then 0.45 in emerald |
| Metadata | 0-7 | 0.70 | 3.70 | 8.60 | 1.50 | 5 rows, mono label + value |
| Chip glyph | 8-11 | 9.30 | 1.20 | 3.40 | 2.10 | asset A2 |
| System ID card | 8-11 | 9.30 | 3.45 | 3.40 | 1.55 | 4 rows |
| Stat strip | 0-12 | 0.70 | 5.55 | 11.933 | 1.28 | 4 tiles of 3 columns |
| Bottom rule | 0-12 | 0.00 | 7.41 | 13.333 | 0.09 | Emerald bar |

#### Content

- Eyebrow: `MINI PROJECT / MICROPROCESSORS AND MICROCONTROLLERS`
- Title: **8051 Hardware Lab**
- Subtitle: Real-time embedded monitoring on the AT89S52
- Deck line: From browser simulator to measured silicon in one build cycle

Metadata rows:

| Label | Value |
|---|---|
| Authors | ATHARVA (24BEL0082) - ADITYA (24BEL0087) |
| Department | Electronics and Communication Engineering |
| Academic year | 2025 - 26 |
| Review | Technical Review Committee |
| Artifacts | Schematic, BOM, 13 Keil C51 programs, test report |

System ID card: Target AT89S52-24PU / Clock 11.0592 MHz / Bus 8-bit shared, P0 / Firmware Keil C51, 13 programs.

Stat strip:

| Value | Label | Note |
|---|---|---|
| 32 / 32 | I/O PINS UTILISED | full allocation, no headroom |
| 0.00 % | UART BAUD ERROR | TH1 = FDH at 11.0592 MHz |
| 0.78 C | ADC RESOLUTION | Vref/2 trimmed to 1.000 V |
| INR 985 | BOM PER BOARD | through-hole, single unit |

#### Visual assets required

- **A2 chip glyph**, vector, DIP-40 outline with seven pins a side and a notch. Drawn in deck.
- Optional: **A17 board photograph** behind the stat strip at 12 % opacity.

#### Design notes

- Blue top rule and emerald bottom rule bracket the deck; the same pair recurs in the header rule
  on every content slide.
- Stat strip tiles alternate blue and emerald top edges so the eye reads four units, not one bar.
- No more than four numbers on the title slide. Each one is defended later.

#### Speaker notes, 45 s

> Phase one built a browser based 8051 simulator and verified fourteen assembly programs against
> hand calculation. This deck covers phase two: the same ideas on a real AT89S52. Four numbers
> frame the work. All thirty two I/O pins are used, so there is no headroom and the architecture
> has to be right the first time. Baud error is exactly zero because the crystal is 11.0592 MHz.
> Temperature resolution is 0.78 degree C because the ADC reference was chosen deliberately. And
> the board costs about 985 rupees.

---

### Slide 2 - Problem statement and constraints

**Purpose.** State the task exactly, then show that the constraints were enumerated before any
component was chosen. This is the slide that earns trust.

#### Wireframe

| Region | Columns | x | y | w | h | Content |
|---|---|---:|---:|---:|---:|---|
| Header | 0-12 | 0.70 | 0.38 | 11.933 | 1.10 | eyebrow, H1, subtitle, dual rule |
| Problem panel | 0-7 | 0.70 | 1.72 | 6.87 | 2.86 | statement, italic body |
| Hard constraint | 0-7 | 0.70 | 3.62 | 6.44 | 0.86 | blue lead in + muted body |
| Constraints panel | 7-12 | 7.79 | 1.72 | 4.84 | 2.86 | 6 rows, colour coded |
| Constraint table | 0-12 | 0.70 | 4.72 | 11.933 | 2.10 | asset A3, 7 rows |
| Footer | 0-12 | 0.70 | 6.94 | 11.933 | 0.25 | rule, tag, page |

#### Content

Statement, set in italic to mark it as the brief:

> Transfer the verified 8051 programs from a software model onto a physical AT89S52, interfacing
> eight LEDs, a two digit seven segment display, a 16x2 character LCD, an eight way DIP switch bank,
> an LM35 temperature sensor through an ADC0804, a MAX232 serial link, a relay and a buzzer, and
> confirm on the bench that every output matches the value the simulator predicted.

Hard constraint: the peripherals require 54 I/O lines and the 8051 provides 32. The architecture
must close a 22 pin deficit without adding a port expander IC.

Constraint chips, colour coded by severity:

| Constraint | Value | Severity |
|---|---|---|
| I/O budget | 54 required, 32 available | blue, structural |
| Port 0 topology | open drain, cannot source | amber |
| Latch read-back | no read path to the latches | amber |
| ISP contention | P1.5-P1.7 shared with SPI | red |
| ADC resolution | 8 bits, reference is a choice | blue |
| No HW debounce | buttons bounce 1 to 10 ms | amber |

Constraint matrix:

| ID | Constraint | Consequence if ignored | Mitigation |
|---|---|---|---|
| C1 | 32 I/O pins for 54 signals | peripherals dropped or an expander IC added | single 8-bit bus on P0 with per-device strobes on P2 |
| C2 | P0 is open drain | the bus never reaches a valid logic 1 | RN1, a 10 kOhm x 9 SIP network, pulls the bus up |
| C3 | Output latches cannot be read | a stale byte is latched into the wrong device | bus_shadow variable plus interrupt gating |
| C4 | SW6-SW8 share the ISP lines | in-circuit programming fails or is corrupted | 1 kOhm series resistors, documented OFF state |
| C5 | 8-bit ADC, 5 V default reference | 1.95 C per step, most of the range wasted | Vref/2 trimmed to 1.000 V, giving 0.78 C |
| C6 | No hardware debounce on the buttons | one press registers as several interrupts | 5 ms resampling, edge triggered IT0 and IT1 |

#### Visual assets required

- **A3 constraint matrix**, seven row table. Severity chips use amber and red only where the
  consequence is a silent failure, which is the point worth making.
- Optional: **A13 minimum system schematic** inset if the committee wants parts on this slide.

#### Design notes

- The statement is the only italic text in the deck. It is a quotation of the brief.
- Severity colour is semantic, not decorative: blue is structural, amber is a design trap, red is a
  failure that damages hardware or blocks programming.
- The table is deliberately the widest element on the slide. It is the evidence load.

#### Speaker notes, 90 s

> The brief is on the left. The interesting part is the number underneath it: fifty four I/O lines
> are needed and the 8051 has thirty two. That deficit is the reason this project is an architecture
> exercise rather than a wiring exercise. On the right are the six constraints, colour coded. C1 is
> structural. C2 and C3 are traps that produce a board which looks alive but misbehaves. C4 is the
> one that can damage a programming session. C5 decides whether the temperature reading is useful.
> C6 is the sort of thing that only appears after you build it. The table below is the mitigation
> for each, and every mitigation is implemented in the schematic.

---

### Slide 3 - Proposed architecture / system block diagram

**Purpose.** Show the whole system in one glance, with the bus as the organising idea.

#### Wireframe

| Region | Columns | x | y | w | h | Content |
|---|---|---:|---:|---:|---:|---|
| Header | 0-12 | 0.70 | 0.38 | 11.933 | 1.10 | eyebrow, H1, subtitle |
| Input nodes | 0-3 | 0.70 | 1.75 / 2.47 / 3.19 | 2.82 | 0.62 | 3 emerald nodes |
| MCU node | centred | 4.75 | 1.75 | 3.83 | 0.95 | blue, elevated fill |
| Output nodes | 9-12 | 9.82 | 1.75 / 2.47 / 3.19 | 2.82 | 0.62 | 3 blue nodes |
| Bus bar | 1-11 | 1.72 | 3.92 | 9.91 | 0.48 | mono caption, blue border |
| Device nodes | 0-12 | 0.70 + i x 3.04 | 4.62 | 2.82 | 0.78 | 4 nodes |
| Device captions | 0-12 | as above | 5.42 | 2.82 | 0.22 | mono pin list |
| Interface table | 0-7 | 0.70 | 5.70 | 6.87 | 1.14 | 6 rows |
| Pin economy panel | 7-12 | 7.79 | 5.70 | 4.84 | 1.14 | 3 lines |

#### Content

Inputs, left, emerald: SW1 8-way DIP on P1.0-P1.7 / PB1 and PB2 on P3.2 and P3.3 / LM35 sensor on
ADC Vin+.

MCU, centre: AT89S52-24PU, 40-pin DIP, 11.0592 MHz.

Outputs, right, blue: Relay and buzzer on P3.4 and P3.5 / Digit selects on P3.6 and P3.7 /
MAX232 and DB9 on P3.0 and P3.1.

Bus bar: `BD0 - BD7   shared 8-bit data bus   port 0   10 kOhm pull-ups`.

Devices on the bus:

| Device | Load | Strobe |
|---|---|---|
| U2 74HC573 | 8 LEDs | P2.0 LED_LE |
| U3 74HC573 | 7-segment x2 | P2.1 SEG_LE |
| LCD1 16x2 | HD44780 8-bit | P2.2-P2.4 E RS RW |
| U4 ADC0804 | LM35 8-bit | P2.5-P2.7 WR RD INTR |

Interface table:

| Interface | Width | Signals | Direction | Device |
|---|---|---|---|---|
| Parallel bus | 8 bit | BD0-BD7 | bidirectional | U2 U3 LCD1 U4 |
| Latch strobe | 1 bit | LED_LE SEG_LE | output | U2 U3 |
| LCD control | 3 bit | E RS RW | output | LCD1 |
| ADC control | 3 bit | WR RD INTR | in / out | U4 |
| Serial + GPIO | 6 bit | TxD RxD P3.4-P3.7 | both | MAX232 Q1-Q4 |

Pin economy panel: 54 pins required to 32 available. Three 8-bit data paths merged into one bus,
saving 24 pins. Eight of them pay for the strobes. Net saving: 16 pins.

#### Visual assets required

- **A1 system block diagram**, vector, drawn to the coordinates above. Arrows from inputs to the MCU
  are emerald, arrows from the MCU to outputs are blue, and the bus arrow is blue at 1.8 pt so it
  reads as the trunk.
- Keep every arrow orthogonal or single-segment diagonal. No bezier curves in a technical diagram.

#### Design notes

- The MCU uses an elevated fill (`#2D3F5C`) distinct from panels, so it reads as silicon and not as
  another card.
- Emerald is input, blue is output. The convention is established here and never broken.
- The bus bar is centred and wider than anything else: it is the answer to slide 2.

#### Speaker notes, 100 s

> Inputs on the left in emerald, outputs on the right in blue. Everything in the middle is the
> AT89S52. The wide bar underneath is the answer to the pin deficit. The LCD needs eight data lines,
> the ADC needs eight, and the two latches need eight each. That is thirty two lines for four
> devices that are only ever touched for a few microseconds at a time. Merge them into one bus and
> spend eight pins on strobes instead: the net saving is sixteen pins, which is exactly what closes
> the gap. The rule is that only the device whose strobe is pulsed captures the byte. That single
> sentence is the whole architecture.

---

### Slide 4 - Hardware and software stack

**Purpose.** Prove that both halves of the stack are specified, with named parts and named tools.

#### Wireframe

| Region | Columns | x | y | w | h | Content |
|---|---|---:|---:|---:|---:|---|
| Header | 0-12 | 0.70 | 0.38 | 11.933 | 1.10 | eyebrow, H1, subtitle |
| Stack bands | 0-12 | 0.70 | 1.72 + i x 0.64 | 11.933 | 0.58 | 4 layers |
| Component grid | 0-12 | 0.70 + i x 3.04 | 4.38 / 5.18 | 2.82 | 0.72 | 8 cards |
| Protocol table | 0-6 | 0.70 | 5.94 | 5.86 | 0.90 | 4 rows |
| Toolchain panel | 6-12 | 6.78 | 5.94 | 5.86 | 0.90 | heading + 2 lines |

#### Content

Stack, top down:

| Layer | Contents | Artifact |
|---|---|---|
| APPLICATION | 13 firmware programs / board.h / 01 blink to 13 self test | `firmware/src` |
| DRIVER | bus, LED, 7-segment, LCD, ADC, UART, switch debounce | `firmware/inc/board.h` |
| INTERFACE | 8-bit parallel / HD44780 8-bit / ADC0804 / UART 9600 8N1 | P0, P2, P3 |
| SILICON | AT89S52, 2x 74HC573, ADC0804, LM35, MAX232, HD44780, BC547 x4, 7805 | through-hole DIP |

Component grid:

| Part | Category | Note |
|---|---|---|
| AT89S52-24PU | MCU | 8 KB flash, 3 timers |
| 74HC573 x2 | latch | LED bank, segment patterns |
| ADC0804LCN | ADC | 8-bit parallel, 606 kHz |
| LM35DZ | sensor | 10 mV per degree C |
| MAX232N | transceiver | TTL to RS-232, 1 uF pump |
| JHD162A | display | 16x2 HD44780, 8-bit |
| BC547 x4 | driver | digits, relay, buzzer |
| L7805CV | regulator | 5.00 V, 1 W, heatsinked |

Protocols:

| Protocol | Pins | Used for |
|---|---|---|
| 8-bit parallel bus | P0.0-P0.7 | latches, LCD, ADC |
| UART 9600 8N1 | P3.0-P3.1 | telemetry and shell |
| SPI (ISP only) | P1.5-P1.7 | flash programming |

Toolchain: Keil uVision 5, C51, level 8, small memory model. USBasp plus `avrdude -p 8052`,
USB to RS-232 adapter, DMM, 20 MHz scope.

#### Visual assets required

- **A4 stack diagram**, four horizontal bands. Reading order must be top down: application at the
  top, silicon at the bottom.
- **A5 component breakdown grid**, 4 x 2 cards, each carrying name, uppercase category and one
  line of spec. Emerald left edge on every card.

#### Design notes

- Stack bands are colour graded from blue at the top to emerald at the bottom, so the layers read as
  a gradient from software to hardware.
- Card category labels use 7.5 pt uppercase mono. They are scaffolding, not content.
- Part numbers are real and orderable. Do not abbreviate them for space.

#### Speaker notes, 85 s

> Four layers. The application layer is thirteen standalone programs, one file each, all building
> against one header. The driver layer is that header: bus arbitration, the LED and segment latches,
> the LCD protocol, the ADC read sequence, the UART, and switch debounce. The interface layer is
> where the pin budget lives: one 8-bit parallel bus, the HD44780 protocol, the ADC0804 handshake
> and a 9600 baud UART. Below that is the silicon, all through-hole DIP so the board can be
> assembled and repaired by hand. Every part is a real orderable number, and the toolchain is Keil
> for the build and a 250 rupee USBasp for the flash.

---

### Slide 5 - Implementation logic and flow chart

**Purpose.** Show control flow, the interrupt boundary, and the one primitive that makes the shared
bus safe.

#### Wireframe

| Region | Columns | x | y | w | h | Content |
|---|---|---:|---:|---:|---:|---|
| Header | 0-12 | 0.70 | 0.38 | 11.933 | 1.10 | eyebrow, H1, subtitle |
| Flow column | 0-3 | 0.98 | 1.72 + stacked | 2.54 | 0.58 / 0.72 | 6 nodes |
| ISR panel | 3-7 | 3.74 | 1.72 | 3.83 | 1.30 | emerald |
| Bus primitive | 3-7 | 3.74 | 3.14 | 3.83 | 1.86 | 6 tiles in 2 x 3 |
| Interrupt panel | 3-7 | 3.74 | 5.12 | 3.83 | 1.72 | amber |
| Stage table | 7-12 | 7.79 | 1.72 | 4.84 | 1.30 | 6 rows |
| Timing table | 7-12 | 7.79 | 3.18 | 4.84 | 1.74 | 7 rows |
| Rationale panel | 7-12 | 7.79 | 5.12 | 4.84 | 1.72 | 4 lines |

#### Content

Control flow, top to bottom:

1. `board_init` - ports, latches, outputs off
2. `display_init` - timer 0 at 5 ms, EE00H
3. `adc_read` - start, wait INTR, read byte
4. `zone decision` - diamond: T < 40 / < 70 / >= 70 C
5. `actuate` - LEDs, relay, buzzer
6. `publish` - LCD, 7-segment, UART at 1 Hz

Timer 0 ISR, every 5 ms: `TH0 = EEH  TL0 = 00H`; `seg_tick()` alternates the two digits; saves and
restores the bus shadow byte.

Bus transfer primitive, six steps:

| Step | Code |
|---|---|
| 1 save | `ea = EA` |
| 2 gate | `EA = 0` |
| 3 place | `BUS = v` |
| 4 strobe | `LE = 1` |
| 5 release | `LE = 0` |
| 6 restore | `BUS = shadow; EA = ea` |

External interrupts: INT0 falling edge sets the emergency latch; INT1 falling edge clears it. Both
ISRs set a flag only, and the main loop does the work, keeping service short.

Stage pipeline:

| Stage | Operation | Failure mode handled |
|---|---|---|
| Acquire | adc_read, INTR both edges | guarded timeout returns |
| Convert | T = raw x 25 / 32 integer | no float library needed |
| Decide | compare at 400 and 700 | emergency overrides all |
| Actuate | latch write, relay, buzzer | interrupts gated |
| Publish | LCD, 7-segment, UART 1 Hz | refresh runs in the ISR |

Timing budget:

| Operation | Cycles | Time |
|---|---:|---:|
| machine cycle | 12 osc | 1.0851 us |
| bus transfer | ~20 | 21.7 us |
| ADC conversion | - | 114 us |
| LCD write | ~30 | 32.6 us |
| display tick | 4608 | 5.000 ms |
| telemetry period | - | 1.000 s |

#### Visual assets required

- **A6 control flow chart**, six nodes with one diamond. The diamond is the only amber shape on the
  slide so the branch is unmistakable.
- **A7 bus primitive sequence**, six tiles in two columns of three, each with a step number and the
  matching line of code.
- **A8 stage pipeline table** and **A9 timing budget table**, right column.

#### Design notes

- The diamond uses amber, matching the constraint severity convention from slide 2.
- The bus primitive is boxed separately because it is the answer to constraint C3. It deserves to be
  quoted in code, not described in prose.
- Timing figures are given to four significant figures where they are exact and marked with a tilde
  where they are measured. Never present an estimate as a specification.

#### Speaker notes, 110 s

> The main loop is a polling pipeline: acquire, convert, decide, actuate, publish. The one thing that
> does not poll is the display. It refreshes from a timer interrupt every five milliseconds, and that
> creates a hazard, because the refresh writes to the same bus the LCD and the ADC use. So every bus
> transfer follows the six step primitive in the middle: save the interrupt state, disable it, place
> the byte, pulse one strobe, release it, then restore both the bus from the shadow variable and the
> interrupt state. Without that, an interrupt landing between the byte and the strobe would load the
> wrong value into the LED latch and the board would visibly glitch. On the right: the stage pipeline
> with the failure mode each stage absorbs, and the timing budget, where the numbers with a tilde are
> measured and the rest are exact.

---

### Slide 6 - Results, benchmark metrics and trade-offs

**Purpose.** Deliver numbers, then show the decisions behind them. Results without trade-offs look
like luck.

#### Wireframe

| Region | Columns | x | y | w | h | Content |
|---|---|---:|---:|---:|---:|---|
| Header | 0-12 | 0.70 | 0.38 | 11.933 | 1.10 | eyebrow, H1, subtitle |
| Metrics row 1 | 0-12 | 0.70 + i x 3.26 | 1.72 | 3.80 | 1.04 | 3 tiles |
| Metrics row 2 | 0-12 | 0.70 + i x 3.26 | 2.86 | 3.80 | 1.04 | 3 tiles |
| Trade-off matrix | 0-12 | 0.70 | 4.36 | 11.933 | 2.48 | 8 rows |

#### Content

Metrics:

| Value | Label | Note |
|---|---|---|
| 0.00 % | BAUD ERROR | TH1 = FDH at 11.0592 MHz |
| 1.00 kHz | TIMER OUTPUT | FE34H reload, +0.17 % |
| 100 Hz | DISPLAY REFRESH | EE00H reload, per digit |
| 0.78 C | ADC RESOLUTION | 7.8125 mV per step |
| 157 mA | BOARD CURRENT | 274 mA peak, relay on |
| 3.4 KB | LARGEST PROGRAM | of 8 KB flash, 30 B RAM |

Trade-off matrix:

| Decision | Alternative rejected | Trade-off accepted | Outcome |
|---|---|---|---|
| Shared 8-bit bus | I2C or SPI port expander IC | 8 extra strobes and software arbitration | 54 pins fitted into 32, no extra IC |
| AT89S52 with ISP | AT89C51, parallel programmer | slightly higher chip cost | programmer cost falls to INR 250 |
| 470 Ohm LED resistors | the usual 330 Ohm | about 15 % less brightness | 53 mA per package, inside the 70 mA limit |
| Vref/2 at 1.000 V | internal 2.5 V reference | one trimpot and one calibration step | 0.78 C per step instead of 1.95 C |
| Software driven bus | MOVX with an address latch | no hardware address decode | port 2 stays free for eight strobes |
| Flags inside the ISRs | doing the work in the ISR | one loop of latency | short, predictable service routines |
| Software debounce | RC filter or Schmitt trigger | 5 ms of loop time | no parts, no spare pins consumed |

#### Visual assets required

- **A10 metrics grid**, six tiles in two rows of three. Emerald top edge for verified results, blue
  for derived values, amber for the current figure because it is the one that drives the power
  design.
- **A11 trade-off matrix**, eight rows. This is the densest table in the deck and the most valuable.
- Optional: **A18 ADC transfer plot** and **A16 terminal capture** as evidence, if the committee
  asks for raw data.

#### Design notes

- Every metric tile carries the derivation in muted text under the label. A number presented without
  its derivation invites the question, and the answer should already be on the slide.
- The trade-off matrix has four columns: what was chosen, what was rejected, what it cost, what it
  bought. Never present a decision as if there were no alternative.
- Row height is uniform. The table is read as a matrix, not as prose.

#### Speaker notes, 120 s

> Six numbers. Zero baud error, because the reload divides exactly at 11.0592 megahertz. One
> kilohertz out of the timer, within two tenths of a percent. A hundred hertz display refresh, above
> the flicker threshold. Zero point seven eight degrees per ADC step. A hundred and fifty seven
> milliamps typical, two hundred and seventy four peak with the relay and the buzzer on. And three
> point four kilobytes for the largest program, out of eight. The table below is the more useful
> part. Every row is a decision, an alternative that was rejected, the cost that was accepted, and
> what it bought. The first row is the architecture. The third row is worth a note: four hundred and
> seventy ohms is not the usual value, and it was chosen because three thirty would put the latch
> package over its seventy milliamp rating. The fourth row doubles the temperature resolution for the
> price of one trimpot and one calibration step.

---

### Slide 7 - Scalability, future scope and conclusion

**Purpose.** Show that the limits are known, then close. Naming your own limits is more credible
than being asked for them.

#### Wireframe

| Region | Columns | x | y | w | h | Content |
|---|---|---:|---:|---:|---:|---|
| Header | 0-12 | 0.70 | 0.38 | 11.933 | 1.10 | eyebrow, H1, subtitle |
| Phase 1 | 0-4 | 0.70 | 1.72 | 3.80 | 2.24 | emerald |
| Phase 2 | 4-8 | 3.96 | 1.72 | 3.80 | 2.24 | blue |
| Phase 3 | 8-12 | 7.22 | 1.72 | 3.80 | 2.24 | amber |
| Conclusion | 0-7 | 0.70 | 4.24 | 6.87 | 2.56 | 4 bullets |
| Limits | 7-12 | 7.79 | 4.24 | 4.84 | 2.56 | 5 rows |

#### Content

Roadmap:

| Phase | Title | Items |
|---|---|---|
| NOW | Single board, verified | 13 programs, 20 tests / INR 985 per board / 9600 baud telemetry |
| NEXT | Recover two pins | LCD on a PCF8574 backpack / frees P2.3 and P2.4 / adds I2C: RTC, EEPROM |
| LATER | Multi-node and PCB | RS-485 or ESP-01 link / KiCad two layer layout / mains rated enclosure |

Conclusion:

- A 22 pin deficit was closed by architecture, not by extra silicon.
- Every constant derives from the 1.0851 microsecond machine cycle.
- Thirteen programs compile clean; the build is staged and measured.
- Every hardware result reconciles with the phase 1 simulator.

Scalability limits:

| Area | Limit |
|---|---|
| Bus | shared P0 caps throughput, a few hundred kHz |
| ADC | one channel, 8-bit, about 114 us per sample |
| Memory | 256 B RAM, no external data memory wired |
| Interrupts | two external sources, no priority nesting |
| Relay | demonstration only, never mains connected |

#### Visual assets required

- **A12 roadmap**, three phase cards with arrows between them. Colour progression emerald to blue to
  amber reads as now, next, later.
- Optional: **A15 oscilloscope capture** in the Now card if a measurement is available.

#### Design notes

- The limits panel is amber, matching the constraint convention. It is not an apology; it is a
  specification of the operating envelope.
- Conclusion bullets are short enough to be read in four seconds each. If the audience is reading,
  the speaker is not needed.
- Do not add a thank you slide. The closing sentence is the last thing the committee hears.

#### Speaker notes, 60 s

> Where this goes next. The board as built is complete and verified. The immediate step is to move
> the LCD onto an I2C backpack, which costs two pins today and returns them, because a PCF8574
> frees P2.3 and P2.4 and puts an I2C bus on the board for a real time clock and an EEPROM. After
> that, a two layer PCB and a proper enclosure. On the right are the limits, stated plainly: the
> shared bus caps throughput, there is one 8-bit ADC channel, there are 256 bytes of RAM, two
> external interrupts with no priority nesting, and the relay is for demonstration only and is never
> connected to mains. Four points to close on. The pin deficit was closed by architecture. Every
> constant derives from one machine cycle. The build is staged and measured. And every hardware
> result matches the simulator, which is the reason the simulator was built first.

---

## 4. Delivery checklist

- [ ] Replace placeholder author metadata with the final submission details.
- [ ] Confirm the roll numbers and department string against the submission form.
- [ ] If measurements are available, add A15, A16, A17 and A18 as an appendix.
- [ ] Rehearse to 13 minutes. Slides 2, 5 and 6 carry the argument and get the most time.
- [ ] Export a PDF alongside the PPTX for the submission bundle.
- [ ] Verify the deck opens in PowerPoint and in LibreOffice Impress before the review.

## 5. Rebuilding

```
pip install python-pptx
python3 tools/build_exec_deck.py     # docs/8051_Hardware_Lab_Review_Deck.pptx
python3 tools/gen_wireframes.py      # docs/wireframes.svg
```
