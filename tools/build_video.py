#!/usr/bin/env python3
"""Render docs/guide/video/8051_Assembly_and_Run.mp4 from the scene script.

Frames are generated with Pillow and piped straight into ffmpeg, so nothing
large is ever written to disk. Scene lengths come from the recorded narration.
"""

import math
import os
import re
import subprocess
import sys
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from video_script import (RESULT_CARDS, END_LINES, PROBLEM_ROWS,
                          TITLE_MAIN, TITLE_SUB)

SCRIPT_NAME = "video_script"
if "--script" in sys.argv:
    SCRIPT_NAME = "video_script_" + sys.argv[sys.argv.index("--script") + 1]
SCRIPT_MOD = __import__(SCRIPT_NAME)
SCENES = SCRIPT_MOD.SCENES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VDIR = os.path.join(ROOT, "docs", "guide", "video")
IMAGES = os.path.join(ROOT, "docs", "guide", "images")
FRAMES = os.path.join(VDIR, "frames")
# each scene script keeps its own narration clips so the two videos
# never overwrite one another
AUDIO = os.path.join(VDIR, "audio" if SCRIPT_NAME == "video_script"
                     else "audio_" + SCRIPT_NAME.replace("video_script_", ""))
OUT = os.path.join(VDIR, getattr(SCRIPT_MOD, "OUT", "output.mp4"))

W, H = 1280, 720
FPS = 24
CAP_H = 134
PRE = 0.55           # silence before each scene's narration
POST = 0.75          # silence after
LEAD = 1.00          # silence before the first scene
TAIL = 1.60          # silence at the very end

BG = (11, 18, 32)
PANEL = (17, 28, 46)
SURF = (30, 41, 59)
BORDER = (36, 53, 77)
BLUE = (37, 99, 235)
BLUE_LT = (96, 165, 250)
EMER = (16, 185, 129)
EMER_LT = (52, 211, 153)
AMBER = (245, 158, 11)
RED = (239, 68, 68)
TEXT = (241, 245, 249)
MUTED = (148, 163, 184)
DIM = (100, 116, 139)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def fp(name, fallback=None):
    p = os.path.join(FONT_DIR, name)
    if os.path.exists(p):
        return p
    return os.path.join(FONT_DIR, fallback or "DejaVuSans.ttf")


F_REG = fp("DejaVuSans.ttf")
F_BOLD = fp("DejaVuSans-Bold.ttf")
F_MONO = fp("DejaVuSansMono.ttf")
F_MBOLD = fp("DejaVuSansMono-Bold.ttf", "DejaVuSansMono.ttf")

_fc = {}


def font(path, size):
    k = (path, size)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(path, size)
    return _fc[k]


# ------------------------------------------------------------------ helpers

def ease(u):
    return u * u * (3.0 - 2.0 * u)


def lerp(a, b, u):
    return a + (b - a) * u


def clamp(v, lo, hi):
    return lo if v < lo else (hi if v > hi else v)


def blend(c1, c2, u):
    return tuple(int(lerp(c1[i], c2[i], u)) for i in range(3))


def tracked(d, xy, text, fnt, fill, tracking=0, anchor="la"):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=fnt, fill=fill, anchor=anchor)
        x += d.textlength(ch, font=fnt) + tracking
    return x


def tracked_w(d, text, fnt, tracking=0):
    return sum(d.textlength(c, font=fnt) + tracking for c in text)


def wrap(d, text, fnt, maxw):
    words = text.split()
    lines, cur = [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=fnt) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def rrect(d, box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


# ------------------------------------------------------------------ images

_imgs = {}


def load_img(name):
    if name in _imgs:
        return _imgs[name]
    src = name if os.path.isabs(name) else os.path.join(
        IMAGES, name) if os.path.exists(os.path.join(IMAGES, name)) \
        else os.path.join(FRAMES, name)
    im = Image.open(src).convert("RGB")
    # pre-resize so it comfortably covers 1600x900
    s = max(1600.0 / im.width, 900.0 / im.height)
    im = im.resize((int(round(im.width * s)), int(round(im.height * s))),
                   Image.LANCZOS)
    _imgs[name] = im
    return im


def kenburns(name, u, zoom, pan):
    im = load_img(name)
    bw, bh = im.size
    z = lerp(zoom[0], zoom[1], ease(u))
    cx = lerp(pan[0][0], pan[1][0], ease(u))
    cy = lerp(pan[0][1], pan[1][1], ease(u))
    cw, ch = W / z, H / z
    x0 = clamp(cx * bw - cw / 2.0, 0, max(0, bw - cw))
    y0 = clamp(cy * bh - ch / 2.0, 0, max(0, bh - ch))
    return im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))) \
             .resize((W, H), Image.BICUBIC)


_cellcache = {}


def cell_img(name, cw, ch):
    k = (name, cw, ch)
    if k in _cellcache:
        return _cellcache[k]
    im = Image.open(os.path.join(IMAGES, name)).convert("RGB")
    s = min(cw / im.width, ch / im.height)
    im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))),
                   Image.LANCZOS)
    _cellcache[k] = im
    return im


# ------------------------------------------------------------------ callouts

def draw_callout(img, c, u, alpha):
    if u < c["t"]:
        return
    a = clamp((u - c["t"]) / 0.10, 0, 1) * alpha
    if a <= 0.01:
        return
    d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    fnt = font(F_BOLD, 17)
    tw = tracked_w(d, c["text"], fnt, 1.6)
    bw = tw + 30
    bh = 36
    cx = c["x"] * W
    cy = c["y"] * H
    up = c.get("dir", "up") == "up"
    bx = clamp(cx - bw / 2.0, 16, W - bw - 16)
    by = (cy - 52 - bh) if up else (cy + 52)
    if by < 60:
        by = cy + 52
    if by + bh > H - CAP_H - 16:
        by = cy - 52 - bh

    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    col = BLUE_LT
    rrect(ld, (bx, by, bx + bw, by + bh), 6,
          fill=col + (int(232 * a),), outline=None)
    rrect(ld, (bx, by, bx + 4, by + bh), 6, fill=EMER + (int(255 * a),))
    tracked(ld, (bx + 17, by + bh / 2), c["text"], fnt,
            (11, 18, 32, int(255 * a)), 1.6, anchor="lm")
    # leader line
    lx = clamp(cx, bx + 10, bx + bw - 10)
    ly = by + bh + 4 if up else by - 4
    ty = cy + (16 if up else -16)
    ld.line([(lx, ly), (lx, ty)], fill=col + (int(200 * a),), width=2)
    ld.ellipse([lx - 4, ty - 4, lx + 4, ty + 4], fill=col + (int(255 * a),))
    img.paste(lay, (0, 0), lay)


# ------------------------------------------------------------------ panels

def panel_title(d, f):
    d.rectangle((0, 0, W, H), fill=BG)
    fnt = font(F_BOLD, 72)
    sub = font(F_REG, 27)
    y = H / 2 - 90
    tw = tracked_w(d, TITLE_MAIN, fnt, 3)
    tracked(d, ((W - tw) / 2, y), TITLE_MAIN, fnt, TEXT, 3)
    d.rectangle(((W - 300) / 2, y + 96, (W + 300) / 2, y + 100), fill=BLUE)
    tw2 = d.textlength(TITLE_SUB, font=sub)
    d.text(((W - tw2) / 2, y + 124), TITLE_SUB, font=sub, fill=MUTED)


def panel_problem(d, f):
    d.rectangle((0, 0, W, H - CAP_H), fill=BG)
    head = font(F_BOLD, 34)
    d.text((150, 66), "FIFTY-FOUR Wires, THIRTY-TWO PINS",
           font=head, fill=TEXT)
    d.rectangle((150, 116, 320, 120), fill=EMER)
    top, bot = 160, H - CAP_H - 40
    n = len(PROBLEM_ROWS)
    rh = (bot - top) / n
    for i, (lab, val) in enumerate(PROBLEM_ROWS):
        y = top + i * rh
        a = clamp((f - i * 0.07) / 0.14, 0, 1)
        if a <= 0:
            continue
        big = i >= 3
        if big:
            rrect(d, (150, y + 4, W - 150, y + rh - 6), 6,
                  fill=blend(BG, SURF, 0.85 * a))
            d.rectangle((150, y + 4, 155, y + rh - 6),
                        fill=blend(BG, EMER if i == 3 else (
                            BLUE if i == 4 else RED), a))
        lf = font(F_BOLD if big else F_REG, 26 if big else 22)
        d.text((176, y + rh / 2), lab, font=lf,
               fill=blend(BG, TEXT if big else MUTED, a), anchor="lm")
        vf = font(F_BOLD, 40 if big else 24)
        t = val
        d.text((W - 176, y + rh / 2), t, font=vf,
               fill=blend(BG, EMER_LT if i == 3 else (
                   BLUE_LT if i == 4 else (RED if i == 5 else MUTED)), a),
               anchor="rm")


def panel_terminal(d, beat, f):
    d.rectangle((0, 0, W, H - CAP_H), fill=BG)
    x0, y0, x1, y1 = 150, 90, W - 150, H - CAP_H - 46
    rrect(d, (x0, y0, x1, y1), 10, fill=(9, 14, 26), outline=BORDER, width=2)
    rrect(d, (x0, y0, x1, y0 + 44), 10, fill=SURF)
    d.rectangle((x0, y0 + 34, x1, y0 + 44), fill=SURF)
    tf = font(F_BOLD, 17)
    tracked(d, (x0 + 20, y0 + 22), beat.get("title", "TERMINAL"), tf, MUTED,
            1.2, anchor="lm")
    for i in range(3):
        cx = x1 - 26 - i * 20
        d.ellipse((cx - 5, y0 + 22 - 5, cx + 5, y0 + 22 + 5),
                  fill=[RED, AMBER, EMER][i])

    lines = beat["lines"]
    mf = font(F_MONO, 23)
    lh = 36
    top = y0 + 62
    n = len(lines)
    per = 0.72 / max(1, n)
    for i, ln in enumerate(lines):
        st = 0.10 + i * per
        a = clamp((f - st) / 0.10, 0, 1)
        if a <= 0:
            continue
        col = MUTED
        if ln.startswith(">"):
            col = BLUE_LT
        elif "OK" in ln or "PASS" in ln:
            col = EMER_LT
        elif "DANGER" in ln:
            col = RED
        elif "WARNING" in ln:
            col = AMBER
        else:
            col = (203, 213, 225)
        d.text((x0 + 22, top + i * lh), ln, font=mf,
               fill=blend((9, 14, 26), col, a), anchor="lm")
        if i == n - 1 or (f - st) < 0.55:
            cw = d.textlength(ln, font=mf)
            if int(f * 3) % 2 == 0:
                d.rectangle((x0 + 26 + cw, top + i * lh - 11,
                             x0 + 32 + cw, top + i * lh + 11), fill=EMER_LT)


ZONE_COL = {"safe": EMER, "warn": AMBER, "danger": RED}
ZONE_GLOW = {"safe": (14, 60, 46), "warn": (66, 46, 8), "danger": (74, 20, 20)}


def panel_lcd(img, beat, f):
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, H - CAP_H), fill=BG)
    z = beat.get("zone", "safe")
    col = ZONE_COL[z]
    lw, lh = 860, 300
    x0, y0 = (W - lw) / 2, (H - CAP_H - lh) / 2 - 10
    rrect(d, (x0 - 26, y0 - 26, x0 + lw + 26, y0 + lh + 74), 14,
          fill=(24, 33, 48), outline=BLUE, width=3)
    glow = Image.new("RGB", (lw, lh), ZONE_GLOW[z])
    gl = Image.new("L", (lw, lh), 0)
    ImageDraw.Draw(gl).ellipse((-lw * .3, -lh * .5, lw * 1.3, lh * 1.5),
                               fill=120)
    img.paste(glow, (int(x0), int(y0)),
             Image.fromarray((np.array(gl) * 0.85).astype(np.uint8)))
    d.rectangle((x0, y0, x0 + lw, y0 + lh), outline=(10, 20, 18), width=2)
    mf = font(F_MBOLD, 62)
    cw = lw / 16.0
    for r, row in enumerate(beat["rows"]):
        for c, chx in enumerate(row[:16]):
            cx = x0 + cw * c + cw / 2
            cy = y0 + 78 + r * 128
            if chx != " ":
                d.text((cx, cy), chx, font=mf, fill=(226, 247, 236),
                       anchor="mm")
    lab = {"safe": "SAFE ZONE", "warn": "WARNING ZONE", "danger": "DANGER ZONE"}[z]
    lf = font(F_BOLD, 26)
    tw = tracked_w(d, lab, lf, 2)
    tracked(d, ((W - tw) / 2, y0 + lh + 26), lab, lf, col, 2)


def panel_results(d, f):
    d.rectangle((0, 0, W, H - CAP_H), fill=BG)
    head = font(F_BOLD, 32)
    d.text((110, 62), "MEASURED RESULTS", font=head, fill=TEXT)
    d.rectangle((110, 110, 280, 114), fill=BLUE)
    cols, rows = 3, 2
    gx0, gy0, gx1, gy1 = 110, 150, W - 110, H - CAP_H - 40
    cw = (gx1 - gx0) / cols
    chh = (gy1 - gy0) / rows
    for i, (val, lab) in enumerate(RESULT_CARDS):
        c, r = i % cols, i // cols
        a = clamp((f - i * 0.06) / 0.16, 0, 1)
        if a <= 0:
            continue
        bx = gx0 + c * cw + 10
        by = gy0 + r * chh + 10
        rrect(d, (bx, by, bx + cw - 20, by + chh - 20), 10,
              fill=blend(BG, SURF, 0.9 * a))
        d.rectangle((bx, by, bx + 5, by + chh - 20), fill=blend(BG, BLUE, a))
        vf = font(F_BOLD, 46)
        d.text((bx + 26, by + 44), val, font=vf,
               fill=blend(BG, BLUE_LT, a), anchor="lm")
        lf = font(F_BOLD, 15)
        tracked(d, (bx + 26, by + 100), lab, lf, blend(BG, MUTED, a), 1.6,
                anchor="lm")


def panel_end(d, f):
    d.rectangle((0, 0, W, H - CAP_H), fill=BG)
    y = (H - CAP_H) / 2 - 80
    f1 = font(F_BOLD, 58)
    tw = tracked_w(d, END_LINES[0], f1, 3)
    tracked(d, ((W - tw) / 2, y), END_LINES[0], f1, TEXT, 3)
    d.rectangle(((W - 340) / 2, y + 84, (W + 340) / 2, y + 88), fill=BLUE)
    f2 = font(F_REG, 27)
    for i, ln in enumerate(END_LINES[1:]):
        tw = d.textlength(ln, font=f2)
        a = clamp((f - 0.25 - i * 0.15) / 0.3, 0, 1)
        d.text(((W - tw) / 2, y + 118 + i * 44), ln, font=f2,
               fill=blend(BG, MUTED, a))
    d.rectangle(((W - 340) / 2, y + 232, (W + 340) / 2, y + 236), fill=EMER)


def render_grid(img, beat, f):
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, H), fill=BG)
    ims = beat["images"]
    cols, rows = beat.get("cols", 4), beat.get("rows", 3)
    st = beat.get("stagger", 0.05)
    if rows == 1:
        gx0, gy0, gx1, gy1 = 90, 120, W - 90, H - CAP_H - 60
    else:
        gx0, gy0, gx1, gy1 = 70, 74, W - 70, H - CAP_H - 40
    cw = (gx1 - gx0) / cols
    chh = (gy1 - gy0) / rows
    for i, nm in enumerate(ims):
        a = clamp((f - i * st) / 0.16, 0, 1)
        if a <= 0:
            continue
        c, r = i % cols, i // cols
        bx = gx0 + c * cw
        by = gy0 + r * chh
        iw, ih = int(cw - 26), int(chh - 26)
        cell = cell_img(nm, iw, ih)
        ox = bx + (cw - cell.width) / 2
        oy = by + (chh - cell.height) / 2
        d.rectangle((ox - 7, oy - 7, ox + cell.width + 7, oy + cell.height + 7),
                    fill=blend(BG, BORDER, a))
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        lay.paste(cell.convert("RGBA"), (int(ox), int(oy)))
        lay.putalpha(Image.fromarray(
            (np.array(lay.getchannel("A")) * a).astype(np.uint8)))
        img.paste(lay, (0, 0), lay)



# ------------------------------------------------- syntax highlighting
C_KW = (86, 156, 214)
C_TYPE = (78, 201, 176)
C_PP = (198, 146, 234)
C_NUM = (181, 206, 168)
C_STR = (206, 145, 120)
C_DEF = (212, 212, 212)
C_CMT = (106, 153, 85)
C_LN = (92, 92, 98)

KEYWORDS = set("if else return while for do switch case break continue "
               "volatile static const struct sizeof goto".split())
TYPES = set("void unsigned char int long bit sfr sbit code data idata "
            "xdata interrupt using".split())
TOKEN = re.compile(r'"[^"]*"|0[xX][0-9A-Fa-f]+[UL]*|\b\d+\b|[A-Za-z_]\w*')


def hl_runs(line):
    """Split one C line into (text, colour) runs."""
    runs = []
    pos = 0
    m = re.match(r"^(\s*#\s*\w+)", line)
    if m:
        runs.append((m.group(1), C_PP))
        pos = m.end()
    ci = line.find("//", pos)
    body, cmt = (line[pos:ci], line[ci:]) if ci >= 0 else (line[pos:], "")
    cur = 0
    for m in TOKEN.finditer(body):
        if m.start() > cur:
            runs.append((body[cur:m.start()], C_DEF))
        t = m.group(0)
        if t.startswith('"'):
            col = C_STR
        elif t[:2].lower() == "0x" or t[0].isdigit():
            col = C_NUM
        elif t in TYPES:
            col = C_TYPE
        elif t in KEYWORDS:
            col = C_KW
        else:
            col = C_DEF
        runs.append((t, col))
        cur = m.end()
    if cur < len(body):
        runs.append((body[cur:], C_DEF))
    if cmt:
        runs.append((cmt, C_CMT))
    return runs


def _win(d, box, title, fill=(30, 30, 30), bar=(45, 45, 48), edge=(64, 68, 74)):
    x0, y0, x1, y1 = box
    rrect(d, (x0, y0, x1, y1), 9, fill=fill, outline=edge, width=2)
    rrect(d, (x0, y0, x1, y0 + 32), 9, fill=bar)
    d.rectangle((x0, y0 + 22, x1, y0 + 32), fill=bar)
    d.text((x0 + 15, y0 + 16), title, font=font(F_REG, 13),
           fill=(196, 196, 200), anchor="lm")


def panel_roadmap(img, beat, f):
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, H - CAP_H), fill=BG)
    d.text((90, 62), "ONE PROJECT, THREE ACTS", font=font(F_BOLD, 30), fill=TEXT)
    d.rectangle((90, 108, 300, 112), fill=BLUE)
    rows = beat.get("rows", [])
    rh = 122
    for i, row in enumerate(rows):
        num, name, sub1, sub2 = row
        a = clamp((f - 0.10 - i * 0.16) / 0.20, 0, 1)
        if a <= 0:
            continue
        y = 164 + i * rh
        col = [BLUE, EMER, AMBER][i % 3]
        rrect(d, (90, y, W - 90, y + rh - 18), 10, fill=blend(BG, SURF, 0.92 * a))
        d.rectangle((90, y, 98, y + rh - 18), fill=blend(BG, col, a))
        d.ellipse((118, y + 28, 168, y + 78), fill=blend(BG, col, a))
        d.text((143, y + 53), num, font=font(F_BOLD, 24),
               fill=blend(BG, (255, 255, 255), a), anchor="mm")
        d.text((194, y + 32), name, font=font(F_BOLD, 25),
               fill=blend(BG, TEXT, a), anchor="lm")
        d.text((194, y + 66), sub1, font=font(F_REG, 17),
               fill=blend(BG, MUTED, a), anchor="lm")
        d.text((194, y + 88), sub2, font=font(F_REG, 16),
               fill=blend(BG, DIM, a), anchor="lm")


def panel_ide(img, beat, f):
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, H - CAP_H), fill=BG)
    x0, y0, x1, y1 = 62, 44, W - 62, H - CAP_H - 26
    _win(d, (x0, y0, x1, y1), beat.get("title", "uVision5"))
    tf = font(F_REG, 13)
    tab = beat.get("tab", "file.c")
    tw = d.textlength(tab, font=tf) + 28
    rrect(d, (x0 + 10, y0 + 32, x0 + 10 + tw, y0 + 58), 5, fill=(30, 30, 30))
    d.text((x0 + 24, y0 + 45), tab, font=tf, fill=(236, 236, 240), anchor="lm")
    d.rectangle((x0, y0 + 58, x1, y0 + 59), fill=(64, 68, 74))

    lines = beat["lines"]
    hlset = set(beat.get("hl", []))
    lh = 21
    fnt = font(F_MONO, 15)
    nf = font(F_MONO, 13)
    top = y0 + 68
    vis = max(1, int((y1 - top - 10) // lh))
    smax = max(0, len(lines) - vis)
    sf = clamp((f - 0.06) / 0.88, 0, 1)
    first = int(round(smax * ease(sf)))
    gx, cx = x0 + 16, x0 + 70
    xmax = x1 - 16
    for i in range(vis):
        idx = first + i
        if idx >= len(lines):
            break
        yy = top + i * lh
        if idx in hlset:
            d.rectangle((cx - 8, yy - 1, x1 - 10, yy + lh - 3), fill=(38, 58, 92))
        d.text((gx, yy + lh / 2), "%3d" % (idx + 1), font=nf, fill=C_LN,
               anchor="lm")
        x = cx
        for txt, col in hl_runs(lines[idx]):
            if x > xmax:
                break
            d.text((x, yy + lh / 2), txt, font=fnt, fill=col, anchor="lm")
            x += d.textlength(txt, font=fnt)


def panel_build(img, beat, f):
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, H - CAP_H), fill=BG)
    x0, y0, x1, y1 = 150, 118, W - 150, H - CAP_H - 86
    _win(d, (x0, y0, x1, y1), beat.get("title", "Build Output"),
         fill=(24, 24, 27), bar=(45, 45, 48))
    lines = beat["lines"]
    mf = font(F_MONO, 19)
    top = y0 + 52
    lh = 40
    per = 0.60 / max(1, len(lines))
    for i, ln in enumerate(lines):
        a = clamp((f - 0.06 - i * per) / 0.10, 0, 1)
        if a <= 0:
            continue
        if "Error(s)" in ln:
            col = (120, 220, 150)
        elif "Size" in ln or "hex" in ln:
            col = (150, 210, 255)
        else:
            col = (198, 203, 210)
        d.text((x0 + 22, top + i * lh), ln, font=mf,
               fill=blend((24, 24, 27), col, a), anchor="lm")
    a = clamp((f - 0.74) / 0.14, 0, 1)
    if a > 0:
        d.rectangle((x0 + 1, y1 - 34, x1 - 1, y1 - 1),
                    fill=blend((24, 24, 27), (16, 82, 50), a))
        d.text((x0 + 22, y1 - 18), "0 Error(s), 0 Warning(s).",
               font=font(F_BOLD, 16), fill=blend((24, 24, 27), (178, 255, 205), a),
               anchor="lm")


def panel_desktop(img, beat, f):
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, H - CAP_H), fill=BG)
    x0, y0, x1, y1 = 170, 92, W - 170, H - CAP_H - 62
    rrect(d, (x0, y0, x1, y1), 9, fill=(249, 249, 250), outline=(188, 190, 196),
          width=2)
    rrect(d, (x0, y0, x1, y0 + 40), 9, fill=(237, 238, 242))
    d.rectangle((x0, y0 + 30, x1, y0 + 40), fill=(237, 238, 242))
    d.text((x0 + 16, y0 + 20), beat.get("title", "Objects"),
           font=font(F_BOLD, 15), fill=(48, 50, 56), anchor="lm")
    rows = beat["lines"]
    lh = 46
    top = y0 + 54
    for i, ln in enumerate(rows):
        a = clamp((f - i * 0.07) / 0.15, 0, 1)
        if a <= 0:
            continue
        yy = top + i * lh
        rrect(d, (x0 + 14, yy, x1 - 14, yy + 38), 5,
              fill=blend((249, 249, 250), (242, 247, 255), a))
        d.rectangle((x0 + 26, yy + 9, x0 + 46, yy + 29),
                    fill=blend((249, 249, 250), (58, 118, 216), a),
                    outline=blend((249, 249, 250), (38, 78, 168), a))
        d.text((x0 + 58, yy + 19), ln, font=font(F_MONO, 16),
               fill=blend((249, 249, 250), (34, 38, 48), a), anchor="lm")


def panel_notice(img, beat, f):
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, H - CAP_H), fill=BG)
    bw, bh = 950, 300
    x0, y0 = (W - bw) / 2, (H - CAP_H - bh) / 2 - 6
    rrect(d, (x0, y0, x0 + bw, y0 + bh), 12, fill=(44, 31, 12), outline=AMBER,
          width=3)
    d.rectangle((x0, y0, x0 + 8, y0 + bh), fill=AMBER)
    tracked(d, (x0 + 36, y0 + 34), beat.get("title", "NOTE"), font(F_BOLD, 15),
            AMBER, 1.8, anchor="lm")
    d.text((x0 + 36, y0 + 78), beat.get("head", ""), font=font(F_BOLD, 29),
           fill=(254, 243, 199), anchor="lm")
    bf = font(F_REG, 21)
    for i, ln in enumerate(wrap(d, beat.get("body", ""), bf, bw - 74)):
        a = clamp((f - 0.26 - i * 0.12) / 0.24, 0, 1)
        d.text((x0 + 36, y0 + 142 + i * 34), ln, font=bf,
               fill=blend((44, 31, 12), (226, 202, 142), a), anchor="lm")


def panel_zones(img, beat, f):
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, H - CAP_H), fill=BG)
    d.text((110, 66), "THREE COMPARISONS", font=font(F_BOLD, 30), fill=TEXT)
    d.rectangle((110, 112, 292, 116), fill=EMER)
    rows = beat.get("rows", [])
    rh = 76
    cols = [150, 330, 590, 880]
    for i, row in enumerate(rows):
        a = clamp((f - 0.14 - i * 0.14) / 0.20, 0, 1)
        if a <= 0:
            continue
        name, cond, temp, act = row
        y = 158 + i * rh
        col = [EMER, AMBER, RED][i % 3]
        rrect(d, (110, y, W - 110, y + rh - 14), 8,
              fill=blend(BG, SURF, 0.9 * a))
        d.rectangle((110, y, 117, y + rh - 14), fill=blend(BG, col, a))
        d.text((cols[0], y + 32), name, font=font(F_BOLD, 22),
               fill=blend(BG, col, a), anchor="lm")
        d.text((cols[1], y + 32), cond, font=font(F_MONO, 19),
               fill=blend(BG, BLUE_LT, a), anchor="lm")
        d.text((cols[2], y + 32), temp, font=font(F_REG, 20),
               fill=blend(BG, TEXT, a), anchor="lm")
        d.text((cols[3], y + 32), act, font=font(F_REG, 19),
               fill=blend(BG, MUTED, a), anchor="lm")


def panel_wiring(img, beat, f):
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, H - CAP_H), fill=BG)
    d.text((92, 52), "SIX WIRES, PROGRAMMED IN CIRCUIT",
           font=font(F_BOLD, 25), fill=TEXT)
    d.rectangle((92, 92, 300, 96), fill=BLUE)
    px0, py0, pw, ph = 96, 176, 252, 300
    rrect(d, (px0, py0, px0 + pw, py0 + ph), 8, fill=SURF, outline=BLUE, width=2)
    d.text((px0 + pw / 2, py0 + 32), "PROGRAMMER", font=font(F_BOLD, 18),
           fill=TEXT, anchor="mm")
    d.text((px0 + pw / 2, py0 + 60), "Arduino ISP or 8051 ISP",
           font=font(F_REG, 13), fill=MUTED, anchor="mm")
    cx0, cy0, cw2, ch2 = 738, 156, 350, 340
    rrect(d, (cx0, cy0, cx0 + cw2, cy0 + ch2), 8, fill=(23, 25, 30),
          outline=(118, 126, 138), width=2)
    rrect(d, (cx0 + 58, cy0 + 44, cx0 + cw2 - 58, cy0 + ch2 - 44), 4,
          fill=(35, 38, 44))
    d.text((cx0 + cw2 / 2, cy0 + ch2 / 2 - 8), "AT89S52",
           font=font(F_BOLD, 23), fill=(202, 210, 222), anchor="mm")
    d.text((cx0 + cw2 / 2, cy0 + ch2 / 2 + 26), "40-pin DIP",
           font=font(F_REG, 14), fill=MUTED, anchor="mm")
    wires = beat.get("wires", [])
    for i, w in enumerate(wires):
        sig, pin, num, col = w
        a = clamp((f - 0.10 - i * 0.085) / 0.16, 0, 1)
        if a <= 0:
            continue
        c = blend(BG, col, a)
        ly = py0 + 96 + i * 33
        ry = cy0 + 66 + i * 42
        d.text((px0 + pw - 16, ly), sig, font=font(F_BOLD, 15), fill=c,
               anchor="rm")
        d.ellipse((px0 + pw - 9, ly - 4, px0 + pw + 1, ly + 6), fill=c)
        d.text((cx0 + 24, ry), "%s   pin %s" % (pin, num),
               font=font(F_MONO, 14), fill=c, anchor="lm")
        d.ellipse((cx0 - 11, ry - 5, cx0 - 1, ry + 5), fill=c)
        pts = []
        for k in range(37):
            t = k / 36.0
            pts.append((lerp(px0 + pw + 1, cx0 - 1, t), lerp(ly, ry, ease(t))))
        d.line(pts, fill=c, width=3, joint="curve")


FLASH_LINES = [
    "$ avrdude -c arduino -p 8052 -P COM3 -b 19200"
    " -U flash:w:12_industrial_monitor.hex:i",
    "",
    "avrdude: AVR device initialized and ready to accept instructions",
    "avrdude: device signature = 0x1e5206 (AT89S52)",
    "avrdude: reading input file 12_industrial_monitor.hex",
    "avrdude: writing flash (3402 bytes)",
    "avrdude: 3402 bytes of flash written",
    "avrdude: verifying flash memory against input file",
    "avrdude: 3402 bytes of flash verified",
    "avrdude done.  Thank you.",
]


def panel_flash(img, beat, f):
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, H - CAP_H), fill=BG)
    x0, y0, x1, y1 = 128, 122, W - 128, H - CAP_H - 74
    rrect(d, (x0, y0, x1, y1), 9, fill=(9, 14, 26), outline=BORDER, width=2)
    d.text((x0 + 20, y0 + 26), "COMMAND PROMPT", font=font(F_BOLD, 14),
           fill=MUTED, anchor="lm")
    d.rectangle((x0, y0 + 44, x1, y0 + 45), fill=BORDER)
    mf = font(F_MONO, 16)
    lh = 27
    top = y0 + 60
    lines = beat.get("lines", FLASH_LINES)
    per = 0.60 / max(1, len(lines))
    for i, ln in enumerate(lines):
        a = clamp((f - 0.05 - i * per) / 0.09, 0, 1)
        if a <= 0:
            continue
        if "verified" in ln or "Thank you" in ln or "written" in ln:
            col = (120, 220, 150)
        elif ln.startswith("$") or ln.startswith(" "):
            col = (150, 210, 255)
        else:
            col = (198, 203, 210)
        d.text((x0 + 22, top + i * lh), ln, font=mf,
               fill=blend((9, 14, 26), col, a), anchor="lm")


# ------------------------------------------------------------------ beats

def render_beat(beat, u, frame):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    k = beat["kind"]
    if k == "image":
        base = kenburns(beat["src"], u, beat.get("zoom", [1.0, 1.1]),
                        beat.get("pan", [[.5, .5], [.5, .5]]))
        img.paste(base, (0, 0))
        for c in beat.get("callouts", []):
            draw_callout(img, c, u, 1.0)
    elif k == "grid":
        render_grid(img, beat, u)
    elif k == "panel":
        p = beat["panel"]
        if p == "title":
            panel_title(d, u)
        elif p == "problem":
            panel_problem(d, u)
        elif p == "terminal":
            panel_terminal(d, beat, u)
        elif p == "lcd":
            panel_lcd(img, beat, u)
        elif p == "results":
            panel_results(d, u)
        elif p == "end":
            panel_end(d, u)
        elif p == "roadmap":
            panel_roadmap(img, beat, u)
        elif p == "ide":
            panel_ide(img, beat, u)
        elif p == "build":
            panel_build(img, beat, u)
        elif p == "desktop":
            panel_desktop(img, beat, u)
        elif p == "notice":
            panel_notice(img, beat, u)
        elif p == "zones":
            panel_zones(img, beat, u)
        elif p == "wiring":
            panel_wiring(img, beat, u)
        elif p == "flash":
            panel_flash(img, beat, u)
    return img


def beat_at(scene, u):
    beats = scene["beats"]
    XF = 0.055
    for i, b in enumerate(beats):
        if u < b["t1"]:
            cur = (b, clamp((u - b["t0"]) / max(1e-6, b["t1"] - b["t0"]), 0, 1))
            nxt = beats[i + 1] if i + 1 < len(beats) else None
            if nxt and u > b["t1"] - XF and b["t1"] > b["t0"]:
                nb = (nxt, clamp((u - nxt["t0"]) /
                                 max(1e-6, nxt["t1"] - nxt["t0"]), 0, 1))
                return cur, nb, clamp((u - (b["t1"] - XF)) / XF, 0, 1)
            return cur, None, 0.0
    return (beats[-1], 1.0), None, 0.0


# ------------------------------------------------------------------ captions

def chunk_text(t, lo=42, hi=96):
    parts = re.split(r"(?<=[.!?]) +", t.strip())
    out = []
    for s in parts:
        if len(s) <= hi:
            out.append(s)
            continue
        subs = re.split(r"(?<=, )|(?<=: )|(?<= - )", s)
        cur = ""
        for sb in subs:
            if cur and len(cur) + len(sb) > hi:
                out.append(cur.strip())
                cur = sb
            else:
                cur += sb
        if cur.strip():
            out.append(cur.strip())
    merged = []
    for c in out:
        if merged and len(merged[-1]) + len(c) + 1 <= hi and len(merged[-1]) < lo:
            merged[-1] = merged[-1] + " " + c
        else:
            merged.append(c)
    return [c for c in merged if c]


def caption_chunks(scene, speech_dur):
    ch = chunk_text(scene["narration"])
    words = [max(1, len(c.split())) for c in ch]
    tot = float(sum(words))
    segs, acc = [], 0.0
    for c, wd in zip(ch, words):
        d = speech_dur * wd / tot
        segs.append((acc, acc + d, c))
        acc += d
    return segs


def draw_caption(img, text, alpha):
    if alpha <= 0.01:
        return
    bar = Image.new("RGBA", (W, CAP_H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bar)
    for i in range(CAP_H):
        a = int(226 * (i / float(CAP_H)) ** 1.5)
        bd.line([(0, i), (W, i)], fill=(11, 18, 32, a))
    bd.line([(0, 0), (W, 0)], fill=BLUE + (int(230 * alpha),), width=3)
    img.paste(bar, (0, H - CAP_H), bar)

    d = ImageDraw.Draw(img)
    fnt = font(F_REG, 27)
    maxw = W - 220
    lines = wrap(d, text, fnt, maxw)
    lh = 37
    y0 = H - CAP_H + 34 - (len(lines) - 1) * lh / 2.0
    for i, ln in enumerate(lines[:3]):
        tw = d.textlength(ln, font=fnt)
        d.text(((W - tw) / 2, y0 + i * lh), ln, font=fnt,
               fill=blend((11, 18, 32), TEXT, alpha), anchor="lm")


def draw_chrome(d, label, prog):
    fnt = font(F_BOLD, 15)
    tracked(d, (44, 40), label, fnt, BLUE_LT, 1.8, anchor="lm")
    wf = font(F_BOLD, 13)
    tw = tracked_w(d, "8051 HARDWARE LAB", wf, 1.8)
    tracked(d, (W - 44 - tw, 40), "8051 HARDWARE LAB", wf, (71, 85, 105), 1.8,
            anchor="lm")
    d.rectangle((0, H - 5, W, H), fill=(30, 41, 59))
    d.rectangle((0, H - 5, int(W * prog), H), fill=EMER)


# ------------------------------------------------------------------ audio

def ffbin():
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def wav_of(path):
    ff = ffbin()
    p = subprocess.run([ff, "-v", "error", "-i", path, "-ar", "44100",
                        "-ac", "1", "-f", "wav", "-"],
                       capture_output=True)
    raw = p.stdout
    import io
    wf = wave.open(io.BytesIO(raw))
    n = wf.getnframes()
    data = np.frombuffer(wf.readframes(n), dtype=np.int16).astype(np.float32)
    wf.close()
    return data / 32768.0


# ------------------------------------------------------------------ main

def main():
    only = None
    limit = None
    shot = None
    args = sys.argv[1:]
    for i, a in enumerate(args):
        if a == "--scenes":
            only = set(args[i + 1].split(","))
        if a == "--limit":
            limit = int(args[i + 1])
        if a == "--shot":
            shot = float(args[i + 1])

    ff = ffbin()
    print("script: %s -> %s" % (SCRIPT_NAME, os.path.basename(OUT)))
    print("loading narration ...")
    durs, tracks = [], []
    for s in SCENES:
        p = os.path.join(AUDIO, s["id"] + ".mp3")
        tr = wav_of(p)
        tracks.append(tr)
        durs.append(len(tr) / 44100.0)
        print("  %s  %.2fs  %d words" % (s["id"], durs[-1],
                                         len(s["narration"].split())))

    starts, t = [], LEAD
    for dd in durs:
        starts.append(t)
        t += PRE + dd + POST
    total = t - POST + TAIL
    print("scenes=%d  total=%.2fs (%.1f min)" % (len(SCENES), total,
                                                 total / 60.0))

    # audio track
    aud = np.zeros(int(total * 44100.0) + 44100, dtype=np.float32)
    for s, dd, st, tr in zip(SCENES, durs, starts, tracks):
        o = int((st + PRE) * 44100.0)
        aud[o:o + len(tr)] += tr
    peak = float(np.max(np.abs(aud))) or 1.0
    if peak > 0.99:
        aud = aud * (0.97 / peak)
    wav_path = os.path.join(VDIR, "_narration.wav")
    import scipy.io.wavfile as wv
    wv.write(wav_path, 44100, (aud * 32767.0).astype(np.int16))
    print("audio: %s" % wav_path)

    # frame plan
    nframes = int(round(total * FPS))
    if limit:
        nframes = min(nframes, limit)
    print("frames: %d" % nframes)

    if shot is not None:
        t_s = shot
        si = 0
        for i in range(len(SCENES)):
            if t_s >= starts[i]:
                si = i
        s = SCENES[si]
        u = clamp((t_s - starts[si]) / (PRE + durs[si] + POST), 0, 1)
        frame = render_frame(s, u, PRE + durs[si] + POST, PRE, durs[si], si,
                             t_s / total)
        frame.save(os.path.join(VDIR, "_shot.png"))
        print("wrote _shot.png at t=%.2f (scene %s)" % (t_s, s["id"]))
        return

    cmd = [ff, "-y", "-v", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % (W, H),
           "-r", str(FPS), "-i", "pipe:0",
           "-i", wav_path,
           "-c:v", "libx264", "-preset", "medium", "-crf", "20",
           "-pix_fmt", "yuv420p", "-movflags", "+faststart",
           "-c:a", "aac", "-b:a", "160k", "-shortest", OUT]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    for fi in range(nframes):
        t_s = fi / float(FPS)
        si = 0
        for i in range(len(SCENES)):
            if t_s >= starts[i]:
                si = i
        s = SCENES[si]
        if only and s["id"] not in only:
            continue
        sd = PRE + durs[si] + POST
        u = clamp((t_s - starts[si]) / sd, 0, 1)
        frame = render_frame(s, u, PRE + durs[si] + POST, PRE, durs[si], si,
                             clamp(t_s / total, 0, 1))
        proc.stdin.write(frame.tobytes())
        if fi % 240 == 0:
            print("  frame %5d/%d  t=%6.1fs" % (fi, nframes, t_s))
            sys.stdout.flush()

    proc.stdin.close()
    err = proc.stderr.read().decode("utf-8", "replace")
    rc = proc.wait()
    if rc != 0:
        print(err[-3000:])
        raise SystemExit("ffmpeg failed rc=%d" % rc)
    print("done -> %s (%.1f MB)" % (OUT, os.path.getsize(OUT) / 1048576.0))


def render_frame(s, u, sdur, pre, dur, sidx, prog):
    cur_b, nxt_b, xf = beat_at(s, u)
    base = render_beat(cur_b[0], cur_b[1], None)
    if nxt_b is not None:
        base = Image.blend(base, render_beat(nxt_b[0], nxt_b[1], None), xf)

    # scrim so the caption bar always reads over bright photography
    scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    for i in range(150):
        y = H - CAP_H - 60 + i
        a = int(160 * (i / 150.0) ** 2)
        sd.line([(0, y), (W, y)], fill=(11, 18, 32, a))
    base.paste(scrim, (0, 0), scrim)

    # caption chunk that matches what is being spoken right now
    local = u * sdur - pre
    cur, calpha = None, 0.0
    for (a0, a1, txt) in caption_chunks(s, dur):
        if a0 - 0.05 <= local < a1 + 0.45:
            cur = txt
            calpha = min(clamp((local - a0) / 0.22, 0, 1),
                         clamp((a1 + 0.45 - local) / 0.30, 0, 1))
            break
    if cur:
        draw_caption(base, cur, calpha)
    d = ImageDraw.Draw(base)
    draw_chrome(d, s["label"], prog)
    return base


if __name__ == "__main__":
    main()
