# Flashing the AT89S52

How to move a HEX file built in Keil on the laptop into the AT89S52 on the board.
The chip is programmed in circuit through SPI. No 12 V supply, no chip removal,
no parallel programmer. Six signal wires, one of which is optional.

Target device: AT89S52-24PU, 40 pin DIP, 11.0592 MHz, 5 V, 8 KB of flash.

---

## 1. Programmer options

| Option | Works out of the box | Cost | Notes |
|---|---|---|---|
| Arduino Uno or Nano as ISP | Yes | Free if you already have one | The current ArduinoISP sketch inverts RESET polarity for 8051 targets automatically. Recommended. |
| USBasp | No | 300 to 500 INR | Stock firmware drives RESET active low, the AVR convention. The AT89S5x needs RESET held high. Needs patched firmware or one inverter gate. |
| Dedicated 8051 USB programmer | Yes | 600 to 1500 INR | Sold as "AT89S52 programmer" or "8051 ISP programmer". Uses its own Windows software. |

The AT89C51 cannot be programmed this way at all. It has no SPI interface and
needs a 12 V parallel programmer. Only the AT89S52 variants of the project files
can be flashed with the steps below.

---

## 2. Prepare the HEX file in Keil

### 2.1 Name the output after the program

By default the HEX is named after the project, so every program would overwrite
the same `finalproject.hex`.

1. `Project` then `Options for Target 'Target 1'`, or press `Alt+F7`.
2. **Output** tab.
3. **Name of Executable**: `01_led_blink`
4. Confirm **Create HEX File** is ticked.
5. `OK`, then `Project` then `Rebuild all target files`.

The file appears at `<project folder>\Objects\01_led_blink.hex`.
Repeat with `02_led_patterns`, `03_switch_led` and so on, one build per program.

### 2.2 Read the HEX before you trust it

Open the HEX in Notepad. It is plain text.

The first data line must begin with `:030000000208`. That is three bytes at
address 0x0000: opcode `02` (LJMP) followed by `08` and a low byte. The last
line must be exactly `:00000001FF`.

If the first line is there, the file is valid and will boot on the chip.

### 2.3 Why the code sits at 0x0800

The evaluation toolchain locates your program at address 0x0800 and plants a
single long jump at the reset vector 0x0000 to reach it. The AT89S52 has
8 KB of flash, address 0x0000 to 0x1FFF, so 0x0800 plus your 1129 bytes fits
comfortably and the chip boots normally.

This is the reason the evaluation tools cannot be used on a 2 KB part such as
an AT89C2051: the code would land past the end of the flash. It is also the
reason the tools refuse anything over 2048 bytes with
`FATAL ERROR L250: CODE SIZE LIMIT ... LIMIT: 0800H BYTES`.

Nothing here is broken. The HEX is real and will run.

---

## 3. Prepare the board

Work through this list before connecting anything.

| Check | Requirement | Why |
|---|---|---|
| Crystal Y1 | 11.0592 MHz fitted across pins 18 and 19 | The ISP write timing is derived from the on chip oscillator. No crystal, no programming. |
| Load capacitors C3a, C3b | 30 pF from each crystal pin to GND | Oscillator will not start reliably without them. |
| EA/VPP, pin 31 | Tied to +5 V | Selects internal flash. Left floating the chip tries to fetch code from external memory. |
| VCC, pin 40 | +5 V, decoupled with 0.1 uF to GND | |
| GND, pin 20 | Common ground with the programmer | |
| Reset network | R1 10 k from pin 9 to GND, C2 10 uF from pin 9 to +5 V | Active high reset, correct for the AT89S52. |
| SW6, SW7, SW8 | Set to OFF | P1.5, P1.6 and P1.7 are the ISP lines and are shared with these three DIP switches. A closed switch fights the programmer. |
| Supply current | Board powered from its own 5 V adapter, not from the programmer | The board draws more than a USB port should supply once the LCD backlight and relay are fitted. |

Leave C2 in place for the first attempt. If the programmer cannot talk to the
chip, desolder or lift one leg of C2 and try again. A 10 uF capacitor on the
reset line makes the RESET edges slow, and some programmers pulse RESET faster
than the RC network can follow.

---

## 4. Wiring

The board carries a 2x5 pin ISP header, J3.

| J3 pin | Signal | AT89S52 pin |
|---:|---|---|
| 1 | MOSI | P1.5 (pin 6) |
| 2 | VCC | +5 V |
| 4, 6, 8, 10 | GND | GND |
| 5 | RESET | RST (pin 9) |
| 7 | SCK | P1.7 (pin 8) |
| 9 | MISO | P1.6 (pin 7) |

### 4.1 If you use an Arduino as ISP

| Arduino pin | J3 pin | Signal |
|---|---|---|
| 11 | 1 | MOSI |
| 12 | 9 | MISO |
| 13 | 7 | SCK |
| 10 | 5 | RESET |
| GND | 4 | GND |
| 5V | not connected | board uses its own supply |

Ground must be common. Power comes from the board's own adapter.

### 4.2 If you use a USBasp

The USBasp 10 pin header shares the same pinout as J3: 1 MOSI, 2 VCC, 4/6/8/10
GND, 5 RESET, 7 SCK, 9 MISO. A straight 10 pin ribbon works, but check the
board with a meter first. Cheap USBasp clones sometimes swap VCC and GND, and
the 5 V or 3.3 V jumper must be on 5 V.

Safer configuration: leave J3 pin 2 (VCC) unconnected and power the board from
its own adapter. Only MOSI, MISO, SCK, RESET and GND are needed.

---

## 5. Route A: Arduino as ISP

This is the route to try first. It needs no hardware modification because the
ArduinoISP sketch shipped with the Arduino IDE already handles the inverted
RESET polarity of the AT89 series.

### 5.1 Load the programmer firmware onto the Arduino

1. Open the Arduino IDE.
2. `File` then `Examples` then `11.ArduinoISP` then `ArduinoISP`.
3. Find the line `#define USE_OLD_STYLE_WIRING` and uncomment it. It sits around
   line 81. This moves the SPI signals to pins 11, 12 and 13 instead of the ICSP
   header, which is what the wiring table above assumes.
4. Upload the sketch to the Arduino.
5. Note the COM port the Arduino is on. Device Manager, `Ports (COM and LPT)`.

### 5.2 Give avrdude a definition for the AT89S52

avrdude does not ship with this part. Create a file `avrdude-8051.conf` next to
avrdude.exe and append the block below.

```
part
    id               = "89s52";
    desc             = "AT89S52";
    stk500_devcode   = 0xE1;
    signature        = 0x1e 0x52 0x06;
    chip_erase_delay = 500000;
    reset            = dedicated;
    pgm_enable       = "1 0 1 0  1 1 0 0    0 1 0 1  0 0 1 1",
                       "x x x x  x x x x    x x x x  x x x x";

    chip_erase       = "1 0 1 0  1 1 0 0    1 0 0 x  x x x x",
                       "x x x x  x x x x    x x x x  x x x x";

    memory "flash"
        size            = 8192;
        read            = "0 0 1 0 0 0 0 0  x x x a12 a11 a10 a9 a8",
                          "a7 a6 a5 a4 a3 a2 a1 a0 o o o o o o o o";
        write           = "0 1 0 0 0 0 0 0  x x x a12 a11 a10 a9 a8",
                          "a7 a6 a5 a4 a3 a2 a1 a0 i i i i i i i i";
        ;
    memory "signature"
        size            = 3;
        read            = "0 0 1 0 1 0 0 0  0 0 0 0 0 0 a1 a0",
                          "0 0 0 0 0 0 0 0  o o o o o o  o  o";
        ;
  ;
```

The `stk500_devcode = 0xE1` line is the important one. ArduinoISP reverses its
RESET output when the device code is 0xE0 or higher, which is exactly what the
AT89S52 needs.

avrdude comes with the Arduino IDE, typically at:

```
C:\Program Files (x86)\Arduino\hardware\tools\avr\bin\avrdude.exe
```

### 5.3 Flash

Open a command prompt in that folder and run:

```
avrdude -C avrdude-8051.conf -c avrisp -p 89s52 -P COM3 -b 19200 -U flash:w:C:\path\to\01_led_blink.hex:i
```

Change `COM3` to your Arduino's port and the path to your HEX file.

Expected output:

```
avrdude: AVR device initialized and ready to accept instructions
avrdude: Device signature = 0x1e5206 (probably 89s52)
avrdude: erasing chip
avrdude: reading input file "01_led_blink.hex"
avrdude: writing flash (1129 bytes):
avrdude: 1129 bytes of flash written
avrdude: verifying flash memory against 01_led_blink.hex:
avrdude: 1129 bytes of flash verified
avrdude done.  Thank you.
```

The signature `0x1e5206` is the confirmation that the chip answered. Everything
before that line is the programmer talking to itself.

---

## 6. Route B: USBasp

A stock USBasp will fail with:

```
avrdude: error: programm enable: target doesn't answer
avrdude: initialization failed, rc=-1
```

This is the polarity problem, not a wiring fault. The USBasp firmware holds
RESET low during programming because that is how an AVR enters programming
mode. The AT89S52 enters programming mode when RESET is held high.

Three ways out:

1. Reflash the USBasp with 8051 aware firmware. Look for
   `UsbAsp-flash_89S52`. It needs a second programmer to install, or the
   USBasp's own self programming jumper.
2. Add one inverter gate, a 74HC1G14 or 74HC04, between the USBasp RESET pin
   and J3 pin 5, with a jumper to bypass it when programming AVR parts. This is
   a two component fix and it is reliable.
3. Use the Arduino route above instead.

With the polarity solved, the Windows GUI ProgISP is the easiest front end:

1. Open ProgISP.
2. **Select Chip**: `AT89S52`.
3. Confirm the programmer is detected. The button next to the chip name stops
   being greyed out.
4. `File` then `Load Flash`, and pick `01_led_blink.hex`.
5. Tick **Chip Erase**, **Program Flash**, **Verify Flash**.
6. Click **Auto**.

The status bar reports `Chip Erase ... Success`, `Program Flash ... Success`,
`Verify Flash ... Success`. Any other result is a real failure, not a warning.

If signature verification fails but the chip is otherwise detected, untick
**Verify Signature**. Some clones report the bytes in a different order.

---

## 7. First run

1. Disconnect the programmer.
2. Power the board off, wait two seconds, power it on.
3. The eight LEDs on P0 flicker once as the ports initialise, then all eight
   blink together, half a second on, half a second off.

That is program 01 running. The chip is now a standalone system: it keeps the
program with the power off and restarts into it every time.

Build and flash the remaining programs in this order. Each one overwrites the
previous, because there is only one flash.

| Order | Program | What you should see |
|---:|---|---|
| 1 | 01_led_blink | All eight LEDs blink together at 1 Hz |
| 2 | 02_led_patterns | Knight rider sweep, then alternate, then binary count |
| 3 | 03_switch_led | SW1 to SW8 each light their matching LED live |
| 4 | 04_seg7_counter | Seven segment counts 00 to 99 |
| 5 | 05_timer0_second | Display counts one per second, timed not delayed |
| 6 | 06_square_wave | 1 kHz square wave on P3.4, visible on a scope |
| 7 | 07_ext_interrupt | INT0 button press increments the count |
| 8 | 08_uart_echo | Terminal at 9600 8N1 echoes every character typed |
| 9 | 09_uart_commands | Terminal commands L, S, R, A, T read the board |
| 10 | 10_adc_7seg | Display shows the LM35 temperature in Celsius |
| 11 | 11_adc_lcd | LCD shows the temperature and a bar graph |
| 12 | 12_industrial_monitor | Full monitor with alarm and relay, may exceed 2 KB |
| 13 | 13_selftest | Walks every output and reports faults on the LCD |

Programs 12 and 13 are the ones most likely to trigger `L250`. If they do,
enable the LX51 linker with `REMOVEUNUSED` as described in `LAPTOP_SETUP.md`,
or trim unused functions out of `firmware\inc\board.h`.

---

## 8. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `initialization failed, rc=-1` | RESET polarity, stock USBasp | Route A, or fit an inverter |
| `target doesn't answer` | No crystal, or crystal not oscillating | Fit Y1 and C3a, C3b. Check 3.5 to 5 V p-p on pin 18 with a scope |
| Signature reads 0x000000 or 0xFFFFFF | Chip not powered, or no common ground | Meter 5 V between pins 40 and 20. Check the ground wire |
| Signature reads but writing fails | Crystal frequency wrong for the ISP clock | Confirm 11.0592 MHz. Lower the bitrate with `-b 9600` |
| Programming works, chip does nothing | EA pin 31 not tied high | Tie pin 31 to +5 V |
| Programming works, chip does nothing | Hex has no LJMP at 0x0000 | Check the first line reads `:030000000208` |
| Programming works, runs, then hangs | Reset network marginal | Confirm R1 10 k to GND and C2 10 uF to +5 V on pin 9 |
| Writes partway then fails | Reset capacitor too large, or switch contention | Lift C2. Confirm SW6, SW7, SW8 are OFF |
| P1 pins read wrong after programming | A DIP switch still closed | SW6, SW7, SW8 must be OFF to program, then set as needed to run |
| `L250 CODE SIZE LIMIT` | Program over 2048 bytes | LX51 and REMOVEUNUSED, or trim unused drivers |
