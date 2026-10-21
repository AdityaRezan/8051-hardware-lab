# Showing the project to faculty - the demo-day playbook

Everything you do in front of a reviewer, in order, with the exact words where
the words matter. Read it once end to end, then rehearse with a phone timer.

Three documents already cover parts of this, so you do not need to invent
anything:

| Source | What it gives you |
|---|---|
| `docs/8051_Hardware_Lab_Review_Deck.pptx` | 7 slides, the formal presentation |
| `docs/DECK_OUTLINE.md` | a speaker script per slide, already timed |
| `docs/guide/8051_How_It_Works.pdf` page 18 | the 30-second pitch and five viva answers |
| `docs/FACULTY_DEMO.md` (this file) | the bench demo, the viva bank, the failure scripts |

The decks make the argument. **The board makes the marks.** Faculty who see a
board boot on its own and misbehave on command believe the rest of the report.
So the running order below puts the board first and the slides second.

---

## 1. What they are actually marking

Most ECE rubrics for a mini project look like this. Prepare one piece of
evidence per row and you are covered whatever the wording.

| Criterion, typical weight | What they want to see | Your evidence |
|---|---|---|
| Problem definition and constraints (10-15 %) | that you understood the task before choosing parts | the 54 vs 32 pin deficit, the six constraints C1 to C6 |
| Design and architecture (20-25 %) | a decision, an alternative, a reason | shared bus + latch + strobe; trade-off matrix |
| Implementation (20-25 %) | that it is really built and really coded | the board working, 13 programs, `board.h` drivers |
| Testing and results (15-20 %) | measured numbers against stated limits | `hardware/TESTING.md` T1 to T20, measured column filled |
| Demonstration and viva (20-25 %) | that you can defend any line of it | this file, sections 6 and 8 |
| Report, presentation, teamwork (10 %) | clean bundle, both members speak | section 9 |

The single most common reason good projects lose marks: the report says
"verified" and the result sheet is blank. **Fill in the Measured column by hand
before the review.** A table with real numbers in someone's handwriting is worth
more than any slide.

---

## 2. The three sentences that earn the marks

Say these slowly, in this order, in the first 90 seconds. If you get cut off
after them, you have still passed the viva.

> **1. What it is.** "This board measures temperature with an 8051 and runs a
> three-zone alarm: green below 40 degrees, yellow to 70, red above that, with a
> relay trip, a buzzer, an LCD, a seven-segment display and 9600 baud telemetry
> to the laptop."

> **2. The constraint.** "The peripherals need 54 separate I/O signals. The
> AT89S52 has 32 pins. So the whole design problem was closing a 22-pin gap."

> **3. The fix, which is the interesting part.** "We did not add a port expander.
> Eight pins of port 0 carry data for four devices in turn, and one strobe pin per
> device from port 2 decides who is listening. The latch holds each byte for the
> device whose gate we pulsed, so all four keep their values between transfers."

Then stop talking and power the board on. Do not explain the code yet.

---

## 3. Twenty minutes before they walk in

The demo fails in setup, not in the demo. Work down this list.

### The bench

- [ ] **Two AT89S52 chips, pre-flashed differently.** This is the trick that
      saves the demo: chip A has `12_industrial_monitor.hex` (the full system),
      chip B has `13_selftest.hex`. Both in IC sockets, swapped in 5 seconds.
      You ordered two chips in the BOM for exactly this reason.
- [ ] Board powered from its own 5 V adapter, **not** from the laptop.
- [ ] **Programmer disconnected.** A dangling ribbon on the ISP header invites
      "is the laptop doing the work?" - which is the one doubt you cannot afford.
- [ ] PuTTY or Tera Term **already open, already connected, already printing
      telemetry**. 9600 8N1, no flow control. Terminal font 16-18 pt so it reads
      from the back of the room. If the COM port is wrong, fix it now, not live.
- [ ] Multimeter on the bench, probes attached, set to DC volts. You will use it
      once, deliberately, in section 5.
- [ ] Laptop: sleep off, notifications off, `8051_Assembly_and_Run.mp4` ready in a
      player, deck open as **PPTX and as PDF** (the PDF is the backup), phone on
      silent, timer where you can see it.
- [ ] Warm water in a sealed plastic bag, or a cup of hot water. **Fingers alone
      reach about 34 degrees Centigrade, and the first zone change is at 40.** If
      you have not tested your heat source, the yellow-to-red demo will not
      happen.
- [ ] Cables taped down. Board tilted towards the audience. Nothing between the
      board and the reviewer's eyes.
- [ ] Spares within reach: 74HC573, 7805, two LEDs, a 470 ohm resistor, the pen
      drive with all 13 HEX files.

### The papers, in one folder, in this order

- [ ] `hardware/TESTING.md` printed, T1 to T20, **Measured column filled in**.
- [ ] The build table printout (13 programs, sizes, `0 ERR`, `STATE OK`).
- [ ] `hardware/SCHEMATIC.md` printed, pin allocation page on top.
- [ ] `hardware/BOM.csv` printed, total visible (about INR 985).
- [ ] Deck PDF, guide PDF, one page each as handouts.
- [ ] The repo link and a QR code to it, on the folder cover.

### The room

- [ ] Board in the middle, laptop to one side. You stand on the **other** side
      of the board from the laptop, so your hands never block the LEDs.
- [ ] Ask for a projector once, at the start, and have a plan without one. The
      board is the demo; the deck is the footnote.

---

## 4. The 12-minute running order

This fits a standard review slot. Section 5 is the 5-minute version if you get
cut short.

| Time | What | Who |
|---:|---|---|
| 0:00-0:01 | The three sentences from section 2, board still off | A |
| 0:01-0:03 | Board tour, pointing at physical parts | A |
| 0:03-0:05 | The constraint: 54 vs 32, and the two options rejected | B |
| 0:05-0:08 | The fix: bus, latch, strobe. Draw it | B |
| 0:08-0:12 | Live demo, four beats (section 6) | A |
| 0:12+ | Numbers, limits, roadmap, then questions | both |

### 0:01-0:03 - the board tour

Point, do not wave. One sentence per part, in this order. Practise until it is
one breath each.

| Point at | Say |
|---|---|
| 40-pin chip | "AT89S52, 8 kilobytes of flash, 256 bytes of RAM, 11.0592 MHz crystal." |
| Crystal and two capacitors | "The crystal sets the machine cycle, 1.0851 microseconds. The 30 pF caps let it start." |
| 74HC573 with LEDs | "The LED latch. It holds the last byte we put on the bus." |
| Second 74HC573 and display | "The segment latch, driving a two-digit display, multiplexed at 100 Hz." |
| LCD | "16 by 2 character LCD, 8-bit mode, sharing the same data lines." |
| DIP switch bank | "Eight switches on port 1. They are the only device with its own full port." |
| LM35 and ADC0804 | "Analogue temperature into an 8-bit converter, reference trimmed to 1.000 volt." |
| MAX232 and DB9 | "Serial link, 9600 baud, zero error, because of the crystal." |
| Relay and buzzer | "Driven through transistors with back-EMF diodes. Demonstration only, never mains." |

### 0:03-0:05 - the constraint

Put the pin budget on the slide or on paper. Say the deficit out loud: **54
required, 32 available, 22 short.** Then name what you rejected, because that is
what separates a build from a design:

- **A bigger microcontroller** - needs a PCB and surface-mount work, and stops
  being a breadboard project.
- **A port expander IC (I2C or SPI)** - two more chips, about INR 250, and every
  single output update becomes a slow serial transaction.
- **What you chose** - share the eight data lines on port 0, give each device a
  latch and a strobe pin, cost: eight strobe pins and software arbitration.

### 0:05-0:08 - the fix, and draw it

Draw this on paper while you talk. It takes 40 seconds and it is the highest
scoring 40 seconds of the review.

```
                    +------------------+
   P0.0-P0.7  ----->| 8-bit shared bus |----+----+----+----+
   (data, 8 wires)  +------------------+    |    |    |    |
                                             v    v    v    v
                                        [LED ] [SEG ] [LCD] [ADC]
                                        [latch] [latch]
                                             ^    ^    ^    ^
   P2.0-P2.7 (strobe, 8 wires) --------------+----+----+----+
```

Then the three lines that prove you understand your own design:

1. "**Only one strobe is high at a time.** A transfer affects exactly one device."
2. "**The latch is what makes sharing legal.** It copies the bus byte and keeps
   it after the strobe falls, so all four devices hold their values at once."
3. "**Port 0 is open drain**, so it cannot pull a line high on its own. RN1, a
   10 k SIP network, does the pulling up. That is constraint C2 in the report."

Expect the follow-up: *"What if two devices are enabled?"* - Answer: "Then two
drivers fight on the bus, we latch garbage, and the board misbehaves but does not
die. The software guarantees it cannot happen: every routine sets the strobe,
writes, clears the strobe, and interrupts are disabled around LCD and ADC
transfers."

---

## 5. The 5-minute version

If the reviewer is late, or says "just show me", do exactly this and nothing else.

1. **30 seconds:** the three sentences, section 2.
2. **60 seconds:** power on. All eight LEDs blink. "Program 01, running from
   flash inside the chip. There is no laptop connected. The chip remembers."
3. **2 minutes:** swap to chip B, `13_selftest`. Let the terminal print
   `LED BANK : OK`, `7 SEGMENT : OK`, ... `SELF TEST: PASS`.
   Say: "That is a power-on self test walking every subsystem, and it is the one
   artefact I would like you to look at."
4. **90 seconds:** swap to chip A, `12_industrial_monitor`. Warm the sensor.
   The zone goes yellow, the relay clicks, the LCD changes. Press PB1:
   `EMERGENCY STOP`, relay drops, buzzer sounds. Press PB2: back to normal.
5. **30 seconds:** "Fifty-four signals into thirty-two pins, no expander. Twenty
   tests, measured. Thank you - I can take questions on any part of it."

That is a complete, defensible demo in five minutes with two chip swaps and one
button press.

---

## 6. The live demo, four beats

Order matters. Credibility first, then drama.

### Beat 1 - it runs on its own (30 s)

Board off, programmer away, laptop turned **towards the reviewer**.

- [ ] Power on. Eight LEDs blink at 1 Hz.
- [ ] Say: "No PC attached. This is `01_led_blink`, in the chip's flash. It
      starts every time power is applied, because flash keeps its contents."
- [ ] Optional 5 seconds that lands well: hold the multimeter on pin 31 (EA).
      "5 volts. If this floated, the chip would look for program memory that is
      not there and do nothing."

### Beat 2 - the self test (90 s)

- [ ] Power off, swap to chip B (`13_selftest`), power on.
- [ ] Point at the terminal as lines appear. Read two out loud, let them read the
      rest.
- [ ] Land on `SELF TEST: PASS`. Then: "If any subsystem fails it prints FAIL and
      blinks a different pattern, so a fault is visible without a terminal."

### Beat 3 - the actual project (2 min)

- [ ] Swap to chip A (`12_industrial_monitor`).
- [ ] Show the LCD: zone, temperature, and the bar graph.
- [ ] Warm the sensor. Narrate what changes and why: "Threshold at 40.0, so the
      zone goes green to yellow, and the relay is energised above 40."
- [ ] Press **PB1**, the emergency button: relay drops, buzzer sounds, LCD reads
      emergency, and the telemetry line changes.
- [ ] Press **PB2**: normal control resumes. Say: "Two external interrupts, INT0
      and INT1, edge triggered, debounced by 5 millisecond resampling."
- [ ] Point at the terminal scrolling: "One telemetry line per second, 9600 8N1."

### Beat 4 - the numbers (60 s)

Say six numbers, each with its derivation. This is where slide 6 pays off.

| Number | Say it like this |
|---|---|
| 0.00 % baud error | "TH1 = FDH. At 11.0592 MHz the divisor is exact. At 12 MHz it is 8 percent out and the link fails." |
| 1.00 kHz | "Timer reload FE34H, within 0.17 percent." |
| 100 Hz display | "EE00H, every 5 milliseconds per digit, above flicker." |
| 0.78 C per step | "Reference trimmed to 1.000 volt gives 7.8125 millivolts per LSB." |
| 157 mA | "274 peak with relay and buzzer on. The 7805 has a heatsink for it." |
| 3.4 KB | "Largest program, of 8 KB flash, about 30 bytes of RAM." |

Then close with your own limits before they find them: shared bus caps
throughput, one 8-bit ADC channel, 256 bytes of RAM, two external interrupts with
no priority nesting, and **the relay is never connected to mains.** Naming your
limits is more credible than being caught by them.

---

## 7. Slide deck, if you are asked to project

Use `docs/8051_Hardware_Lab_Review_Deck.pptx`, 7 slides,
`docs/DECK_OUTLINE.md` has 45 to 120 second speaker notes per slide. Compressed
version:

| Slide | One line |
|---|---|
| 1 Title | 32 of 32 pins, 0.00 % baud error, 0.78 C resolution, INR 985 |
| 2 Problem | The brief, then the 22-pin deficit and constraints C1 to C6 |
| 3 Architecture | Block diagram: bus, strobes, four devices, one road |
| 4 Stack | Hardware list and the 13-program software list, side by side |
| 5 Logic | The flow: read, convert, decide, act - and where the ISRs fit |
| 6 Results | Six numbers, then the trade-off matrix |
| 7 Close | Now / next / later, and the limits panel |

Rules for the deck: **do not read it out.** Each slide gets one claim and one
number. The board is what you point at. If a slide does not answer a question
someone asked, skip it.

Do not add a thank-you slide. The last sentence is the last thing they hear:
"Fifty-four signals, thirty-two pins, thirteen programs, twenty measured tests."

---

## 8. The viva bank

Grouped by where it comes from. You will get roughly five of these. Answers are
written to be said in two sentences, not essays.

### Architecture

**Q. Why not use a bigger microcontroller?**
Then it stops being a breadboard project - any larger device means surface mount
and a PCB. The 32-pin budget was the constraint given to us, so the architecture
is the answer to it.

**Q. Why not a port expander?**
Two more chips, about 250 rupees, and every output update becomes a serial
transaction. Sharing the bus cost us eight strobe pins and a few microseconds per
transfer instead.

**Q. Explain the shared bus in one sentence.**
Eight port 0 wires carry data for the LED latch, the segment latch, the LCD and
the ADC in turn, and one strobe pin per device decides who captures the byte.

**Q. Why a latch and not a plain buffer?**
A buffer passes data through and loses it. The 74HC573 copies the byte on the
strobe edge and holds it indefinitely, so all four devices can keep their values
between transfers.

**Q. Why the 74HC573 and not the 74HC373?**
Same function, different pinout. The board layout is wired for the 573, and the
373 will not drop into that footprint.

**Q. What happens if two strobes are high together?**
Two devices drive the bus at once, we latch garbage, and the board misbehaves.
It is prevented in software: strobe, write, clear strobe, and interrupts are
disabled during LCD and ADC cycles.

**Q. Why does port 0 need external pull-ups?**
Port 0 is open drain - it can pull a line low but cannot pull it high. RN1, a
10 k SIP network, provides the high level. Any other port has weak internal
pull-ups.

**Q. How many pins did you actually use?**
32 of 32. Port 0 is the bus, port 1 is the switches, port 2 is eight strobes,
port 3 carries the UART, the two interrupts, the relay, the buzzer and the two
digit selects.

### Firmware

**Q. Why 11.0592 MHz and not 12?**
It divides exactly into 9600 baud, so the serial error is literally zero with
TH1 = FDH. At 12 MHz the error is over 8 percent and the link fails.

**Q. Derive the timer reload for 5 milliseconds.**
One machine cycle is 1.0851 microseconds at this crystal. 5000 microseconds
divided by 1.0851 is 4608 counts, and 65536 minus 4608 is 60928, which is EE00H.

**Q. What does the 5 millisecond interrupt do?**
It refreshes one digit of the display, alternating between the two, so each digit
gets 100 Hz. It also maintains a millisecond counter. It stays short so the main
loop is never delayed.

**Q. Why flags inside the ISR instead of doing the work there?**
A short ISR keeps latency predictable and cannot block the display refresh. The
ISR sets a flag, the main loop acts on it.

**Q. What is `bus_shadow` for?**
The latches cannot be read back. We keep the last byte written in a RAM variable,
save and restore it around bus operations, so we always know what is latched.

**Q. How are the buttons debounced?**
Software: 5 millisecond resampling with edge-triggered INT0 and INT1, so one
press is one interrupt. No RC parts and no spare pins.

**Q. How does the temperature become a number?**
The LM35 gives 10 millivolts per degree into an 8-bit ADC. With the reference
trimmed to 1.000 volt each step is 7.8125 millivolts, so T equals raw times 25
over 32, which is 0.78 degrees per step.

**Q. Delay routine or timer - which is more accurate?**
The timer, by a wide margin. The delay loop is calibrated to the crystal and to
the compiler; program 05 uses the hardware timer and is the one that passes the
one-second test to within 0.2 seconds.

### Hardware and build

**Q. Why is EA tied high?**
It selects internal flash. Floating or low, the chip fetches from external program
memory that does not exist, and it appears completely dead.

**Q. How do you program it in circuit?**
SPI on P1.5, P1.6, P1.7 plus RESET, through a 2x5 header. Six wires, no 12 volt
supply, no chip removal. The 8051 needs RESET high, which is why a stock USBasp
fails and an Arduino-as-ISP works.

**Q. What breaks if switches 6 to 8 are closed while programming?**
They share the three SPI pins and fight the programmer. That is why they are
documented as OFF, and why there are 1 k series resistors.

**Q. Why 470 ohm LED resistors and not 330?**
330 would put the latch package over its 70 milliamp total limit. 470 keeps it at
about 53 milliamps, and costs roughly 15 percent brightness.

**Q. Is the relay mains rated?**
The relay contacts are, but **we never connect mains.** It is a demonstration
load, low voltage only, and that is stated as a limit in the report.

**Q. What happens when the power goes off?**
The flash keeps the program, so it restarts on power-up. Variables in RAM are
lost, which is why nothing relies on remembered state.

### Process and honesty

**Q. What is the 0x0800 thing in the HEX file?**
The free Keil linker places code at 0x0800 and plants a long jump at address 0.
On an 8 KB part that boots normally. It only matters on a 2 KB device, and it is
also why the free version refuses anything over 2048 bytes.

**Q. How do you know the temperature is right?**
Test T11 compares it against a reference thermometer over 25 to 60 degrees, and
ours agreed within 1.5 degrees. That is the number in the result sheet.

**Q. What failed during development?**
Pick a true one and tell it in three lines: what broke, how you found it, what
you changed. The reset circuit and the ISP contention are the two honest,
instructive ones, both already documented in `START_HERE.md`.

**Q. What would you do differently?**
A two-layer PCB with a ground plane, and a digital-output sensor to remove the
ADC and its reference entirely. Then move the LCD onto an I2C backpack, which
returns two pins.

**Q. Which parts did you write and which are libraries?**
`board.h` is our own driver layer - every pin alias, constant and driver function
in one file - and the thirteen programs are ours. The compiler, the startup code
and the C library are the toolchain's.

Never claim a result you cannot show. If you did not measure it, say "not
measured, specified as X" - that answer is respected. An invented number is the
one thing that ends a viva badly.

---

## 9. If it fails in front of them

It happens. The recovery is a script, not panic. **Keep talking, narrate the
diagnosis.** A calm, correct fault-finding sequence scores better than a board
that works, because it shows you know the system.

| What breaks live | Your first move | What to say |
|---|---|---|
| Nothing lights up | check 5 V, then EA pin 31 | "Either power or the EA strap. It is EA far more often than the code." |
| Board runs but telemetry is blank | check COM port, 9600 8N1 | "Serial is fine on the board, it is the terminal. I will show the LCD instead." |
| LCD blank | turn the contrast pot R9 | "Contrast, not the interface. This pot is the usual suspect." |
| Zone will not go yellow | your heat source is too cool | "Fingers reach 34 degrees and the threshold is 40. I will use the emergency path instead, which proves the same decision logic." |
| Chip B will not run | swap to chip A, then to program 01 | "I have a second chip flashed with the self test. Let me use that." |
| Nothing works at all | stop soldering. Switch to evidence | "The board has an intermittent fault I will not debug in front of you. Here is the recorded run, the build table and the twenty measured tests." |

Keep these ready, in this order: the recorded video
`docs/guide/video/8051_Start_To_Finish.mp4`, the build table printout, the filled
result sheet, the deck PDF. **A recorded run plus measured data is a legitimate
submission.** What is not legitimate is spending 10 minutes silently re-seating
chips.

Rule of thumb: **three minutes maximum** on any fault in front of a reviewer.
Then switch to evidence and offer to debug it afterwards.

---

## 10. Who says what

Two authors, so split by subject, not by turn. Faculty notice when one person
answers everything.

**ATHARVA (24BEL0082)** - architecture and hardware
- the 54 vs 32 deficit and the shared bus
- schematic, pin allocation, power supply, the build stages
- the build questions in section 8

**ADITYA (24BEL0087)** - firmware and results
- the 13 programs, `board.h`, the timers and constants
- the test results and the telemetry demo
- the code questions in section 8

Both must be able to answer "what was your part" without contradicting each
other, and both should have run the demo alone at least once before the review.
If one of you is absent, the other should still be able to do section 5.

---

## 11. Rehearse three times, then stop

1. **Rehearsal 1 - alone, no audience, with the timer.** Section 5, the 5-minute
   version, twice. You are learning the hands, not the words.
2. **Rehearsal 2 - the 12-minute order, out loud, to your partner.** They interrupt
   with three questions from section 8 at random moments. That is what a viva
   feels like.
3. **Rehearsal 3 - the full thing, recorded on a phone.** Watch it once at 2x
   speed. You will find four things: you say "basically", you turn your back to
   the audience, you apologise unnecessarily, and you talk too fast at the start.
   Fix only those.

Then leave it alone. Over-rehearsed demos sound recited, and faculty notice that
too.

---

## 12. Do not do these

- **Do not say "the AI/Internet wrote the code."** If asked about assistance,
  say what is true and specific: "the driver layer and the thirteen programs are
  ours; the toolchain, the datasheets and the reference designs are not." Then
  prove it by answering one deep question, which is what actually settles it.
- **Do not read the slides.** One claim per slide, then talk.
- **Do not claim the relay is mains connected.** It is the fastest way to lose
  marks for safety awareness.
- **Do not say "it works perfectly."** Say what was tested and what the tolerance
  was.
- **Do not blame the lab** for the 2 KB compiler limit in a way that sounds like
  an excuse. It is a toolchain decision and you handled it.
- **Do not leave the programmer plugged in** during the demo. It raises exactly
  the doubt you cannot afford.
- **Do not debug silently.** Narrate, or switch to evidence.
- **Do not skip the result sheet.** Blank measured columns are the most common
  avoidable loss.

---

## 13. The one-page card

`docs/DEMO_CARD.md` is the same information reduced to one printable page: the
numbers, the three sentences, the demo beats, the button map and the fault
recovery. Print it, put it under the board, and do not memorise the rest.
