# -*- coding: utf-8 -*-
"""
زیباسازی و فارسی‌سازی کامل رابط کاربری نرم‌افزار موسسه.

این اسکریپت پس از apply_branding.py روی سورس راست‌دسک اجرا می‌شود و:
  ۱) زبان پیش‌فرض برنامه را فارسی می‌کند (همهٔ نوشته‌ها فارسی می‌شوند)
  ۲) چیدمان را راست‌به‌چپ می‌کند
  ۳) رنگ‌های سراسری برنامه را به رنگ‌های سازمانی موسسه تغییر می‌دهد
  ۴) نام نمایشی «RustDesk» را از نوار بالای پنجره برمی‌دارد
  ۵) نشان «powered by» را از صفحهٔ اصلی حذف می‌کند
  ۶) نشانی‌های rustdesk.com را با نشانی موسسه عوض می‌کند

اجرا:
    python nrisp_ui.py --repo ../rustdesk
"""

import argparse
import io
import sys
from pathlib import Path

OK = '[+]'
MISS = '[!]'
SKIP = '[-]'
rows = []


def note(kind, where, detail=''):
    rows.append((kind, where, detail))
    print(f'{kind} {where}' + (f'   ->  {detail}' if detail else ''))


def read(p: Path):
    with io.open(p, encoding='utf-8') as f:
        return f.read()


def write(p: Path, s: str):
    with io.open(p, 'w', encoding='utf-8', newline='') as f:
        f.write(s)


def edit(p: Path, pairs, label=None, required=False):
    """جایگزینی متن دقیق؛ اگر لازم باشد، نبودِ متن خطای واضح می‌دهد."""
    label = label or p.name
    if not p.exists():
        note(MISS, label, f'فایل موجود نیست: {p}')
        return
    s = read(p)
    changed = 0
    for old, new in pairs:
        if old and old in s:
            s = s.replace(old, new)
            changed += 1
        elif new and new in s:
            note(SKIP, label, 'از قبل اعمال شده')
        else:
            note(MISS, label, f'پیدا نشد: {old[:60]}')
    if changed:
        write(p, s)
        note(OK, label, f'{changed} تغییر')


def restyle_theme(repo: Path):
    """رنگ‌های سراسری برنامه"""
    p = repo / 'flutter/lib/common.dart'
    if not p.exists():
        note(MISS, 'common.dart', 'فایل نیست')
        return
    edit(p, [
        ('static const Color grayBg = Color(0xFFEFEFF2);',
         'static const Color grayBg = Color(0xFFF3F6FC);'),
        ('static const Color accent = Color(0xFF0071FF);',
         'static const Color accent = Color(0xFF0E3091);'),
        ('static const Color accent50 = Color(0x770071FF);',
         'static const Color accent50 = Color(0x770E3091);'),
        ('static const Color accent80 = Color(0xAA0071FF);',
         'static const Color accent80 = Color(0xAA0E3091);'),
        ('static const Color button = Color(0xFF2C8CFF);',
         'static const Color button = Color(0xFF0E3091);'),
        ('static const Color idColor = Color(0xFF00B6F0);',
         'static const Color idColor = Color(0xFFE89B25);'),
        ('primary: Colors.blue,', 'primary: const Color(0xFF0E3091),'),
    ], label='common.dart (رنگ‌های سازمانی)')


def persian_default(repo: Path):
    """زبان پیش‌فرض = فارسی، چیدمان راست‌به‌چپ"""
    # ۱) رشته‌های ترجمه از کتابخانهٔ فارسی خوانده شوند
    p = repo / 'flutter/lib/models/native_model.dart'
    if p.exists():
        edit(p, [
            ('  static get localeName => Platform.localeName;',
             "  static get localeName => 'fa';"),
        ], label='native_model.dart (زبان فارسی)')
    else:
        note(MISS, 'native_model.dart', 'فایل نیست')

    # ۲) جهت چیدمان کل برنامه راست‌به‌چپ شود
    m = repo / 'flutter/lib/main.dart'
    if m.exists():
        s = read(m)
        n = s.count('debugShowCheckedModeBanner: false,')
        if n == 0:
            note(MISS, 'main.dart', 'جای تعیین زبان پیدا نشد')
        elif 'locale: const Locale(\'fa\'),' in s:
            note(SKIP, 'main.dart', 'زبان از قبل تنظیم شده')
        else:
            s = s.replace('debugShowCheckedModeBanner: false,',
                          "debugShowCheckedModeBanner: false,\n"
                          "      locale: const Locale('fa'),")
            write(m, s)
            note(OK, 'main.dart', f'زبان فارسی در {n} پنجره تنظیم شد')
    else:
        note(MISS, 'main.dart', 'فایل نیست')


def tabbar_title(repo: Path):
    """نام نمایشی در نوار بالای پنجره"""
    p = repo / 'flutter/lib/desktop/widgets/tabbar_widget.dart'
    if not p.exists():
        note(MISS, 'tabbar_widget.dart', 'فایل نیست')
        return
    old = ('                            child: const Text(\n'
           '                              "RustDesk",\n'
           '                              style: TextStyle(fontSize: 13),\n'
           '                            ).marginOnly(left: 2))')
    new = ('                            child: Text(\n'
           '                              nrispAppNameFa,\n'
           "                              style: const TextStyle(\n"
           '                                  fontSize: 13,\n'
           '                                  fontWeight: FontWeight.w700,\n'
           '                                  color: NrispBrand.blue),\n'
           '                            ).marginOnly(left: 2))')
    edit(p, [(old, new)], label='tabbar_widget.dart (نام نرم‌افزار)')
    # افزودن import پنل اختصاصی
    s = read(p)
    imp = "import 'package:flutter_hbb/nrisp/nrisp_id_panel.dart';\n"
    if imp not in s:
        anchor = "import 'package:flutter_hbb/models/state_model.dart';\n"
        if anchor in s:
            s = s.replace(anchor, anchor + imp, 1)
            write(p, s)
            note(OK, 'tabbar_widget.dart (import)')
        else:
            note(MISS, 'tabbar_widget.dart (import)', 'جای import پیدا نشد')


def drop_powered(repo: Path):
    """حذف نشان powered by از صفحهٔ اصلی"""
    p = repo / 'flutter/lib/desktop/pages/desktop_home_page.dart'
    if not p.exists():
        note(MISS, 'desktop_home_page.dart', 'فایل نیست')
        return
    old = ('      if (bind.isCustomClient())\n'
           '        Align(\n'
           '          alignment: Alignment.center,\n'
           '          child: loadPowered(context),\n'
           '        ),\n')
    edit(p, [(old, '      // نشان «قدرت‌گرفته از» حذف شد؛ هویت بصری موسسه جای آن است\n')],
         label='desktop_home_page.dart (حذف نشان سازنده)')


def replace_links(repo: Path):
    """نشانی‌های بیرونی"""
    targets = [
        'flutter/lib/desktop/pages/desktop_home_page.dart',
        'flutter/lib/desktop/pages/desktop_setting_page.dart',
        'flutter/lib/mobile/pages/settings_page.dart',
    ]
    for rel in targets:
        p = repo / rel
        if not p.exists():
            continue
        s = read(p)
        before = s
        s = s.replace('https://rustdesk.com/', 'https://nrisp.ac.ir/')
        s = s.replace('https://rustdesk.com', 'https://nrisp.ac.ir')
        s = s.replace("'rustdesk.com'", "'nrisp.ac.ir'")
        if s != before:
            write(p, s)
            note(OK, rel, 'نشانی‌ها با نشانی موسسه عوض شد')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    args = ap.parse_args()
    repo = Path(args.repo).resolve()
    if not (repo / 'Cargo.toml').exists() or not (repo / 'flutter').exists():
        print(f'ERROR: پوشهٔ سورس راست‌دسک نیست: {repo}')
        sys.exit(2)

    print(f'سورس: {repo}')
    persian_default(repo)
    restyle_theme(repo)
    tabbar_title(repo)
    drop_powered(repo)
    replace_links(repo)

    print('\n--- خلاصه ---')
    print(f"اعمال‌شده: {sum(1 for r in rows if r[0] == OK)}   "
          f"از قبل: {sum(1 for r in rows if r[0] == SKIP)}   "
          f"پیدا نشد: {sum(1 for r in rows if r[0] == MISS)}")
    if any(r[0] == MISS for r in rows):
        print('موارد پیدا نشده در بالا فهرست شده‌اند.')


if __name__ == '__main__':
    main()
