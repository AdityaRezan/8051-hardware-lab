# Hardware - 8051 Hardware Lab Board

This folder is the physical implementation of the 8051 mini project. The simulator phase proved the
programs in software; this phase puts the same ideas on a real AT89S52 with real peripherals, real
timing and real measurement.

---

## Documents

| File | Contents |
|---|---|
| [SCHEMATIC.md](SCHEMATIC.md) | pin budget, complete pin allocation, block diagram, wiring tables for every subsystem, and all design calculations |
| [BOM.md](BOM.md) | bill of materials with indicative Indian pricing and a cost summary |
| [BOM.csv](BOM.csv) | the same list in machine readable form |
| [ASSEMBLY.md](ASSEMBLY.md) | ten stage build procedure with a pass measurement at the end of each stage, plus a fault table |
| [TESTING.md](TESTING.md) | twenty test cases with acceptance limits, calibration procedure, sample telemetry and a results template |
| [min-system.svg](min-system.svg) | schematic of the minimum system: crystal, reset, EA strap, decoupling |

---

## What the board does

| Function | Hardware | Firmware |
|---|---|---|
| Eight LED output bank | 74HC573 latch and 470 Ohm resistors on the shared bus | `led_write` |
| Eight bit digital input | 8 way DIP switch on port 1 with pull-ups | `switch_read` |
| Two digit numeric display | second 74HC573, two digit common cathode display, two BC547 | `seg_tick` refresh from timer 0 |
| Text output | 16x2 HD44780 in 8-bit mode on the shared bus | `lcd_string`, `lcd_number` |
| Analog temperature | LM35 into ADC0804 with Vref/2 at 1.00 V | `adc_read`, `adc_to_celsius` |
| Serial link | MAX232 and DB9 at 9600 8N1 | `uart_string`, `uart_number` |
| Interrupts | PB1 on INT0, PB2 on INT1, falling edge | `int0_isr`, `int1_isr` |
| Actuators | 5 V SPDT relay and buzzer on BC547 drivers | `RELAY`, `BUZZER` |
| Zone control | green, yellow, red LEDs plus relay and buzzer | `12_industrial_monitor.c` |

---

## At a glance

| Parameter | Value |
|---|---|
| Microcontroller | AT89S52-24PU, 40 pin DIP |
| Fallback device | AT89C51-24PU, pin compatible |
| Crystal | 11.0592 MHz |
| Machine cycle | 1.0851 microseconds |
| Supply | 7 to 12 V in, 5.00 V regulated by a 7805 |
| Typical current | 157 mA, 274 mA with relay and buzzer on |
| Digital I/O used | 32 of 32 pins |
| Serial | 9600 8N1, TH1 = FDH, zero percent error |
| ADC | 8 bits, Vref/2 = 1.000 V, 7.8125 mV per LSB |
| Temperature range | 0 to 199.2 degrees C at 0.78 C resolution |
| Display refresh | 100 Hz per digit from a 5 ms timer 0 interrupt |
| Cost for one board | about INR 985 in components |
| Cost for a full setup | about INR 1,715 including adapter and programmers |

---

## Connection to the earlier simulator phase

| Simulator program | Hardware equivalent |
|---|---|
| 01 LED blinking on P1 | `01_led_blink.c` |
| 02 alternating patterns | `02_led_patterns.c` |
| 05 BCD up counter | `04_seg7_counter.c` |
| 09 seven segment counter with MOVC | `seg_number` and the `SEG7` table in code memory |
| 10 square wave with timer 0 | `05_timer0_second.c`, `06_square_wave.c` |
| 11 serial transmission | `08_uart_echo.c`, `09_uart_commands.c` |
| 12 external interrupt INT0 | `07_ext_interrupt.c` |
| 13 switch input on P2 | `03_switch_led.c` |
| future scope, LCD and sensors | `10_adc_7seg.c`, `11_adc_lcd.c`, `12_industrial_monitor.c` |

The assembly programs drove ports directly because the simulator had no bus. On real hardware the
peripherals are behind latches on a shared bus, so the equivalent C programs drive the bus and strobe
an enable instead of writing to a port. The observable behaviour is identical.

---

## Safety

- The relay is rated for mains switching but must never be connected to mains during laboratory
  demonstration. Use a 5 V or 12 V lamp on J4, or leave the contacts open and watch the coil.
- The 7805 dissipates about 1 W at 9 V and 250 mA. Fit the heatsink.
- Disconnect power before inserting or removing the microcontroller.
- Set DIP switches 6, 7 and 8 to OFF before every programming cycle.
