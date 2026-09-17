#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ساخت برگه‌ی معرفی هویت بصری (Brand Sheet)
نمایش لوگو، آیکون‌ها در اندازه‌های واقعی، نشان خالص و رنگ‌های سازمانی.

اجرا:  python3 branding/tools/make_brand_sheet.py
خروجی: branding/brand-sheet.png
"""

import json
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
BRAND_DIR = os.path.dirname(HERE)
OUT_DIR = os.path.join(BRAND_DIR, "out")
FONT_DIR = os.path.join(BRAND_DIR, "assets", "fonts")

W = 1400
PAD = 30
BG = (245, 248, 250)
CARD = (255, 255, 255)
LINE = (223, 232, 238)
INK = (28, 40, 56)
MUTED = (122, 138, 152)


def fa(size, bold=False):
    name = "Vazirmatn-Bold.ttf" if bold else "Vazirmatn-Regular.ttf"
    p = os.path.join(FONT_DIR, name)
    if os.path.exists(p):
        return ImageFont.truetype(p, size)
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)


def latin(size, bold=True):
    for c in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
              else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
              "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"):
        if os.path.exists(c):
            return ImageFont.truetype(c, size)
    return fa(size, bold)


def load(name):
    return Image.open(os.path.join(OUT_DIR, name)).convert("RGBA")


def main():
    with open(os.path.join(BRAND_DIR, "branding.json"), encoding="utf-8") as f:
        brand = json.load(f)

    blue = tuple(int(brand["colors"]["primary"].lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    orange = tuple(int(brand["colors"]["accent"].lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))

    # --- چیدمان کارت‌ها ---
    CARD1 = (PAD, PAD, W - PAD, 300)          # لوگو
    CARD2 = (PAD, 330, W - PAD, 750)          # آیکون‌ها
    CARD3 = (PAD, 780, W - PAD, 1080)         # نشان و رنگ‌ها
    H = CARD3[3] + PAD

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    for (x0, y0, x1, y1) in (CARD1, CARD2, CARD3):
        d.rounded_rectangle([x0, y0, x1, y1], radius=18, fill=CARD, outline=LINE)

    def title(txt, y, x=None):
        d.text((x or (W - PAD - 40), y), txt, font=fa(26, True), fill=INK, anchor="ra")

    def srcline(txt, y):
        d.text((W - PAD - 40, y), txt, font=fa(19), fill=MUTED, anchor="ra")

    # ---------------- کارت ۱: لوگو ----------------
    title("لوگو", CARD1[1] + 22)
    srcline(brand["company_fa"], CARD1[1] + 62)
    srcline("nrisp.ac.ir", CARD1[1] + 92)

    # لوگوی داخل برنامه: فقط نشان. اندازهٔ واقعی‌اش ۶۰ پیکسل است
    emblem = load("emblem.png")
    box = Image.new("RGB", (70, 70), CARD)
    real = emblem.resize((60, 60), Image.LANCZOS)
    box.paste(real, (5, 5), real)
    img.paste(box, (CARD1[0] + 45, CARD1[1] + 78))
    d.rectangle([CARD1[0] + 50, CARD1[1] + 83, CARD1[0] + 110, CARD1[1] + 143],
                outline=(205, 218, 228))
    d.text((CARD1[0] + 80, CARD1[3] - 62), "داخل برنامه", font=fa(18), fill=MUTED, anchor="ma")
    d.text((CARD1[0] + 80, CARD1[3] - 38), "۶۰ پیکسل", font=fa(16), fill=MUTED, anchor="ma")

    d.line([CARD1[0] + 160, CARD1[1] + 60, CARD1[0] + 160, CARD1[3] - 60],
           fill=LINE, width=2)

    # لوگوی کامل با نام: برای اسناد و سرصفحه
    full = load("logo_full.png")
    target_h = 120
    full = full.resize((int(full.width * target_h / full.height), target_h), Image.LANCZOS)
    max_w = CARD1[2] - (CARD1[0] + 200) - 430
    if full.width > max_w:
        full = full.resize((max_w, int(full.height * max_w / full.width)), Image.LANCZOS)
    img.paste(full, (CARD1[0] + 200, CARD1[1] + 75), full)
    d.text((CARD1[0] + 200 + full.width / 2, CARD1[3] - 50),
           "نسخهٔ کامل، برای اسناد و سرصفحه", font=fa(18), fill=MUTED, anchor="ma")

    # ---------------- کارت ۲: آیکون‌ها ----------------
    title("آیکون برنامه در اندازه‌های واقعی", CARD2[1] + 22)
    icon = load("icon.png")
    sizes = [16, 24, 32, 48, 64, 128, 256]
    gap = 52
    x = CARD2[0] + 55
    base = CARD2[1] + 310          # خط پایه‌ی آیکون‌ها
    for s in sizes:
        ic = icon.resize((s, s), Image.LANCZOS)
        img.paste(ic, (x, base - s), ic)
        d.text((x + s / 2, base + 16), str(s), font=latin(17, False), fill=MUTED, anchor="ma")
        x += s + gap

    # ---------------- کارت ۳: نشان و رنگ‌ها ----------------
    title("نشان خالص و رنگ‌های سازمانی", CARD3[1] + 22)

    # نشان روی زمینه روشن
    em = load("emblem.png").resize((150, 150), Image.LANCZOS)
    box = Image.new("RGB", (170, 170), CARD)
    box.paste(em, (10, 10), em)
    img.paste(box, (CARD3[0] + 60, CARD3[1] + 80))
    d.text((CARD3[0] + 145, CARD3[3] - 60), "روی زمینه روشن",
           font=fa(18), fill=MUTED, anchor="ma")

    # نشان روی زمینه آبی
    emw = load("emblem_white.png").resize((150, 150), Image.LANCZOS)
    box2 = Image.new("RGB", (170, 170), blue)
    box2.paste(emw, (10, 10), emw)
    img.paste(box2, (CARD3[0] + 250, CARD3[1] + 80))
    d.text((CARD3[0] + 335, CARD3[3] - 60), "روی زمینه آبی",
           font=fa(18), fill=MUTED, anchor="ma")

    # نمونه رنگ‌ها
    swatches = [(brand["colors"]["primary"], "آبی موسسه"),
                (brand["colors"]["accent"], "نارنجی موسسه"),
                ("#EFEFF2", "خاکستری زمینه")]
    x = CARD3[0] + 470
    for hexc, label in swatches:
        rgb = tuple(int(hexc.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
        d.rounded_rectangle([x, CARD3[1] + 80, x + 150, CARD3[1] + 200],
                            radius=12, fill=rgb, outline=LINE)
        d.text((x + 75, CARD3[1] + 212), hexc.upper(), font=latin(19), fill=INK, anchor="ma")
        d.text((x + 75, CARD3[1] + 240), label, font=fa(18), fill=MUTED, anchor="ma")
        x += 180

    out = os.path.join(BRAND_DIR, "brand-sheet.png")
    img.save(out)
    print("ساخته شد:", out, img.size)


if __name__ == "__main__":
    main()
