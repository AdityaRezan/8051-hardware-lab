# Schematic and Connection Tables - 8051 Hardware Lab Board

Target device: Atmel AT89S52-24PU, 40 pin plastic DIP, 11.0592 MHz, 5 V supply.
Fallback device: AT89C51-24PU, same pinout, programmed with a parallel programmer instead of SPI.

---

## 1. Why the board needs a shared data bus

The 8051 has 32 I/O lines. A straightforward allocation of every peripheral would need 54.

| Peripheral | Dedicated pins required |
|---|---:|
| 8 LED output bank | 8 |
| 8 way DIP switch input | 8 |
| 7-segment segment lines | 8 |
| 7-segment digit selects | 2 |
| 16x2 LCD, 8-bit data plus RS RW E | 11 |
| ADC0804, 8-bit data plus WR RD INTR | 11 |
| UART TxD and RxD | 2 |
| INT0 and INT1 push buttons | 2 |
| Relay driver and buzzer driver | 2 |
| **Total required** | **54** |
| **Available on the 8051** | **32** |

The eight data lines of the LCD, the ADC, the LED latch and the segment latch are all passive 8-bit
parallel loads that are only read or written for a few microseconds at a time. They are therefore
merged into one 8-bit data bus on port 0. Each device keeps its own latch-enable or enable pin, so a
transfer only affects the device whose enable is strobed.

| Peripheral | Pins after bus sharing |
|---|---:|
| Shared 8-bit data bus (P0) | 8 |
| DIP switch bank (P1) | 8 |
| Strobes and control (P2.0 to P2.7) | 8 |
| UART, interrupts, relay, buzzer, digit selects (P3) | 8 |
| **Total used** | **32** |

The bus is driven by software, not by MOVX. This keeps the code readable on a teaching board and
leaves port 2 free for control strobes. Every write is: place the byte on P0, pulse the enable line
of the target device, and leave the byte on the bus as the shadow value.

---

## 2. Complete pin allocation

| Pin | Signal | Direction | Board net | Destination |
|---:|---|---|---|---|
| 40 | VCC | power | +5V | 7805 output |
| 20 | GND | power | GND | common ground plane |
| 19 | XTAL1 | in | XTAL1 | Y1 pin 1, C3a to GND |
| 18 | XTAL2 | out | XTAL2 | Y1 pin 2, C3b to GND |
| 9 | RST | in | RESET | R1 to GND, C2 to +5V, PB3 to +5V, J3 pin 5 |
| 31 | EA/VPP | in | +5V | tied high, selects internal flash |
| 30 | ALE | - | not connected | unused, no external memory |
| 29 | PSEN | - | not connected | unused, no external memory |
| 39 | P0.0 / AD0 | bidir | BD0 | U2 D0, U3 D0, LCD1 D0, U4 DB0, RN1 |
| 38 | P0.1 / AD1 | bidir | BD1 | U2 D1, U3 D1, LCD1 D1, U4 DB1, RN1 |
| 37 | P0.2 / AD2 | bidir | BD2 | U2 D2, U3 D2, LCD1 D2, U4 DB2, RN1 |
| 36 | P0.3 / AD3 | bidir | BD3 | U2 D3, U3 D3, LCD1 D3, U4 DB3, RN1 |
| 35 | P0.4 / AD4 | bidir | BD4 | U2 D4, U3 D4, LCD1 D4, U4 DB4, RN1 |
| 34 | P0.5 / AD5 | bidir | BD5 | U2 D5, U3 D5, LCD1 D5, U4 DB5, RN1 |
| 33 | P0.6 / AD6 | bidir | BD6 | U2 D6, U3 D6, LCD1 D6, U4 DB6, RN1 |
| 32 | P0.7 / AD7 | bidir | BD7 | U2 D7, U3 D7, LCD1 D7, U4 DB7, RN1 |
| 1 | P1.0 | in | SW1 | DIP switch 1, RN2 pull-up |
| 2 | P1.1 | in | SW2 | DIP switch 2, RN2 pull-up |
| 3 | P1.2 | in | SW3 | DIP switch 3, RN2 pull-up |
| 4 | P1.3 | in | SW4 | DIP switch 4, RN2 pull-up |
| 5 | P1.4 | in | SW5 | DIP switch 5, RN2 pull-up |
| 6 | P1.5 | in | SW6 and MOSI | DIP switch 6 via R4a, J3 pin 1 |
| 7 | P1.6 | in | SW7 and MISO | DIP switch 7 via R4b, J3 pin 9 |
| 8 | P1.7 | in | SW8 and SCK | DIP switch 8 via R4c, J3 pin 7 |
| 21 | P2.0 | out | LED_LE | U2 pin 11 (LE) |
| 22 | P2.1 | out | SEG_LE | U3 pin 11 (LE) |
| 23 | P2.2 | out | LCD_E | LCD1 pin 6 (E) |
| 24 | P2.3 | out | LCD_RS | LCD1 pin 4 (RS) |
| 25 | P2.4 | out | LCD_RW | LCD1 pin 5 (RW) |
| 26 | P2.5 | out | ADC_WR | U4 pin 3 (WR, active low) |
| 27 | P2.6 | out | ADC_RD | U4 pin 2 (RD, active low) |
| 28 | P2.7 | in | ADC_INTR | U4 pin 5 (INTR, active low) |
| 10 | P3.0 / RxD | in | RXD | U5 pin 12 (R1OUT) |
| 11 | P3.1 / TxD | out | TXD | U5 pin 11 (T1IN) |
| 12 | P3.2 / INT0 | in | PB1 | emergency button, pull-up R2a |
| 13 | P3.3 / INT1 | in | PB2 | mode button, pull-up R2b |
| 14 | P3.4 / T0 | out | RELAY_DRV | JP1 pin 1, then Q3 base via R3a |
| 15 | P3.5 / T1 | out | BUZZ_DRV | Q4 base via R3b |
| 16 | P3.6 / WR | out | DIG1 | Q1 base via R2c |
| 17 | P3.7 / RD | out | DIG2 | Q2 base via R2d |

Note on R2 and R3: the bill of materials lists R2 and R3 as quantities of two. Populate four
4.7 kOhm parts for the two digit transistors and two interrupt pull-ups, and two 1 kOhm parts for
the relay and buzzer bases.

---

## 3. Block diagram

```
                      +---------------------------+
   7 - 12 V DC  ----> |  D1 1N4007   U7 7805      | ----> +5V rail
   (J1 barrel)        |  C4 100uF    C5 100uF     |        |
                      +---------------------------+        |
                                                           |
     +5V --------------------------------------------------+---------+---------+
                                                                     |         |
   +-------------------------+       8-bit data bus BD0..BD7          |         |
   |   U1  AT89S52           |<======================================>+--+      |
   |   11.0592 MHz           |       (P0 open drain, RN1 10k pull-ups) |  |      |
   |   P2.0 LED_LE  ---------|-----> U2 74HC573 ----> RN3 470R ----> 8 LEDs     |
   |   P2.1 SEG_LE  ---------|-----> U3 74HC573 ----> RN4 470R ---+             |
   |   P2.2 LCD_E   ---------|-----> LCD1 16x2 E                   |            |
   |   P2.3 LCD_RS  ---------|-----> LCD1 16x2 RS                  |            |
   |   P2.4 LCD_RW  ---------|-----> LCD1 16x2 RW                  |            |
   |   P2.5 ADC_WR  ---------|-----> U4 ADC0804 WR\                v            |
   |   P2.6 ADC_RD  ---------|-----> U4 ADC0804 RD\         DSP1 2-digit        |
   |   P2.7 ADC_INTR <-------|-----  U4 ADC0804 INTR\       common cathode      |
   |                         |                                 a..g,dp          |
   |   P1.0..P1.7   <========|===== SW1 8-way DIP switch          | |           |
   |                         |      (RN2 10k pull-ups)          Q1  Q2          |
   |   P3.0 RxD     <--------|-----  U5 MAX232 R1OUT            |    |          |
   |   P3.1 TxD     -------->|-----> U5 MAX232 T1IN --> DB9 J2   |    |          |
   |                         |                                  |    |          |
   |   P3.2 INT0    <--------|-----  PB1 emergency button  P3.6 -+    |          |
   |   P3.3 INT1    <--------|-----  PB2 mode button       P3.7 ------+          |
   |                         |                                                   |
   |   P3.4 T0      -------->|-----> JP1 ----> Q3 BC547 ----> RLY1 5 V SPDT      |
   |   P3.5 T1      -------->|-----> Q4 BC547 ----> BZ1 buzzer                   |
   +-------------------------+                                                   |
                                                                                 |
        U6 LM35 (J5) --> U4 ADC0804 Vin+   with Vref/2 set to 1.00 V by R8  <----+
```

---

## 4. Subsystem wiring

### 4.1 Minimum system (U1)

| Connection | From | To |
|---|---|---|
| Crystal | Y1 pins 1 and 2 | U1 pins 19 and 18 |
| Load capacitor C3a 30 pF | U1 pin 19 | GND |
| Load capacitor C3b 30 pF | U1 pin 18 | GND |
| Reset pull-down R1 10 kOhm | U1 pin 9 | GND |
| Reset capacitor C2 10 uF, positive leg | U1 pin 9 | +5V |
| Reset button PB3 | U1 pin 9 | +5V |
| EA/VPP strap | U1 pin 31 | +5V |
| Decoupling C1 0.1 uF | U1 pin 40 | U1 pin 20, as close to the pins as possible |
| Supply | U1 pin 40 | +5V |
| Ground | U1 pin 20 | GND |

The AT89S52 starts oscillating about 1 ms after power is applied and the reset pulse from R1 and C2
holds RST high for roughly 100 ms, which is far longer than the required two machine cycles.

### 4.2 Power supply

| Connection | From | To |
|---|---|---|
| J1 centre pin | barrel jack positive | D1 anode |
| D1 cathode | - | U7 pin 1 (input) |
| C4 100 uF/25 V, C6a 0.1 uF | U7 pin 1 | GND |
| U7 pin 2 (GND) | - | GND |
| C5 100 uF/16 V, C6b 0.1 uF | U7 pin 3 (output) | GND |
| Power LED D11 and R5 330 Ohm in series | +5V | GND |
| Heatsink HS1 | U7 tab | - |

Input range 7 V to 12 V. At 9 V and 250 mA the regulator dissipates about 1 W, so HS1 is required.

### 4.3 LED output bank (U2)

| Signal | U2 74HC573 pin | Destination |
|---|---|---|
| D0 to D7 | 2 to 9 | BD0 to BD7 |
| LE | 11 | P2.0 (LED_LE) |
| OE (active low) | 1 | GND |
| Q0 to Q7 | 19, 18, 17, 16, 15, 14, 13, 12 | RN3 470 Ohm, then LED anodes |
| VCC | 20 | +5V, C6c 0.1 uF to GND |
| GND | 10 | GND |

Each LED cathode goes to GND. A logic 1 in a latch bit lights the corresponding LED.

### 4.4 Seven segment display (U3, Q1, Q2, DSP1)

| Signal | From | To |
|---|---|---|
| D0 to D7 | BD0 to BD7 | U3 pins 2 to 9 |
| LE | P2.1 (SEG_LE) | U3 pin 11 |
| OE | GND | U3 pin 1 |
| Q0 to Q7 | U3 pins 19, 18, 17, 16, 15, 14, 13, 12 | RN4 470 Ohm |
| RN4 outputs | - | DSP1 segments a b c d e f g dp |
| Digit 1 common cathode | DSP1 pin for digit 1 | Q1 collector |
| Digit 2 common cathode | DSP1 pin for digit 2 | Q2 collector |
| Q1, Q2 emitters | - | GND |
| Q1 base | R2c 4.7 kOhm | P3.6 |
| Q2 base | R2d 4.7 kOhm | P3.7 |

Segment bit map: Q0 = a, Q1 = b, Q2 = c, Q3 = d, Q4 = e, Q5 = f, Q6 = g, Q7 = dp.

| Digit | Pattern | Digit | Pattern |
|---|---|---|---|
| 0 | 3FH | 5 | 6DH |
| 1 | 06H | 6 | 7DH |
| 2 | 5BH | 7 | 07H |
| 3 | 4FH | 8 | 7FH |
| 4 | 66H | 9 | 6FH |

The digits are multiplexed: timer 0 interrupts every 5 ms and alternately latches the digit 1
pattern with P3.6 high and the digit 2 pattern with P3.7 high. Refresh rate per digit is 100 Hz,
which is above the flicker fusion limit.

### 4.5 16x2 character LCD (LCD1)

| LCD pin | Name | Destination |
|---:|---|---|
| 1 | VSS | GND |
| 2 | VDD | +5V, C6d 0.1 uF to GND |
| 3 | VO | wiper of R9 10 kOhm potentiometer, ends to +5V and GND |
| 4 | RS | P2.3 |
| 5 | RW | P2.4 |
| 6 | E | P2.2 |
| 7 to 14 | D0 to D7 | BD0 to BD7 |
| 15 | A (backlight anode) | +5V through R7 220 Ohm |
| 16 | K (backlight cathode) | GND |

The module is used in 8-bit mode. RW is driven so the firmware can poll the busy flag if needed; the
shipped driver uses software delays instead, so RW may be tied to GND to save one port pin.

### 4.6 Temperature input (U4 ADC0804 and U6 LM35)

| ADC pin | Name | Destination |
|---:|---|---|
| 1 | CS (active low) | GND, permanently selected |
| 2 | RD (active low) | P2.6 |
| 3 | WR (active low) | P2.5 |
| 4 | CLK IN | junction of R6 and C8 |
| 5 | INTR (active low) | P2.7 |
| 6 | Vin(+) | LM35 output, J5 pin 2 |
| 7 | Vin(-) | GND |
| 8 | AGND | GND |
| 9 | Vref/2 | wiper of R8 10 kOhm trimpot, ends to +5V and GND, C10 0.1 uF to GND |
| 10 | DGND | GND |
| 11 to 18 | DB7 to DB0 | BD7 to BD0 |
| 19 | CLK R | other end of R6 10 kOhm |
| 20 | VCC | +5V, C6e 0.1 uF to GND |

The internal clock oscillator is the RC network formed by R6 between pin 19 and pin 4 and C8 from
pin 4 to ground; this is the self-clocking arrangement given in the ADC0804 datasheet.

LM35 (TO-92, flat face towards you, pins 1-2-3 left to right):

| LM35 pin | Name | Destination |
|---:|---|---|
| 1 | Vs | +5V, C9 0.1 uF to GND |
| 2 | Vout | U4 pin 6 |
| 3 | GND | GND |

### 4.7 Serial link (U5 MAX232 and J2 DB9)

| MAX232 pin | Name | Destination |
|---:|---|---|
| 1 | C1+ | C7a positive leg |
| 3 | C1- | C7a negative leg |
| 4 | C2+ | C7b positive leg |
| 5 | C2- | C7b negative leg |
| 2 | V+ | C7c positive leg, negative leg to +5V |
| 6 | V- | C7d negative leg, positive leg to GND |
| 11 | T1IN | P3.1 (TxD) |
| 12 | R1OUT | P3.0 (RxD) |
| 13 | R1IN | J2 pin 3 |
| 14 | T1OUT | J2 pin 2 |
| 15 | GND | GND |
| 16 | VCC | +5V, C6f 0.1 uF to GND |

C7a to C7d are 1 uF for a MAX232 and 0.1 uF for a MAX232A or MAX3232. C3 is returned to VCC, not to
ground, because that connection is correct for both Maxim and TI parts.

DB9 female on the board (J2): pin 2 to T1OUT, pin 3 to R1IN, pin 5 to GND. This makes the board a
DCE device so a straight through serial cable works with a USB to RS-232 adapter.

### 4.8 Relay, buzzer and push buttons

| Element | Connection |
|---|---|
| JP1 pin 1 | P3.4 |
| JP1 pin 2 | R3a 1 kOhm to Q3 base |
| Q3 emitter | GND |
| Q3 collector | RLY1 coil pin 1 |
| RLY1 coil pin 2 | +5V |
| D2 1N4007 | cathode to +5V, anode to Q3 collector (flyback) |
| RLY1 COM and NO | J4 screw terminals |
| Q4 base | R3b 1 kOhm from P3.5 |
| Q4 emitter | GND |
| Q4 collector | BZ1 negative terminal |
| BZ1 positive terminal | +5V |
| PB1 | P3.2 to GND, with R2a 4.7 kOhm from P3.2 to +5V |
| PB2 | P3.3 to GND, with R2b 4.7 kOhm from P3.3 to +5V |

A logic 1 on P3.4 energises the relay and a logic 1 on P3.5 sounds the buzzer. The buttons are
active low and generate a falling edge, which is what IT0 and IT1 are configured to detect.

### 4.9 DIP switch input bank

| Element | Connection |
|---|---|
| SW1 contacts 1 to 8 | P1.0 to P1.7, each to GND through the switch |
| RN2 10 kOhm x9, pins 2 to 9 | P1.0 to P1.7 pull-ups |
| RN2 pin 1 (common) | +5V |
| R4a, R4b, R4c 1 kOhm | in series with P1.5, P1.6, P1.7 to their switches |

Closed switch reads as 0, open switch reads as 1. The series resistors on P1.5 to P1.7 protect the
ISP programmer when a switch is closed during programming. Set SW6, SW7 and SW8 to OFF before
flashing the device.

### 4.10 ISP header (J3, 2x5 pin)

| J3 pin | Signal | Destination |
|---:|---|---|
| 1 | MOSI | P1.5 (U1 pin 6) |
| 2 | VCC | +5V |
| 4, 6, 8, 10 | GND | GND |
| 5 | RESET | RST (U1 pin 9) |
| 7 | SCK | P1.7 (U1 pin 8) |
| 9 | MISO | P1.6 (U1 pin 7) |

---

## 5. Design calculations

### 5.1 Machine cycle

One machine cycle is 12 oscillator periods.

```
Tcy = 12 / 11.0592 MHz = 1.0851 microseconds
```

### 5.2 UART baud rate, 9600 baud

Timer 1 in mode 2 (8-bit auto reload), SMOD = 0.

```
TH1 = 256 - (11059200 / (384 x 9600)) = 256 - 3 = 253 = 0xFD
```

Error is exactly zero percent, which is the reason 11.0592 MHz is used instead of 12 MHz.

### 5.3 Display refresh, 5 ms

Timer 0 in mode 1 (16-bit), interrupt every 5 ms.

```
counts = 5000 / 1.0851 = 4608
reload = 65536 - 4608 = 60928 = 0xEE00     TH0 = 0xEE, TL0 = 0x00
```

### 5.4 One second blink

Timer 0 in mode 1, reload every 50 ms, twenty interrupts per second.

```
counts = 50000 / 1.0851 = 46080
reload = 65536 - 46080 = 19456 = 0x4C00    TH0 = 0x4C, TL0 = 0x00
```

### 5.5 1 kHz square wave

Timer 0 in mode 1, reload every half period of 500 microseconds.

```
counts = 500 / 1.0851 = 461
reload = 65536 - 460 = 65076 = 0xFE34      TH0 = 0xFE, TL0 = 0x34
measured output = 1 / (2 x 460 x 1.0851 us) = 1001.7 Hz
```

### 5.6 ADC reference and transfer function

Vref/2 is set to 1.00 V with R8, so the full scale input is 2.00 V.

```
LSB      = 2.00 V / 256 = 7.8125 mV
LM35 gain = 10 mV per degree C
1 LSB    = 0.78125 degree C
T (C)    = raw x 0.78125 = raw x 25 / 32
range    = 0 to 199.2 degree C
resolution = 0.78 degree C
```

Leaving pin 9 open selects the internal 2.5 V reference and gives 0 to 5 V full scale, which wastes
more than half the ADC range for an LM35. Setting Vref/2 to 1.00 V uses the range properly.

### 5.7 ADC clock and conversion time

```
fclk = 1 / (1.1 x R6 x C8) = 1 / (1.1 x 10 kOhm x 150 pF) = 606 kHz
conversion = about 66 to 73 clock periods = about 110 to 120 microseconds
```

### 5.8 LED current

```
I per LED = (5.0 - 1.9) / 470 = 6.6 mA
I per latch package, 8 LEDs on = 52.8 mA
```

74HC573 is rated for 70 mA total through the package, so 470 Ohm is used rather than 330 Ohm. With
330 Ohm the eight LED total would be 75 mA and exceed the rating.

### 5.9 Current budget

| Load | Typical | Maximum |
|---|---:|---:|
| U1 AT89S52 at 11.0592 MHz | 25 mA | 30 mA |
| U2 plus 8 LEDs | 53 mA | 53 mA |
| U3 plus one 7-segment digit | 53 mA | 53 mA |
| LCD1 logic and backlight | 10 mA | 14 mA |
| U4 ADC0804 | 3 mA | 5 mA |
| U5 MAX232 | 10 mA | 15 mA |
| U6 LM35 | 0.1 mA | 0.2 mA |
| Transistor bases | 3 mA | 4 mA |
| RLY1 coil when energised | 0 mA | 70 mA |
| BZ1 buzzer when on | 0 mA | 30 mA |
| **Total** | **157 mA** | **274 mA** |

A 500 mA supply is comfortable and the 7805 needs its heatsink above about 150 mA of continuous load.

---

## 6. Constraints and errata

1. Port 0 is open drain. It cannot drive a logic 1 without RN1, and with RN1 fitted the rise time
   limits the bus to a few hundred kilohertz, which is far above anything used here.
2. P1.5, P1.6 and P1.7 are shared between the DIP switches and the ISP header. Set SW6, SW7 and SW8
   to OFF while programming.
3. P3.4 drives the relay through jumper JP1. Remove the shunt before running the square wave program
   and probing the pin, otherwise the relay coil loads the signal.
4. The 7-segment display must be common cathode. A common anode display requires the segment table to
   be inverted and the digit transistors to switch +5V instead of ground.
5. The LCD and the ADC share the data bus. The firmware saves, writes and restores the bus byte
   around every transfer, and disables interrupts during LCD and ADC accesses so the display refresh
   interrupt cannot corrupt a transfer.
6. Do not connect the relay contacts to mains voltage during laboratory demonstration. Use a 5 V or
   12 V lamp load on J4, or leave the contacts unconnected and observe the coil LED.
