# Firmware - Keil C51 for the 8051 Hardware Lab Board

Thirteen standalone Embedded C programs for the board documented in `../hardware/SCHEMATIC.md`.
Every program is a single translation unit that includes `inc/board.h`, so each one is compiled as
its own Keil target.

The sources contain no comments and use only the C subset that the Keil C51 compiler accepts:
declarations at the start of a block, no `//` comments, no `stdint.h`, and the Keil specific `sbit`,
`code` and `interrupt` keywords.

---

## 1. Directory layout

```
firmware/
  inc/
    board.h            pin definitions, bus drivers and peripheral drivers
  src/
    01_led_blink.c     LED bank blink
    02_led_patterns.c  running light and pattern sequences
    03_switch_led.c    DIP switch to LED mirror with threshold flash
    04_seg7_counter.c  seven segment 00 to 99 counter
    05_timer0_second.c one second blink from the timer 0 interrupt
    06_square_wave.c   1 kHz square wave on P3.4
    07_ext_interrupt.c INT0 and INT1 push button handling
    08_uart_echo.c     serial banner and echo
    09_uart_commands.c serial command shell
    10_adc_7seg.c      LM35 temperature on the seven segment display
    11_adc_lcd.c       LM35 temperature and bar graph on the LCD
    12_industrial_monitor.c  full zone monitor, relay, buzzer, telemetry
    13_selftest.c      power on self test for every subsystem
  keil/
    <program>_AT89S52.uvprojx    uVision 5 project, AT89S52 target
    <program>_AT89C51.uvprojx    uVision 5 project, AT89C51 target
```

---

## 2. Board abstraction

| Definition | Meaning |
|---|---|
| `BUS` | port 0, the shared 8-bit data bus |
| `SWITCH` | port 1, the DIP switch bank |
| `LED_LE` | P2.0, latch enable of the LED latch |
| `SEG_LE` | P2.1, latch enable of the segment latch |
| `LCD_E`, `LCD_RS`, `LCD_RW` | P2.2, P2.3, P2.4 |
| `ADC_WR`, `ADC_RD`, `ADC_INTR` | P2.5, P2.6, P2.7 |
| `RELAY`, `SQW` | P3.4, relay driver and square wave test point |
| `BUZZER` | P3.5 |
| `DIG1`, `DIG2` | P3.6, P3.7 digit selects |
| `PB_EMERG`, `PB_MODE` | P3.2, P3.3 push button inputs |

Helper functions in `board.h`: `board_init`, `delay_ms`, `led_write`, `seg_latch`, `seg_number`,
`seg_hex`, `seg_tick`, `display_init`, `lcd_init`, `lcd_gotoxy`, `lcd_string`, `lcd_number`,
`adc_read`, `adc_to_celsius`, `uart_init`, `uart_tx`, `uart_string`, `uart_hex`, `uart_number`,
`uart_rx_ready`, `uart_rx`, `switch_read`, `rol8`, `ror8`.

`seg_tick` and `adc_read` save and restore the bus byte, and the LCD and ADC drivers disable
interrupts during a transfer, so the 5 ms display refresh interrupt cannot corrupt a bus cycle.

---

## 3. Building in Keil uVision

### 3.1 Using the supplied project files

1. Copy the whole repository to a path with no spaces, for example `C:\8051lab\`.
2. Open `firmware\keil\01_led_blink_AT89S52.uvprojx`.
3. If uVision reports that the project was created by a different version, accept the migration.
4. Press F7 to build. The hex file appears in `firmware\keil\Objects\`.

The include path `..\inc` and the output hex file are already configured.

### 3.2 Creating a project by hand

If the project file is rejected, create the target manually; it takes about a minute.

1. Project, New uVision Project, name it after the program.
2. Select the device: Atmel AT89S52. For an AT89C51 board select Atmel AT89C51 instead.
3. Answer No when asked to copy the startup code; these programs do not need it.
4. Right click Source Group 1, Add Existing Files, and add `firmware\src\<program>.c`.
5. Options for Target, C51 tab, set Include Paths to `..\inc`.
6. Options for Target, Output tab, tick Create HEX File and set the format to Intel HEX-386.
7. Options for Target, Target tab, set Xtal to 11.0592 MHz and Memory Model to Small.
8. For an AT89C51 target, add `CHIP_AT89C51` to the C51 Define box so that `board.h` includes
   `REG51.H` instead of `REGX52.H`.
9. Build.

### 3.3 Compiler switches that matter

| Setting | Value | Reason |
|---|---|---|
| Device | AT89S52 | matches the on-board part |
| Memory model | Small | all data fits in the 128 byte internal RAM |
| Oscillator | 11.0592 MHz | exact 9600 baud with TH1 = FDH |
| Create HEX | enabled | output for the programmer |
| Optimization level | 8 | default, keeps `delay_1ms` as a DJNZ loop |

Do not enable Register Bank 1 for the interrupt service routines; the programs use bank 0 and the
`using` keyword is deliberately not used.

---

## 4. Programming the device

### 4.1 AT89S52 with a USBasp

Most USBasp boards sold in India ship with firmware that supports 8051 SPI programming.

```
avrdude -p 8052 -c usbasp -U flash:w:01_led_blink.hex:i
```

If that fails, use ProgISP 1.72 or Khazama AVR Programmer on Windows, select the device as AT89S52,
load the hex file and press Chip Erase then Program Flash.

Before programming, set DIP switches 6, 7 and 8 to OFF. They share P1.5, P1.6 and P1.7 with the SPI
lines and will corrupt the transfer if they are closed.

### 4.2 AT89C51

The AT89C51 has no SPI interface and needs a parallel or universal programmer. Build the
`<program>_AT89C51.uvprojx` project with `CHIP_AT89C51` defined and flash the resulting hex with the
programmer supplied with the kit.

### 4.3 Fuse and configuration bits

There are none. On both parts, tie EA/VPP to +5 V so the device boots from internal flash.

---

## 5. Running a program

1. Set DIP switches 6, 7 and 8 to OFF.
2. Connect the USBasp to J3, flash the hex file, disconnect the programmer.
3. Keep the 9 V adapter connected and press PB3 to reset.
4. For serial programs, connect the USB to RS-232 adapter and open a terminal at 9600 8N1, no flow
   control, no line ending translation.
5. For `06_square_wave.hex`, remove the JP1 shunt first so the relay coil does not load P3.4.

---

## 6. Program reference

| Program | Peripherals used | What to observe | Keil code size (approx) |
|---|---|---|---:|
| 01_led_blink | U2 latch, 8 LEDs | eight LEDs toggle every 500 ms | 1.1 KB |
| 02_led_patterns | U2 latch, 8 LEDs | running light, then AAH, 55H, blink | 1.2 KB |
| 03_switch_led | P1 switches, U2 latch | LEDs follow the switches, flash when P1 >= 80H | 1.2 KB |
| 04_seg7_counter | U3 latch, Q1, Q2, DSP1 | 00 to 99 at two counts per second | 1.3 KB |
| 05_timer0_second | timer 0, U2 latch | one second blink from the interrupt | 1.2 KB |
| 06_square_wave | timer 0, P3.4 | 1.00 kHz on a scope, JP1 removed | 1.1 KB |
| 07_ext_interrupt | INT0, INT1, U2, DSP1 | PB1 alternates 0FH and F0H, PB2 increments | 1.3 KB |
| 08_uart_echo | UART, MAX232, U2 | banner and echo on the terminal | 1.4 KB |
| 09_uart_commands | UART, U2, U3, relay, buzzer | HLP, LED HH, SEG NN, RLY N, BUZ N, TMP | 3.0 KB |
| 10_adc_7seg | ADC0804, LM35, U3 | temperature in degrees C on the display | 1.5 KB |
| 11_adc_lcd | ADC0804, LM35, LCD | temperature and bar graph on the LCD | 2.0 KB |
| 12_industrial_monitor | everything | zone LEDs, relay, buzzer, LCD, telemetry | 3.4 KB |
| 13_selftest | everything | PASS or FAIL report on the terminal | 2.6 KB |

Sizes are for the C51 compiler at optimization level 8 without the library `printf`. All thirteen fit
in the 8 KB flash of the AT89S52 individually; the largest, program 12, uses about 40 percent of the
flash and about 30 bytes of internal RAM.

---

## 7. Verification status

All thirteen files were compiled with the SDCC `mmcs51` backend as a syntax and semantics check after
mapping the Keil specific keywords (`sbit`, `code`, `interrupt N`) to their SDCC equivalents. Every
file compiled with zero errors and zero warnings.

The SDCC mapping is only used for checking. The shipped sources are Keil C51 and must be built with
Keil uVision, which is what the `.uvprojx` files configure.

Note the one arithmetic convention that has to stay consistent between the firmware and the hardware:
`adc_to_celsius` implements `T = raw x 25 / 32`, which assumes Vref/2 is adjusted to 1.000 V as
described in `../hardware/ASSEMBLY.md` stage 7. A different reference needs a different constant.
