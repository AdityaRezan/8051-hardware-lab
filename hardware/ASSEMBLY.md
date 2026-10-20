# Assembly Procedure - 8051 Hardware Lab Board

Estimated build time on a breadboard: 4 to 6 hours. Soldering the same circuit on a dot PCB adds
another 3 to 4 hours. Build and test in the order given; each stage ends with a measurement that must
pass before the next stage is wired.

Do not connect the relay contacts to mains voltage at any point.

---

## Stage 0 - Bench preparation

1. Work on a clean, dry, non-conductive surface with a bench supply or the 9 V adapter available.
2. Keep the anti-static bag for the AT89S52 and handle the IC by its body, not by its pins.
3. Sort every component against `BOM.csv` before starting. Eighty-odd parts take twenty minutes to
   count and save an hour of fault finding later.
4. Have a multimeter in continuity mode on the bench for the whole build.

---

## Stage 1 - Power supply (build this first, test it alone)

1. Fit J1, D1, U7 with HS1, C4, C5, C6a, C6b, D11 and R5 on the breadboard.
2. Check the orientation of D1 (band towards the regulator), C4 and C5 (long leg positive), and D11
   (flat side of the LED is the cathode, which goes towards GND through R5).
3. Apply 9 V to J1 with nothing else connected.

| Measurement | Expected |
|---|---|
| U7 pin 3 to GND | 5.00 V, tolerance 4.85 to 5.15 V |
| U7 pin 1 to GND | 8.3 V with a 9 V adapter, about 0.7 V lost in D1 |
| D11 | lit |
| U7 tab temperature after 5 minutes | warm, not too hot to touch |

If the output is below 4.8 V or above 5.2 V, stop and correct it. Every other stage depends on this.

---

## Stage 2 - Minimum system

1. Fit S1, U1, Y1, C3a, C3b, R1, C2, PB3, C1 and the EA strap.
2. Keep the crystal leads short, under 25 mm, and keep C3a and C3b right at the crystal pins.
3. Tie pin 31 to +5V. If pin 31 is left floating the device reads its program from external memory
   and appears completely dead.
4. Apply power and check:

| Measurement | Expected |
|---|---|
| U1 pin 40 to pin 20 | 5.00 V |
| U1 pin 31 to GND | 5.00 V |
| U1 pin 9, steady state | below 0.5 V |
| U1 pin 9 while PB3 is held | above 4.0 V, returns to 0 V on release |
| U1 pin 18 (XTAL2) on a scope | 11.0592 MHz sine, roughly 2 to 3 V peak to peak |
| U1 pin 30 (ALE) on a scope | 1.843 MHz square wave, about 553 ns period divided by 3 |

ALE is the quickest proof that the device is running. If a scope is not available, load
`13_selftest.hex` and confirm the serial banner appears.

---

## Stage 3 - LED output bank

1. Fit U2 in its socket, RN1 (bus pull-ups), RN3 (470 Ohm) and LEDs D3 to D10.
2. Wire U2 D0 to D7 to BD0 to BD7, LE to P2.0, OE to GND.
3. Wire U2 Q0 to Q7 through RN3 to the LED anodes, LED cathodes to GND.
4. Fit C6c across U2 pins 20 and 10.
5. Load `01_led_blink.hex`.

| Measurement | Expected |
|---|---|
| All eight LEDs | blink together, on for 0.5 s, off for 0.5 s |
| U2 pin 11 (LE) on a scope | about 2.7 microsecond positive pulse, repeating once per second |
| LED on current | 6 to 7 mA measured in series with one LED |
| U2 pin 20 to pin 10 | 5.00 V |

If the LEDs are lit permanently or never light, check that OE (pin 1) is actually grounded and that
LE is wired to pin 11, not pin 1.

---

## Stage 4 - DIP switch input bank

1. Fit SW1, RN2 and R4a, R4b, R4c.
2. Wire RN2 common to +5V, RN2 pins 2 to 9 to P1.0 to P1.7.
3. Wire each switch contact from its port pin to GND.
4. Load `03_switch_led.hex`.

| Measurement | Expected |
|---|---|
| All switches OFF | all LEDs off, P1 reads FFH |
| Switch 1 ON only | LED on U2 Q0 lights, P1 reads FEH |
| Switch 8 ON only | LED on U2 Q7 lights, P1 reads 7FH |
| Switch 8 ON with any other switch ON | all LEDs flash at about 5 Hz |

Leave SW6, SW7 and SW8 OFF from now on while programming.

---

## Stage 5 - Seven segment display

1. Fit U3, RN4, DSP1, Q1, Q2 and the base resistors R2c and R2d.
2. Wire U3 D0 to D7 to the bus, LE to P2.1, OE to GND.
3. Wire U3 Q0 to Q7 through RN4 to segments a b c d e f g dp. Verify the segment order with the
   display datasheet; getting it wrong shows mirrored or scrambled digits.
4. Wire Q1 and Q2 collectors to the two digit common cathodes, emitters to GND, bases via 4.7 kOhm
   to P3.6 and P3.7.
5. Load `04_seg7_counter.hex`.

| Measurement | Expected |
|---|---|
| Display | counts 00 to 99 at two counts per second |
| P3.6 on a scope | 5 ms high, 5 ms low square wave |
| P3.7 on a scope | same, inverted with respect to P3.6 |
| Segment current | 6 to 7 mA in series with one segment |

If both digits show the same number, the digit transistors are not switching; check the base
resistors and the transistor pinout (E-B-C for BC547 with the flat face towards you).

---

## Stage 6 - Serial link

1. Fit U5, C7a to C7d and J2. Observe capacitor polarity: C7c positive leg to pin 2 and negative leg
   to +5V; C7d positive leg to GND and negative leg to pin 6.
2. Wire T1IN to P3.1, R1OUT to P3.0, T1OUT to J2 pin 2, R1IN to J2 pin 3, J2 pin 5 to GND.
3. Connect the USB to RS-232 adapter and open a terminal at 9600 8N1, no flow control.
4. Load `08_uart_echo.hex`.

| Measurement | Expected |
|---|---|
| Terminal on power up | banner "8051 HARDWARE LAB" then "9600 8N1 - TYPE TO ECHO" |
| Typing a character | character is echoed and the LED bank shows its ASCII code |
| U5 pin 2 (V+) to GND | about +9 V |
| U5 pin 6 (V-) to GND | about -9 V |
| P3.1 idle | high |

If the terminal shows nothing: swap J2 pins 2 and 3 first, then confirm V+ and V- are present, then
confirm the terminal is set to 9600 and not 115200.

---

## Stage 7 - Temperature input

1. Fit U4, R6, C8, R8, C10, C9, J5 and the LM35.
2. Wire the data bus: U4 DB0 to DB7 (pins 18 down to 11) to BD0 to BD7.
3. Wire WR to P2.5, RD to P2.6, INTR to P2.7, CS to GND.
4. Wire Vin(+) to J5 pin 2 and Vin(-) to GND.
5. Set R8 so that U4 pin 9 measures exactly 1.000 V, then leave it alone.
6. Load `10_adc_7seg.hex`.

| Measurement | Expected |
|---|---|
| U4 pin 9 | 1.000 V after calibration |
| U4 pin 4 on a scope | about 606 kHz |
| U4 pin 5 (INTR) on a scope | low pulse about 110 microseconds wide, repeating every cycle |
| Display at room temperature (30 C) | shows 30, plus or minus 2 counts |
| LM35 output at 30 C | 300 mV |
| LM35 output after touching the sensor | rises towards 350 mV, display rises with it |

If the display shows 00 or 99 permanently, the LM35 is unplugged, reversed or the reference is wrong.

---

## Stage 8 - Character LCD

1. Fit LCD1, R9 and R7. Use a 16 pin female header so the module can be removed later.
2. Wire D0 to D7 to the bus, RS to P2.3, RW to P2.4, E to P2.2, VO to the R9 wiper, A through R7 to
   +5V, K to GND.
3. Set R9 to roughly mid position.
4. Load `11_adc_lcd.hex`.

| Measurement | Expected |
|---|---|
| Line 1 | "T=30.4C A=039" style reading, updating four times a second |
| Line 2 | 16 character bar graph, growing as the sensor warms |
| VO | about 0.5 to 1.0 V for good contrast |
| LCD pin 6 (E) on a scope | pulse train only while the display is being written |

If line 1 is blank but the backlight is lit, adjust R9. If both rows are blank, check the contrast
first, then the E and RS wiring.

---

## Stage 9 - Relay and buzzer

1. Fit Q3, R3a, D2, RLY1, JP1, J4, Q4, R3b and BZ1.
2. Wire JP1 between P3.4 and R3a. Fit the shunt for normal operation.
3. Wire D2 across the relay coil with the cathode to +5V.
4. Load `12_industrial_monitor.hex` and warm the sensor above 40 C.

| Measurement | Expected |
|---|---|
| Relay click | audible as the temperature crosses 40 C |
| Q3 collector when the relay is on | below 0.3 V |
| Buzzer | sounds above 70 C and during an emergency stop |
| J4 continuity | open when off, closed when on |

Remove the JP1 shunt before running `06_square_wave.hex`.

---

## Stage 10 - Final checkout

1. Load `13_selftest.hex` with the terminal connected.
2. Confirm every line reports OK and the final line reads SELF TEST: PASS.
3. Confirm the relay clicks three times and the buzzer beeps three times during the test.
4. Re-torque nothing, but re-seat every IC and press down each socketed part.
5. Photograph the board and record the measured values in `TESTING.md`.
6. Optionally transfer the circuit to a dot PCB, keeping the crystal leads short and running a
   continuous ground along one edge.

---

## Common faults

| Symptom | Most likely cause |
|---|---|
| No 5 V output | D1 reversed, or U7 pins misread (input is pin 1, ground pin 2, output pin 3) |
| Device appears totally dead | EA (pin 31) not tied to +5V |
| Device runs erratically | C1 missing, or crystal leads too long |
| LEDs stuck on or off | U2 pin 1 (OE) not grounded, or LE wired to the wrong pin |
| Display shows scrambled digits | segment order a to g does not match Q0 to Q6 |
| Both 7-segment digits identical | digit transistor base resistors missing or transistors wired E-C swapped |
| Terminal shows garbage | baud rate mismatch, or the crystal is 12 MHz instead of 11.0592 MHz |
| Terminal shows nothing | J2 pins 2 and 3 swapped, or V+ and V- absent |
| ADC always 00H or FFH | LM35 unplugged, reversed, or Vref/2 not set to 1.00 V |
| ADC reading 2 to 3 degrees high at room temperature | Vref/2 below 1.00 V, recalibrate R8 |
| LCD blank with backlight on | R9 contrast setting |
| Relay never clicks | JP1 shunt missing |
| Programming fails | SW6, SW7 or SW8 closed, or the USBasp VCC jumper not set for 5 V |
