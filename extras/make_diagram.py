#!/usr/bin/env python3
"""Tao 04-workflow-diagram.png — Xanh SM Su co pin thap (quy trinh hien tai). Nhan tieng Viet."""
import os
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1800, 1240
SCALE = 2
img = Image.new("RGB", (W * SCALE, H * SCALE), "#ffffff")
d = ImageDraw.Draw(img)

FONT_DIR = "/System/Library/Fonts/Supplemental"
def font(size, bold=False):
    name = "Arial Unicode.ttf"  # ho tro day du dau tieng Viet
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size * SCALE)

f_title = font(38, bold=True)
f_sub   = font(21)
f_step  = font(23, bold=True)
f_body  = font(18)
f_time  = font(19, bold=True)
f_tag   = font(17, bold=True)
f_arrow = font(16, bold=True)
f_leg   = font(18)
f_legb  = font(21, bold=True)

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
        ly = (my - 26) if label_side == "above" else (my - h_ / 2 - 4)
        pad = 6
        d.rectangle([S(mx) - w_/2 - pad, S(ly) - pad,
                     S(mx) + w_/2 + pad, S(ly) + h_ + pad], fill="#ffffff")
        d.text((S(mx) - w_/2, S(ly)), label, font=f_arrow, fill=ARROW_CL)

# Tieu de
center_text(W/2, 38, "Xanh SM - Sự cố pin thấp của tài xế", f_title, INK)
center_text(W/2, 92, "Quy trình hiện tại (xử lý thủ công, trước khi có AI)", f_sub, "#52606d")

BW, BH = 480, 215
x1, x2, x3 = 40, 660, 1280
row1_y = 160
row2_y = 525

box(x1, row1_y, BW, BH, "normal", 1, "Tài xế báo sự cố",
    ["Kênh: app / hotline", "Nhập: vị trí, % pin"], "2 phút")
arrow(x1 + BW, row1_y + BH/2, x2, row1_y + BH/2, "đến điều phối")

box(x2, row1_y, BW, BH, "normal", 2, "Điều phối hỏi thêm",
    ["Biển số, loại xe, % pin,", "có khách trên xe không?"], "3 phút")
arrow(x2 + BW, row1_y + BH/2, x3, row1_y + BH/2, "tra dashboard")

box(x3, row1_y, BW, BH, "bottle", 3, "Tra trạm sạc",
    ["Tìm trạm gần nhất còn trụ", "trống, đúng loại cổng sạc"], "5 phút", tag="NÚT THẮT")

arrow(x3 + BW/2, row1_y + BH, x3 + BW/2, row2_y, "xét quãng đường so với pin", label_side="above")

box(x3, row2_y, BW, BH, "bottle", 4, "Quyết định xử lý an toàn",
    ["Đi trạm gần nhất HOẶC", "gọi xe sạc / cứu hộ di động"], "3 phút", tag="NÚT THẮT")
arrow(x3, row2_y + BH/2, x2 + BW, row2_y + BH/2, "gửi tài xế")

box(x2, row2_y, BW, BH, "done", 5, "Soạn & gửi hướng dẫn",
    ["Gửi hướng dẫn cho tài xế,", "ghi log case & theo dõi"], "2 phút")

# Banner tong thoi gian
banner_y = row2_y + BH + 28
rrect(x2, banner_y, BW, 56, 14, "#eef2f7", "#4a5568", width=2)
center_text(x2 + BW/2, banner_y + 14, "Tổng thời gian thủ công: ~15 phút / case", f_time, INK)

# Chu giai (trai)
lx, ly, lw, lh = 40, 885, 800, 300
rrect(lx, ly, lw, lh, 16, "#fafbfc", "#cbd5e0", width=2)
d.text((S(lx + 24), S(ly + 20)), "Chú giải & dữ kiện chính", font=f_legb, fill=INK)
def swatch(yy, color, border, label):
    d.rounded_rectangle([S(lx+24), S(yy), S(lx+24+34), S(yy+24)], radius=S(5),
                        fill=color, outline=border, width=2*SCALE)
    d.text((S(lx+72), S(yy)), label, font=f_leg, fill=INK)
swatch(ly + 66,  NORMAL_BG, NORMAL_BD, "Bước bình thường")
swatch(ly + 108, BOTTLE_BG, BOTTLE_BD, "Nút thắt (chậm / dễ sai)")
swatch(ly + 150, DONE_BG,   DONE_BD,   "Bàn giao cho tài xế / đóng case")
d.text((S(lx+24), S(ly+198)), "Chuỗi bàn giao:", font=f_legb, fill=INK)
d.text((S(lx+24), S(ly+232)), "tài xế -> điều phối -> dashboard trạm sạc -> tài xế",
       font=f_leg, fill="#52606d")
d.text((S(lx+24), S(ly+264)), "Nút thắt: bước 3 & 4 (~8 trong 15 phút)",
       font=f_leg, fill=BOTTLE_TX)

# Quy tac AI tuong lai (phai)
nx, ny, nw, nh = 890, 885, 870, 300
rrect(nx, ny, nw, nh, 16, NOTE_BG, NOTE_BD, width=2)
d.text((S(nx+24), S(ny+20)), "Quy tắc an toàn AI (trạng thái tương lai)", font=f_legb, fill="#8a6d1a")
notes = [
    "Nếu pin < 5% VÀ trạm > 5 km:",
    "      -> dispatch_mobile_charger (không đi xa).",
    "Mọi tin nhắn AI bắt đầu bằng [DRAFT_ONLY].",
    "Điều phối viên duyệt trước khi gửi.",
    "AI không quyết bồi thường, hủy chuyến, đổi giá.",
]
for i, ln in enumerate(notes):
    d.text((S(nx+24), S(ny+66 + i*42)), ln, font=f_body, fill=INK)

out = img.resize((W, H), Image.LANCZOS)
out.save("/Users/kenz_de/projects/ai-product-lab-t-c-cow-b-ng/04-workflow-diagram.png")
print("saved 04-workflow-diagram.png", out.size)
