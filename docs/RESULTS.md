# What the results are, and how to show her

You have the software and the hardware. So the question is no longer "does it
work" - it is "what do I claim, and how do I prove it in front of one person in
six minutes".

This file has the results. `docs/FACULTY_DEMO.md` has the long demo and the viva
bank. `docs/DEMO_CARD.md` is the one page you keep under the board.
`docs/8051_Results_Sheet.pdf` is the two page sheet **she** holds while you demo.

---

## 1. There are four kinds of result here

A reviewer believes results in this order, weakest to strongest. Aim to show at
least three.

| Kind | What it is | Example | Where it lives |
|---|---|---|---|
| **Behaviour** | something she can see happen with her own eyes | LEDs blink on power-up with no PC attached | the board |
| **Number** | a measured value against a stated limit | 5.02 V on the rail, 1.4 % off from 5.00 | multimeter |
| **Pass/fail** | a stated test with an acceptance tolerance | T6: 10 transitions in 10.0 s, limit +/-0.2 s | `hardware/TESTING.md` |
| **Evidence** | a record you can hand over | build table, terminal capture, video, filled result sheet | papers and files |

Behaviour alone gets you "it works". Behaviour **plus** numbers plus a filled
result sheet is what turns a demo into a grade.

---

## 2. Results program by program - what she will actually see

Flash in this order. Each one shows a different capability, so you do not need
all thirteen - but this is the full result list.

| # | Program | Result she can see, in ten seconds | Kind | Test |
|---:|---|---|---|---|
| 1 | 01_led_blink | 8 LEDs blink together at 1 Hz, board runs with no PC attached | behaviour | T3 |
| 2 | 02_led_patterns | sweep, then alternating AA/55, then binary count | behaviour | T3 |
| 3 | 03_switch_led | each DIP switch lights its own LED, no flicker on contact | behaviour | T4 |
| 4 | 04_seg7_counter | two-digit display counts 00 to 99, no ghosting | behaviour | T5 |
| 5 | 05_timer0_second | display steps once per second, timed not delayed | behaviour | T6 |
| 6 | 06_square_wave | 1.00 kHz on P3.4 on a scope, 50 % duty, JP1 removed | number | T7 |
| 7 | 07_ext_interrupt | PB1 alternates the pattern, one press = one change | behaviour | T8 |
| 8 | 08_uart_echo | every character typed on the PC comes back | behaviour | T9 |
| 9 | 09_uart_commands | `HLP` lists commands, `LED FF` lights all, `RLY 1` clicks the relay | behaviour | T10 |
| 10 | 10_adc_7seg | display shows the LM35 temperature, tracks your finger | number | T11 |
| 11 | 11_adc_lcd | LCD line 1 temperature, line 2 bar graph grows when warmed | behaviour | T12 |
| 12 | 12_industrial_monitor | **the whole system**: zone LEDs, relay trip at 40 C, buzzer, LCD, telemetry once per second | all four | T13-T17 |
| 13 | 13_selftest | walks every subsystem on the terminal, ends `SELF TEST: PASS` | pass/fail | T1, T17 |

The two that carry the demo: **13** proves everything at once, **12** is the
project. Programs 01 to 11 are the evidence that each block works on its own.

---

## 3. The numbers - designed value against what to measure

This is the table to fill in before the review. The right-hand column is the
tolerance your own `hardware/TESTING.md` defines; do not widen it afterwards.

| Quantity | Designed value | How to measure it | Acceptance | Measured |
|---|---|---|---|---|
| 5 V rail | 5.00 V | DMM, U7 pin 3 and U1 pin 40 | 4.85-5.15 V | ______ |
| Machine cycle | 1.0851 us | derived from the scope on ALE | - | (derived) |
| UART baud error | 0.00 %, TH1 = FDH | 9600 8N1 terminal, no framing errors | exact | ______ |
| Display refresh | 100 Hz per digit | scope on DIG1, 5 ms tick | 95-105 Hz | ______ |
| Timer output | 1.00 kHz, reload FE34H | scope on P3.4, JP1 removed | 980-1020 Hz | ______ |
| 1 s tick | 1.000 s, timer 0 | stopwatch, 10 transitions | +/-0.2 s | ______ |
| ADC step | 7.8125 mV | Vref/2 trimmed to 1.000 V, DMM | 0.99-1.01 V | ______ |
| Temperature | 0.78 C per step | against a reference thermometer, 25-60 C | within 1.5 C | ______ |
| Zone trip | 40.0 C and 70.0 C | warm the LM35 slowly, watch the LCD | +0/-0.5 C | ______ |
| Board current | 157 mA typ, 274 peak | ammeter in series with the 9 V input | under 200 mA | ______ |
| Largest program | 3.4 KB of 8 KB flash | Keil build output | under 2048 B for the free build | ______ |
| Cost per board | INR 985 | `hardware/BOM.csv` totals | - | (fixed) |

Six of these are worth quoting out loud:

- **32 of 32 I/O pins used** - zero headroom, so the architecture had to be right.
- **0.00 % baud error** - the only reason the crystal is 11.0592 MHz.
- **1.00 kHz from a timer**, within 0.17 %.
- **0.78 C per ADC step**, from trimming the reference to 1.000 V.
- **157 mA typical, 274 mA peak**, which is what sizes the 7805 and its heatsink.
- **3.4 KB largest program** of 8 KB, so there is room to grow.

---

## 4. The twenty tests, grouped so you can finish them

`hardware/TESTING.md` is the authoritative list, T1 to T20. In a two hour lab
session, run them in this order - the cheap ones first, because they are the ones
you will be asked for.

| Group | Tests | Time | Needs |
|---|---|---|---|
| Bring-up | T1 self test, T2 rails, T20 supply rejection | 15 min | DMM, terminal |
| Timing | T3 blink, T5 counter, T6 one second | 15 min | stopwatch |
| Input | T4 switches, T8 interrupts | 10 min | fingers |
| Analogue | T11 temperature, T12 LCD bar | 20 min | reference thermometer, warm water |
| System | T13 zones, T14 relay, T15 emergency, T16 reset, T17 telemetry | 25 min | warm water, terminal |
| Electrical | T7 square wave, T9 echo, T10 commands, T18 current, T19 thermals | 25 min | scope, ammeter |

Two shortcuts that are legitimate:

- **T1 (self test) covers the outputs of T3, T4, T5, T11 and T12 in one program.**
  Run T1 first; if it passes, you have a strong baseline and the individual tests
  are confirmations, not discoveries.
- **T19 (regulator thermals) runs while you do everything else.** Start it, do the
  rest, touch the tab at the end.

---

## 5. The results paragraph - copy this into the report

Fill the blanks with your own numbers, and delete any line you did not measure.

> The board was assembled in ten stages, each stage measured before the next was
> fitted. All thirteen Keil C51 programs compiled with zero errors; the largest
> `13_selftest` measured ____ bytes of the 8192 available. The regulated rail
> measured ____ V at U1 pin 40 against a 5.00 V +/- 0.15 V requirement.
> The power-on self test reported PASS on every subsystem. Timing results: the
> 1 Hz blink measured ____ s per half cycle (T3, limit +/-0.3 s), the timer-driven
> one second tick measured ____ s over ten transitions (T6, limit +/-0.2 s), and
> the timer square wave measured ____ kHz (T7, limit 1.00 kHz +/- 20 Hz). The
> serial link ran at 9600 8N1 with zero framing errors in ____ bytes transferred
> (T9). The LM35 and ADC0804 agreed with a reference thermometer to within ____ C
> across 25 to 60 C (T11, limit 1.5 C), a resolution of 0.78 C per step from a
> 1.000 V reference. Zone thresholds tripped at ____ C and ____ C against a
> specification of 40.0 C and 70.0 C (T13). Emergency stop dropped the relay and
> sounded the buzzer within ____ ms (T15), and normal control resumed on reset
> (T16). Telemetry produced ____ frames in 10 s against one per second (T17).
> Supply current measured ____ mA with the relay off, against a 200 mA limit
> (T18), and the rail held 4.90-5.10 V with the input varied from 7 V to 12 V
> (T20).

Then one conclusion sentence, and nothing more:

> The 22-pin deficit between the 54 required peripheral signals and the 32
> available I/O pins was closed by architecture - one shared 8-bit bus with a
> latch and a strobe per device - and every measured result matched the prediction
> of the phase one simulator within its stated tolerance.

---

## 6. How to show her - the six-minute one-on-one

For a single reviewer, not a committee. No projector, no slide advance. She
holds the result sheet, you hold nothing and keep both hands free.

### Before she arrives (5 minutes)

- [ ] Two chips in sockets: **A** = `12_industrial_monitor`, **B** = `13_selftest`.
      Both already flashed. This is the whole trick - no laptop, no flashing live.
- [ ] Programmer **unplugged and off the bench**.
- [ ] Terminal open, connected, already printing telemetry, font large.
- [ ] Multimeter on, DC volts, probes clipped where you need them, or set aside.
- [ ] Warm water in a sealed bag, plus one cold object (a metal ruler or a glass
      of tap water), so you can **raise and lower** the temperature. Going up only
      shows one threshold; going down shows hysteresis and the relay releasing.
- [ ] **Print `docs/8051_Results_Sheet.pdf`** and put it in her hand. She will
      follow it while you talk, which means she is following your argument.
- [ ] `hardware/TESTING.md` with the measured column filled, underneath it, in
      case she asks for the raw sheet.

### The six minutes, with the words

| Time | You do | You say |
|---:|---|---|
| 0:00 | board off, hand her the sheet | "This is a temperature monitor on an AT89S52 with a three-zone alarm. The design problem was that the peripherals need 54 I/O signals and the chip has 32." |
| 0:40 | power on, **no PC attached** | "No laptop connected. That program is in the chip's flash, so it starts on every power-up. That is the result I want to start with, because everything else runs from it." |
| 1:10 | swap to chip B (self test) | "This one tests itself. LED bank, display, relay, buzzer, LCD, ADC - it walks each and reports. Last line should read SELF TEST: PASS." |
| 2:30 | swap to chip A, point at LCD | "Now the actual project. Zone, temperature, bar graph. Thresholds are 40 and 70." |
| 3:00 | warm the sensor in the bag | "At 40 the zone goes yellow and the relay energises. That relay is low voltage only - it is never connected to mains." |
| 4:00 | remove the bag, let it cool | "And it drops out again below 40, so it is a threshold, not a latch." |
| 4:30 | press **PB1**, then **PB2** | "Emergency stop: relay drops, buzzer sounds, LCD and telemetry both read emergency. PB2 returns it to normal. Those are the two external interrupts, debounced in software." |
| 5:20 | point at terminal | "One telemetry line per second at 9600 baud. The baud error is zero, which is why the crystal is 11.0592 MHz and not 12." |
| 5:40 | hands off the board | "Fifty-four signals into thirty-two pins, no port expander. Twenty tests documented, the measured ones are on the sheet in your hand. I can take questions on any part of it." |

Then **stop talking.** Silence invites the questions you have answers for, and
lets her finish reading the sheet.

### The two things that make it land

1. **She holds the paper your board is proving.** A result sheet in her hand,
   with the measured column filled in ink, is the single strongest object in the
   room.
2. **Both directions on the temperature.** Up to yellow is a demo. Up *and* down
   is a control loop, and that is the difference between a toy and a project.

---

## 7. The five questions she is most likely to ask

| Question | Your answer |
|---|---|
| "Why not use a bigger chip with more pins?" | "It would need a PCB and surface-mount work, and the 32-pin budget was the constraint. Closing that gap is the project." |
| "Is the temperature accurate?" | "0.78 C per step, from trimming the reference to 1.000 V, and within 1.5 C of a reference thermometer from 25 to 60 C - that is T11 on the sheet." |
| "What happens if power fails?" | "The program is in flash and restarts on power-up. Variables are lost, so nothing depends on remembered state." |
| "Did you write the code?" | "The thirteen programs and the driver layer in `board.h` are ours. The compiler and the C library are the toolchain." Then prove it: open `board.h` and explain `adc_to_celsius` - "it is raw times 25 over 32, because 7.8125 millivolts per step over 10 millivolts per degree." |
| "What would you improve?" | "A two-layer PCB with a ground plane, a digital-output sensor to remove the ADC and its reference, and the LCD on an I2C backpack to return two pins." |

Expect one deep question on the **shared bus**, because it is the only unusual
thing here. Answer in three sentences: eight port 0 lines carry data for four
devices in turn; one strobe pin per device decides who captures the byte; the
74HC573 holds it afterwards, which is what makes the sharing legal.

---

## 8. Three honesty rules

1. **Never write a measured number you did not measure.** "Not measured, specified
   as X" is a respected answer and costs nothing. An invented number costs the
   whole result sheet.
2. **Never say "it works perfectly."** Say what was tested and what the tolerance
   was. Perfect is a claim; a tolerance is a measurement.
3. **Never let a live fault run past three minutes.** If it breaks, say "that is
   an intermittent I will not debug in front of you", and hand over the recorded
   run and the filled sheet. A calm diagnosis scores better than a board that
   happens to work, and far better than ten silent minutes of re-seating chips.

---

## 9. What to carry in, in one bag

| Item | Why |
|---|---|
| Board, powered, with chips A and B in sockets | the demo |
| 5 V adapter, spare fuse, 9 V adapter | it will be one of these |
| Multimeter | two of your numbers need it |
| Laptop with terminal already open | telemetry and self test |
| `docs/8051_Results_Sheet.pdf` printed, x2 | one for her, one for you |
| `hardware/TESTING.md` printed, measured column filled | the raw evidence |
| Build table printout, `STATE OK` column visible | proves all 13 compile |
| Warm water in a sealed bag, and something cold | both threshold directions |
| Pen drive with all 13 `.hex` files | "can you leave me the code?" |
| Spare 74HC573, 7805, LEDs, 470 R | five-minute repair |
