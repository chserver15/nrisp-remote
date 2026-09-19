#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اعمال هویت بصری شرکت روی سورس راست‌دسک.

این اسکریپت هیچ چیزی را حدس نمی‌زند: هر تغییر را با متن دقیق پیدا می‌کند،
اعمال می‌کند و در پایان گزارش می‌دهد چه چیزی عوض شد و چه چیزی پیدا نشد.
اجرای دوباره‌ی آن بی‌خطر است (تغییرات تکراری اعمال نمی‌شوند).

نمونه اجرا:
    python3 branding/tools/apply_branding.py --repo ../rustdesk
    python3 branding/tools/apply_branding.py --repo ../rustdesk --check-only
    python3 branding/tools/apply_branding.py --repo ../rustdesk --rename-exe --android-package
"""

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BRAND_DIR = HERE.parent
OUT_DIR = BRAND_DIR / "out"

# نتایج ممکن برای هر تغییر
OK = "OK"          # اعمال شد
DONE = "DONE"      # قبلاً اعمال شده بود
MISS = "MISS"      # متن پیدا نشد (نسخه‌ی سورس متفاوت است)
SKIP = "SKIP"      # عمداً رد شد


class Report:
    def __init__(self):
        self.rows = []

    def add(self, status, where, detail=""):
        self.rows.append((status, where, detail))

    def count(self, status):
        return sum(1 for r in self.rows if r[0] == status)

    def dump(self):
        marks = {OK: "[+]", DONE: "[=]", MISS: "[!]", SKIP: "[-]"}
        for status, where, detail in self.rows:
            line = f"{marks.get(status, '[?]')} {where}"
            if detail:
                line += f"  ->  {detail}"
            print(line)
        print("\n--- summary ---")
        print(f"applied: {self.count(OK)}   already: {self.count(DONE)}   "
              f"not found: {self.count(MISS)}   skipped: {self.count(SKIP)}")
        if self.count(MISS):
            print("NOTE: 'not found' entries usually mean the upstream source changed; "
                  "check them by hand, they are listed above.")


REPORT = Report()
PRIMARY = "#0E3091"  # مقدار پیش‌فرض؛ از branding.json به‌روز می‌شود


# ---------------------------------------------------------------- helpers

def read_text(p: Path):
    with open(p, encoding="utf-8") as f:
        return f.read()


def write_text(p: Path, s: str):
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(s)


def edit(path: Path, pairs, label=None):
    """جایگزینی متن دقیق؛ هر جفت (قدیم، جدید) جداگانه گزارش می‌شود"""
    label = label or str(path.name)
    if not path.exists():
        REPORT.add(MISS, label, f"file missing: {path}")
        return
    src = read_text(path)
    out = src
    for old, new in pairs:
        if old == new:
            continue
        if isinstance(new, str) and new in out and old not in out:
            REPORT.add(DONE, label, short(new))
            continue
        if old not in out:
            REPORT.add(MISS, label, short(old))
            continue
        out = out.replace(old, new)
        REPORT.add(OK, label, short(new))
    if out != src:
        write_text(path, out)


def short(s, n=64):
    if not isinstance(s, str):
        s = getattr(s, "__name__", repr(s))
    s = " ".join(s.split())
    return s if len(s) <= n else s[: n - 3] + "..."


def rx_edit(path: Path, pattern, repl, label=None, expect=1, flags=0):
    """جایگزینی الگویابی، مناسب وقتی مقدار متغیر است"""
    label = label or str(path.name)
    if not path.exists():
        REPORT.add(MISS, label, f"file missing: {path}")
        return
    src = read_text(path)
    new, n = re.subn(pattern, repl, src, flags=flags)
    if n == 0:
        REPORT.add(MISS, label, short(pattern))
        return
    if src == new:
        REPORT.add(DONE, label, short(repl))
        return
    write_text(path, new)
    REPORT.add(OK, label, f"{n} place(s)")


def copy_asset(src: Path, dst: Path, label=None):
    label = label or str(dst.name)
    if not src.exists():
        REPORT.add(MISS, label, f"missing source asset: {src}")
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    REPORT.add(OK, label)


# ---------------------------------------------------------------- sections

def apply_assets(repo: Path):
    print("\n== assets / icons ==")
    pairs = [
        ("icon.png", "res/icon.png"),
        ("icon.ico", "res/icon.ico"),
        ("tray-icon.ico", "res/tray-icon.ico"),
        ("32x32.png", "res/32x32.png"),
        ("64x64.png", "res/64x64.png"),
        ("128x128.png", "res/128x128.png"),
        ("128x128@2x.png", "res/128x128@2x.png"),
        ("mac-icon.png", "res/mac-icon.png"),
        ("scalable.svg", "res/scalable.svg"),
        ("logo.svg", "res/logo.svg"),
        ("logo-header.svg", "res/logo-header.svg"),
        ("rustdesk-banner.svg", "res/rustdesk-banner.svg"),
        ("app_icon.ico", "flutter/windows/runner/resources/app_icon.ico"),
        ("AppIcon.icns", "flutter/macos/Runner/AppIcon.icns"),
        # دارایی‌های داخل رابط کاربری
        ("logo.png", "flutter/assets/logo.png"),
        ("logo_light.png", "flutter/assets/logo_light.png"),
        ("logo_dark.png", "flutter/assets/logo_dark.png"),
        ("icon.png", "flutter/assets/icon.png"),
        ("icon.svg", "flutter/assets/icon.svg"),
    ]
    for src_name, dst_rel in pairs:
        copy_asset(OUT_DIR / src_name, repo / dst_rel)

    # آیکون‌های اندروید
    for dpi in ("mdpi", "hdpi", "xhdpi", "xxhdpi", "xxxhdpi"):
        base = f"flutter/android/app/src/main/res/mipmap-{dpi}"
        for kind in ("ic_launcher", "ic_launcher_round", "ic_launcher_foreground"):
            copy_asset(OUT_DIR / f"android_{kind}_{dpi}.png", repo / f"{base}/{kind}.png")
        copy_asset(OUT_DIR / f"android_ic_stat_logo_{dpi}.png", repo / f"{base}/ic_stat_logo.png")

    # آیکون‌های آی‌اواس
    ios_dir = repo / "flutter/ios/Runner/Assets.xcassets/AppIcon.appiconset"
    if ios_dir.exists():
        for f in ios_dir.glob("Icon-App-*.png"):
            cand = OUT_DIR / f"ios_{f.name}"
            if cand.exists():
                copy_asset(cand, f)
    else:
        REPORT.add(MISS, "ios AppIcon", "folder not found")

    # آیکون ترک‌بار مک: باید تک‌رنگ (قالب) باشد تا مک خودش رنگ‌آمیزی کند
    copy_asset(OUT_DIR / "tray_mac_template.png", repo / "res/mac-tray-dark-x2.png")
    copy_asset(OUT_DIR / "tray_mac_template.png", repo / "res/mac-tray-light-x2.png")


def apply_metadata(repo: Path, brand, rename_exe: bool):
    print("\n== app metadata ==")
    app = brand["app_name_en"]
    # نام نصب‌شوندگی: نصب‌کننده فقط [a-zA-Z0-9-] را می‌پذیرد، پس نام بدون فاصله لازم است
    safe = brand.get("app_name_safe") or app
    exe = brand["exe_name"]
    scheme = brand.get("url_scheme") or exe
    company = brand["company_en"]
    year = brand.get("copyright_year", "")
    copyright_line = f"Copyright © {year} {company}. All rights reserved."
    desc = brand.get("file_description") or app

    # Cargo.toml
    edit(repo / "Cargo.toml", [
        ('name = "RustDesk"\nidentifier = "com.carriez.rustdesk"',
         f'name = "{safe}"\nidentifier = "{brand["app_identifier"]}"'),
        ('description = "RustDesk Remote Desktop"', f'description = "{desc}"'),
    ])

    # نام نمایشی برنامه (سراسری در کد راست)
    cfg = repo / "libs/hbb_common/src/config.rs"
    rx_edit(cfg, r'APP_NAME: RwLock<String> = RwLock::new\("[^"]*"\.to_owned\(\)\)',
            f'APP_NAME: RwLock<String> = RwLock::new("{safe}".to_owned())',
            label="config.rs (APP_NAME)")

    # سرور و کلید عمومی
    # حالت پیش‌فرض: خالی بودن هر دو یعنی از سرورهای عمومی خودِ راست‌دسک استفاده شود.
    # اگر روزی سرور اختصاصی گرفتید، این دو مقدار را پر کنید و اسکریپت را دوباره اجرا کنید.
    server = (brand.get("server") or "").strip()
    pubkey = (brand.get("public_key") or "").strip()
    placeholder_key = "PASTE_ID_ED25519_PUB_HERE"
    if server and pubkey and pubkey != placeholder_key:
        rx_edit(cfg, r'RENDEZVOUS_SERVERS: &\[&str\] = &\["[^"]*"\]',
                f'RENDEZVOUS_SERVERS: &[&str] = &["{server}"]',
                label="config.rs (RENDEZVOUS_SERVERS)")
        rx_edit(cfg, r'RS_PUB_KEY: &str = "[^"]*"', f'RS_PUB_KEY: &str = "{pubkey}"',
                label="config.rs (RS_PUB_KEY)")
    else:
        REPORT.add(SKIP, "config.rs (server settings)",
                   "خالی است → سرورهای عمومی راست‌دسک استفاده می‌شود")

    # ویندوز: عنوان پنجره و اطلاعات فایل اجرایی
    if app.isascii():
        edit(repo / "flutter/windows/runner/main.cpp",
             [('std::wstring app_name = L"RustDesk";',
               f'std::wstring app_name = L"{safe}";')])
    else:
        REPORT.add(SKIP, "main.cpp", "app_name_en must be ASCII")

    rc_pairs = [
        ('VALUE "CompanyName", "Purslane Tech Pte. Ltd." "\\0"',
         f'VALUE "CompanyName", "{company}" "\\0"'),
        ('VALUE "FileDescription", "RustDesk Remote Desktop" "\\0"',
         f'VALUE "FileDescription", "{desc}" "\\0"'),
        ('VALUE "ProductName", "RustDesk" "\\0"',
         f'VALUE "ProductName", "{app}" "\\0"'),
        ('VALUE "InternalName", "rustdesk" "\\0"',
         f'VALUE "InternalName", "{exe}" "\\0"'),
    ]
    m = re.search(r'VALUE "LegalCopyright", "([^"]*)"', read_text(repo / "flutter/windows/runner/Runner.rc"))
    if m:
        rc_pairs.append((f'VALUE "LegalCopyright", "{m.group(1)}" "\\0"',
                         f'VALUE "LegalCopyright", "{copyright_line}" "\\0"'))
    if rename_exe:
        rc_pairs.append(('VALUE "OriginalFilename", "rustdesk.exe" "\\0"',
                         f'VALUE "OriginalFilename", "{exe}.exe" "\\0"'))
    edit(repo / "flutter/windows/runner/Runner.rc", rc_pairs)

    # لینوکس
    edit(repo / "flutter/linux/my_application.cc", [
        ('gtk_header_bar_set_title(header_bar, "rustdesk");',
         f'gtk_header_bar_set_title(header_bar, "{exe}");'),
        ('gtk_window_set_title(window, "rustdesk");',
         f'gtk_window_set_title(window, "{exe}");'),
        ('gtk_icon_theme_load_icon(theme, "rustdesk",',
         f'gtk_icon_theme_load_icon(theme, "{exe}",'),
    ])

    # فایل‌های میان‌بر و سرویس لینوکس
    edit(repo / "res/rustdesk.desktop", [
        ("Name=RustDesk", f"Name={app}"),
        ("Exec=rustdesk %u", f"Exec={exe} %u"),
        ("Icon=rustdesk", f"Icon={exe}"),
        ("StartupWMClass=rustdesk", f"StartupWMClass={exe}"),
    ])
    edit(repo / "res/rustdesk.service", [("Description=RustDesk", f"Description={app}")])
    # فایل لینک عمیق لینوکس (طرح‌واره‌ی اختصاصی شرکت)
    edit(repo / "res/rustdesk-link.desktop", [
        ("Name=RustDesk", f"Name={app}"),
        ("MimeType=x-scheme-handler/rustdesk;",
         f"MimeType=x-scheme-handler/{scheme};"),
        ("TryExec=rustdesk", f"TryExec={exe}"),
        ("Exec=rustdesk %u", f"Exec={exe} %u"),
        ("Icon=rustdesk", f"Icon={exe}"),
        ("StartupWMClass=rustdesk", f"StartupWMClass={exe}"),
    ])
    # طرح‌واره‌ی لینک عمیق در کد راست
    edit(repo / "src/common.rs", [
        ('format!("{}://", get_app_name().to_lowercase())',
         f'format!("{{}}://", "{scheme}")'),
    ], label="src/common.rs (URI scheme)")

    # مک
    mac = repo / "flutter/macos/Runner/Configs/AppInfo.xcconfig"
    if mac.exists():
        rx_edit(mac, r"PRODUCT_NAME = .*", f"PRODUCT_NAME = {app}", label="AppInfo.xcconfig")
        rx_edit(mac, r"PRODUCT_BUNDLE_IDENTIFIER = .*",
                f"PRODUCT_BUNDLE_IDENTIFIER = {brand['app_identifier']}",
                label="AppInfo.xcconfig")
        rx_edit(mac, r"PRODUCT_COPYRIGHT = .*", f"PRODUCT_COPYRIGHT = {copyright_line}",
                label="AppInfo.xcconfig")

    # ساخت dmg مک هم نام برنامه را دنبال کند + آیکون‌های نصب لینوکس
    build_py = repo / "build.py"
    if build_py.exists():
        edit(build_py, [
            ("apps/rustdesk.png", f"apps/{exe}.png"),
            ("apps/rustdesk.svg", f"apps/{exe}.svg"),
            ('--volname \\"RustDesk Installer\\"', f'--volname \\"{app} Installer\\"'),
            ('--icon RustDesk.app 200 190 --hide-extension RustDesk.app rustdesk.dmg',
             f'--icon {app}.app 200 190 --hide-extension {app}.app {exe}.dmg'),
            ('./build/macos/Build/Products/Release/RustDesk.app',
             f'./build/macos/Build/Products/Release/{app}.app'),
        ], label="build.py (macOS dmg)")


def apply_mobile(repo: Path, brand, android_package: bool):
    print("\n== mobile labels ==")
    app = brand["app_name_en"]
    scheme = brand.get("url_scheme") or brand["exe_name"]

    edit(repo / "flutter/android/app/src/main/AndroidManifest.xml", [
        ('android:label="RustDesk"', f'android:label="{app}"'),
        ('android:label="RustDesk Input"', f'android:label="{app} Input"'),
        ('<data android:scheme="rustdesk" />',
         f'<data android:scheme="{scheme}" />'),
    ])

    plist = repo / "flutter/ios/Runner/Info.plist"
    rx_edit(plist,
            r"(<key>CFBundleDisplayName</key>\s*<string>)[^<]*(</string>)",
            lambda m: m.group(1) + app + m.group(2),
            label="Info.plist (DisplayName)")
    rx_edit(plist,
            r"(<key>CFBundleName</key>\s*<string>)[^<]*(</string>)",
            lambda m: m.group(1) + app + m.group(2),
            label="Info.plist (BundleName)")
    rx_edit(plist,
            r"(<key>CFBundleURLSchemes</key>\s*<array>\s*<string>)[^<]*(</string>)",
            lambda m: m.group(1) + scheme + m.group(2),
            label="Info.plist (URL scheme)")
    rx_edit(plist,
            r"(<key>CFBundleURLName</key>\s*<string>)[^<]*(</string>)",
            lambda m: m.group(1) + brand["app_identifier"] + m.group(2),
            label="Info.plist (URL name)")

    gradle = repo / "flutter/android/app/build.gradle"
    if android_package:
        pkg = brand["app_identifier"].replace("-", "_")
        edit(gradle, [
            ('applicationId "com.carriez.flutter_hbb"', f'applicationId "{pkg}"'),
            ('namespace "com.carriez.flutter_hbb"', f'namespace "{pkg}"'),
        ], label="android build.gradle")
        # جابه‌جایی پوشه‌ی کد کاتلین و تغییر نام بسته
        old_dir = repo / "flutter/android/app/src/main/kotlin/com/carriez/flutter_hbb"
        new_dir = repo / "flutter/android/app/src/main/kotlin" / Path(*pkg.split("."))
        if old_dir.exists() and not new_dir.exists():
            new_dir.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(old_dir), str(new_dir))
            REPORT.add(OK, "android kotlin package folder", str(new_dir.relative_to(repo)))
            for kt in new_dir.glob("*.kt"):
                txt = read_text(kt)
                if "package com.carriez.flutter_hbb" in txt:
                    write_text(kt, txt.replace("package com.carriez.flutter_hbb", f"package {pkg}"))
                    REPORT.add(OK, f"kotlin package line: {kt.name}")
        elif new_dir.exists():
            REPORT.add(DONE, "android kotlin package folder")
        else:
            REPORT.add(MISS, "android kotlin package folder", str(old_dir))
        # شناسه‌ی بسته در آی‌اواس
        pbx = repo / "flutter/ios/Runner.xcodeproj/project.pbxproj"
        if pbx.exists():
            edit(pbx, [("com.carriez.flutterHbb", brand["app_identifier"])], label="Runner.xcodeproj")
    else:
        REPORT.add(SKIP, "android/ios package id", "use --android-package to change it")


def apply_flutter_strings(repo: Path):
    print("\n== in-app visible strings ==")
    # عنوان نوار بالای پنجره‌ی اصلی که در دارت ثابت نوشته شده بود
    # عنوان نوار بالا در nrisp_ui.py با نام فارسی گذاشته می‌شود


def apply_exe_rename(repo: Path, brand, enabled: bool):
    print("\n== executable file name ==")
    if not enabled:
        REPORT.add(SKIP, "exe name", "use --rename-exe to rename rustdesk.exe")
        return
    exe = brand["exe_name"]
    edit(repo / "flutter/windows/CMakeLists.txt",
         [('set(BINARY_NAME "rustdesk")', f'set(BINARY_NAME "{exe}")')])
    edit(repo / "flutter/linux/CMakeLists.txt",
         [('set(BINARY_NAME "rustdesk")', f'set(BINARY_NAME "{exe}")')])
    # نام بستهٔ Cargo عمداً عوض نمی‌شود:
    # ساخت با پرچم --locked انجام می‌شود و Cargo.lock نام بستهٔ اصلی را
    # ثبت کرده است؛ با تغییر آن، قفل ناهمخوان می‌شود و ساخت متوقف می‌شود.
    # نام دیده‌شدهٔ برنامه از CMakeLists، Runner.rc و رشته‌های سورس می‌آید، نه از نام بسته.
    REPORT.add(SKIP, "Cargo.toml (package name)",
               "نام بستهٔ راست دست‌نخورده ماند تا Cargo.lock با --locked معتبر بماند")
    edit(repo / "build.py", [
        ("hbb_name = 'rustdesk'", f"hbb_name = '{exe}'"),
        ("-e ../../{flutter_build_dir_2}/rustdesk.exe",
         f"-e ../../{{flutter_build_dir_2}}/{exe}.exe"),
        ("-e ../../{res_dir}/rustdesk-", f"-e ../../{{res_dir}}/{exe}-"),
    ], label="build.py (exe name)")


def verify(repo: Path, brand):
    """گزارش نشانه‌های باقی‌مانده‌ی برند قبلی در جاهایی که کاربر می‌بیند"""
    print("\n== leftover check (user-visible places only) ==")
    targets = [
        "res/rustdesk.desktop", "res/rustdesk.service",
        "flutter/windows/runner/Runner.rc",
        "flutter/windows/runner/main.cpp",
        "flutter/linux/my_application.cc",
        "flutter/macos/Runner/Configs/AppInfo.xcconfig",
        "flutter/android/app/src/main/AndroidManifest.xml",
        "flutter/ios/Runner/Info.plist",
    ]
    hits = 0
    for rel in targets:
        p = repo / rel
        if not p.exists():
            continue
        for i, line in enumerate(read_text(p).splitlines(), 1):
            if "RustDesk" in line or "rustdesk" in line:
                # نام‌های داخلی که عمداً دست نخورده‌اند
                if rel.endswith("rustdesk.desktop") or rel.endswith("rustdesk.service"):
                    continue
                hits += 1
                print(f"  remaining: {rel}:{i}: {short(line.strip(), 80)}")
    if not hits:
        print("  clean - no user-visible old brand strings")
    print("\nNOTE: internal identifiers (RustDeskIdd, platform channels, librustdesk, "
          "service internals) are intentionally untouched; renaming them breaks the app.")


def apply_ui(repo: Path, brand, enabled: bool):
    """
    لایهٔ ظاهری اختصاصی موسسه:
      ۱) کپی پنل شناسهٔ دستگاه
      ۲) جایگزینی لوگو و تختهٔ شناسه و رمز در صفحهٔ اصلی با آن پنل
      ۳) تغییر رنگ‌های سراسری برنامه به رنگ‌های موسسه
      ۴) زیباتر کردن کارت اتصال
    """
    print("\n== custom UI layer ==")
    if not enabled:
        REPORT.add(SKIP, "custom UI", "use --ui to install the institute UI")
        return

    # ۱) کپی فایل پنل
    src = BRAND_DIR.parent / "ui" / "flutter" / "lib" / "nrisp" / "nrisp_id_panel.dart"
    dst = repo / "flutter" / "lib" / "nrisp" / "nrisp_id_panel.dart"
    copy_asset(src, dst)

    # ۲) صفحهٔ اصلی: چیدمان شبیه درسان — کارت اتصال در چپ، ستون شناسه در راست
    home = repo / "flutter/lib/desktop/pages/desktop_home_page.dart"
    edit(home, [
        # افزودن import
        ("import 'package:flutter_hbb/desktop/pages/connection_page.dart';",
         "import 'package:flutter_hbb/desktop/pages/connection_page.dart';\n"
         "import 'package:flutter_hbb/nrisp/nrisp_id_panel.dart';"),
        # جابه‌جایی دو ستون
        ("""    return _buildBlock(
        child: Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        buildLeftPane(context),
        if (!isIncomingOnly) const VerticalDivider(width: 1),
        if (!isIncomingOnly) Expanded(child: buildRightPane(context)),
      ],
    ));""",
         """    // چیدمان سازمان: کارت بزرگ اتصال در سمت چپ، ستون شناسه و تنظیمات در سمت راست
    return _buildBlock(
        child: Row(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        if (isIncomingOnly)
          Expanded(child: buildLeftPane(context))
        else ...[
          // در چیدمان راست‌به‌چپ، فرزند نخست سمت راست می‌نشیند
          const NrispIdPanel(),
          Expanded(child: buildRightPane(context)),
        ],
      ],
    ));"""),
    ], label="desktop_home_page.dart (چیدمان دو ستونی)")

    # ۳) رنگ‌های سراسری برنامه
    edit(repo / "flutter/lib/common.dart", [
        ("  static const Color accent = Color(0xFF0071FF);",
         f'  static const Color accent = Color(0xFF{PRIMARY.lstrip("#")});'),
        ("  static const Color accent50 = Color(0x770071FF);",
         f'  static const Color accent50 = Color(0x77{PRIMARY.lstrip("#")});'),
        ("  static const Color accent80 = Color(0xAA0071FF);",
         f'  static const Color accent80 = Color(0xAA{PRIMARY.lstrip("#")});'),
        ("  static const Color idColor = Color(0xFF00B6F0);",
         f'  static const Color idColor = Color(0xFF{PRIMARY.lstrip("#")});'),
        ("  static const Color button = Color(0xFF2C8CFF);",
         f'  static const Color button = Color(0xFF{PRIMARY.lstrip("#")});'),
    ], label="common.dart (theme colors)")

    # ۴) کارت اتصال: گوشه‌های گردتر و سایهٔ نرم
    edit(repo / "flutter/lib/desktop/pages/connection_page.dart", [
        ("""      decoration: BoxDecoration(
          borderRadius: const BorderRadius.all(Radius.circular(13)),
          border: Border.all(color: Theme.of(context).colorScheme.background)),""",
         """      decoration: BoxDecoration(
          color: Theme.of(context).scaffoldBackgroundColor,
          borderRadius: const BorderRadius.all(Radius.circular(18)),
          border: Border.all(color: Theme.of(context).colorScheme.background),
          boxShadow: [
            BoxShadow(
                color: Colors.black.withOpacity(0.05),
                blurRadius: 18,
                offset: const Offset(0, 5))
          ]),"""),
    ], label="connection_page.dart (connect card)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=str(BRAND_DIR.parent / "rustdesk"),
                    help="مسیر پوشه‌ی سورس راست‌دسک")
    ap.add_argument("--check-only", action="store_true", help="فقط بررسی، بدون تغییر")
    ap.add_argument("--rename-exe", action="store_true",
                    help="تغییر نام فایل اجرایی (نیاز به آزمایش ساخت دارد)")
    ap.add_argument("--android-package", action="store_true",
                    help="تغییر شناسه‌ی بسته‌ی اندروید و آی‌اواس")
    ap.add_argument("--ui", action="store_true",
                    help="نصب لایه‌ی ظاهری اختصاصی موسسه")
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    if not (repo / "Cargo.toml").exists() or not (repo / "flutter").exists():
        print(f"ERROR: not a rustdesk source folder: {repo}")
        sys.exit(1)

    with open(BRAND_DIR / "branding.json", encoding="utf-8") as f:
        brand = json.load(f)
    global PRIMARY
    PRIMARY = brand["colors"]["primary"]

    print(f"repo    : {repo}")
    print(f"app     : {brand['app_name_en']}  ({brand['app_name_fa']})")
    print(f"company : {brand['company_en']}")
    if args.check_only:
        print("\ncheck-only mode: nothing will be written")
        verify(repo, brand)
        return

    apply_assets(repo)
    apply_metadata(repo, brand, args.rename_exe)
    apply_mobile(repo, brand, args.android_package)
    apply_flutter_strings(repo)
    apply_ui(repo, brand, args.ui)
    apply_exe_rename(repo, brand, args.rename_exe)
    REPORT.dump()
    verify(repo, brand)


if __name__ == "__main__":
    main()
