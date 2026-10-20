# Doing the code work on your own laptop

How to write, build and check the 8051 firmware away from the lab machine, and
how to get it onto the chip. Read the first section before you install anything,
because one of the choices has a trap in it that will cost you an evening.

## Contents

1. The three routes
2. Route A: Keil uVision on Windows
3. The 2 KB trap
4. Getting a licence
5. Opening the projects in this repository
6. Building and finding the .hex file
7. Flashing the chip
8. Route B: working with no hardware at all
9. Route C: licence-free builds with SDCC
10. Workflow: home versus lab
11. Troubleshooting

---

## 1. The three routes

| Route | What you need | What you get | Catch |
|---|---|---|---|
| **A. Keil on Windows** | Windows laptop | The real toolchain, exactly what the lab uses | Free version is capped at 2 KB of code |
| **B. Simulator** | Any laptop | Run and step the logic with no board | Does not prove the wiring |
| **C. SDCC** | Windows, macOS or Linux | Free compiler, no licence, no limit | Different syntax; used for checking, not for the final build |

Most people end up using **A for the final build and B or C at home**, then
flashing in the lab. That is the combination described in section 10.

---

## 2. Route A: Keil uVision on Windows

Keil is Windows software. There is no macOS or Linux version. On Linux it can be
made to run under Wine, and on macOS under a virtual machine, but both are more
trouble than they are worth.

1. Go to **https://www.keil.com/download/product/**
2. Click **C51** (not MDK-Arm). The current version is C51 v9.61.
3. Fill in the form. It asks for a real address and phone number; the download
   is a normal executable.
4. Run the installer and accept the default path, `C:\Keil\`. Installing
   somewhere else causes include-path problems later.
5. Launch uVision.

You do not need a licence to install it. You do need one to build anything over
2 KB, which is the next section.

---

## 3. The 2 KB trap

This is the single most important thing in this document.

The free evaluation version of the C51 compiler, assembler and linker is limited
to **2 KB of object code** (2048 bytes, shown as `0800H`). Source code may be any
size. When you exceed it, the linker stops with:

```
*** FATAL ERROR L250: CODE SIZE LIMIT IN RESTRICTED VERSION EXCEEDED
    MODULE:  C:\Keil\C51\LIB\C51S.LIB (-----)
    LIMIT:   0800H BYTES
```

The evaluation version also places code at offset `0x0800` instead of `0x0000`,
so even a program that fits will not run correctly on the board until it is
built with a licensed compiler.

**This matters for this project.** The largest program here,
`12_industrial_monitor.c`, is about 3.4 KB compiled. It will not build in the
evaluation version, and neither will most of the later programs. The early ones
(`01_led_blink` through roughly `05_timer0_second`) are small enough to build,
which is useful, but they are not the ones you need.

So: if you plan to work at home, either get a licence (next section) or use
Route C for local checking and build the real thing on a licensed machine.

To find out where you stand, open any project, go to **Help > License
Management** (with the project open, or the option is greyed out) and read the
serial number. If it says `EVAL VERSION`, you are capped.

---

## 4. Getting a licence

In order of how much I would recommend them:

**Use the college's licensed machines.** The lab almost certainly has full PK51
licences. This is the clean route, it costs nothing, and it is what the project
is specified against. Build the final `.hex` files there.

**Free PK51 from Silicon Labs.** Silicon Labs gives away a full, unlimited PK51
licence for 8051 development. The steps are in their application note AN104
(https://www.silabs.com/documents/public/application-notes/an104.pdf):

1. Get a Product Serial Number from https://pages.silabs.com/lp-keil-pk51.html
   (a PSN that has been published on their product page is `32KW7-ECJ6G-YN57V`).
2. In uVision, open **File > License Management** and copy the CID.
3. Go to https://www.keil.com/license/install.htm, enter the PSN and CID, and a
   License ID Code (LIC) is emailed to you.
4. Paste the LIC into the **New License ID Code** box and click **Add LIC**.

The licence arrives as "PK51 Prof. Developers Kit for Silabs" and it removes the
code size limit entirely. Be aware this is intended for Silicon Labs parts, and
it is build-support only with no debugging. Using it for an Atmel part is a grey
area, so treat it as a stopgap and build the submitted firmware on the college's
own licensed tools.

**Buy it.** A PK51 licence is not cheap, and is not worth it for one project.

**Do not use a keygen.** Beyond the obvious, a cracked toolchain on a machine
you submit coursework from is a risk you do not need, and the generated binaries
carry the evaluation stub anyway.

---

## 5. Opening the projects in this repository

There are 26 ready-made projects in `firmware/keil/`. Each of the 13 programs
has one for the AT89S52 and one for the AT89C51:

```
firmware/keil/12_industrial_monitor_AT89S52.uvprojx
firmware/keil/12_industrial_monitor_AT89C51.uvprojx
```

**Use the `_AT89S52` ones.** The AT89C51 projects are there so the same source
can be compiled for the older chip, but see section 7 about why they cannot be
flashed with the programmer in this build.

To open one: **Project > Open Project**, browse to `firmware/keil/`, and pick
the file. The projects already have the right settings:

| Setting | Value |
|---|---|
| Vendor | Atmel |
| Device | AT89S52 |
| Create HEX File | yes |
| Include path | `..\inc` |
| Optimisation level | 8 |

**One thing is not set and you should set it.** The crystal frequency is not
stored in these project files, so uVision will default to 12 MHz. Everything in
this project is timed off 11.0592 MHz, and the baud rate calculation depends on
it exactly. Go to **Options for Target > Target** and set **Xtal (MHz)** to
`11.0592`. If you forget, the simulator's timing will be wrong and any
calculated delays will be off by about 8 percent.

Keep the folder structure as it is. The projects reach the shared header through
`..\inc`, so `board.h` must stay one directory up from the project files.

---

## 6. Building and finding the .hex file

1. **Project > Build Target**, or press F7.
2. The Build Output window at the bottom shows the result. A clean build ends
   with a line like `Program Size: data=30.0 xdata=0 code=3402` and
   `0 Error(s), 0 Warning(s)`.
3. The `.hex` file lands in `firmware/keil/Objects/`, named after the program,
   for example `Objects\12_industrial_monitor.hex`.

If you see `L250` here, go back to section 3.

If you see `WARNING L16: UNCALLED SEGMENT, IGNORED FOR OVERLAY PROCESS`, that is
harmless here: it is the linker noticing an interrupt service routine that no
code calls directly, which is normal, since the hardware calls it.

---

## 7. Flashing the chip

### The AT89S52 is programmed over SPI, in circuit

You do not remove the chip. Six wires are needed, and **the crystal and its two
capacitors must already be fitted**, because the chip needs a clock to accept
programming:

| Programmer | AT89S52 pin | Pin number |
|---|---|---|
| MOSI | P1.5 | 6 |
| MISO | P1.6 | 7 |
| SCK | P1.7 | 8 |
| RESET | RST | 9 |
| VCC | VCC | 40 |
| GND | GND | 20 |

### A stock USBasp will not work

This is the second trap, and it is the reason people conclude their programmer
is broken.

A standard USBasp is an AVR programmer. AVR chips reset on a **low** signal; the
8051 resets on a **high** one. Stock USBasp firmware drives RESET the AVR way, so
the AT89S52 never enters programming mode and avrdude reports:

```
avrdude: error: program enable: target doesn't answer.
```

Your options:

- **Use an Arduino as the programmer.** This is the easiest route and the one I
  would take. Upload the **ArduinoISP** sketch (`File > Examples > 11.ArduinoISP`)
  to any Arduino, wire it as above, and use the avrdude that ships with the
  Arduino IDE with an 8051-aware configuration file. Full instructions:
  https://www.instructables.com/Program-8051-With-Arduino/
- **Buy a dedicated 8051 ISP programmer.** Widely sold as a "USB ISP programmer
  for 8051 / AT89S5x" and cheap. Unlike a generic USBasp, its firmware drives
  RESET correctly. This is what to buy if you are ordering anyway.
- **Re-flash the USBasp** with 8051-capable firmware. Do not bother: flashing the
  USBasp itself needs a second programmer, so you are back where you started.

With a working 8051-capable programmer and an 8051-aware `avrdude.conf`, the
command looks like:

```
avrdude -c usbasp -p 8052 -U flash:w:12_industrial_monitor.hex:i
```

`-p 8052` is the avrdude part name for the AT89S52. Do **not** try to read or
write fuse bits: the 8051 has no fuses and the attempt returns a confusing error.

### The AT89C51 cannot be programmed this way at all

The "C" part has no SPI programming interface. It needs a **parallel**
programmer with a **12 V VPP** supply. The "S" part was created specifically to
fix this, which is why the board is specified around the AT89S52.

The `_AT89C51` projects are still useful: they prove the source compiles for the
older part, which is a legitimate thing to show. They just cannot be flashed
with the hardware in this build.

---

## 8. Route B: working with no hardware at all

If you want to write and test logic on the laptop with no board, use a
simulator. This is genuinely useful for getting ahead before a lab session.

| Simulator | Cost | Platforms | Good for |
|---|---|---|---|
| **Proteus VSM** | paid (trial available) | Windows | Whole circuit: chip plus LEDs, LCD, sensor. Most common in Indian engineering colleges, and it will simulate this board directly from a `.hex` file. |
| **EdSim51** | free | Windows, macOS, Linux (Java) | Learning the instruction set. Has virtual LEDs, 7-segment, keypad, UART, ADC. Download: https://sourceforge.net/projects/edsim51/ |
| **MCU 8051 IDE** | free | Windows, Linux | Free IDE with a built-in simulator and SDCC support. https://sourceforge.net/projects/mcu8051ide/ |
| **ucsim** | free | Windows, macOS, Linux | Command-line simulator that ships with SDCC. Good for automated checks. |

**Proteus is the one to use if your college has it.** Draw the circuit, point the
AT89C52/AT89S52 part at your `.hex` file, set the clock to 11.0592 MHz, and run
it. You get the LEDs, the display and the LCD animating, which is as close to
the real board as you will get without the hardware.

Note that a simulator proves the **logic**. It does not prove the **wiring**, the
pull-ups, the current limits, or whether your particular LM35 is wired the right
way round. Budget lab time for that.

---

## 9. Route C: licence-free builds with SDCC

SDCC is a free, open-source 8051 compiler with no code size limit and versions
for Windows, macOS and Linux. Its syntax differs slightly from Keil's, which
matters: **the source in this repository is deliberately written in Keil C51
style** (`sbit`, `interrupt n`, `REGX52.H`), so it will not compile under SDCC
unchanged.

The repository includes `tools/check_sdcc.py`, which copies the source to a
scratch directory, applies the small set of syntax translations needed for SDCC,
compiles all 13 programs, and reports the code size of each. It never touches
the original files.

```
sudo apt install sdcc          # Linux
brew install sdcc              # macOS
# Windows: https://sdcc.sourceforge.net/

python3 tools/check_sdcc.py
```

The translations it applies:

| Keil C51 | SDCC |
|---|---|
| `sbit NAME = P2^0;` | `__sbit __at (0xA0) NAME;` (approximated as a plain byte) |
| `void isr(void) interrupt 1` | `void isr(void) __interrupt(1)` |
| `using 1` | `__using(1)` |
| `unsigned char code tbl[]` | `unsigned char __code tbl[]` |
| `#include <REGX52.H>` | `#include <8052.h>` |

Use this to catch syntax errors, typos and logic mistakes at home for free. Then
open the same, unmodified `.c` files in Keil for the real build.

---

## 10. Workflow: home versus lab

**At home, on the laptop:**

1. Edit the `.c` files in `firmware/src/` and `board.h` in `firmware/inc/`. Any
   editor works; VS Code is fine.
2. Check it compiles. Use `tools/check_sdcc.py` if you have no Keil licence, or
   Keil directly if you do.
3. If you have a licence, build in Keil and check the reported code size against
   the 8192 byte flash limit.
4. Simulate in Proteus or EdSim51 to watch the logic run.
5. Commit your work and push it.

**In the lab:**

1. Pull your latest commit onto a licensed machine.
2. Open the matching `_AT89S52.uvprojx`, set Xtal to 11.0592 if it is not
   already, and do **Project > Rebuild All Target Files**. A clean rebuild
   matters: stale object files compiled by an evaluation version are a common
   cause of a mysterious `L250`.
3. Flash `Objects\<name>.hex` to the chip.
4. Run the matching test from `hardware/TESTING.md`.

That way the laptop is where you think and write, and the lab is only where you
compile the real binary and press go.

---

## 11. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `FATAL ERROR L250 ... LIMIT: 0800H BYTES` | Evaluation version, program over 2 KB | Get a licence, or use SDCC. Rebuild all; stale objects cause this too. |
| `RESTRICTED VERSION WITH 0800H BYTE CODE SIZE LIMIT` | Same, reported by the linker | Same. |
| Program builds but does nothing on the board | Code was linked at offset `0x0800` | Rebuild with a licensed compiler so code starts at `0x0000`. |
| `error: program enable: target doesn't answer` | Stock USBasp driving RESET with the wrong polarity, or no crystal fitted | Use an Arduino as ISP or a dedicated 8051 programmer. Check the crystal and its two 33 pF capacitors are in place. |
| Chip programs but will not run afterwards | RESET line not pulled up, or EA not tied high | Check the 10 k pull-up on RST and that EA (pin 31) is at 5 V. |
| `Cannot find file REGX52.H` | Include path wrong | Options for Target > C51 > Include Paths must contain `..\inc`. Do not move the folders. |
| Serial link gives garbage characters | Wrong crystal frequency assumed | Confirm Xtal is set to 11.0592 and that TH1 is `0xFD`. At 12 MHz the error is over 8 percent and the link fails. |
| `WARNING L16: UNCALLED SEGMENT` | Interrupt routine not called by any code | Normal. Ignore it. |
| LCD shows blocks on the top row only | Contrast too high, or init raced the power supply | Adjust the contrast pot. Add a longer delay before `lcd_init()`. |
| Everything works in the simulator but not on the board | Wiring, not code | Check the bus pull-up network RN1 on P0. Without it, P0 cannot drive high. |
