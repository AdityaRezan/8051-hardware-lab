import math
import random
import time
import tkinter as tk

SEG7_CODES = [0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F]

C = {
    "bg": "#0A111F",
    "panel": "#0F1A2E",
    "panel2": "#13223A",
    "card": "#0C1526",
    "line": "#22314D",
    "text": "#E6EDF7",
    "muted": "#8CA0BE",
    "cyan": "#22D3EE",
    "blue": "#4DA3FF",
    "green": "#2ECC71",
    "yellow": "#F4C20D",
    "red": "#FF4757",
    "seg_on": "#00F0FF",
    "seg_off": "#152C3C",
    "off": "#141F35",
}

ZONES = [
    {"name": "SAFE", "lo": 0, "hi": 40, "led": "GREEN", "color": "green", "duty": 30, "dac": 1.5, "buzzer": False},
    {"name": "WARNING", "lo": 40, "hi": 71, "led": "YELLOW", "color": "yellow", "duty": 60, "dac": 3.0, "buzzer": False},
    {"name": "DANGER", "lo": 70, "hi": 102, "led": "RED", "color": "red", "duty": 99, "dac": 5.0, "buzzer": True},
]


def zone_index(temp):
    if temp < 40:
        return 0
    if temp <= 70:
        return 1
    return 2


def poly_arc(cx, cy, r, a0, a1, steps=24):
    pts = []
    for k in range(steps + 1):
        a = math.radians(a0 + (a1 - a0) * k / steps)
        pts.extend([cx + r * math.cos(a), cy + r * math.sin(a)])
    return pts


class SevenSegmentDigit(tk.Canvas):
    def __init__(self, master):
        super().__init__(master, width=56, height=96, bg=C["card"], highlightthickness=0)
        t = 9

        def hseg(cx, cy, ln):
            return [(cx - ln, cy), (cx - ln + t // 2, cy - t // 2), (cx + ln - t // 2, cy - t // 2),
                    (cx + ln, cy), (cx + ln - t // 2, cy + t // 2), (cx - ln + t // 2, cy + t // 2)]

        def vseg(cx, cy, ln):
            return [(cx, cy - ln), (cx + t // 2, cy - ln + t // 2), (cx + t // 2, cy + ln - t // 2),
                    (cx, cy + ln), (cx - t // 2, cy + ln - t // 2), (cx - t // 2, cy - ln + t // 2)]

        self.segs = [
            self.create_polygon(hseg(28, 10, 15), fill=C["seg_off"], outline=""),
            self.create_polygon(vseg(46, 29, 16), fill=C["seg_off"], outline=""),
            self.create_polygon(vseg(46, 67, 16), fill=C["seg_off"], outline=""),
            self.create_polygon(hseg(28, 86, 15), fill=C["seg_off"], outline=""),
            self.create_polygon(vseg(10, 67, 16), fill=C["seg_off"], outline=""),
            self.create_polygon(vseg(10, 29, 16), fill=C["seg_off"], outline=""),
            self.create_polygon(hseg(28, 48, 15), fill=C["seg_off"], outline=""),
        ]

    def show(self, digit):
        code = SEG7_CODES[digit] if isinstance(digit, int) and 0 <= digit <= 9 else 0
        for i, sid in enumerate(self.segs):
            on = (code >> i) & 1
            self.itemconfig(sid, fill=C["seg_on"] if on else C["seg_off"])


class Led(tk.Canvas):
    def __init__(self, master, pin, name, color):
        super().__init__(master, width=100, height=58, bg=C["panel2"], highlightthickness=0)
        self.color = C[color]
        self.bulb = self.create_oval(38, 5, 62, 29, fill=C["off"], outline=C["line"], width=2)
        self.create_text(50, 38, text=pin, font=("Helvetica", 8, "bold"), fill=C["muted"])
        self.create_text(50, 49, text=name, font=("Helvetica", 8), fill=C["text"])

    def set(self, on):
        self.itemconfig(self.bulb, fill=self.color if on else C["off"],
                        outline=self.color if on else C["line"])


class BitRow(tk.Frame):
    def __init__(self, master, title):
        super().__init__(master, bg=C["panel2"])
        head = tk.Frame(self, bg=C["panel2"])
        head.pack(fill="x", padx=8, pady=(4, 0))
        tk.Label(head, text=title, bg=C["panel2"], fg=C["muted"],
                 font=("Helvetica", 7, "bold")).pack(side="left")
        self.value = tk.Label(head, text="", bg=C["panel2"], fg=C["cyan"],
                              font=("Courier", 9, "bold"))
        self.value.pack(side="right")
        row = tk.Frame(self, bg=C["panel2"])
        row.pack(padx=8, pady=(2, 6))
        self.cells = {}
        for i in range(7, -1, -1):
            box = tk.Frame(row, bg=C["panel2"])
            box.pack(side="left", padx=2)
            cv = tk.Canvas(box, width=18, height=18, bg=C["panel2"], highlightthickness=0)
            cv.pack()
            sq = cv.create_rectangle(1, 1, 17, 17, fill=C["off"], outline=C["line"])
            tk.Label(box, text="D%d" % i, bg=C["panel2"], fg=C["muted"],
                     font=("Helvetica", 6)).pack()
            self.cells[i] = (cv, sq)

    def set_byte(self, value):
        for i in range(8):
            cv, sq = self.cells[i]
            on = (value >> i) & 1
            cv.itemconfig(sq, fill=C["cyan"] if on else C["off"],
                          outline=C["cyan"] if on else C["line"])
        self.value.config(text="0x%02X   %3d   %s" % (value, value, format(value, "08b")))


class Gauge(tk.Canvas):
    def __init__(self, master, title, lo, hi, bands):
        super().__init__(master, width=178, height=150, bg=C["panel2"], highlightthickness=0)
        self.cx, self.cy, self.r = 89, 72, 58
        self.lo, self.hi = lo, hi
        for b0, b1, col in bands:
            a0 = 135 + 270 * (b0 - lo) / (hi - lo)
            a1 = 135 + 270 * (b1 - lo) / (hi - lo)
            self.create_line(*poly_arc(self.cx, self.cy, self.r, a0, a1),
                             fill=C[col], width=9, capstyle="round")
        for i in range(11):
            a = math.radians(135 + 27 * i)
            r1, r2 = self.r - 15, self.r - 9
            self.create_line(self.cx + r1 * math.cos(a), self.cy + r1 * math.sin(a),
                             self.cx + r2 * math.cos(a), self.cy + r2 * math.sin(a),
                             fill=C["line"], width=2)
        self.needle = self.create_line(self.cx, self.cy, self.cx, self.cy - (self.r - 18),
                                       fill="#F1F5F9", width=3, capstyle="round")
        self.create_oval(self.cx - 5, self.cy - 5, self.cx + 5, self.cy + 5,
                         fill="#0C1526", outline=C["line"])
        self.vtext = self.create_text(self.cx, self.cy + 30, text="--",
                                      font=("Helvetica", 15, "bold"), fill=C["text"])
        self.utext = self.create_text(self.cx, self.cy + 46, text="",
                                      font=("Helvetica", 8), fill=C["muted"])
        self.create_text(self.cx, 142, text=title, font=("Helvetica", 8, "bold"), fill=C["muted"])

    def set(self, value, vstr, ustr, color=None):
        frac = max(0.0, min(1.0, (value - self.lo) / (self.hi - self.lo)))
        a = math.radians(135 + 270 * frac)
        x = self.cx + (self.r - 18) * math.cos(a)
        y = self.cy + (self.r - 18) * math.sin(a)
        self.coords(self.needle, self.cx, self.cy, x, y)
        self.itemconfig(self.vtext, text=vstr, fill=color or C["text"])
        self.itemconfig(self.utext, text=ustr)


class MotorFan(tk.Canvas):
    def __init__(self, master, size=176):
        super().__init__(master, width=size, height=size, bg=C["panel2"], highlightthickness=0)
        self.size = size

    def draw(self, angle, duty):
        self.delete("all")
        cx = cy = self.size // 2
        spin = duty > 0
        fill = "#38BDF8" if spin else "#233450"
        outline = "#7DD3FC" if spin else "#31435F"
        for i in range(4):
            a0 = angle + i * 90
            pts = []
            for k in range(11):
                th = math.radians(a0 + 5 * k)
                pts.extend([cx + 62 * math.cos(th), cy + 62 * math.sin(th)])
            for k in range(10, -1, -1):
                th = math.radians(a0 + 5 * k)
                pts.extend([cx + 20 * math.cos(th), cy + 20 * math.sin(th)])
            self.create_polygon(pts, fill=fill, outline=outline)
        self.create_oval(cx - 68, cy - 68, cx + 68, cy + 68, outline=C["line"], width=2)
        self.create_oval(cx - 14, cy - 14, cx + 14, cy + 14, fill="#0C1526",
                         outline=C["cyan"], width=2)
        self.create_text(cx, cy, text="M", font=("Helvetica", 9, "bold"), fill=C["cyan"])


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Smart Industrial Automation & Monitoring System - 8051 + ARM Cortex-M")
        self.root.geometry("1380x880")
        self.root.configure(bg=C["bg"])
        self.temp = 32.0
        self.auto = True
        self.target = 75.0
        self.target_time = time.monotonic()
        self.emergency = False
        self.adc = 0
        self.last_adc = -1
        self.last_log_time = 0.0
        self.duty = 0
        self.dac_v = 0.0
        self.dac_byte = 0
        self.ccr = 0
        self.zone = 0
        self.packets = 0
        self.angle = 0.0
        self.start_time = time.monotonic()
        self.last_tx = 0.0
        self._build_ui()
        self.log("SYSTEM BOOT : 8051 AT89S52 MASTER NODE ONLINE", "sys")
        self.log("SYSTEM BOOT : ARM CORTEX-M STM32 SLAVE NODE ONLINE", "sys")
        self.log("UART LINK ESTABLISHED : 9600 BAUD (TH1=0xFD, MODE 1)", "sys")
        self.tick()
        self.root.after(33, self.animate)

    def _panel(self, parent, title, subtitle, accent):
        p = tk.Frame(parent, bg=C["panel"], highlightbackground=C["line"], highlightthickness=1)
        head = tk.Frame(p, bg=C["panel"])
        head.pack(fill="x", padx=10, pady=(8, 0))
        tk.Frame(head, bg=accent, width=4, height=30).pack(side="left", padx=(0, 8))
        box = tk.Frame(head, bg=C["panel"])
        box.pack(side="left")
        tk.Label(box, text=title, bg=C["panel"], fg=C["text"],
                 font=("Helvetica", 11, "bold"), anchor="w").pack(fill="x")
        tk.Label(box, text=subtitle, bg=C["panel"], fg=C["muted"],
                 font=("Helvetica", 7), anchor="w").pack(fill="x")
        return p

    def _build_ui(self):
        self.root.grid_columnconfigure(0, minsize=380, weight=1)
        self.root.grid_columnconfigure(1, minsize=330, weight=1)
        self.root.grid_columnconfigure(2, minsize=430, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self._build_header()
        self._build_left_panel()
        self._build_middle_panel()
        self._build_right_panel()
        self._build_monitor()
        self._build_status_bar()

    def _build_header(self):
        head = tk.Frame(self.root, bg=C["panel"], highlightbackground=C["line"], highlightthickness=1)
        head.grid(row=0, column=0, columnspan=3, sticky="ew", padx=6, pady=(6, 2))
        tk.Frame(head, bg=C["cyan"], width=6).pack(side="left", fill="y")
        box = tk.Frame(head, bg=C["panel"])
        box.pack(side="left", padx=14, pady=8)
        tk.Label(box, text="SMART INDUSTRIAL AUTOMATION & MONITORING SYSTEM",
                 bg=C["panel"], fg=C["text"], font=("Helvetica", 16, "bold")).pack(anchor="w")
        tk.Label(box, text="8051 AT89S52 MASTER  \u2192  UART 9600  \u2192  ARM CORTEX-M STM32 SLAVE   |   ATHARV 24BEL0082  \u2022  ADITYA 24BEL0087   |   MPC PROJECT",
                 bg=C["panel"], fg=C["muted"], font=("Helvetica", 8)).pack(anchor="w")
        badges = tk.Frame(head, bg=C["panel"])
        badges.pack(side="right", padx=12)
        for text, color in [("8051 AT89S52", "cyan"), ("ARM CORTEX-M", "red"), ("PYTHON GUI", "green")]:
            b = tk.Frame(badges, bg=C["panel"], highlightbackground=C[color], highlightthickness=1)
            b.pack(side="left", padx=4)
            tk.Label(b, text=text, bg=C["panel"], fg=C[color],
                     font=("Helvetica", 8, "bold"), padx=8, pady=4).pack()

    def _build_left_panel(self):
        p = self._panel(self.root, "8051 AT89S52 \u2014 MASTER NODE",
                        "LM35 \u2192 ADC0804 \u2192 TEMP CALC \u2192 7-SEG \u2192 LEDS \u2192 UART TX", "cyan")
        p.grid(row=1, column=0, sticky="nsew", padx=6, pady=6)

        lm = tk.Frame(p, bg=C["card"], highlightbackground=C["line"], highlightthickness=1)
        lm.pack(fill="x", padx=10, pady=(8, 4))
        tk.Label(lm, text="LM35 TEMPERATURE SENSOR", bg=C["card"], fg=C["muted"],
                 font=("Helvetica", 8, "bold")).pack(anchor="w", padx=10, pady=(6, 0))
        row = tk.Frame(lm, bg=C["card"])
        row.pack(fill="x", padx=10)
        self.temp_label = tk.Label(row, text="32.0 \u00b0C", bg=C["card"], fg=C["green"],
                                   font=("Helvetica", 24, "bold"))
        self.temp_label.pack(side="left")
        self.lm35_v = tk.Label(row, text="VOUT = 0.320 V (10 mV/\u00b0C)", bg=C["card"],
                               fg=C["muted"], font=("Helvetica", 8))
        self.lm35_v.pack(side="right", pady=(8, 0))
        self.slider = tk.Scale(lm, from_=0, to=102, resolution=0.1, orient="horizontal",
                               bg=C["card"], fg=C["text"], troughcolor="#0A101E",
                               highlightthickness=0, bd=0, activebackground=C["cyan"],
                               length=330, showvalue=False, command=self._on_slider)
        self.slider.set(self.temp)
        self.slider.pack(fill="x", padx=10, pady=(0, 2))
        mrow = tk.Frame(lm, bg=C["card"])
        mrow.pack(fill="x", padx=10, pady=(0, 8))
        self.btn_auto = tk.Button(mrow, text="AUTO SIM", font=("Helvetica", 8, "bold"),
                                  bg=C["cyan"], fg="#06202B", bd=0, padx=10, pady=3,
                                  cursor="hand2", command=lambda: self._set_mode(True))
        self.btn_auto.pack(side="left")
        self.btn_manual = tk.Button(mrow, text="MANUAL", font=("Helvetica", 8, "bold"),
                                    bg=C["panel2"], fg=C["muted"], bd=0, padx=10, pady=3,
                                    cursor="hand2", command=lambda: self._set_mode(False))
        self.btn_manual.pack(side="left", padx=6)

        ad = tk.Frame(p, bg=C["card"], highlightbackground=C["line"], highlightthickness=1)
        ad.pack(fill="x", padx=10, pady=4)
        self.adc_bits = BitRow(ad, "ADC0804 DATA BUS (P2.0-7)")
        self.adc_bits.pack(fill="x")
        self.adc_calc = tk.Label(ad, text="T = ADC \u00d7 2 / 5 = 32 \u00b0C", bg=C["card"],
                                 fg=C["cyan"], font=("Courier", 9, "bold"))
        self.adc_calc.pack(anchor="w", padx=10, pady=(0, 6))

        sg = tk.Frame(p, bg=C["card"], highlightbackground=C["line"], highlightthickness=1)
        sg.pack(fill="x", padx=10, pady=4)
        tk.Label(sg, text="2-DIGIT 7-SEGMENT DISPLAY (P0.0-7)", bg=C["card"], fg=C["muted"],
                 font=("Helvetica", 8, "bold")).pack(anchor="w", padx=10, pady=(6, 0))
        drow = tk.Frame(sg, bg=C["card"])
        drow.pack(pady=4)
        self.digit_tens = SevenSegmentDigit(drow)
        self.digit_tens.pack(side="left", padx=8)
        self.digit_units = SevenSegmentDigit(drow)
        self.digit_units.pack(side="left", padx=8)
        tk.Label(sg, text="SEG7 TABLE LOOKUP : 3F 06 5B 4F 66 6D 7D 07 7F 6F", bg=C["card"],
                 fg=C["muted"], font=("Courier", 7)).pack(pady=(0, 6))

        ld = tk.Frame(p, bg=C["card"], highlightbackground=C["line"], highlightthickness=1)
        ld.pack(fill="x", padx=10, pady=(4, 10))
        tk.Label(ld, text="ALERT ZONE LEDS (PORT 1)", bg=C["card"], fg=C["muted"],
                 font=("Helvetica", 8, "bold")).pack(anchor="w", padx=10, pady=(6, 0))
        r1 = tk.Frame(ld, bg=C["card"])
        r1.pack(pady=2)
        self.led_green = Led(r1, "P1.0", "SAFE", "green")
        self.led_green.pack(side="left", padx=4)
        self.led_yellow = Led(r1, "P1.1", "WARNING", "yellow")
        self.led_yellow.pack(side="left", padx=4)
        self.led_red = Led(r1, "P1.2", "DANGER", "red")
        self.led_red.pack(side="left", padx=4)
        r2 = tk.Frame(ld, bg=C["card"])
        r2.pack(pady=(2, 6))
        self.led_emg = Led(r2, "P1.7", "EMERGENCY", "red")
        self.led_emg.pack(side="left", padx=4)
        tk.Label(r2, text="CJNE / JC ZONE COMPARE\n40 C AND 70 C THRESHOLDS", bg=C["card"],
                 fg=C["muted"], font=("Helvetica", 7), justify="left").pack(side="left", padx=14)

    def _build_middle_panel(self):
        p = self._panel(self.root, "UART LINK \u2014 SYSTEM STATE",
                        "8051 P3.1 TX \u2192 ARM PA0 RX  |  ZONE ACTION TABLE", "yellow")
        p.grid(row=1, column=1, sticky="nsew", padx=6, pady=6)

        uw = tk.Frame(p, bg=C["card"], highlightbackground=C["line"], highlightthickness=1)
        uw.pack(fill="x", padx=10, pady=(8, 4))
        self.uart_canvas = tk.Canvas(uw, width=300, height=110, bg=C["card"], highlightthickness=0)
        self.uart_canvas.pack(pady=4)
        cv = self.uart_canvas
        cv.create_text(150, 12, text="UART 9600 BAUD (TH1=0xFD, MODE 1)", font=("Helvetica", 7),
                       fill=C["muted"])
        cv.create_rectangle(8, 36, 92, 76, outline=C["cyan"], width=2)
        cv.create_text(50, 47, text="8051", font=("Helvetica", 8, "bold"), fill=C["cyan"])
        cv.create_text(50, 61, text="P3.1 TX", font=("Helvetica", 7), fill=C["muted"])
        cv.create_rectangle(208, 36, 292, 76, outline=C["red"], width=2)
        cv.create_text(250, 47, text="ARM", font=("Helvetica", 8, "bold"), fill=C["red"])
        cv.create_text(250, 61, text="PA0 RX", font=("Helvetica", 7), fill=C["muted"])
        cv.create_line(92, 56, 208, 56, fill=C["line"], width=3)
        self.uart_dot = cv.create_oval(0, 51, 10, 61, fill=C["yellow"], outline="", state="hidden")
        self.uart_byte = cv.create_text(150, 40, text="", font=("Courier", 8, "bold"),
                                        fill=C["yellow"], state="hidden")
        self.uart_count = cv.create_text(150, 96, text="PACKETS : 0", font=("Helvetica", 8),
                                         fill=C["cyan"])

        zt = tk.Frame(p, bg=C["card"], highlightbackground=C["line"], highlightthickness=1)
        zt.pack(fill="x", padx=10, pady=4)
        tk.Label(zt, text="TEMPERATURE ZONES & SYSTEM ACTIONS", bg=C["card"], fg=C["muted"],
                 font=("Helvetica", 8, "bold")).pack(anchor="w", padx=8, pady=(6, 2))
        cols = ["ZONE", "TEMP", "LED", "MOTOR", "DAC", "BUZZER"]
        widths = [70, 55, 55, 50, 42, 48]
        header = tk.Frame(zt, bg=C["card"])
        header.pack(fill="x", padx=8)
        for col, w in zip(cols, widths):
            tk.Label(header, text=col, bg=C["card"], fg=C["muted"], width=w,
                     font=("Helvetica", 7, "bold"), anchor="w").pack(side="left")
        self.zone_rows = []
        rows = [
            ("SAFE", "< 40 \u00b0C", "GREEN", "30 %", "1.5 V", "OFF", "green"),
            ("WARNING", "40-70 \u00b0C", "YELLOW", "60 %", "3.0 V", "OFF", "yellow"),
            ("DANGER", "> 70 \u00b0C", "RED", "99 %", "5.0 V", "ON", "red"),
            ("EMERGENCY", "BUTTON", "OFF", "STOP", "0.0 V", "ON", "red"),
        ]
        tints = {"green": "#0E2B1D", "yellow": "#2B2307", "red": "#2B0E12"}
        for row in rows:
            fr = tk.Frame(zt, bg=C["card"])
            fr.pack(fill="x", padx=8, pady=1)
            labels = []
            for val, w in zip(row[:6], widths):
                lb = tk.Label(fr, text=val, bg=C["card"], fg=C["text"], width=w,
                              font=("Helvetica", 8), anchor="w")
                lb.pack(side="left")
                labels.append(lb)
            self.zone_rows.append({"frame": fr, "labels": labels, "tint": tints[row[6]]})

        st = tk.Frame(p, bg=C["card"], highlightbackground=C["line"], highlightthickness=1)
        st.pack(fill="x", padx=10, pady=4)
        self.state_label = tk.Label(st, text="SYSTEM RUNNING", bg=C["card"], fg=C["green"],
                                    font=("Helvetica", 14, "bold"))
        self.state_label.pack(pady=(8, 0))
        self.state_8051 = tk.Label(st, text="8051 : RUNNING MAIN LOOP", bg=C["card"],
                                   fg=C["muted"], font=("Courier", 8))
        self.state_8051.pack()
        self.state_arm = tk.Label(st, text="ARM : RUNNING CONTROL LOOP", bg=C["card"],
                                  fg=C["muted"], font=("Courier", 8))
        self.state_arm.pack()

        er = tk.Frame(p, bg=C["card"], highlightbackground=C["line"], highlightthickness=1)
        er.pack(fill="x", padx=10, pady=(4, 10))
        tk.Label(er, text="EMERGENCY PUSH BUTTON \u2014 INT0 (8051) / EXTI0 (ARM)",
                 bg=C["card"], fg=C["muted"], font=("Helvetica", 7, "bold")).pack(pady=(6, 2))
        self.btn_stop = tk.Button(er, text="EMERGENCY STOP", bg="#8B1120", fg="#FFFFFF",
                                  activebackground="#C2172E", font=("Helvetica", 13, "bold"),
                                  bd=0, pady=10, cursor="hand2",
                                  command=self.trigger_emergency)
        self.btn_stop.pack(fill="x", padx=12)
        self.btn_reset = tk.Button(er, text="RESET SYSTEM", bg="#0E3A5C", fg=C["cyan"],
                                   activebackground="#15537F", font=("Helvetica", 10, "bold"),
                                   bd=0, pady=6, cursor="hand2", state="disabled",
                                   command=self.reset_system)
        self.btn_reset.pack(fill="x", padx=12, pady=(6, 10))

    def _build_right_panel(self):
        p = self._panel(self.root, "ARM CORTEX-M STM32 \u2014 SLAVE NODE",
                        "UART RX \u2192 NVIC \u2192 TIM2 PWM \u2192 DAC0808 \u2192 ACTUATORS", "red")
        p.grid(row=1, column=2, sticky="nsew", padx=6, pady=6)

        rx = tk.Frame(p, bg=C["card"], highlightbackground=C["line"], highlightthickness=1)
        rx.pack(fill="x", padx=10, pady=(8, 4))
        tk.Label(rx, text="USART1 RX (PA0)", bg=C["card"], fg=C["muted"],
                 font=("Helvetica", 8, "bold")).pack(side="left", padx=10, pady=8)
        self.rx_label = tk.Label(rx, text="0x00   T = 0 \u00b0C", bg=C["card"], fg=C["cyan"],
                                 font=("Courier", 11, "bold"))
        self.rx_label.pack(side="right", padx=10)

        gr = tk.Frame(p, bg=C["panel"])
        gr.pack(fill="x", padx=10, pady=4)
        g1 = tk.Frame(gr, bg=C["card"], highlightbackground=C["line"], highlightthickness=1)
        g1.pack(side="left", fill="both", expand=True)
        self.pwm_gauge = Gauge(g1, "TIM2 CH1 PWM DUTY (PA1)", 0, 100,
                               [(0, 40, "green"), (40, 75, "yellow"), (75, 100, "red")])
        self.pwm_gauge.pack()
        self.ccr_label = tk.Label(g1, text="CCR = 0 / ARR 999", bg=C["card"], fg=C["muted"],
                                  font=("Courier", 8))
        self.ccr_label.pack(pady=(0, 6))
        g2 = tk.Frame(gr, bg=C["card"], highlightbackground=C["line"], highlightthickness=1)
        g2.pack(side="left", fill="both", expand=True)
        self.dac_gauge = Gauge(g2, "DAC0808 OUTPUT (PB0-7)", 0, 5,
                               [(0, 2, "green"), (2, 4, "yellow"), (4, 5, "red")])
        self.dac_gauge.pack()
        self.dac_label = tk.Label(g2, text="ANALOG VOLTAGE OUT", bg=C["card"], fg=C["muted"],
                                  font=("Courier", 8))
        self.dac_label.pack(pady=(0, 6))

        ac = tk.Frame(p, bg=C["card"], highlightbackground=C["line"], highlightthickness=1)
        ac.pack(fill="x", padx=10, pady=4)
        lcol = tk.Frame(ac, bg=C["card"])
        lcol.pack(side="left", padx=(10, 0), pady=6)
        self.fan = MotorFan(lcol, size=170)
        self.fan.pack()
        self.motor_label = tk.Label(lcol, text="SPEED : 0 %", bg=C["card"], fg=C["cyan"],
                                    font=("Helvetica", 10, "bold"))
        self.motor_label.pack()
        tk.Label(lcol, text="TIM2 PWM \u2192 L293D \u2192 12V DC MOTOR", bg=C["card"],
                 fg=C["muted"], font=("Helvetica", 7)).pack(pady=(0, 6))
        rcol = tk.Frame(ac, bg=C["card"])
        rcol.pack(side="left", expand=True, pady=6)
        self.dac_bits = BitRow(rcol, "DAC0808 DATA BUS (PB0-7)")
        self.dac_bits.pack(fill="x", padx=8)
        ledrow = tk.Frame(rcol, bg=C["card"])
        ledrow.pack(pady=6)
        self.led_buzz = Led(ledrow, "PA2", "BUZZER", "red")
        self.led_buzz.pack(side="left")
        self.led_shutdown = Led(ledrow, "PA3", "SHUTDOWN", "red")
        self.led_shutdown.pack(side="left")
        ledrow2 = tk.Frame(rcol, bg=C["card"])
        ledrow2.pack(pady=(0, 6))
        self.led_pc0 = Led(ledrow2, "PC0", "NVIC STOP", "red")
        self.led_pc0.pack(side="left")
        self.led_beat = Led(ledrow2, "PC13", "HEARTBEAT", "cyan")
        self.led_beat.pack(side="left")

    def _build_monitor(self):
        p = tk.Frame(self.root, bg=C["panel"], highlightbackground=C["line"], highlightthickness=1)
        p.grid(row=2, column=0, columnspan=3, sticky="ew", padx=6, pady=2)
        tk.Label(p, text="SERIAL MONITOR \u2014 USB-UART", bg=C["panel"], fg=C["muted"],
                 font=("Helvetica", 8, "bold")).pack(anchor="w", padx=10, pady=(5, 0))
        self.monitor = tk.Text(p, bg="#0A101E", fg=C["muted"], font=("Courier", 9), height=8,
                               state="disabled", bd=0, insertbackground=C["cyan"],
                               selectbackground=C["cyan"])
        self.monitor.pack(fill="x", padx=10, pady=(2, 8), expand=True)
        self.monitor.tag_configure("tx", foreground=C["cyan"])
        self.monitor.tag_configure("rx", foreground=C["green"])
        self.monitor.tag_configure("sys", foreground=C["muted"])
        self.monitor.tag_configure("warn", foreground=C["yellow"])
        self.monitor.tag_configure("err", foreground=C["red"])

    def _build_status_bar(self):
        bar = tk.Frame(self.root, bg=C["panel"], highlightbackground=C["line"], highlightthickness=1)
        bar.grid(row=3, column=0, columnspan=3, sticky="ew", padx=6, pady=(2, 6))
        self.status_state = tk.Label(bar, text="RUNNING", bg=C["panel"], fg=C["green"],
                                     font=("Helvetica", 9, "bold"))
        self.status_state.pack(side="left", padx=12, pady=4)
        self.status_info = tk.Label(bar, text="", bg=C["panel"], fg=C["muted"],
                                    font=("Courier", 9))
        self.status_info.pack(side="left")
        self.status_uptime = tk.Label(bar, text="UPTIME 00:00", bg=C["panel"], fg=C["muted"],
                                      font=("Courier", 9))
        self.status_uptime.pack(side="right", padx=12)

    def _set_mode(self, auto):
        self.auto = auto
        if auto:
            self.btn_auto.config(bg=C["cyan"], fg="#06202B")
            self.btn_manual.config(bg=C["panel2"], fg=C["muted"])
            self.log("SIMULATION MODE : AUTO TEMPERATURE SWEEP", "sys")
        else:
            self.btn_auto.config(bg=C["panel2"], fg=C["muted"])
            self.btn_manual.config(bg=C["cyan"], fg="#06202B")
            self.log("SIMULATION MODE : MANUAL (LM35 SLIDER)", "sys")

    def _on_slider(self, value):
        if not self.auto:
            self.temp = float(value)

    def log(self, message, tag):
        stamp = time.strftime("%H:%M:%S")
        self.monitor.config(state="normal")
        self.monitor.insert("end", "[%s] %s\n" % (stamp, message), tag)
        total = int(self.monitor.index("end-1c").split(".")[0])
        if total > 200:
            self.monitor.delete("1.0", "%d.0" % (total - 200))
        self.monitor.see("end")
        self.monitor.config(state="disabled")

    def _highlight_zone_row(self, index):
        for i, row in enumerate(self.zone_rows):
            active = i == index
            bg = row["tint"] if active else C["card"]
            row["frame"].config(bg=bg)
            for lb in row["labels"]:
                lb.config(bg=bg)

    def trigger_emergency(self):
        if self.emergency:
            return
        self.emergency = True
        self.duty = 0
        self.dac_v = 0.0
        self.dac_byte = 0
        self.ccr = 0
        self.packets += 1
        self.last_tx = time.monotonic()
        self.digit_tens.show(None)
        self.digit_units.show(None)
        self.led_green.set(False)
        self.led_yellow.set(False)
        self.led_red.set(False)
        self.led_emg.set(True)
        self.led_shutdown.set(True)
        self.led_pc0.set(True)
        self.adc_bits.set_byte(0)
        self.dac_bits.set_byte(0)
        self.pwm_gauge.set(0, "0", "DUTY 0 %", C["red"])
        self.dac_gauge.set(0, "0.0", "0.0 V OUT", C["red"])
        self.ccr_label.config(text="CCR = 0 / ARR 999  [STOPPED]")
        self.motor_label.config(text="SPEED : 0 %  (BRAKE)", fg=C["red"])
        self.rx_label.config(text="0xFF   EMERGENCY FRAME")
        self.uart_canvas.itemconfig(self.uart_byte, text="0xFF")
        self._highlight_zone_row(3)
        self.state_label.config(text="EMERGENCY SHUTDOWN", fg=C["red"])
        self.state_8051.config(text="8051 : HALTED IN EMERGISR", fg=C["red"])
        self.state_arm.config(text="ARM : NVIC ISR ACTIVE", fg=C["red"])
        self.btn_stop.config(state="disabled", bg="#3A0A14")
        self.btn_reset.config(state="normal")
        self.status_state.config(text="EMERGENCY", fg=C["red"])
        self.log("!! EMERGENCY BUTTON : INT0 (8051) + EXTI0 (ARM) TRIGGERED", "err")
        self.log("NVIC ISR : MOTOR STOP | BUZZER ON | ALL OUTPUTS CLEARED", "err")
        self.log("8051 TX P3.1 -> 0xFF (SHUTDOWN FRAME)", "tx")
        self.log("ARM RX PA0 <- 0xFF : EMERGENCY SHUTDOWN ACKNOWLEDGED", "rx")

    def reset_system(self):
        if not self.emergency:
            return
        self.emergency = False
        self.last_adc = -1
        self.led_emg.set(False)
        self.led_shutdown.set(False)
        self.led_pc0.set(False)
        self.motor_label.config(fg=C["cyan"])
        self.state_8051.config(text="8051 : RUNNING MAIN LOOP", fg=C["muted"])
        self.state_arm.config(text="ARM : RUNNING CONTROL LOOP", fg=C["muted"])
        self.btn_stop.config(state="normal", bg="#8B1120")
        self.btn_reset.config(state="disabled")
        self.status_state.config(text="RUNNING", fg=C["green"])
        self.log("SYSTEM RESET : RESTARTING NORMAL OPERATION", "sys")

    def tick(self):
        if not self.emergency:
            now = time.monotonic()
            if self.auto:
                if now - self.target_time > 6 or abs(self.target - self.temp) < 0.5:
                    self.target = random.uniform(22, 98)
                    self.target_time = now
                step = max(-1.1, min(1.1, self.target - self.temp))
                self.temp = max(0.0, min(102.0, self.temp + step + random.uniform(-0.15, 0.15)))
                self.slider.set(self.temp)
            self.adc = max(0, min(255, int(round(self.temp * 2.5))))
            t8051 = (self.adc * 2) // 5
            self.zone = zone_index(t8051)
            z = ZONES[self.zone]
            self.duty = z["duty"]
            self.dac_v = z["dac"]
            self.dac_byte = int(round(self.dac_v * 255 / 5.0))
            self.ccr = int(round(self.duty * 999 / 100.0))
            self.packets += 1
            self.last_tx = now
            zcolor = C[z["color"]]
            self.temp_label.config(text="%.1f \u00b0C" % self.temp, fg=zcolor)
            self.lm35_v.config(text="VOUT = %.3f V (10 mV/\u00b0C)" % (self.temp / 100.0))
            self.adc_bits.set_byte(self.adc)
            self.adc_calc.config(text="T = ADC \u00d7 2 / 5 = %d \u00b0C" % t8051)
            shown = min(t8051, 99)
            self.digit_tens.show(shown // 10)
            self.digit_units.show(shown % 10)
            self.led_green.set(self.zone == 0)
            self.led_yellow.set(self.zone == 1)
            self.led_red.set(self.zone == 2)
            self._highlight_zone_row(self.zone)
            self.rx_label.config(text="0x%02X   T = %d \u00b0C" % (self.adc, t8051))
            self.pwm_gauge.set(self.duty, "%d" % self.duty, "DUTY %d %%" % self.duty, zcolor)
            self.ccr_label.config(text="CCR = %d / ARR 999" % self.ccr)
            self.motor_label.config(text="SPEED : %d %%" % self.duty)
            self.dac_gauge.set(self.dac_v, "%.1f" % self.dac_v, "%.1f V OUT" % self.dac_v, zcolor)
            self.dac_bits.set_byte(self.dac_byte)
            self.uart_canvas.itemconfig(self.uart_count, text="PACKETS : %d" % self.packets)
            if self.adc != self.last_adc and now - self.last_log_time > 0.4:
                self.last_adc = self.adc
                self.last_log_time = now
                self.log("8051 TX P3.1 -> 0x%02X  T=%d C  ZONE=%s" % (self.adc, t8051, z["name"]), "tx")
                self.log("ARM RX PA0 <- 0x%02X  PWM=%d%% CCR=%d  DAC=%.1fV" %
                         (self.adc, self.duty, self.ccr, self.dac_v), "rx")
            self.status_info.config(text="TEMP %.1f C  |  ZONE %-7s  |  PWM %d %%  |  DAC %.1f V  |  TX %d"
                                    % (self.temp, z["name"], self.duty, self.dac_v, self.packets))
        self.root.after(200, self.tick)

    def animate(self):
        now = time.monotonic()
        if not self.emergency and self.duty > 0:
            self.angle = (self.angle + 0.15 * self.duty + 1.0) % 360
        self.fan.draw(self.angle, 0 if self.emergency else self.duty)
        buzzer_on = (not self.emergency and ZONES[self.zone]["buzzer"]) or self.emergency
        fast = int(now * 5) % 2 == 0
        slow = int(now * 2) % 2 == 0
        self.led_buzz.set(buzzer_on and fast)
        self.led_beat.set(slow)
        if self.emergency:
            self.state_label.config(fg=C["red"] if fast else "#7A0E1A")
        elif self.zone == 2:
            self.state_label.config(text="SYSTEM RUNNING", fg=C["red"] if fast else "#7A2B33")
        else:
            self.state_label.config(text="SYSTEM RUNNING", fg=C["green"])
        elapsed = int(now - self.start_time)
        self.status_uptime.config(text="UPTIME %02d:%02d" % (elapsed // 60, elapsed % 60))
        age = now - self.last_tx
        if age < 0.45 and not self.emergency:
            prog = age / 0.45
            x = 96 + prog * 100
            self.uart_canvas.coords(self.uart_dot, x - 5, 51, x + 5, 61)
            self.uart_canvas.itemconfig(self.uart_dot, state="normal", fill=C["yellow"])
            self.uart_canvas.itemconfig(self.uart_byte, text="0x%02X" % self.adc, state="normal")
        elif self.emergency and age < 1.2:
            prog = min(1.0, age / 0.6)
            x = 96 + prog * 100
            self.uart_canvas.coords(self.uart_dot, x - 5, 51, x + 5, 61)
            self.uart_canvas.itemconfig(self.uart_dot, state="normal", fill=C["red"])
        else:
            self.uart_canvas.itemconfig(self.uart_dot, state="hidden")
            self.uart_canvas.itemconfig(self.uart_byte, state="hidden")
        self.root.after(33, self.animate)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    App().run()
