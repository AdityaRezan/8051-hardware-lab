# Test Procedure and Expected Results

Fill in the Measured column as each test is run. A test is passed only when the measured value is
inside the acceptance limit in the Expected column.

---

## 1. Equipment

| Item | Purpose |
|---|---|
| Digital multimeter, 4.5 digit preferred | voltages, continuity, calibration of Vref/2 |
| Oscilloscope, 20 MHz or better | ALE, crystal, INTR pulse, baud timing, square wave |
| Bench supply or 9 V adapter | board power |
| USBasp programmer | flashing the AT89S52 |
| USB to RS-232 adapter | serial link to a PC |
| Terminal program (PuTTY, Tera Term, screen) | 9600 8N1, no flow control |
| Reference thermometer | LM35 accuracy check |
| Heat source (warm water in a sealed bag, or a soldering iron held 50 mm away) | exercising the zones |

A scope is optional for tests T1 to T4 and T11 to T12; everything else can be verified with the
multimeter, the LED bank, the display and the terminal.

---

## 2. Firmware under test

| Program | Exercise |
|---|---|
| 01_led_blink.hex | T3 LED bank |
| 03_switch_led.hex | T4 DIP switch input |
| 04_seg7_counter.hex | T5 seven segment counter |
| 05_timer0_second.hex | T6 one second timing |
| 06_square_wave.hex | T7 timer output frequency |
| 07_ext_interrupt.hex | T8 external interrupts |
| 08_uart_echo.hex | T9 serial loopback and echo |
| 09_uart_commands.hex | T10 command shell |
| 10_adc_7seg.hex | T11 ADC and LM35 |
| 11_adc_lcd.hex | T12 LCD and bar graph |
| 12_industrial_monitor.hex | T13 to T16 zone logic, relay, buzzer, telemetry |
| 13_selftest.hex | T1 and T17 full bring-up |

---

## 3. Test matrix

| # | Test | Procedure | Expected | Measured | Pass |
|---|---|---|---|---|---|
| T1 | Power on self test | Load 13_selftest.hex, watch the terminal | Every line reports OK, final line SELF TEST: PASS | | |
| T2 | Supply rails | Measure U7 pin 3, U1 pin 40, U5 pin 16 | 5.00 V plus or minus 0.15 V at each | | |
| T3 | LED bank | Load 01_led_blink.hex, time 10 cycles | 20 half cycles in 10.0 s plus or minus 0.3 s | | |
| T4 | DIP switch input | Load 03_switch_led.hex, close switches 1 to 7 one at a time | Corresponding LED lights within 10 ms, no false triggering | | |
| T5 | Seven segment counter | Load 04_seg7_counter.hex, time 00 to 99 | 50 s plus or minus 2 s for a full count | | |
| T6 | One second timing | Load 05_timer0_second.hex, time 10 LED transitions | 10 transitions in 10.0 s plus or minus 0.2 s | | |
| T7 | Square wave output | Remove JP1, load 06_square_wave.hex, probe P3.4 | 1.00 kHz plus or minus 20 Hz, 50 percent duty | | |
| T8 | External interrupts | Load 07_ext_interrupt.hex, press PB1 ten times | LED bank alternates 0FH and F0H on every press, no double triggering | | |
| T9 | Serial echo | Short J2 pins 2 and 3 with a wire, send bytes | Every byte is echoed exactly, no framing errors | | |
| T10 | Command shell | Load 09_uart_commands.hex, send HLP then LED FF then RLY 1 | Help list printed, LEDs all on, relay clicks | | |
| T11 | ADC and LM35 | Load 10_adc_7seg.hex, compare with the reference thermometer | Within 1.5 degrees C of the reference over 25 to 60 C | | |
| T12 | LCD and bar graph | Load 11_adc_lcd.hex, warm the sensor | Line 1 tracks the temperature, line 2 bars increase monotonically | | |
| T13 | Zone thresholds | Load 12_industrial_monitor.hex, sweep the temperature | Green below 40.0 C, yellow 40.0 to 69.9 C, red at 70.0 C and above | | |
| T14 | Relay control | Same as T13 | Relay energises at 40.0 C and drops out below 40.0 C | | |
| T15 | Emergency stop | Press PB1 during normal operation | Relay drops out, buzzer sounds, LCD shows EMERGENCY STOP, telemetry zone reads EMERGENCY | | |
| T16 | Emergency reset | Press PB2 after T15 | System returns to normal zone control, buzzer stops | | |
| T17 | Telemetry frame rate | Load 12_industrial_monitor.hex, count lines for 10 s | 10 lines, one per second | | |
| T18 | Current consumption | Ammeter in series with the 9 V input, relay off, display at 88 | Below 200 mA | | |
| T19 | Regulator thermals | Run for 15 minutes, touch U7 tab | Warm but holdable, below about 60 C | | |
| T20 | Supply rejection | Vary the input from 7 V to 12 V | 5 V rail stays inside 4.90 to 5.10 V, no reset or display flicker | | |

---

## 4. Calibration

### 4.1 ADC reference

1. Power the board and put the black lead on GND.
2. Measure U4 pin 9 and adjust R8 until it reads exactly 1.000 V.
3. Confirm the LM35 output voltage equals 10 mV per degree C at a known temperature.
4. Confirm the transfer function `T = raw x 25 / 32` against two temperatures at least 20 degrees
   apart. If both readings are off by the same factor, R8 has drifted; if only one is off, the LM35
   is picking up noise and needs a shorter lead or a 0.1 uF capacitor directly across its supply pins.

### 4.2 Delay routines

`delay_ms()` in `board.h` is written for 11.0592 MHz and assumes the loop body compiles to a single
DJNZ instruction. Verify it once:

1. Load `05_timer0_second.hex`, which uses the hardware timer, and confirm T6 passes.
2. Load `01_led_blink.hex`, which uses `delay_ms(500)`, and confirm T3 passes.
3. If T3 is off by more than 5 percent while T6 is correct, change the two literal 250 values in
   `delay_1ms()` proportionally. Do not change the timer reloads; T6 passing proves the crystal and
   the machine cycle are correct.

---

## 5. Sample telemetry (program 12, recorded at 9600 8N1)

```
8051 ZONE MONITOR 9600 8N1
T=28.1C ADC=36 ZONE=SAFE FAN=0 BUZ=0
T=28.1C ADC=36 ZONE=SAFE FAN=0 BUZ=0
T=41.4C ADC=53 ZONE=WARNING FAN=1 BUZ=0
T=41.4C ADC=53 ZONE=WARNING FAN=1 BUZ=0
T=64.0C ADC=82 ZONE=WARNING FAN=1 BUZ=0
T=72.6C ADC=93 ZONE=DANGER FAN=1 BUZ=1
T=72.6C ADC=93 ZONE=EMERGENCY FAN=0 BUZ=1
T=71.0C ADC=91 ZONE=DANGER FAN=1 BUZ=1
```

Check the arithmetic on one line. The raw count is printed in decimal: 36 x 25 / 32 = 28.125, and the
firmware prints the integer part and one decimal digit, giving 28.1C. Inverting the same line, a raw
count of 93 gives 93 x 25 / 32 = 72.6C, which is above the 70.0 C threshold and correctly switches the
zone to DANGER. Confirm on the bench that every printed pair agrees with the transfer function.

---

## 6. Sample self test output (program 13)

```
8051 HARDWARE LAB
POWER ON SELF TEST

LED BANK      : OK
7 SEGMENT     : OK
RELAY DRIVER  : OK
BUZZER        : OK
LCD 16X2      : OK
ADC0804 + LM35: RAW=24 T=28C

SELF TEST: PASS
```

RAW is printed in hexadecimal by `uart_hex`, so RAW=24 means 24H = 36 decimal, which converts to
36 x 25 / 32 = 28 C. The self test fails the ADC line if the raw code is 00H or FFH, which is what an
unplugged or reversed LM35 produces.

---

## 7. Results template

Copy this block into the project report once the tests are run.

| Test | Expected | Measured | Result |
|---|---|---|---|
| T2 supply | 5.00 V | | |
| T3 LED timing | 10.0 s | | |
| T5 counter | 50 s | | |
| T7 square wave | 1.00 kHz | | |
| T11 LM35 at 30 C | within 1.5 C | | |
| T11 LM35 at 50 C | within 1.5 C | | |
| T13 green to yellow | 40.0 C | | |
| T13 yellow to red | 70.0 C | | |
| T18 current | below 200 mA | | |

---

## 8. Known limitations

| Limitation | Reason | Effect |
|---|---|---|
| Temperature resolution is 0.78 C | 8-bit ADC with a 2 V full scale | The last digit moves in steps |
| Temperature accuracy is about plus or minus 1.5 C | LM35 tolerance plus reference drift | Good enough for zone switching, not for metrology |
| The relay is specified for 10 A at 250 VAC but is demonstrated on 5 V loads | Laboratory safety | Demonstrate with a lamp, never with mains |
| No hardware debounce on PB1 and PB2 | Pin count | Firmware debounces by polling, and the ISR latches a flag rather than doing work |
| Port 0 bus rise time is set by RN1 at 10 kOhm | Open drain outputs | Bus is limited to a few hundred kHz, far above the 1 kHz used here |
