# DEMO CARD - print this one page, keep it under the board

Full detail: `docs/FACULTY_DEMO.md`

---

## 1. Open with these three sentences

1. **What it is.** "This board measures temperature with an 8051 and runs a three-zone alarm:
   green below 40, yellow to 70, red above, with relay trip, buzzer, LCD, seven-segment display
   and 9600 baud telemetry."
2. **The constraint.** "The peripherals need 54 I/O signals. The AT89S52 has 32 pins. The design
   problem was closing a 22-pin gap."
3. **The fix.** "No port expander. Eight port 0 lines carry data for four devices in turn, and one
   strobe per device on port 2 decides who is listening. The latch holds each byte, so all four
   keep their values."

Then **power the board on**. Stop talking about code.

---

## 2. Demo beats

| # | Do | Should see | Line |
|---|---|---|---|
| 1 | Power on, **no programmer attached** | 8 LEDs blink 1 Hz | "In flash. Starts on every power-up." |
| 2 | Swap to chip B, power on | Terminal: OK lines, `SELF TEST: PASS` | "Walks every subsystem." |
| 3 | Swap to chip A, warm sensor | green to yellow, relay clicks, LCD changes | "Threshold 40.0." |
| 4 | Press **PB1**, then **PB2** | relay drops, buzzer, EMERGENCY, then normal | "INT0 and INT1, 5 ms debounce." |
| 5 | Point at terminal | one telemetry line per second | "9600 8N1, zero error." |

Chip A = `12_industrial_monitor.hex`. Chip B = `13_selftest.hex`. **Both pre-flashed in sockets.**

---

## 3. Numbers, with the derivation attached

| 32 / 32 | 0.00 % | 1.00 kHz | 100 Hz | 0.78 C | 157 mA | 3.4 KB |
|---|---|---|---|---|---|---|
| pins used | baud error, TH1 = FDH | timer FE34H, +0.17 % | display, EE00H per digit | per ADC step, Vref/2 = 1.000 V | typ, 274 peak | largest program of 8 KB |

Other constants: machine cycle **1.0851 us**, crystal **11.0592 MHz** (not 12: 8 % baud error),
ADC step **7.8125 mV**, LED resistor **470 ohm** (53 mA in the package, limit 70),
board **INR 985**, tests **T1 to T20**.

---

## 4. Pin map, if they point

| Port | Job |
|---|---|
| P0 | shared 8-bit bus: LED latch, segment latch, LCD, ADC (needs RN1 pull-ups, open drain) |
| P1 | 8-way DIP switch bank (P1.5-1.7 shared with ISP: SW6-8 OFF to program) |
| P2 | strobes: P2.0 LED, P2.1 SEG, P2.2-2.4 LCD E/RS/RW, P2.5-2.7 ADC WR/RD/INTR |
| P3 | P3.2 PB1 INT0, P3.3 PB2 INT1, P3.4 relay, P3.5 buzzer, P3.6/3.7 digit select |

---

## 5. If it breaks, keep talking

| Symptom | Check | Say |
|---|---|---|
| Dead | 5 V, then **EA pin 31** | "Power or the EA strap." |
| No telemetry | COM port, 9600 8N1 | "Board is fine, terminal is not. I'll use the LCD." |
| LCD blank | contrast pot R9 | "Contrast, the usual suspect." |
| No yellow zone | heat source too cool - fingers are 34 C, threshold is 40 | "I'll use the emergency path to show the same decision logic." |
| Anything | 3 minutes max, then evidence | "Intermittent fault, I won't debug in front of you. Here is the recorded run and the measured tests." |

Evidence, in order: video `docs/guide/video/8051_Start_To_Finish.mp4`, build table printout,
filled `hardware/TESTING.md`, deck PDF.

---

## 6. Never

Never say the relay is mains connected. Never say "it works perfectly". Never leave the
programmer plugged in. Never debug in silence. Never claim a number you did not measure -
"not measured, specified as X" is a good answer.

Close with: **"Fifty-four signals, thirty-two pins, thirteen programs, twenty measured tests."**
