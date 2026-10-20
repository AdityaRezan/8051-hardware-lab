# Shooting script - filming the real board

This is the companion to `8051_Assembly_and_Run.mp4`. The animated video is
finished and can be submitted as it stands. This script lets you re-cut it with
real footage of your own bench under exactly the same narration, so the
voiceover, the captions and the timing all stay as they are. Only the pictures
change.

The narration is already recorded in `audio/01.mp3` to `audio/10.mp3`. Running
`python3 tools/build_video.py` mixes those ten clips onto the final timeline and
writes the mixed track to `docs/guide/video/_narration.wav`, which is the audio
file you mux your footage against. Every scene has a fixed length. Film each
shot a few seconds longer than the slot and trim to fit.

## Timeline

| # | Scene | Slot | Length | Speech starts |
|---|---|---|---|---|
| 01 | The problem | 0:01 - 0:27 | 27 s | 0:01 |
| 02 | The fix | 0:27 - 0:55 | 28 s | 0:28 |
| 03 | The parts | 0:55 - 1:25 | 30 s | 0:56 |
| 04 | Stage 1 to 2 - power and minimum system | 1:25 - 2:00 | 35 s | 1:25 |
| 05 | Stage 3 to 5 - outputs, inputs, display | 2:00 - 2:35 | 36 s | 2:00 |
| 06 | Stage 6 to 7 - serial link and temperature | 2:35 - 3:12 | 36 s | 2:36 |
| 07 | Stage 8 to 9 - LCD, relay, buzzer | 3:12 - 3:42 | 31 s | 3:12 |
| 08 | Stage 10 - self test | 3:42 - 4:03 | 21 s | 3:43 |
| 09 | Running - the zone monitor | 4:03 - 4:35 | 32 s | 4:04 |
| 10 | Emergency stop and results | 4:35 - 5:11 | 36 s | 4:36 |

## Before you start

- Phone on a tripod or a cheap overhead arm. Shoot **4K if you have it**, then
  export at 1080p: the crop gives you room to reframe without losing sharpness.
- Shoot **landscape**, lock the exposure and the white balance, and turn the
  phone's own microphone off. The narration is already recorded; camera audio
  only gets in the way.
- Two light sources at roughly 45 degrees, one from each side, plus something
  white above to kill the shadow your phone casts on the board. A desk lamp
  through a sheet of paper is enough.
- Clean the bench. Anything that is not part of the project should be out of
  frame. This matters more than the camera you use.
- Film every build stage **before** you fit the part, then fit it, then film the
  result. That gives you a natural before/after cut.

## Shot list

### 01 - The problem (0:01 - 0:27)

1. **Wide establishing shot.** The finished board, static, slow push-in or a
   slow left-to-right slide. Hold for the full slot. This is your title shot.
2. **Insert: the chip in your fingers.** Turn it so the pins catch the light.
   Cut to this when the narration says "thirty-two pins to spare".
3. **Optional:** a hand-written card reading `54 needed / 32 available / 22
   short`. Two seconds is plenty.

### 02 - The fix (0:27 - 0:55)

1. **Overhead, tight on the bus wires.** The eight jumper wires running from
   port 0 across the board. Trace along them slowly with a finger or a
   screwdriver tip so the viewer's eye follows.
2. **Insert: one latch chip**, then a slow tilt up to the four strobe wires
   leaving port 2.

### 03 - The parts (0:55 - 1:25)

1. **Flat-lay of everything.** All eighty parts laid out and roughly sorted on
   the bench, camera directly overhead, slow pan across the whole layout. Shoot
   this before you build anything.
2. **Three or four quick inserts** of individual parts picked up and put down:
   the sensor, the relay, the LCD, the crystal. One second each.

### 04 - Stage 1 to 2 - power and minimum system (1:25 - 2:00)

1. **Fit the power section.** Hands placing the jack, the regulator and the
   capacitors. Film from overhead with the camera just off your shoulder.
2. **The money shot:** multimeter probes on the regulator output, display
   showing 5.00 V. Hold it steady for four seconds. Cut to this on "reads five
   point zero".
3. **Fit the chip, the crystal and the reset circuit.** One continuous take is
   fine; it will cut down into three beats.

### 05 - Stage 3 to 5 - outputs, inputs, display (2:00 - 2:35)

1. **LED bank blinking.** Program 01 loaded. Overhead, and let it run - the
   movement is the shot.
2. **Switch insert.** A finger closes one DIP switch and the matching LED
   lights. Shoot this a few times; the first take usually has your hand in the
   wrong place.
3. **Display counting.** Program 04 running, camera close enough that the
   digits fill a third of the frame.

### 06 - Stage 6 to 7 - serial link and temperature (2:35 - 3:12)

1. **Fit the MAX232 and the connector**, then the cable running off frame
   toward the PC.
2. **Screen capture or a phone pointed at the terminal.** Type `LED FF`, then
   `RLY 1`. Film the screen, not the keyboard. If you can capture the screen
   directly, do - it is far sharper than filming it.
3. **LM35 insert**, then the converter going into its socket.
4. **Program 10 running**, display showing the temperature, with a real
   thermometer beside the board if you have one.

### 07 - Stage 8 to 9 - LCD, relay, buzzer (3:12 - 3:42)

1. **LCD close-up.** Program 11. Line one is the number, line two is the bar.
   Hold the sensor between your fingers and film the bar growing. Shoot this
   several times - it needs one clean take where the number climbs steadily.
2. **Relay insert.** Film it close enough to see the mechanism move, and make
   sure you actually capture the click. If your phone microphone is off, the
   click is lost, so consider recording this one take with audio on and dubbing
   the sound in later.
3. **Fit the buzzer.**

### 08 - Stage 10 - self test (3:42 - 4:03)

1. **Terminal capture, program 13.** Screen record it if you can. The lines
   appear quickly, so capture at a high frame rate or it will look like a jump
   cut. This is the shortest scene in the video, so one clean take is all you
   need.

### 09 - Running - the zone monitor (4:03 - 4:35)

1. **Overhead of the board running normally**, green zone LED lit.
2. **The heat sequence.** Warm the sensor and hold the shot while the zone LED
   walks green to yellow to red. Do not cut during this - the transition is the
   whole point of the scene.
3. **Split shot if you can:** board on one side, terminal showing the telemetry
   lines on the other. If not, cut between the two.

### 10 - Emergency stop and results (4:35 - 5:11)

1. **Press PB1.** One continuous take: relay drops out, LCD changes, red LED.
2. **Press PB2** and film the recovery in the same take.
3. **Results.** Either your measured readings on paper, a screenshot of your
   results table, or simply a final wide shot of the board working. End on the
   board, not on a slide.

## Re-cutting your footage under the existing narration

Export each clip already trimmed to the slot length, then lay them end to end
and mux against the narration. With ffmpeg:

```
# one clip per scene, in order, already trimmed to the slot lengths
ffmpeg -f concat -safe 0 -i clips.txt -i _narration.wav \
  -c:v libx264 -crf 20 -pix_fmt yuv420p -r 24 -s 1280x720 \
  -c:a aac -b:a 160k -shortest 8051_Assembly_and_Run_real.mp4
```

`clips.txt` is a plain list:

```
file '01_wide.mp4'
file '02_bus.mp4'
...
```

If you only want to replace a few scenes rather than the whole video, keep the
animated ones and drop your footage in for the rest - the slot lengths are
identical, so the narration stays in sync either way.

Keep the captions. The video is designed to be readable with the sound off, and
a viva panel will often play it muted.

## What to avoid

- Shooting under a single overhead light. Every part casts a shadow and the
  board reads as a dark mess.
- Handheld for the close-ups. At this scale, camera shake is very obvious.
- Filming the LCD straight on. It reflects everything; tilt the board about 15
  degrees instead.
- Long unbroken takes of you fitting jumper wires. Cut them down; nobody needs
  to watch the whole placement.
- Music. It fights the narration and dates the video.
