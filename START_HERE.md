# Start here: from nothing to a running board

This is the whole project in the order you actually do it. Read it top to
bottom. Every step tells you what to do, what you should see, and what to do
if you do not see it.

Two halves:

- **Part A happens on your laptop.** You finish it at home. Output: 13 HEX files.
- **Parts B and C happen on the bench.** Output: a board that runs.

If you only care about the software half - build the HEX files, flash them, and
have the circuit start by itself in the lab - read
[`docs/SOFTWARE_RUNBOOK.md`](docs/SOFTWARE_RUNBOOK.md) instead. It is this same
process as a tick-box list with a minute-by-minute lab-day timeline.

Do Part A completely before you go to the lab. The lab machine does not need
Keil installed.

---

## The four traps

Everything that goes wrong in this project is one of these four. Read them once
now so you recognise them later.

**1. The free Keil compiler stops at 2048 bytes.** It is not broken and it is
not your code. `FATAL ERROR L250: CODE SIZE LIMIT ... LIMIT: 0800H BYTES` means
the program is too big for the free version. Part A6 deals with it.

**2. That same free compiler puts your code at address 0x0800 instead of
0x0000.** This is fine on an 8 KB chip. The linker plants a long jump at
address 0, the chip boots, jumps, and runs. It is only a problem if the HEX has
no jump at address 0, which is why the build script checks for it.

**3. A stock USBasp cannot program an AT89S52.** AVR chips reset on a low
signal. The 8051 resets on a high one. Stock USBasp firmware never gets the
chip into programming mode and reports
`initialization failed, rc=-1`, which looks like a wiring fault but is not.

**4. The AT89C51 cannot be programmed this way at all.** It has no SPI
interface. It needs a parallel programmer with 12 V. Always open the
`_AT89S52` project, never the `_AT89C51` one, if you intend to put the file on
a chip.

---

## Part A - On the laptop

### A1. Get the files

Download the repository as a ZIP from GitHub and extract it.

Common mistake: extracting produces a folder inside a folder with the same
name, so you end up with `8051-hardware-lab-main\8051-hardware-lab-main\`. It
works, but every path below is one level shorter if you move the inner folder
up one level. Do that first.

The three folders that matter:

```
firmware\src\     13 programs, 01 to 13
firmware\inc\     board.h, the shared driver library
firmware\keil\    26 ready made uVision projects
tools\            the build script and the checkers
```

### A2. Install Keil C51

Skip this if you already built something.

1. Download C51 from `https://www.keil.com/demo/eval/c51.htm`.
2. Install it. Accept the defaults. It will ask for a serial number on first
   run; choose to run as the evaluation version, which needs none.
3. Confirm it installed the 8051 tools, not just the ARM ones. Start uVision,
   then `Project > New uVision Project`. If you can find **AT89S52** in the
   device list, the C51 tools are present. If the device list has no Atmel 8051
   parts, you installed MDK-ARM and need the C51 pack as well.

The evaluation version is enough to finish Part A. It is limited to 2048 bytes
of object code, which is trap 1 above.

### A3. Open exactly one project

This is the step most people get wrong.

There are 13 programs and each one has its own `main()`. If you put more than
one `.c` file in a single project, the linker finds 13 copies of `main` and
reports hundreds of errors. That is what happened with the project called
`finalproject`. Do not use it. Delete it or ignore it.

Instead:

1. `Project > Open Project`.
2. Go to `firmware\keil\`.
3. Open `01_led_blink_AT89S52.uvprojx`.

Note the `_AT89S52` ending. There is also a `01_led_blink_AT89C51.uvprojx`.
That one compiles but the chip cannot be programmed with a normal ISP
programmer. Always take the `AT89S52` one.

The project already has the device set to AT89S52, the crystal set to
11.0592 MHz, the HEX output switched on, and the include path pointing at
`..\inc`. You do not need to configure any of that.

### A4. Build it and read the output

`Project > Rebuild all target files`.

You want this line, or something very close to it:

```
Program Size: data=30.0 xdata=0 code=1129
"01_led_blink" - 0 Error(s), 20 Warning(s).
```

- **0 Error(s)** is the part that matters. Errors stop the build. Warnings do not.
- **20 Warning(s)** all reading `L16: UNCALLED SEGMENT` is expected. `board.h`
  contains all 26 drivers; this program calls three of them. The other 23 are
  compiled in but never run. Harmless, but wasteful, and A6 removes them.
- The last number, **code=1129**, is the size in bytes. It must be under 2048.

The HEX file is now at `firmware\keil\Objects\01_led_blink.hex`.

### A5. Build all 13 at once

Do not repeat A3 and A4 thirteen times.

Double-click `tools\Build-All-HEX.bat`. If Windows blocks it, right-click and
run with PowerShell, or open PowerShell yourself and run:

```
cd tools
.\build_all_hex.ps1
```

It finds Keil, builds all 13 projects, reads the size from each, checks each
HEX, and copies every good one into `firmware\hex`. It prints:

```
  PROGRAM              CODE    DATA     ERR    WARN  HEX         STATE
  --------------------------------------------------------------------
  01_led_blink         1129    30.0       0      20  ok          OK
  02_led_patterns      1180    30.0       0      18  ok          OK
  ...

  11 ready, 2 over the 2048 byte limit, 0 failed.
```

If it cannot find Keil, tell it where:

```
.\build_all_hex.ps1 -KeilPath C:\Keil_v5\UV4
```

Send this table to whoever is helping you. It is the single most useful piece
of information in the whole project.

### A6. If something is too big

`OVER LIMIT` means the program built cleanly but is larger than 2048 bytes.
Two switches, cheapest first:

```
.\build_all_hex.ps1 -Small
.\build_all_hex.ps1 -Small -LX51
```

- `-Small` sets optimisation level 9 and favours size over speed. Safe. Usually
  5 to 15 percent.
- `-LX51` switches to the extended linker and turns on `REMOVEUNUSED`, which
  deletes every driver the program never calls. This is the one that matters,
  because `board.h` currently puts all 26 drivers into every program. That is
  why an LED blink costs 1129 bytes instead of about 200.

If `-LX51` reports `L257: Extended Linker Requires Upgrade to PK51`, your
licence level does not include the extended linker. Use `-Small` only. If the
build log still shows `BL51` after using `-LX51`, set it by hand once:
`Options for Target > Device > tick Use Extended Linker (LX51) instead of
BL51`, then `LX51 Misc > Misc Controls: REMOVEUNUSED`.

Last resort, if a program is still over: open `firmware\inc\board.h` and delete
the drivers that program does not use. Programs 12 and 13 are the only likely
candidates.

### A7. Put the HEX files on a pen drive

Copy the whole `firmware\hex` folder. Also copy `docs\FLASHING.md` onto the
same drive, or keep this file on your phone.

That folder and that document are everything you need at the bench. You are
done with the laptop.

---

## Part B - On the bench

### B1. Buy the parts

`hardware\BOM.csv` has all 80 items with Indian sources and prices, roughly
985 INR per board. The parts that actually matter:

| Ref | Part | Why it is critical |
|---|---|---|
| U1 | AT89S52-24PU | The only 8051 here that can be programmed with a cheap ISP programmer |
| Y1 | 11.0592 MHz crystal | Not 12 MHz. The UART baud rate is only exact at 11.0592 |
| C3a, C3b | 30 pF | The oscillator will not start reliably without them |
| U7 | 7805 | Needs the heatsink |
| U2, U3 | 74HC573 | The shared bus latches. 74HC373 will not drop in |
| U4 | ADC0804 | |
| LCD1 | 16x2 HD44780 | |
| U5 | MAX232 | Serial link |
| JP1 | Jumper on P3.4 | Remove it to test the square wave |

Order two AT89S52 chips. They cost 120 INR and a damaged one ends your day.

### B2. Build the power supply first

Stage 1 of `hardware\ASSEMBLY.md`. Build it alone and test it alone. Do not
plug a chip in until the 5 V rail measures between 4.90 and 5.10 V with nothing
else connected.

A wrong supply destroys every chip on the board at once. This is not the stage
to rush.

### B3. Build the minimum system

Stage 2. Six things, and once it is built the board will run programs 01, 02
and 03 with nothing else fitted:

| Connection | Detail |
|---|---|
| Pin 40 to +5 V, pin 20 to GND | With 0.1 uF decoupling right at the pins |
| Crystal across pins 18 and 19 | 11.0592 MHz |
| 30 pF from pin 18 to GND, 30 pF from pin 19 to GND | |
| Pin 31 (EA) to +5 V | Miss this and the chip looks for code that is not there |
| R1 10 k from pin 9 to GND, C2 10 uF from pin 9 to +5 V | Active high reset |
| 2x5 ISP header | MOSI to P1.5, MISO to P1.6, SCK to P1.7, RESET to pin 9, VCC, GND |

Measure 5 V between pins 40 and 20 before going further.

### B4. Build the rest, one stage at a time

Follow `hardware\ASSEMBLY.md` and test after every stage. The order matters
because each stage can be tested with a program you already have.

| Stage | What goes on | Test it with |
|---:|---|---|
| 3 | LED bank, 74HC573 and eight 470 Ohm resistors | `01_led_blink.hex` |
| 4 | DIP switch bank and 10 k pull-ups | `03_switch_led.hex` |
| 5 | Seven segment display and two BC547 drivers | `04_seg7_counter.hex` |
| 6 | MAX232 and DB9 | `08_uart_echo.hex` |
| 7 | LM35 and ADC0804 | `10_adc_7seg.hex` |
| 8 | 16x2 LCD | `11_adc_lcd.hex` |
| 9 | Relay, buzzer, emergency stop buttons | `12_industrial_monitor.hex` |
| 10 | Final checkout | `13_selftest.hex` |

Solder the IC sockets, not the chips. A socket costs 8 INR and turns a dead
chip into a two minute swap instead of a rebuild.

---

## Part C - Joining them

### C1. Pick a programmer

You need one of these. They are not interchangeable.

| Option | Works as is | Notes |
|---|---|---|
| Arduino Uno or Nano running ArduinoISP | Yes | The easiest route. The sketch already handles the 8051 reset polarity. |
| USBasp | No | Needs patched firmware or one inverter gate. See trap 3. |
| Dedicated AT89S52 USB programmer | Yes | 600 to 1500 INR, sold as "8051 ISP programmer". Uses its own software. |

If you have an Arduino anywhere in the house, use it. Section 5 of
`docs\FLASHING.md` has the sketch change, the avrdude configuration block, and
the exact command.

### C2. Wire it

Six connections to the ISP header. Before connecting:

- Set **SW6, SW7 and SW8 to OFF**. Those three DIP switches share the SPI pins
  with the programmer. A closed switch fights it.
- Confirm the crystal and both 30 pF capacitors are fitted. The chip programs
  through the on-chip oscillator, so no crystal means no programming.
- Power the board from its own adapter. Leave the programmer's VCC pin
  unconnected unless the board is small enough to run from USB.

| Signal | AT89S52 pin | Arduino pin |
|---|---|---|
| MOSI | P1.5, pin 6 | 11 |
| MISO | P1.6, pin 7 | 12 |
| SCK | P1.7, pin 8 | 13 |
| RESET | pin 9 | 10 |
| GND | pin 20 | GND |

Ground must be common between the board and the programmer.

### C3. Flash

With an Arduino:

```
avrdude -C avrdude-8051.conf -c avrisp -p 89s52 -P COM3 -b 19200 -U flash:w:01_led_blink.hex:i
```

The line that proves it worked:

```
avrdude: Device signature = 0x1e5206 (probably 89s52)
```

Then `1129 bytes of flash written` and `1129 bytes of flash verified`.

With a USBasp and ProgISP: select chip `AT89S52`, load the HEX, tick Chip
Erase, Program Flash and Verify Flash, click Auto. Three Success lines.

Both routes are written out in full in `docs\FLASHING.md`.

### C4. Power on

1. Disconnect the programmer.
2. Power off, wait two seconds, power on.

All eight LEDs blink together, half a second on, half a second off. That is
program 01 running. The chip keeps the program with the power off and restarts
into it every time.

---

## Part D - The 13 programs, in order

Flash them in this order. Each overwrites the previous one, because there is
only one flash.

| Order | Program | What you should see |
|---:|---|---|
| 1 | 01_led_blink | All eight LEDs blink together at 1 Hz |
| 2 | 02_led_patterns | Sweep, then alternate, then binary count |
| 3 | 03_switch_led | Each switch lights its matching LED |
| 4 | 04_seg7_counter | Display counts 00 to 99 |
| 5 | 05_timer0_second | One count per second, timed not delayed |
| 6 | 06_square_wave | 1 kHz on P3.4, needs JP1 removed and a scope |
| 7 | 07_ext_interrupt | Pressing PB1 increments the count |
| 8 | 08_uart_echo | Terminal at 9600 8N1 echoes every character |
| 9 | 09_uart_commands | Commands L, S, R, A, T read the board |
| 10 | 10_adc_7seg | Display shows the LM35 temperature |
| 11 | 11_adc_lcd | LCD shows temperature and a bar graph |
| 12 | 12_industrial_monitor | Zones, alarm, relay, telemetry |
| 13 | 13_selftest | Walks every output and reports faults |

`hardware\TESTING.md` has 20 numbered tests, T1 to T20, each with the
measurement to take and the tolerance it must meet. If you are being graded,
that table is your result sheet.

---

## Part E - When it does not work

Work down this list. Most faults are in the first four rows.

| Symptom | First thing to check |
|---|---|
| Nothing happens at all | 5 V between pins 40 and 20. Then pin 31 tied to +5 V. |
| Programming works, chip does nothing | Pin 31 to +5 V. Then the crystal: 3.5 to 5 V peak to peak on pin 18. |
| `initialization failed, rc=-1` | Trap 3. Wrong programmer polarity, or SW6 to SW8 not OFF. |
| `target doesn't answer` | Crystal not fitted or not oscillating. Check both 30 pF capacitors. |
| Signature reads 0x000000 or 0xFFFFFF | No common ground, or chip not powered. |
| Chip programs, hangs when running | Reset network. R1 10 k to GND and C2 10 uF to +5 V on pin 9. |
| Timing is 8 percent fast | Wrong crystal. Must be 11.0592 MHz, not 12. |
| Serial link gives garbage | Wrong crystal, or baud rate not 9600 8N1. |
| Some LEDs or segments dead | Latch orientation, or the 470 Ohm resistor bank fitted backwards. |
| LCD blank | Contrast potentiometer R9. It is usually just the wiper position. |

A chip that programs correctly but will not run almost always has a bad reset
circuit. Check R1 and C2 on pin 9 before suspecting the code.

---

## Where each file lives

| File | What it is |
|---|---|
| `START_HERE.md` | This document |
| `README.md` | What the project is and why the design is shaped this way |
| `docs\SOFTWARE_RUNBOOK.md` | The software half only, as a tick-box runbook with a lab-day timeline |
| `docs\FACULTY_DEMO.md` | Showing it to faculty: bench setup, 12 minute script, viva question bank |
| `docs\DEMO_CARD.md` | The one page you keep under the board during the demo |
| `docs\LAPTOP_SETUP.md` | Installing Keil, the eval limits, licence routes |
| `docs\FLASHING.md` | Programmers, wiring, avrdude, ProgISP, fault table |
| `hardware\BOM.csv` | 80 parts with Indian sources and prices |
| `hardware\SCHEMATIC.md` | Every pin of every chip, with the design calculations |
| `hardware\ASSEMBLY.md` | Stages 0 to 10, with a test after each |
| `hardware\TESTING.md` | Tests T1 to T20 with tolerances |
| `firmware\src\` | The 13 programs |
| `firmware\inc\board.h` | The shared driver library |
| `firmware\keil\` | 26 ready made uVision projects |
| `tools\Build-All-HEX.bat` | Builds all 13 and reports sizes |
| `docs\guide\video\` | Two narrated walkthrough videos |
