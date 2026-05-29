#!/usr/bin/env python3
"""Generate 04-workflow-diagram.png — Xanh SM Critical Battery Incident (current-state)."""
import os
import math
from PIL import Image, ImageDraw, ImageFont

# ---- Canvas ----
W, H = 1800, 1200
SCALE = 2  # supersample for crisp edges
img = Image.new("RGB", (W * SCALE, H * SCALE), "#ffffff")
d = ImageDraw.Draw(img)

FONT_DIR = "/System/Library/Fonts/Supplemental"
def font(size, bold=False):
    name = "Arial Bold.ttf" if bold else "Arial.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size * SCALE)

f_title = font(40, bold=True)
f_sub   = font(22)
f_step  = font(24, bold=True)
f_body  = font(19)
f_time  = font(20, bold=True)
f_tag   = font(18, bold=True)
f_arrow = font(17, bold=True)
f_leg   = font(19)
f_legb  = font(22, bold=True)

# ---- Colors ----
INK      = "#1f2933"
NORMAL_BG= "#eaf2fb"
NORMAL_BD= "#2b6cb0"
BOTTLE_BG= "#fde2e2"
BOTTLE_BD= "#c0392b"
BOTTLE_TX= "#c0392b"
DONE_BG  = "#e3f6e8"
DONE_BD  = "#2f855a"
ARROW_CL = "#4a5568"
NOTE_BG  = "#fff7e0"
NOTE_BD  = "#d69e2e"

def S(v):
    return v * SCALE

def rrect(x, y, w, h, r, fill, outline, width=3):
    d.rounded_rectangle([S(x), S(y), S(x + w), S(y + h)], radius=S(r),
                        fill=fill, outline=outline, width=width * SCALE)

def tw_of(text, fnt):
    bb = d.textbbox((0, 0), text, font=fnt)
    return bb[2] - bb[0], bb[3] - bb[1]

def center_text(cx, y, text, fnt, fill):
    w_, _ = tw_of(text, fnt)
    d.text((S(cx) - w_ / 2, S(y)), text, font=fnt, fill=fill)

def wrap_lines(cx, y, lines, fnt, fill, lh):
    for i, ln in enumerate(lines):
        center_text(cx, y + i * lh, ln, fnt, fill)

def box(x, y, w, h, kind, num, title, body_lines, time_txt, tag=None):
    if kind == "bottle":
        bg, bd, tx = BOTTLE_BG, BOTTLE_BD, BOTTLE_TX
    elif kind == "done":
        bg, bd, tx = DONE_BG, DONE_BD, INK
    else:
        bg, bd, tx = NORMAL_BG, NORMAL_BD, INK
    rrect(x, y, w, h, 18, bg, bd, width=3)
    cx = x + w / 2
    center_text(cx, y + 18, f"{num}. {title}", f_step, tx)
    wrap_lines(cx, y + 60, body_lines, f_body, INK, 26)
    center_text(cx, y + h - 36, time_txt, f_time, bd)
    if tag:
        center_text(cx, y + h - 64, tag, f_tag, BOTTLE_TX)

def arrow(x1, y1, x2, y2, label=None, label_side="on"):
    d.line([S(x1), S(y1), S(x2), S(y2)], fill=ARROW_CL, width=4 * SCALE)
    ang = math.atan2(y2 - y1, x2 - x1)
    L = 16
    for da in (math.radians(150), math.radians(-150)):
        hx = x2 + L * math.cos(ang + da)
        hy = y2 + L * math.sin(ang + da)
        d.line([S(x2), S(y2), S(hx), S(hy)], fill=ARROW_CL, width=4 * SCALE)
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        w_, h_ = tw_of(label, f_arrow)
        if label_side == "above":
            ly = my - 26
        else:
            ly = my - h_ / 2 - 4
        pad = 6
        d.rectangle([S(mx) - w_/2 - pad, S(ly) - pad,
                     S(mx) + w_/2 + pad, S(ly) + h_ + pad], fill="#ffffff")
        d.text((S(mx) - w_/2, S(ly)), label, font=f_arrow, fill=ARROW_CL)

# ---- Title ----
center_text(W/2, 38, "Xanh SM - Critical Battery Incident", f_title, INK)
center_text(W/2, 94, "Current-State Workflow (manual triage, before AI)", f_sub, "#52606d")

# ---- Layout: snake. Row1 L->R (1,2,3), Row2 R->L (4,5) ----
BW, BH = 470, 210
x1, x2, x3 = 50, 665, 1280
row1_y = 160
row2_y = 520

box(x1, row1_y, BW, BH, "normal", 1, "Driver reports incident",
    ["Channel: app / hotline", "Input: location, battery %"], "2 min")
arrow(x1 + BW, row1_y + BH/2, x2, row1_y + BH/2, "to dispatcher")

box(x2, row1_y, BW, BH, "normal", 2, "Dispatcher collects info",
    ["Plate, vehicle type, battery %,", "passenger on board?"], "3 min")
arrow(x2 + BW, row1_y + BH/2, x3, row1_y + BH/2, "to dashboard")

box(x3, row1_y, BW, BH, "bottle", 3, "Check charging station",
    ["Find nearest station with a", "free port and correct connector"], "5 min", tag="BOTTLENECK")

# vertical connector box3 -> box4
arrow(x3 + BW/2, row1_y + BH, x3 + BW/2, row2_y, "evaluate range vs battery", label_side="above")

box(x3, row2_y, BW, BH, "bottle", 4, "Decide safe action",
    ["Route to nearest station OR", "dispatch mobile charger"], "3 min", tag="BOTTLENECK")
arrow(x3, row2_y + BH/2, x2 + BW, row2_y + BH/2, "to driver")

box(x2, row2_y, BW, BH, "done", 5, "Draft and send guide",
    ["Send instructions to driver,", "log case and follow up"], "2 min")

# ---- Total time banner (below box 5, no overlap with legend) ----
banner_y = row2_y + BH + 28
rrect(x2, banner_y, BW, 56, 14, "#eef2f7", "#4a5568", width=2)
center_text(x2 + BW/2, banner_y + 14, "Total manual time approx. 15 min / case", f_time, INK)

# ---- Legend / key facts (bottom-left) ----
lx, ly, lw, lh = 50, 870, 760, 290
rrect(lx, ly, lw, lh, 16, "#fafbfc", "#cbd5e0", width=2)
d.text((S(lx + 24), S(ly + 20)), "Legend & key facts", font=f_legb, fill=INK)
def swatch(yy, color, border, label):
    d.rounded_rectangle([S(lx+24), S(yy), S(lx+24+34), S(yy+24)], radius=S(5),
                        fill=color, outline=border, width=2*SCALE)
    d.text((S(lx+72), S(yy)), label, font=f_leg, fill=INK)
swatch(ly + 66,  NORMAL_BG, NORMAL_BD, "Normal step")
swatch(ly + 108, BOTTLE_BG, BOTTLE_BD, "Bottleneck (slow / error-prone)")
swatch(ly + 150, DONE_BG,   DONE_BD,   "Hand-off to driver / case closed")
d.text((S(lx+24), S(ly+196)), "Hand-off chain:", font=f_legb, fill=INK)
d.text((S(lx+24), S(ly+230)), "driver -> dispatcher -> station dashboard -> driver",
       font=f_leg, fill="#52606d")
d.text((S(lx+24), S(ly+260)), "Bottlenecks: steps 3 & 4 (approx. 8 of 15 min)",
       font=f_leg, fill=BOTTLE_TX)

# ---- Future AI safety rule (bottom-right) ----
nx, ny, nw, nh = 860, 870, 890, 290
rrect(nx, ny, nw, nh, 16, NOTE_BG, NOTE_BD, width=2)
d.text((S(nx+24), S(ny+20)), "Future AI safety rule (target state)", font=f_legb, fill="#8a6d1a")
notes = [
    "If battery < 5% AND station > 5 km:",
    "      -> dispatch_mobile_charger (never route far).",
    "Every AI message starts with [DRAFT_ONLY].",
    "Dispatcher approves before anything is sent.",
    "AI never decides refunds, cancellations or pricing.",
]
for i, ln in enumerate(notes):
    d.text((S(nx+24), S(ny+66 + i*42)), ln, font=f_body, fill=INK)

# ---- Downscale & save ----
out = img.resize((W, H), Image.LANCZOS)
out.save("/Users/kenz_de/projects/ai-product-lab-t-c-cow-b-ng/04-workflow-diagram.png")
print("saved 04-workflow-diagram.png", out.size)
