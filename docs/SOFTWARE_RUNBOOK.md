# Software Runbook - from an empty laptop to a circuit that runs by itself

This is the software half of the project, written as a list of things you do in
order. Tick each box. When the last box is ticked, the board runs with no laptop
attached.

If you only read one section, read **Section 6 (lab day)**. That is the part
that has to go right in front of your evaluator.

Related documents, for depth only - you do not need them to finish:

| Document | Use it when |
|---|---|
| `START_HERE.md` | the whole project, hardware included |
| `docs/LAPTOP_SETUP.md` | Keil will not install, or the 2 KB limit bites |
| `docs/FLASHING.md` | the programmer will not talk to the chip |
| `firmware/README.md` | you need to know what a driver function does |
| `hardware/ASSEMBLY.md` | you are actually soldering the board |
| `hardware/TESTING.md` | the result sheet, tests T1 to T20 |

---

## 0. What "the software part" actually is

Three things, and only three:

1. **Source code** - 13 programs in `firmware/src/`, already written, in Keil C51.
2. **HEX files** - the same 13 programs compiled into the machine code a chip can
   hold. This is the step you do on your laptop. It is the only real work.
3. **A chip that has one of those HEX files inside it** - done in the lab with a
   programmer, six wires, about 90 seconds.

The important idea, because it answers "how does it start running when I reach
the lab":

> The AT89S52 keeps its program in flash memory that does not need power. You
> write a program into it once. From then on, **every time you switch the board
> on, the chip starts that program by itself**. No laptop, no compiler, no
> "Run" button. The circuit runs because power reached pin 40.

So the sequence is always the same, and it is the sequence this document follows:

```
laptop:  source  ->  Keil  ->  .hex file
                                 |
                        pen drive (or the lab PC)
                                 |
bench:   8051 chip  <-  programmer  <-  .hex file
                        |
                    power on  ->  it runs
```

You load **one program at a time**. There is one flash, so program 2 overwrites
program 1. Flicking between them is normal and is what the demo is.

---

## 1. Two days before: laptop preparation

Do this at home. The lab machine does not need Keil, and you do not want to be
installing a compiler while a queue waits for the bench.

- [ ] **A Windows laptop.** Keil is Windows only. No Mac, no Linux, no
      Chromebook, no phone.
- [ ] **The repository, extracted to a path with no spaces.** Good:
      `C:\8051lab\`. Bad: `C:\Users\Aditya\Downloads\8051 hardware lab (1)\`.
      Spaces break the include path and give you 40 confusing errors.
      Download the ZIP from GitHub, extract, then check there is not a folder
      inside a folder with the same name - move the inner one up if there is.
- [ ] **Keil C51 installed.** Go to <https://www.keil.com/demo/eval/c51.htm>,
      download **C51** (not MDK-ARM), install to the default `C:\Keil_v5\`.
- [ ] **Proof that the 8051 tools installed, not just ARM.** Open uVision,
      `Project > New uVision Project`, and look for **Atmel > AT89S52** in the
      device list. If the list is empty or shows only Arm parts, you installed the
      wrong package.
- [ ] **A pen drive**, with room for the repo plus your notes.

You do **not** need a licence to build programs under 2048 bytes. Programs
01 to 08 fit. Programs 09, 12 and 13 are bigger and will refuse to build in the
free version. Section 3 handles that, and it is not a problem for the demo.

---

## 2. Build one program first, by hand

Never start with "build all 13". Build one, read the log, then batch the rest.
If the single build fails, 13 identical failures tell you nothing.

- [ ] Open `firmware\keil\` and double-click **`01_led_blink_AT89S52.uvprojx`**.
      Note the `_AT89S52` ending. There is also a `..._AT89C51` project; that chip
      has no ISP interface and cannot be flashed with a cheap programmer.
      Always take the `_AT89S52` one.
- [ ] If uVision offers to migrate the project to a newer version, say yes.
- [ ] Press **F7** (`Project > Rebuild all target files`).
- [ ] Read the build output window at the bottom. You are looking for exactly
      two things:

```
Program Size: data=30.0 xdata=0 code=1129
"01_led_blink" - 0 Error(s), 20 Warning(s).
```

- [ ] `0 Error(s)`. That is the pass condition.
- [ ] About 20 warnings, all saying `L16: UNCALLED SEGMENT`. Expected and
      harmless: `board.h` carries all 26 drivers and this program calls three,
      so the linker mentions the other 23. They are not errors.
- [ ] `code=1129` - a number under 2048. That is the program's size in bytes.

- [ ] Look at `firmware\keil\Objects\01_led_blink.hex`. It exists. That is a
      program that can go into a chip.

**If you got `FATAL ERROR L250: CODE SIZE LIMIT ... LIMIT: 0800H BYTES`** you
picked a big program by accident, or your Keil is the free version and the program
is genuinely over 2048 bytes. That is Section 3's job.

---

## 3. Build all 13 at once

- [ ] In `tools\`, double-click **`Build-All-HEX.bat`**.
      If Windows blocks it: right-click, `Run with PowerShell`, or open PowerShell
      yourself and type:

```powershell
cd C:\8051lab\tools
.\build_all_hex.ps1
```

- [ ] It finds Keil by itself, builds 13 projects, and prints a table:

```
  PROGRAM              CODE    DATA     ERR    WARN  HEX         STATE
  --------------------------------------------------------------------
  01_led_blink         1129    30.0       0      20  ok          OK
  02_led_patterns      1180    30.0       0      18  ok          OK
  ...

  11 ready, 2 over the 2048 byte limit, 0 failed.
```

- [ ] Read the **STATE** column only.

| STATE | Meaning | Do what |
|---|---|---|
| `OK` | built, fits, HEX checked | nothing, it is ready |
| `OVER LIMIT` | built but bigger than 2048 bytes | Section 3.1 |
| `ERRORS` | a real code or project problem | open that one project, rebuild, read the message |
| `BAD HEX` | no reset jump at address 0 | rebuild that project from clean |
| `FATAL` | the 2 KB limit or a linker licence | Section 3.1 |

- [ ] Every HEX that says `OK` has now been copied into `firmware\hex\`.
      That folder is your deliverable.

### 3.1 The programs that come back OVER LIMIT

Expect **09, 12 and 13** to be over on the free compiler, and 11 to be close.
This is the 2048 byte evaluation cap, not your code. Two switches, cheapest first:

```powershell
.\build_all_hex.ps1 -Small          # optimisation 9, favours size, ~5-15% smaller
.\build_all_hex.ps1 -Small -LX51    # also deletes every driver the program never calls
```

`-LX51` is the one that recovers real space, because `board.h` otherwise pulls all
26 drivers into every program. If it answers `L257: Extended Linker Requires
Upgrade to PK51`, your licence level does not include it - use `-Small` only.

Three honest ways out, in order of preference:

1. **Build on the college's licensed PC.** The lab almost certainly has full
   PK51. Copy the whole repo onto the pen drive, open the four projects there,
   press F7, copy the HEX files back. Costs 15 minutes and solves it completely.
2. **Free full PK51 from Silicon Labs.** Steps in `docs/LAPTOP_SETUP.md`
   section 4 (product serial number, CID, LIC). Grey area for an Atmel part,
   but it builds.
3. **Trim `firmware/inc/board.h` by hand** for programs 12 and 13: delete the
   drivers those two never call. Last resort, and remember to keep a copy.

Programs 09, 12 and 13 are the good demo ones, so do not skip this - but note
that programs **01 to 08 and 10** are enough to prove the whole board works, and
those build for free.

---

## 4. Check the HEX files before you trust them

- [ ] Open one HEX in Notepad. It is plain text.
- [ ] The **first line starts with** `:0300000002...` - three bytes at address 0,
      the first being opcode `02` (a long jump). That is the chip's boot jump.
- [ ] The **last line is exactly** `:00000001FF`.
- [ ] If both are true, the file boots. `Build-All-HEX.bat` already checks this,
      which is why it prints `ok` in the HEX column.

---

## 5. Pack the pen drive

Everything below, on one pen drive. This is your entire software submission.

- [ ] `firmware\hex\` - the compiled programs. **This is the important one.**
- [ ] `firmware\src\` and `firmware\inc\` - the source, in case you must rebuild.
- [ ] `firmware\keil\` - the projects, in case the lab PC is licensed.
- [ ] `docs\FLASHING.md` - the programmer wiring and the commands.
- [ ] `docs\SOFTWARE_RUNBOOK.md` - this file.
- [ ] A screenshot or photo of the **build table** from Section 3.
      Evaluators like evidence that all 13 compile.
- [ ] `hardware\TESTING.md` printed, if you are being marked on measurements.

---

## 6. Lab day, minute by minute

Target: **90 minutes** from walking in to a board that is running.

### 0:00-0:20 - Board is built and the power is right

Do not skip this because "the power supply was fine at home". Every dead 8051
story starts here.

- [ ] Board unpowered, no chip in the socket yet (sockets, not soldered chips).
- [ ] Power the board from its own 5 V adapter.
- [ ] Multimeter, DC volts, black probe on GND, red on the +5 V rail:
      **4.90 to 5.10 V**. If not, stop - fix the supply, do not fit the chip.
- [ ] Power off. Fit both chips: the AT89S52 in its 40-pin socket, the 74HC573s
      in theirs, all with pin 1 in the right place.
- [ ] Power on again, confirm 5 V **between pin 40 and pin 20** of the chip
      socket pins themselves.
- [ ] Confirm pin 31 (EA) sits at 5 V. Miss this and the chip looks for code
      that is not there, and does absolutely nothing.
- [ ] Confirm the 11.0592 MHz crystal and both 30 pF capacitors are fitted.
      The chip programs through its own oscillator: **no crystal, no programming.**

### 0:20-0:30 - Prepare for programming

- [ ] Power off.
- [ ] **DIP switches 6, 7 and 8 to OFF.** They share P1.5, P1.6, P1.7 with the
      programmer and will corrupt the transfer. This single mistake looks exactly
      like a dead chip.
- [ ] Connect the programmer to the 2x5 ISP header **J3**. Ground must be common
      with the board. Leave the programmer's VCC pin unconnected; the board runs
      from its own adapter.

| Signal | J3 pin | AT89S52 pin | Arduino pin (Arduino-as-ISP) |
|---|---:|---|---:|
| MOSI | 1 | P1.5 (6) | 11 |
| MISO | 9 | P1.6 (7) | 12 |
| SCK | 7 | P1.7 (8) | 13 |
| RESET | 5 | RST (9) | 10 |
| GND | 4 | GND (20) | GND |
| VCC | 2 | - | leave disconnected |

- [ ] Power the board on. The programmer is powered from USB.

> If you bought a **USBasp**: a stock one often cannot program an AT89S52 at all,
> because AVR chips reset on a low signal and the 8051 resets on a high one. It
> reports `initialization failed, rc=-1`, which is not a wiring fault. Use an
> Arduino as ISP (free, works immediately) or a dedicated "8051 ISP programmer".
> Details in `docs/FLASHING.md` sections 1 and 5.

### 0:30-0:40 - Flash program 01

Pick your route.

**Route A - Arduino as ISP + avrdude** (recommended)

- [ ] Arduino IDE, `File > Examples > 11.ArduinoISP > ArduinoISP`, uncomment
      `#define USE_OLD_STYLE_WIRING`, upload to the Arduino.
- [ ] Device Manager, `Ports (COM and LPT)` - note the COM number, say COM3.
- [ ] Create `avrdude-8051.conf` next to `avrdude.exe` with the AT89S52 block
      from `docs/FLASHING.md` section 5.2 (`stk500_devcode = 0xE1` is the line
      that matters).
- [ ] Run:

```
avrdude -C avrdude-8051.conf -c avrisp -p 89s52 -P COM3 -b 19200 -U flash:w:01_led_blink.hex:i
```

- [ ] Success looks exactly like this:

```
avrdude: Device signature = 0x1e5206 (probably 89s52)
avrdude: 1129 bytes of flash written
avrdude: 1129 bytes of flash verified
```

**Route B - USBasp with ProgISP / Khazama** (Windows, GUI)

- [ ] Select chip **AT89S52**, load the HEX, tick `Chip Erase`, `Program Flash`,
      `Verify Flash`, click **Auto**. You want three `Success` lines.

**Route C - Dedicated 8051 programmer**

- [ ] Use the vendor's own software, same idea: select AT89S52, erase, program,
      verify.

### 0:40-0:45 - First run, on its own

This is the moment the software half is done.

- [ ] **Disconnect the programmer.**
- [ ] Power off, wait two seconds, power on.

**All eight LEDs blink together, half a second on, half a second off.**

- [ ] If yes: the software works, the chip works, the board works. Everything
      after this is showing off.
- [ ] If no: Section 8. Do not start re-flashing randomly; the fault is almost
      always one of six things and the table finds it in a minute.

### 0:45-1:15 - The remaining programs, in order

Re-flash each one and confirm what you see. Screenshot or film each - that is
your evidence pack.

| Order | HEX to flash | What you should see | Needs a PC? |
|---:|---|---|---|
| 1 | `01_led_blink` | all 8 LEDs blink, 1 Hz | no |
| 2 | `02_led_patterns` | sweep, alternate, binary count | no |
| 3 | `03_switch_led` | each DIP switch lights its LED | no |
| 4 | `04_seg7_counter` | 7-segment counts 00 to 99 | no |
| 5 | `05_timer0_second` | one change per second, timed | no |
| 6 | `06_square_wave` | 1 kHz on a scope, **remove JP1 first** | scope only |
| 7 | `07_ext_interrupt` | pressing PB1 changes the pattern | no |
| 8 | `08_uart_echo` | terminal echoes each character | yes, serial |
| 9 | `09_uart_commands` | commands `L`, `S`, `R`, `A`, `T` | yes, serial |
| 10 | `10_adc_7seg` | display shows LM35 temperature | no |
| 11 | `11_adc_lcd` | LCD shows temperature + bar graph | no |
| 12 | `12_industrial_monitor` | zones, relay, buzzer, telemetry | partly |
| 13 | `13_selftest` | walks every output, prints PASS or FAIL | yes, serial |

- [ ] Serial programs: USB-to-RS232 adapter into the DB9, terminal at
      **9600 baud, 8 data bits, no parity, 1 stop bit, no flow control**
      (PuTTY, Tera Term, or the Arduino IDE Serial Monitor). No line-ending
      translation.

### 1:15-1:30 - Leave it running

- [ ] Load `13_selftest.hex` if you want a final PASS report, or
      `12_industrial_monitor.hex` if you want the board to sit there doing the
      full job.
- [ ] Disconnect the programmer, power cycle, confirm it runs from cold.
- [ ] Leave the board powered and running. **This is the deliverable:** a circuit
      that starts itself.

### If you are short on time

Flash only two things: **12** (the full system: zones, relay, buzzer, telemetry)
and **13** (self-test, which proves every subsystem in one go). Those two plus
program 01 cover 90 % of what an evaluator asks.

---

## 7. What "done" looks like - the evidence pack

Keep these five things. They are what you show if marks are challenged:

1. The build table from Section 3 - all 13 compile, sizes listed.
2. `firmware\hex\` - 13 HEX files.
3. A video, 20 seconds, of the board blinking on power-up with nothing attached.
4. The `13_selftest` output showing `SELF TEST: PASS`.
5. `hardware/TESTING.md` with the measured column filled in.

---

## 8. It does not run - triage in one minute

Work top to bottom. The first four rows are 90 % of real faults.

| Symptom | Likely cause | Check |
|---|---|---|
| Nothing lights, ever | no power, or no program in the chip | 5 V between pin 40 and pin 20; then re-flash |
| Programs and verifies fine, chip does nothing | **EA pin 31 floating** | meter pin 31, must be 5 V |
| Same, but pin 31 is at 5 V | crystal not oscillating | crystal fitted? both 30 pF caps? 3.5-5 V p-p on pin 18 |
| Chip runs, then hangs or restarts randomly | reset network wrong | R1 10 k from pin 9 to GND, C2 10 uF from pin 9 to +5 V |
| `initialization failed, rc=-1` | USBasp polarity (AVR vs 8051 reset) | use Arduino-as-ISP, or check SW6-SW8 are OFF |
| `target doesn't answer` | no oscillator, or no common ground | crystal, caps, GND between board and programmer |
| Signature `0x000000` / `0xFFFFFF` | chip unpowered or no common ground | board's own adapter on, GND shared |
| LEDs or segments partly dead | hardware: latch direction, resistor bank | move to `hardware/ASSEMBLY.md` stage 3/5 |
| Timing 8 % fast | wrong crystal | must be **11.0592 MHz**, not 12 |
| Serial is garbage | wrong baud or wrong crystal | 9600 8N1, 11.0592 MHz crystal |
| LCD blank | contrast pot R9 | turn the pot; it is usually just the wiper |
| Everything fine but program 12/13 missing | 2 KB evaluation limit | Section 3.1 |

The rule that saves the most time:

> **A chip that programs and verifies but does not run is a hardware problem
> every time.** Flash, verify and silence mean the software is in the chip
> correctly. Stop editing code and go look at pin 31, the crystal, and the reset
> circuit.

---

## 9. Appendix - the whole thing as copy-paste commands

```powershell
# 1. build one program (open the project in uVision and press F7, or:)
"C:\Keil_v5\UV4\UV4.exe" -j0 -r "C:\8051lab\firmware\keil\01_led_blink_AT89S52.uvprojx" -o build.log

# 2. build all 13, copy HEX into firmware\hex
cd C:\8051lab\tools
.\build_all_hex.ps1

# 3. if anything is OVER LIMIT
.\build_all_hex.ps1 -Small
.\build_all_hex.ps1 -Small -LX51

# 4. see what you produced
dir ..\firmware\hex

# 5. flash (Arduino as ISP; change COM3 to your port)
avrdude -C avrdude-8051.conf -c avrisp -p 89s52 -P COM3 -b 19200 -U flash:w:01_led_blink.hex:i
```

Terminal settings for programs 08, 09, 12, 13: **9600 / 8 / N / 1 / no flow
control**.

---

## 10. The five-line version

1. Install Keil C51 on a Windows laptop.
2. Open `01_led_blink_AT89S52.uvprojx`, press F7, see `0 Error(s)`.
3. Run `tools\Build-All-HEX.bat`, get 13 HEX files in `firmware\hex`.
4. Pen drive. Lab. 5 V check, SW6-8 OFF, programmer on J3, flash.
5. Power cycle. It runs. Nothing else needed - the chip remembers.
