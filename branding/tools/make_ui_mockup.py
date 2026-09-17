#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ساخت نمونهٔ ظاهر برنامه (صفحهٔ اصلی) به‌صورت HTML با فونت و نشان جاسازی‌شده.
خروجی در مرورگر یا در پیش‌نمایش باز می‌شود و ظاهر نهایی را نشان می‌دهد.

اجرا:  python3 branding/tools/make_ui_mockup.py
خروجی: branding/ui-mockup.html
"""

import base64
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BRAND_DIR = os.path.dirname(HERE)
OUT_DIR = os.path.join(BRAND_DIR, "out")
FONT_DIR = os.path.join(BRAND_DIR, "assets", "fonts")


def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def main():
    with open(os.path.join(BRAND_DIR, "branding.json"), encoding="utf-8") as f:
        brand = json.load(f)

    font_regular = b64(os.path.join(FONT_DIR, "Vazirmatn-Regular.ttf"))
    font_bold = b64(os.path.join(FONT_DIR, "Vazirmatn-Bold.ttf"))
    emblem = b64(os.path.join(OUT_DIR, "emblem.png"))

    blue = brand["colors"]["primary"]
    orange = brand["colors"]["accent"]

    html = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<title>نمونهٔ ظاهر برنامه — {brand['app_name_fa']}</title>
<style>
  @font-face {{ font-family: Vazirmatn; font-weight: 400;
    src: url(data:font/ttf;base64,{font_regular}) format('truetype'); }}
  @font-face {{ font-family: Vazirmatn; font-weight: 700;
    src: url(data:font/ttf;base64,{font_bold}) format('truetype'); }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background:#eef1f4; font-family:Vazirmatn,Tahoma,sans-serif;
    display:flex; align-items:center; justify-content:center; min-height:100vh; padding:24px; }}
  .window {{ width:1060px; height:640px; background:#fff; border-radius:14px;
    box-shadow:0 24px 60px rgba(20,40,70,.16); overflow:hidden;
    display:flex; flex-direction:column; direction:rtl; }}
  .titlebar {{ height:42px; background:#f8fafb; border-bottom:1px solid #e4ebf1;
    display:flex; align-items:center; gap:9px; padding:0 16px; }}
  .titlebar img {{ width:18px; height:18px; }}
  .titlebar .name {{ font-size:12.5px; font-weight:700; color:#16222e; }}
  .body {{ flex:1; display:flex; }}
  /* ---------- پنل چپ ---------- */
  .pane {{ width:230px; background:#efeff2; border-left:1px solid #e4ebf1;
    padding:18px 14px; display:flex; flex-direction:column; }}
  .brand {{ display:flex; align-items:center; gap:9px; padding:0 2px 14px; }}
  .brand img {{ width:26px; height:26px; }}
  .brand .t1 {{ font-size:12.5px; font-weight:700; color:#16222e; line-height:1.35; }}
  .brand .t2 {{ font-size:9.5px; color:#7a8a98; line-height:1.35; }}
  .card {{ background:#fff; border:1px solid #e4ebf1; border-radius:16px;
    box-shadow:0 6px 18px rgba(20,40,70,.06); padding:13px 14px 11px; text-align:center; }}
  .card .lbl {{ font-size:10.5px; color:#7a8a98; }}
  .card .id {{ font-size:26px; font-weight:700; color:{blue}; letter-spacing:1.6px;
    direction:ltr; margin:4px 0 9px; }}
  .copy {{ display:inline-flex; align-items:center; gap:6px; background:#eef3fb;
    color:{blue}; font-size:11px; font-weight:700; padding:5px 12px; border-radius:20px; cursor:pointer; }}
  .pw {{ margin-top:10px; background:#f3f7fc; border-radius:12px; padding:9px 12px;
    display:flex; align-items:center; justify-content:space-between; }}
  .pw .l {{ font-size:9.5px; color:#7a8a98; }}
  .pw .v {{ font-size:15px; font-weight:700; letter-spacing:3px; direction:ltr; color:#16222e; }}
  .pw .r {{ font-size:14px; color:#7a8a98; }}
  .status {{ display:flex; align-items:center; gap:8px; margin:16px 4px 0; }}
  .dot {{ width:8px; height:8px; border-radius:50%; background:#1e9e6a; }}
  .status span {{ font-size:11.5px; color:#16222e; }}
  .settings {{ margin-top:14px; background:#fff; border:1px solid #e4ebf1; border-radius:12px;
    padding:11px; text-align:center; font-size:12.5px; font-weight:700; color:#16222e; cursor:pointer; }}
  .site {{ margin-top:auto; text-align:center; font-size:10px; color:#7a8a98; direction:ltr; }}
  /* ---------- پنل راست ---------- */
  .main {{ flex:1; padding:34px 40px; display:flex; flex-direction:column; }}
  .connect {{ background:#fff; border:1px solid #e4ebf1; border-radius:18px;
    box-shadow:0 10px 26px rgba(20,40,70,.07); padding:24px 26px 22px; width:620px; margin:0 auto; }}
  .connect h2 {{ font-size:15px; font-weight:700; color:#16222e; text-align:center; margin-bottom:18px; }}
  .input {{ background:#f6f8fa; border:1px solid #e4ebf1; border-radius:11px;
    height:48px; display:flex; align-items:center; padding:0 16px;
    font-size:13px; color:#aab6c2; direction:ltr; justify-content:flex-end; }}
  .row {{ display:flex; gap:12px; margin-top:14px; }}
  .btn {{ border:none; border-radius:12px; height:44px; font-family:inherit;
    font-size:13px; font-weight:700; cursor:pointer; }}
  .btn-primary {{ background:{orange}; color:#fff; width:110px; }}
  .btn-ghost {{ background:#eef3fb; color:{blue}; flex:0 0 auto; padding:0 18px; }}
  .recent {{ width:620px; margin:26px auto 0; }}
  .recent h3 {{ font-size:13px; font-weight:700; color:#16222e; margin-bottom:12px; }}
  .item {{ background:#fff; border:1px solid #e4ebf1; border-radius:12px;
    padding:12px 14px; display:flex; align-items:center; gap:12px; margin-bottom:9px; }}
  .avatar {{ width:30px; height:30px; border-radius:9px; background:#eef3fb; }}
  .item .nm {{ font-size:12.5px; font-weight:700; color:#16222e; }}
  .item .di {{ font-size:10.5px; color:#7a8a98; direction:ltr; }}
  .item .go {{ margin-right:auto; font-size:11.5px; color:{blue}; font-weight:700; }}
</style>
</head>
<body>
<div class="window">
  <div class="titlebar">
    <img src="data:image/png;base64,{emblem}" alt="">
    <span class="name">NRISP Remote Access</span>
  </div>
  <div class="body">
    <div class="pane">
      <div class="brand">
        <img src="data:image/png;base64,{emblem}" alt="">
        <div>
          <div class="t1">دسترسی راه دور</div>
          <div class="t2">موسسه تحقیقات سیاست علمی کشور</div>
        </div>
      </div>

      <div class="card">
        <div class="lbl">شناسهٔ این دستگاه</div>
        <div class="id">482 913 705</div>
        <div class="copy">کپی شناسه</div>
      </div>

      <div class="pw">
        <div class="r">↻</div>
        <div>
          <div class="l">رمز یک‌بارمصرف</div>
          <div class="v">641820</div>
        </div>
      </div>

      <div class="status">
        <div class="dot"></div>
        <span>آمادهٔ دریافت اتصال</span>
      </div>

      <div class="settings">تنظیمات</div>

      <div class="site">nrisp.ac.ir</div>
    </div>

    <div class="main">
      <div class="connect">
        <h2>برای اتصال، شناسهٔ دستگاه مقابل را وارد کنید</h2>
        <div class="input">شناسهٔ دستگاه</div>
        <div class="row">
          <button class="btn btn-primary">اتصال</button>
          <button class="btn btn-ghost">انتقال فایل</button>
          <button class="btn btn-ghost">نمایش فقط</button>
        </div>
      </div>

      <div class="recent">
        <h3>دستگاه‌های اخیر</h3>
        <div class="item">
          <div class="avatar"></div>
          <div>
            <div class="nm">سرور آزمایشگاه</div>
            <div class="di">318 774 026</div>
          </div>
          <div class="go">اتصال</div>
        </div>
        <div class="item">
          <div class="avatar"></div>
          <div>
            <div class="nm">رایانهٔ دبیرخانه</div>
            <div class="di">905 112 448</div>
          </div>
          <div class="go">اتصال</div>
        </div>
      </div>
    </div>
  </div>
</div>
</body>
</html>
"""
    out = os.path.join(BRAND_DIR, "ui-mockup.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("ساخته شد:", out, f"({len(html)//1024} کیلوبایت)")


if __name__ == "__main__":
    main()
