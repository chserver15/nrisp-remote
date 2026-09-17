#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تولید همه‌ی آیکون‌ها و لوگوهای موسسه از روی branding.json

نشان به‌کاررفته «شمسه»ی موسسه است: دوازده ترک (مربع) آبی گرد یک سان (دایره) نارنجی.
هندسه‌ی نشان از روی فایل لوگوی اصلی موسسه اندازه‌گیری و بازسازی شده است.

اجرا:  python3 branding/tools/generate_icons.py
"""

import json
import os
import struct
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("ماژول Pillow نصب نیست. اجرا کنید:  pip install pillow")
    sys.exit(1)

HERE = os.path.dirname(os.path.abspath(__file__))
BRAND_DIR = os.path.dirname(HERE)
OUT_DIR = os.path.join(BRAND_DIR, "out")
FONT_DIR = os.path.join(BRAND_DIR, "assets", "fonts")
SS = 4  # supersampling برای لبه‌های نرم

# هندسه‌ی نشان موسسه (اندازه‌گیری‌شده از لوگوی اصلی)
EMBLEM_OFFSETS = [(0, -3), (1, -2), (2, -1), (3, 0), (2, 1), (1, 2),
                  (0, 3), (-1, 2), (-2, 1), (-3, 0), (-2, -1), (-1, -2)]
EMBLEM_CELL = 9.0 / 63.0      # اندازه‌ی هر ترک نسبت به قاب نشان
EMBLEM_CIRCLE = 26.5 / 63.0   # قطر دایره‌ی مرکزی نسبت به قاب نشان
# اصلاح بصری: در اندازه‌های کوچک، ترک‌ها و دایره ۱۰ درصد ضخیم‌تر می‌شوند تا
# آیکون در ۱۶ و ۲۴ پیکسل هم واضح باشد. هندسهٔ رسمی لوگو دست‌نخورده می‌ماند.
ICON_OPTICAL_SCALE = 1.10


def load_brand():
    with open(os.path.join(BRAND_DIR, "branding.json"), encoding="utf-8") as f:
        return json.load(f)


def hex2rgb(h):
    h = h.strip().lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def gradient_rgb(size, c_top, c_bottom):
    img = Image.new("RGB", (1, size))
    px = img.load()
    for y in range(size):
        px[0, y] = lerp(c_top, c_bottom, y / max(1, size - 1))
    return img.resize((size, size), Image.BILINEAR)


# ------------------------------------------------------------------ نشان

def draw_emblem(size, petal_color, circle_color, bg=None, radius_ratio=None,
                pad_ratio=0.0):
    """
    رسم نشان شمسه‌ی موسسه.
    petal_color / circle_color می‌توانند RGB یا RGBA باشند.
    bg اگر داده شود، پشت نشان یک مربع گرد با آن رنگ کشیده می‌شود.
    """
    W = max(size * SS, 512)
    canvas = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas, "RGBA")

    if bg is not None:
        rr = int(W * (radius_ratio if radius_ratio is not None else 0.226))
        if len(bg) == 4:
            grad = gradient_rgb(W, lerp(bg[:3], (255, 255, 255), 0.18), bg[:3]).convert("RGBA")
        else:
            grad = gradient_rgb(W, lerp(bg, (255, 255, 255), 0.18), bg).convert("RGBA")
        mask = Image.new("L", (W, W), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, W - 1, W - 1], radius=rr, fill=255)
        canvas.paste(grad, (0, 0), mask)

    inner = W * (1.0 - 2 * pad_ratio)
    off = (W - inner) / 2.0
    cell = EMBLEM_CELL * inner
    cd = EMBLEM_CIRCLE * inner
    cx = cy = W / 2.0

    def col(c):
        return c if len(c) == 4 else (c[0], c[1], c[2], 255)

    for dx, dy in EMBLEM_OFFSETS:
        x = cx + dx * cell
        y = cy + dy * cell
        d.rectangle([x - cell / 2, y - cell / 2, x + cell / 2, y + cell / 2],
                    fill=col(petal_color))
    r = cd / 2.0
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col(circle_color))

    return canvas.resize((size, size), Image.LANCZOS)


def draw_icon(size, colors, optical=True):
    """
    آیکون برنامه: مربع گرد آبی موسسه + شمسهٔ سفید و نارنجی.
    با optical=True ترک‌ها ۱۰٪ ضخیم‌تر می‌شوند تا در اندازه‌های کوچک واضح بمانند.
    """
    global EMBLEM_CELL, EMBLEM_CIRCLE
    blue = hex2rgb(colors["primary"])
    orange = hex2rgb(colors["accent"])
    saved = (EMBLEM_CELL, EMBLEM_CIRCLE)
    if optical:
        EMBLEM_CELL *= ICON_OPTICAL_SCALE
        EMBLEM_CIRCLE *= ICON_OPTICAL_SCALE
    try:
        return draw_emblem(size, (255, 255, 255, 255), orange, bg=blue,
                           pad_ratio=0.185)
    finally:
        EMBLEM_CELL, EMBLEM_CIRCLE = saved


# ------------------------------------------------------------------ متن

def find_font(bold=False):
    name = "Vazirmatn-Bold.ttf" if bold else "Vazirmatn-Regular.ttf"
    local = os.path.join(FONT_DIR, name)
    if os.path.exists(local):
        return local
    for c in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
              "/Library/Fonts/Arial Bold.ttf", "C:/Windows/Fonts/tahoma.ttf",
              "C:/Windows/Fonts/segoeuib.ttf"]:
        if os.path.exists(c):
            return c
    return None


def text_size(draw, txt, font):
    box = draw.textbbox((0, 0), txt, font=font, direction="rtl")
    return box[2] - box[0], box[3] - box[1], box


def draw_lockup(emblem, text, text_color, height=256, max_width=None,
                target_size=None):
    """
    لوگوی افقی: نشان + نام فارسی موسسه.
    اندازهٔ قلم خودکار کوچک می‌شود تا متن هرگز بریده نشود.
    اگر target_size داده شود، خروجی دقیقاً همان اندازه می‌شود.
    """
    em = emblem.resize((height, height), Image.LANCZOS)
    font_path = find_font(bold=True)
    if not font_path or not text:
        return em
    if target_size:
        W, H = target_size
        height = H
        em = emblem.resize((H, H), Image.LANCZOS)
    else:
        W = max_width or int(height * 4.2)
        H = height

    pad_left = int(H * 0.10)   # فاصلهٔ نشان از متن
    pad_right = int(H * 0.04)

    font = None
    probe = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    for size in range(int(H * 0.46), 10, -1):
        f = ImageFont.truetype(font_path, size)
        tw, th, box = text_size(probe, text, f)
        if H * 0.92 + pad_left + tw + pad_right <= W:
            font, font_px = f, size
            break
    if font is None:
        font, font_px = ImageFont.truetype(font_path, 12), 12
        tw, th, box = text_size(probe, text, font)

    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    canvas.alpha_composite(em, (0, (H - em.height) // 2))
    d = ImageDraw.Draw(canvas)
    # راست‌چین، عمودی وسط
    d.text((W - pad_right, H / 2), text, font=font, fill=text_color,
           direction="rtl", anchor="rm")
    return canvas


# ------------------------------------------------------------------ برداری

def svg_emblem_group(cx, cy, unit, petal, circle):
    """گروه برداری نشان، برای گذاشتن داخل SVG بزرگ‌تر"""
    cell = EMBLEM_CELL * unit * 63
    parts = []
    for dx, dy in EMBLEM_OFFSETS:
        x = cx + dx * cell - cell / 2
        y = cy + dy * cell - cell / 2
        parts.append(f'  <rect x="{x:.2f}" y="{y:.2f}" width="{cell:.2f}" '
                     f'height="{cell:.2f}" fill="{petal}"/>')
    r = EMBLEM_CIRCLE * unit * 63 / 2
    parts.append(f'  <circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="{circle}"/>')
    return "\n".join(parts)


def svg_icon(colors):
    blue = colors["primary"]
    orange = colors["accent"]
    l = "#%02X%02X%02X" % lerp(hex2rgb(blue), (255, 255, 255), 0.18)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{l}"/>
      <stop offset="1" stop-color="{blue}"/>
    </linearGradient>
  </defs>
  <rect width="1024" height="1024" rx="231" ry="231" fill="url(#bg)"/>
{svg_emblem_group(512, 512, 1024 * (1 - 2 * 0.185) * 0.9 / 1024 * 1024 / 1024, "#FFFFFF", orange)}
</svg>
'''


def svg_banner(colors, text):
    blue = colors["primary"]
    orange = colors["accent"]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 240" width="900" height="240">
  <rect width="900" height="240" fill="none"/>
{svg_emblem_group(120, 120, 150/63*63/1024, blue, orange)}
  <text x="866" y="136" text-anchor="end" font-family="Vazirmatn, Tahoma, sans-serif"
        font-size="46" font-weight="700" fill="{blue}" direction="rtl">{text}</text>
</svg>
'''


def write_icns(master, path):
    chunks = [(b"ic07", 128), (b"ic08", 256), (b"ic09", 512),
              (b"ic11", 32), (b"ic12", 64), (b"ic13", 256), (b"ic14", 512)]
    body = b""
    for typ, size in chunks:
        tmp = os.path.join(OUT_DIR, f"_tmp_{size}.png")
        master.resize((size, size), Image.LANCZOS).save(tmp, "PNG")
        with open(tmp, "rb") as f:
            data = f.read()
        os.remove(tmp)
        body += typ + struct.pack(">I", len(data) + 8) + data
    with open(path, "wb") as f:
        f.write(b"icns" + struct.pack(">I", len(body) + 8) + body)


def main():
    brand = load_brand()
    colors = brand["colors"]
    company_fa = brand.get("company_fa") or brand.get("app_name_fa", "")
    os.makedirs(OUT_DIR, exist_ok=True)

    blue = hex2rgb(colors["primary"])
    orange = hex2rgb(colors["accent"])

    # نشان خالص با رنگ‌های موسسه (روی زمینه‌ی روشن)
    emblem_color = draw_emblem(1024, blue, orange)
    emblem_white = draw_emblem(1024, (255, 255, 255, 255), orange)
    emblem_solid = draw_emblem(1024, (255, 255, 255, 255), (255, 255, 255, 255))

    # آیکون برنامه
    master = draw_icon(1024, colors)
    custom = os.path.join(BRAND_DIR, "custom", "icon.png")
    if os.path.exists(custom):
        master = Image.open(custom).convert("RGBA").resize((1024, 1024), Image.LANCZOS)
        print("using custom logo:", custom)
    master.save(os.path.join(OUT_DIR, "icon.png"))
    emblem_color.save(os.path.join(OUT_DIR, "emblem.png"))
    emblem_white.save(os.path.join(OUT_DIR, "emblem_white.png"))

    for s in (16, 24, 32, 48, 64, 128, 256, 512):
        master.resize((s, s), Image.LANCZOS).save(os.path.join(OUT_DIR, f"{s}x{s}.png"))

    master.resize((32, 32), Image.LANCZOS).save(os.path.join(OUT_DIR, "32x32.png"))
    master.resize((64, 64), Image.LANCZOS).save(os.path.join(OUT_DIR, "64x64.png"))
    master.resize((128, 128), Image.LANCZOS).save(os.path.join(OUT_DIR, "128x128.png"))
    master.resize((256, 256), Image.LANCZOS).save(os.path.join(OUT_DIR, "128x128@2x.png"))
    master.resize((512, 512), Image.LANCZOS).save(os.path.join(OUT_DIR, "mac-icon.png"))

    ico_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    master.save(os.path.join(OUT_DIR, "icon.ico"), sizes=ico_sizes)
    master.save(os.path.join(OUT_DIR, "app_icon.ico"), sizes=ico_sizes)
    master.save(os.path.join(OUT_DIR, "tray-icon.ico"), sizes=[(16, 16), (24, 24), (32, 32), (48, 48)])
    # ترک‌بار مک: تصویر تک‌رنگ (قالب)
    tray_mac = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    tray_mac.alpha_composite(emblem_solid.resize((64, 64), Image.LANCZOS))
    tray_mac.save(os.path.join(OUT_DIR, "tray_mac_template.png"))

    # لوگوی داخل برنامه: فقط نشان.
    # دلیل بررسی‌شده: رابط کاربری این لوگو را حداکثر ۳۰۰×۶۰ نشان می‌دهد؛
    # متن نام در آن اندازه ریز و ناخوانا می‌شد، پس نام حذف شد و نشان
    # در اندازهٔ کامل و واضح دیده می‌شود. نام برنامه در نوار بالا و
    # عنوان پنجره به‌هر‌حال هست.
    for nm, em in (("logo.png", emblem_color),
                   ("logo_light.png", emblem_color),
                   ("logo_dark.png", emblem_white)):
        em.resize((512, 512), Image.LANCZOS).save(os.path.join(OUT_DIR, nm))
    # نسخهٔ ۳۰۰×۶۰ دقیقاً هم‌اندازهٔ قاب رابط کاربری، برای پیش‌نمایش
    for nm, em in (("logo_300x60.png", emblem_color),
                   ("logo_dark_300x60.png", emblem_white)):
        sq = em.resize((60, 60), Image.LANCZOS)
        canvas = Image.new("RGBA", (300, 60), (0, 0, 0, 0))
        canvas.alpha_composite(sq, (0, 0))
        canvas.save(os.path.join(OUT_DIR, nm))

    # لوگوی کامل (نشان + نام) برای اسناد، سرصفحه، پاورپوینت و فایل نصبی
    blue_ink = tuple(blue) + (255,)
    white_ink = (255, 255, 255, 255)
    draw_lockup(emblem_color, company_fa, blue_ink, height=320).save(
        os.path.join(OUT_DIR, "logo_full.png"))
    draw_lockup(emblem_white, company_fa, white_ink, height=320).save(
        os.path.join(OUT_DIR, "logo_full_dark.png"))
    draw_lockup(emblem_color, company_fa, blue_ink, target_size=(900, 180)).save(
        os.path.join(OUT_DIR, "logo_with_name.png"))
    draw_lockup(emblem_white, company_fa, white_ink, target_size=(900, 180)).save(
        os.path.join(OUT_DIR, "logo_with_name_dark.png"))

    # برداری
    with open(os.path.join(OUT_DIR, "icon.svg"), "w", encoding="utf-8") as f:
        f.write(svg_icon(colors))
    with open(os.path.join(OUT_DIR, "scalable.svg"), "w", encoding="utf-8") as f:
        f.write(svg_icon(colors))
    for name in ("logo.svg", "logo-header.svg", "rustdesk-banner.svg"):
        with open(os.path.join(OUT_DIR, name), "w", encoding="utf-8") as f:
            f.write(svg_banner(colors, company_fa))

    write_icns(master, os.path.join(OUT_DIR, "AppIcon.icns"))

    # اندروید
    for dpi, s in {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}.items():
        ic = master.resize((s, s), Image.LANCZOS)
        ic.save(os.path.join(OUT_DIR, f"android_ic_launcher_{dpi}.png"))
        ic.save(os.path.join(OUT_DIR, f"android_ic_launcher_round_{dpi}.png"))
        canvas_s = int(s * 108 / 48)
        fg = Image.new("RGBA", (canvas_s, canvas_s), (0, 0, 0, 0))
        inner = master.resize((int(canvas_s * 0.62), int(canvas_s * 0.62)), Image.LANCZOS)
        fg.alpha_composite(inner, ((canvas_s - inner.width) // 2,
                                   (canvas_s - inner.height) // 2))
        fg.save(os.path.join(OUT_DIR, f"android_ic_launcher_foreground_{dpi}.png"))
        # آیکون وضعیت اندروید: تک‌رنگ سفید
        emblem_solid.resize((s, s), Image.LANCZOS).save(
            os.path.join(OUT_DIR, f"android_ic_stat_logo_{dpi}.png"))

    # آی‌اواس
    ios = {
        "Icon-App-20x20@1x.png": 20, "Icon-App-20x20@2x.png": 40, "Icon-App-20x20@3x.png": 60,
        "Icon-App-29x29@1x.png": 29, "Icon-App-29x29@2x.png": 58, "Icon-App-29x29@3x.png": 87,
        "Icon-App-40x40@1x.png": 40, "Icon-App-40x40@2x.png": 80, "Icon-App-40x40@3x.png": 120,
        "Icon-App-60x60@2x.png": 120, "Icon-App-60x60@3x.png": 180,
        "Icon-App-76x76@1x.png": 76, "Icon-App-76x76@2x.png": 152,
        "Icon-App-83.5x83.5@2x.png": 167, "Icon-App-1024x1024@1x.png": 1024,
    }
    for name, s in ios.items():
        master.resize((s, s), Image.LANCZOS).save(os.path.join(OUT_DIR, f"ios_{name}"))

    print("ساخته شد در:", OUT_DIR)
    print("تعداد فایل:", len(os.listdir(OUT_DIR)))


if __name__ == "__main__":
    main()
