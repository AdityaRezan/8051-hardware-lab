# Dividing the work - both ways

Two ways to cut this project, and you need both:

- **By part (1 to 13)** - the order you actually do things, with the dependencies
  that stop you doing them out of order.
- **By person** - who owns which part, so nothing is done twice and nothing is
  left undone.

Both mappings are below, then a four week plan and a cross-training list.

Read with: `START_HERE.md` (the whole project in order),
`docs/SOFTWARE_RUNBOOK.md` (Part 1 to 2 in detail),
`hardware/ASSEMBLY.md` (Part 4 to 8 in detail),
`docs/RESULTS.md` (Part 10 in detail),
`docs/FACULTY_DEMO.md` (Part 13 in detail).

- **ATHARVA (24BEL0082)** - hardware lead: schematic, procurement, build, electrical tests
- **ADITYA (24BEL0087)** - firmware lead: toolchain, HEX files, flashing, software tests

Nobody owns a part alone. Every part names a **lead** and a **shadow**, and the
shadow has to be able to do it once, alone, before the review.

---

## 1. The thirteen parts at a glance

| Part | What it is | Lead | Hours | Depends on |
|---:|---|---|---:|---|
| 1 | Laptop toolchain and one clean build | ADITYA | 4-6 | - |
| 2 | Build all 13 HEX files | ADITYA | 3-4 | 1 |
| 3 | Procurement, INR 985 of parts | ATHARVA | 2 + waiting | - |
| 4 | Power supply, then the minimum system | ATHARVA | 4 | 3 |
| 5 | Output stage: LED bank and display | ATHARVA | 4 | 4 |
| 6 | Input and serial stage: switches, MAX232 | ATHARVA | 3 | 4 |
| 7 | Analogue and LCD stage | ATHARVA | 4 | 4 |
| 8 | Actuators and final checkout | ATHARVA | 3 | 5-7 |
| 9 | Bring-up: flash and prove it runs | ADITYA | 2 | 2, 4 |
| 10 | Test campaign, T1 to T20 | BOTH | 5 | 8, 9 |
| 11 | Documentation package | split | 4 | 5-10 |
| 12 | Report and deck | BOTH | 5 | 10, 11 |
| 13 | Demo rehearsal and delivery | BOTH | 2 | 12 |

Total: about **45 hours** of work, roughly **22-24 hours each**, spread over four
weeks. Parts 1-2 and part 3 run in parallel, which is the whole reason this fits.

---

## 2. The dependency picture

```
        PART 1  laptop + one clean build (ADITYA)
           |
        PART 2  all 13 HEX files (ADITYA)
           |                                   PART 3  buy the parts (ATHARVA)
           |                                      |
           |                                   PART 4  power supply -> minimum system  <== GATE
           |                                      |
           |                        +-------------+-------------+
           |                        |             |             |
           |                     PART 5        PART 6        PART 7
           |                     outputs      inputs+serial  analogue+LCD
           |                        |             |             |
           |                        +------ PART 8 actuators ---+
           |                                      |
           +-------------------------> PART 9  bring-up / flash (ADITYA)
                                                  |
                                            PART 10  T1..T20 (BOTH)
                                                  |
                                       PART 11 docs -> PART 12 report+deck
                                                  |
                                            PART 13  rehearse, deliver
```

Three things this picture tells you:

1. **Part 3 can start on day one.** Order parts the same evening you start
   installing Keil, because shipping is the longest lead time in the project.
2. **Part 4 is the gate.** Nothing on the hardware side moves until the 5 V rail
   measures right. Build the supply alone and test it alone.
3. **Part 9 needs only parts 2 and 4.** The moment the chip sits in a powered
   minimum system, you can flash program 01 and prove the whole chain works -
   before the display, the LCD or the sensor exist. If that fails, you want to
   know it in week two, not week four.

---

## 3. Part by part, with the done condition

Each part below is finished only when the **done when** line is true. Not "mostly
finished" - true.

### Part 1 - Laptop toolchain and one clean build
**Lead ADITYA, shadow ATHARVA. 4-6 hours. Output: a working Keil install.**

- Install Keil C51 (not MDK-ARM), repo extracted to a path with no spaces.
- Confirm AT89S52 appears in the device list.
- Open `01_led_blink_AT89S52.uvprojx`, press F7.
- Read the two meaningful lines: `0 Error(s)` and `code=1129`.
- Understand the 20 `L16: UNCALLED SEGMENT` warnings well enough to explain them.

**Done when:** a screenshot of `0 Error(s)` and `code=1129` exists, and ATHARVA
has repeated the build on his own machine or on yours.

### Part 2 - Build all 13 HEX files
**Lead ADITYA, shadow ATHARVA. 3-4 hours. Output: `firmware/hex/` with HEX files.**

- Run `tools\Build-All-HEX.bat`, read only the STATE column.
- Handle the OVER LIMIT cases (09, 12, 13) with `-Small`, then `-Small -LX51`.
- If those still fail: build them on a licensed college PC.
- Verify one HEX by eye: first line starts `:0300000002`, last is `:00000001FF`.

**Done when:** the build table printout shows at least 11 `OK`, and every HEX is
on the pen drive. The three big ones are the demo programs, so 13 is the target,
not 11.

### Part 3 - Procurement
**Lead ATHARVA, shadow ADITYA. 2 hours of ordering. Output: parts on the bench.**

- Order from `hardware/BOM.csv`, about INR 985 per board.
- **Two AT89S52 chips.** A damaged one should not end the day, and the second
  chip is what makes the demo work (see Part 13).
- Do not substitute: 11.0592 MHz crystal, 74HC573 (not 373), AT89S52 (not
  AT89C51), ADC0804, HD44780 LCD.
- Order sockets, not just chips.

**Done when:** every line item is either on the bench or in transit, and there is
one spare of each IC.

### Part 4 - Power supply, then the minimum system
**Lead ATHARVA, shadow ADITYA. 4 hours. Output: a chip that is alive.**

- Stage 1 only: build the 7805 supply. **No chip fitted.**
- Measure 4.90-5.10 V with nothing else connected.
- Stage 2: pin 40 and 20 with decoupling, crystal and both 30 pF, **EA (pin 31)
  tied to +5 V**, reset network R1 10 k / C2 10 uF, and the ISP header.
- Measure 5 V between pins 40 and 20 of the socket itself.

**Done when:** 5.00 V +/- 0.15 V measured at the chip socket, and the reset line
sits low with the button released.

### Part 5 - LED bank and display
**Lead ATHARVA, shadow ADITYA. 4 hours. Output: stages 3 and 5 fitted.**

- LED latch (74HC573), eight 470 R resistors, then the segment latch and the two
  digit drivers.
- Test each stage immediately with `01_led_blink.hex`, then `04_seg7_counter.hex`.
- Check the latch orientation before powering - it is the most common fault here.

**Done when:** all eight LEDs blink and the display counts 00 to 99 with no
ghosting.

### Part 6 - DIP switches and the serial link
**Lead ATHARVA, shadow ADITYA. 3 hours. Output: stages 4 and 6 fitted.**

- Eight DIP switches with 10 k pull-ups, then MAX232 and the DB9.
- Test with `03_switch_led.hex`, then `08_uart_echo.hex`.
- Note the SW6-SW8 / SPI contention now, because it will bite in Part 9.

**Done when:** each switch lights its LED, and a terminal at 9600 8N1 echoes
characters.

### Part 7 - LM35 converter and the LCD
**Lead ATHARVA, ADITYA assists. 4 hours. Output: stages 7 and 8 fitted.**

- ADC0804 with the LM35, and Vref/2 **trimmed to 1.000 V** - this is calibration,
  not assembly.
- Then the 16x2 LCD in 8-bit mode, contrast pot R9 set.
- Test with `10_adc_7seg.hex`, then `11_adc_lcd.hex`.

**Done when:** the display reads room temperature and tracks a finger, and the
LCD shows both lines.

### Part 8 - Relay, buzzer, final checkout
**Lead ATHARVA, shadow ADITYA. 3 hours. Output: stages 9 and 10 fitted.**

- Relay and buzzer through BC547 drivers with back-EMF diodes.
- Emergency and mode buttons.
- Run `12_industrial_monitor.hex` and `13_selftest.hex`.

**Done when:** the self test prints PASS and the relay clicks on command.

### Part 9 - Bring-up
**Lead ADITYA, shadow ATHARVA. 2 hours. Output: a board that runs alone.**

- SW6-SW8 OFF, programmer on J3, ground common, board on its own supply.
- Flash `01_led_blink.hex`. Signature should read `0x1e5206`.
- Disconnect the programmer, power cycle.

**Done when:** the LEDs blink with **no PC attached**. That is the whole software
half proven.

### Part 10 - Test campaign
**Both, split by test type. 5 hours. Output: a filled `hardware/TESTING.md`.**

| ADITYA - timing, serial, software | ATHARVA - electrical, analogue, hardware |
|---|---|
| T1 self test | T2 supply rails |
| T3 blink timing | T7 square wave (scope) |
| T4 switch input | T11 ADC vs reference thermometer |
| T5 counter | T12 LCD bar graph |
| T6 one second | T18 current draw |
| T8 interrupts | T19 regulator thermals |
| T9 echo | T20 supply rejection |
| T10 command shell | |
| T13-T17 zones, relay, emergency, telemetry | |

Two rules: **you may not record a number you did not measure**, and **the person
who did not run the test signs it**. Start T19 (15 minute thermal run) first and
do everything else while it runs.

**Done when:** the measured column is filled in ink for all 20, and any FAIL has a
one-line explanation.

### Part 11 - Documentation package
**Split. 4 hours. Output: the submission bundle.**

| ATHARVA | ADITYA |
|---|---|
| `hardware/SCHEMATIC.md` checked against the board as built | `firmware/README.md` matches the 13 programs |
| `hardware/BOM.csv` with actual prices paid | build table printout, `STATE OK` visible |
| `hardware/ASSEMBLY.md` notes where the build deviated | `docs/8051_Results_Sheet.pdf` filled |
| photos of each assembly stage | terminal captures: self test and telemetry |

**Done when:** no document describes a board you did not build. Deviations are
written down, not hidden - they are marks, not embarrassments.

### Part 12 - Report and deck
**Both. 5 hours. Output: report PDF plus `docs/8051_Hardware_Lab_Review_Deck.pptx`.**

- ATHARVA writes the architecture, schematic and build chapters.
- ADITYA writes the firmware, constants and results chapters.
- Each reads the other's chapters for factual errors.
- Rehearse the deck once against the clock (13 minutes).

**Done when:** both of you can present any slide, not just your own.

### Part 13 - Demo rehearsal and delivery
**Both. 2 hours. Output: a demo that cannot fail.**

- Pre-flash chip A (`12_industrial_monitor`) and chip B (`13_selftest`).
- Each of you runs the full six-minute demo alone, once, with no help.
- Run the failure scripts: unplug the sensor, close SW6, blank the LCD contrast.
- Print the result sheet twice and the demo card once.

**Done when:** each of you has delivered the demo solo to the other, and the
fault-recovery table has been used at least once for real.

---

## 4. Four week plan

Dates move; the shape does not.

| Week | Focus | Parts | Checkpoint at the end of the week |
|---|---|---|---|
| **1** | toolchain + build all HEX | 1, 2 (+3 ordering) | build table with 11+ OK; parts ordered |
| **2** | power and minimum system | 3, 4, then 9 early | 5 V measured, program 01 blinking on the bare board |
| **3** | the peripheral stages | 5, 6, 7, 8 | self test prints PASS |
| **4** | measure, write, rehearse | 10, 11, 12, 13 | result sheet filled, both demo solo |

The deliberate trick is **Part 9 in week 2**, before the board is finished. Flash
into a minimum system the moment you have one. If the toolchain, the programmer
or the reset circuit is wrong, you find out with the board half empty, when a fix
is cheap.

---

## 5. Handoffs - three moments where work passes between you

Most team projects fail at handoffs, not at tasks. Write these in a shared note
with a date when they happen.

| Handoff | From -> to | What must be true | Where it is recorded |
|---|---|---|---|
| H1 | ADITYA -> ATHARVA | the 13 HEX files are on the pen drive and the build table is printed | shared folder + printed table |
| H2 | ATHARVA -> ADITYA | board passes the minimum-system measurement, so flashing is safe | photo of the multimeter reading |
| H3 | both -> report | the measured column is complete and signed by whoever ran each test | `hardware/TESTING.md` |

If H2 slips, ADITYA is not idle - parts 11 and 12 can start early with the
firmware chapter and the deck.

---

## 6. Cross-training, so one absence does not stop the project

Both of you must be able to do these **alone**, once, before the review:

| Skill | Owner | Why it must be shared |
|---|---|---|
| Flash a HEX with the programmer | ADITYA | a dead programmer on review day cannot stop the demo |
| Read a build log and say why it failed | ADITYA | the words "0 errors, 20 warnings, code=1129" must be explainable |
| Measure 5 V at the chip socket correctly | ATHARVA | the first question in every fault table |
| Check EA (pin 31) and the crystal | ATHARVA | 90 % of "programs but does nothing" |
| Explain the shared bus in three sentences | ATHARVA | the highest scoring question in the viva |
| Explain raw x 25 / 32 for the temperature | ADITYA | the most likely deep question on the code |

Rule: **whoever owns a part teaches it to the other in five minutes.** If it
cannot be taught in five minutes, it is not understood well enough to be graded.

---

## 7. What each of you can be asked about, honestly

| Question | ATHARVA answers | ADITYA answers |
|---|---|---|
| Why 32 pins for 54 signals | the deficit, the bus, the strobes | the software arbitration, the interrupt gating |
| How is it powered | 7805, heatsink, 157/274 mA | why the rail matters to the ADC reference |
| How is it programmed | ISP header, six wires, reset polarity | the HEX, the 0x0800 offset, avrdude |
| How fast is it | the crystal, 1.0851 us | the reload constants TH1, EE00, FE34 |
| How accurate is it | LM35, ADC0804, trimmed reference | raw x 25 / 32, 0.78 C per step |
| What is not finished | stated limits panel | program sizes, unused drivers |

Every answer above has a home in the repo, so nobody has to memorise anything -
the point is knowing **which document to open**.

---

## 8. Mapping parts to marks

| Rubric row | Fed by parts | Evidence it produces |
|---|---|---|
| Problem definition and constraints | 1, 12 | the 54 vs 32 deficit, C1-C6 |
| Design and architecture | 3, 4, 12 | schematic, pin allocation, bus diagram |
| Implementation | 5-9 | a working board, 13 programs |
| Testing and results | 10 | `TESTING.md` filled, result sheet PDF |
| Demonstration and viva | 13 | the six-minute demo, both members solo |
| Report and presentation | 11, 12 | bundle, deck, guide |

If a rubric row has no part feeding it, that is the row you lose. Section 8 is
the fastest way to find the gap.

---

## 9. The one-page tracking table

Copy this into your notebook. Tick as you go, write the date in the last column.

| Part | Owner | Started | Finished | Date | Note |
|---:|---|---|---|---|---|
| 1 laptop + clean build | ADITYA | | | | |
| 2 all 13 HEX | ADITYA | | | | |
| 3 procurement | ATHARVA | | | | |
| 4 power + minimum system | ATHARVA | | | | |
| 5 outputs | ATHARVA | | | | |
| 6 inputs + serial | ATHARVA | | | | |
| 7 analogue + LCD | ATHARVA | | | | |
| 8 actuators + checkout | ATHARVA | | | | |
| 9 bring-up | ADITYA | | | | |
| 10 tests T1-T20 | BOTH | | | | |
| 11 documentation | split | | | | |
| 12 report + deck | BOTH | | | | |
| 13 rehearsal | BOTH | | | | |

---

## 10. Three rules for dividing work in a two person project

1. **Divide by deliverable, not by activity.** "You do the code, I do the
   hardware" is not a division - it is two projects that meet at the end. Both of
   you touch the board in Parts 10 and 13, and that is intentional.
2. **Nobody submits a part they cannot explain.** If one person built the ADC
   stage alone, the other must still be able to say what Vref/2 does and why it
   is 1.000 V.
3. **Write the deviation down.** "We used a 74HC373 because the shop had no 573"
   is a documented engineering decision. Hidden, it is a mark lost to a question
   you cannot answer.
