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
import shutil
import sys
from pathlib import Path

BRAND_FONTS = Path(__file__).resolve().parent.parent / 'assets' / 'fonts'

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
    """پوستهٔ تیره و نارنجی شبیه درسان‌دسک."""
    p = repo / 'flutter/lib/common.dart'
    if not p.exists():
        note(MISS, 'common.dart', 'فایل نیست')
        return
    edit(p, [
        # رنگ اصلی: نارنجی
        ('static const Color accent = Color(0xFF0E3091);',
         'static const Color accent = Color(0xFFFB4201);'),
        ('static const Color accent50 = Color(0x770E3091);',
         'static const Color accent50 = Color(0x77FB4201);'),
        ('static const Color accent80 = Color(0xAA0E3091);',
         'static const Color accent80 = Color(0xAAFB4201);'),
        ('static const Color button = Color(0xFF0E3091);',
         'static const Color button = Color(0xFFFB4201);'),
        ('static const Color idColor = Color(0xFF0E3091);',
         'static const Color idColor = Color(0xFFFB4201);'),
        ('static const Color grayBg = Color(0xFFEFEFF2);',
         'static const Color grayBg = Color(0xFFF4F6F9);'),
        ('static const Color border = Color(0xFFCCCCCC);',
         'static const Color border = Color(0xFFE3E7EE);'),
        ('static const Color hoverBorder = Color(0xFF999999);',
         'static const Color hoverBorder = Color(0xFFFB4201);'),
        # پوستهٔ تیره: زمینه و کارت‌های تیره
        ('hoverColor: Color.fromARGB(255, 45, 46, 53),',
         'hoverColor: Color(0xFF24282F),'),
        ('scaffoldBackgroundColor: Color(0xFF18191E),',
         'scaffoldBackgroundColor: Color(0xFF181B21),'),
        ('dialogBackgroundColor: Color(0xFF18191E),',
         'dialogBackgroundColor: Color(0xFF20242B),'),
        ('cardColor: Color(0xFF24252B),',
         'cardColor: Color(0xFF20242B),'),
        # پوستهٔ روشن: زمینهٔ نرم و کارت سفید (مثل درسان با تم روشن)
        ('scaffoldBackgroundColor: Colors.white,',
         'scaffoldBackgroundColor: Color(0xFFF7F8FA),'),
        ('    cardColor: grayBg,', '    cardColor: Colors.white,'),
        ('hoverColor: Color.fromARGB(255, 224, 224, 224),',
         'hoverColor: Color(0xFFF1F3F7),'),
        # رنگ اصلی: نارنجی روی هر دو پوسته
        ('primary: Colors.blue,', 'primary: const Color(0xFFFB4201),'),
        ('secondary: accent,', 'secondary: const Color(0xFFFF7A3D),'),
        ('background: Color(0xFF24252B),', 'background: Color(0xFF1F232A),'),
        # ورودی‌ها و دکمه‌های خطی
        ("""        ? InputDecorationTheme(
            fillColor: Color(0xFF24252B),
            filled: true,
            isDense: true,
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(8),
            ),
          )""",
         """        ? InputDecorationTheme(
            fillColor: Color(0xFF24282F),
            filled: true,
            isDense: true,
            hintStyle: const TextStyle(color: Color(0xFF98A2B0)),
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(12),
              borderSide: const BorderSide(color: Color(0xFF2A2F37)),
            ),
            enabledBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(12),
              borderSide: const BorderSide(color: Color(0xFF2A2F37)),
            ),
            focusedBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(12),
              borderSide: const BorderSide(color: Color(0xFFFB4201), width: 1.4),
            ),
          )"""),
        ("""      style: OutlinedButton.styleFrom(
        backgroundColor: Color(0xFF24252B),""",
         """      style: OutlinedButton.styleFrom(
        backgroundColor: Color(0xFF24282F),"""),
        ('side: BorderSide(color: Colors.white12, width: 0.5),',
         'side: const BorderSide(color: Color(0xFF2A2F37), width: 1),'),
        # نوار بالای پنجره
    ], label='common.dart (پوستهٔ تیرهٔ نارنجی)')


def force_dark(repo: Path):
    """برنامه همیشه با پوستهٔ تیره باز می‌شود (مثل درسان)."""
    p = repo / 'flutter/lib/common.dart'
    src = read(p)
    old = """  static ThemeMode currentThemeMode() {
    final preference = getThemeModePreference();
    if (preference == ThemeMode.system) {
      if (WidgetsBinding.instance.platformDispatcher.platformBrightness ==
          Brightness.light) {
        return ThemeMode.light;
      } else {
        return ThemeMode.dark;
      }
    } else {
      return preference;
    }
  }"""
    new = """  static ThemeMode currentThemeMode() {
    // پوستهٔ تیرهٔ سازمانی — همیشه تیره
    return ThemeMode.dark;
  }"""
    if old in src:
        write(p, src.replace(old, new, 1))
        note(OK, 'common.dart (پوستهٔ تیرهٔ همیشگی)')
    else:
        note(MISS, 'common.dart (پوستهٔ تیرهٔ همیشگی)', 'تابع پیدا نشد')


def dorsan_look(repo: Path):
    """کارت اتصال بزرگ و دکمهٔ درشت نارنجی مثل درسان‌دسک."""
    p = repo / 'flutter/lib/desktop/pages/connection_page.dart'
    if not p.exists():
        note(MISS, 'connection_page.dart', 'فایل نیست')
        return
    edit(p, [
        ("""    var w = Container(
      width: 320 + 20 * 2,
      padding: const EdgeInsets.fromLTRB(20, 24, 20, 22),
      decoration: BoxDecoration(
          color: Theme.of(context).scaffoldBackgroundColor,
          borderRadius: const BorderRadius.all(Radius.circular(18)),
          border: Border.all(color: Theme.of(context).colorScheme.background),
          boxShadow: [
            BoxShadow(
                color: Colors.black.withOpacity(0.05),
                blurRadius: 18,
                offset: const Offset(0, 5))
          ]),""",
         """    var w = Container(
      width: 520,
      padding: const EdgeInsets.fromLTRB(30, 30, 30, 28),
      decoration: BoxDecoration(
          color: Theme.of(context).cardColor,
          borderRadius: const BorderRadius.all(Radius.circular(22)),
          border: Border.all(color: Theme.of(context).dividerColor),
          boxShadow: [
            BoxShadow(
                color: Colors.black.withOpacity(0.16),
                blurRadius: 24,
                offset: const Offset(0, 10))
          ]),"""),
        ("""                          style: const TextStyle(
                            fontFamily: 'WorkSans',
                            fontSize: 22,
                            height: 1.4,
                          ),""",
         """                          style: const TextStyle(
                            fontFamily: 'WorkSans',
                            fontSize: 19,
                            height: 1.5,
                            color: Color(0xFFF2F4F7),
                          ),"""),
        ("""                          decoration: InputDecoration(
                              filled: false,
                              counterText: '',""",
         """                          decoration: InputDecoration(
                              filled: true,
                              fillColor: const Color(0xFF24282F),
                              counterText: '',"""),
        ("""                              contentPadding: const EdgeInsets.symmetric(
                                  horizontal: 15, vertical: 13)),""",
         """                              contentPadding: const EdgeInsets.symmetric(
                                  horizontal: 16, vertical: 18)),"""),
        ("""                SizedBox(
                  height: 28.0,
                  child: ElevatedButton(
                    onPressed: () {
                      onConnect();
                    },
                    child: Text(translate("Connect")),
                  ),
                ),
                const SizedBox(width: 8),
                Container(
                  height: 28.0,
                  width: 28.0,
                  decoration: BoxDecoration(
                    border: Border.all(color: Theme.of(context).dividerColor),
                    borderRadius: BorderRadius.circular(8),
                  ),""",
         """                SizedBox(
                  height: 46.0,
                  child: ElevatedButton(
                    onPressed: () {
                      onConnect();
                    },
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color(0xFFFB4201),
                      foregroundColor: Colors.white,
                      elevation: 0,
                      padding: const EdgeInsets.symmetric(horizontal: 26),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(23),
                      ),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        const Icon(Icons.arrow_back_rounded,
                            size: 18, color: Colors.white),
                        const SizedBox(width: 8),
                        Text(translate("Connect"),
                            style: const TextStyle(
                                fontSize: 14, fontWeight: FontWeight.w700)),
                      ],
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                Container(
                  height: 46.0,
                  width: 46.0,
                  decoration: BoxDecoration(
                    color: const Color(0xFF24282F),
                    border: Border.all(color: const Color(0xFF2A2F37)),
                    borderRadius: BorderRadius.circular(23),
                  ),"""),
        ("""            Row(
              children: [
                Flexible(child: _buildRemoteIDTextField(context)),
              ],
            ).marginOnly(top: 22),""",
         """            Container(
              margin: const EdgeInsets.fromLTRB(12, 22, 12, 4),
              padding: const EdgeInsets.symmetric(vertical: 30),
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: [
                    const Color(0xFFFB4201).withOpacity(0.10),
                    const Color(0xFFFB4201).withOpacity(0.0),
                  ],
                ),
                borderRadius: BorderRadius.circular(22),
                border: Border.all(color: Theme.of(context).dividerColor),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Flexible(child: _buildRemoteIDTextField(context)),
                ],
              ),
            ).marginOnly(top: 22),"""),
    ], label='connection_page.dart (کارت اتصال درسان‌گونه)')


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
           '                                  color: nrispOrange),\n'
           '                            ).marginOnly(left: 2))')
    edit(p, [(old, new)], label='tabbar_widget.dart (نام نرم‌افزار)')

    # اگر apply_branding پیش‌تر نام انگلیسی را گذاشته باشد، اینجا فارسی می‌شود
    s = read(p)
    eng = ('                            child: Text(\n'
           '                              appName,\n'
           '                              style: const TextStyle(fontSize: 13),\n')
    fa = ('                            child: Text(\n'
          '                              nrispAppNameFa,\n'
          '                              style: const TextStyle(\n'
          '                                  fontSize: 13,\n'
          '                                  fontWeight: FontWeight.w700,\n'
          '                                  color: nrispOrange),\n')
    if eng in s:
        s = s.replace(eng, fa, 1)
        write(p, s)
        note(OK, 'tabbar_widget.dart (نام فارسی در نوار بالا)')
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



FA_APP_NAME = 'دسترسی راه دور موسسه'


def fa_brand_cleanup(repo: Path):
    """نام برند اصلی را از متن ترجمه‌های فارسی برمی‌دارد (فقط مقدار، نه کلید)."""
    import re as _re
    path = repo / 'src' / 'lang' / 'fa.rs'
    if not path.exists():
        note(MISS, 'src/lang/fa.rs', 'فایل نبود')
        return
    src = read(path)
    pat = _re.compile(r'\("((?:[^"\\]|\\.)*)",\s*"((?:[^"\\]|\\.)*)"\)')
    counter = {'n': 0}

    def _fix(m):
        key, val = m.group(1), m.group(2)
        if key == 'powered_by_me' or key.startswith('upgrade_rustdesk_server_pro'):
            return m.group(0)
        if 'RustDesk' not in val:
            return m.group(0)
        counter['n'] += 1
        return m.group(0).replace('"' + val + '"',
                                  '"' + val.replace('RustDesk', FA_APP_NAME) + '"', 1)

    new_src = pat.sub(_fix, src)
    left = sum(1 for m in pat.finditer(new_src)
               if 'RustDesk' in m.group(2)
               and m.group(1) != 'powered_by_me'
               and not m.group(1).startswith('upgrade_rustdesk_server_pro'))
    write(path, new_src)
    note(OK if left == 0 else MISS, 'src/lang/fa.rs (نام برند در ترجمه‌ها)',
         f'{counter["n"]} متن اصلاح شد | باقی‌مانده: {left}')


def replace_visible_urls(repo: Path):
    """نشانی‌های برند اصلی که روی صفحه دیده می‌شوند."""
    jobs = [
        (repo / 'flutter/lib/common.dart',
         [("launchUrl(Uri.parse('https://rustdesk.com'));",
           "launchUrl(Uri.parse('https://nrisp.ac.ir'));")],
         'common.dart (نشانی درباره)'),
        (repo / 'flutter/lib/desktop/pages/connection_page.dart',
         [('const url = "https://rustdesk.com/pricing";',
           'const url = "https://nrisp.ac.ir";')],
         'connection_page.dart (نشانی صفحهٔ ارتقا)'),
        (repo / 'flutter/lib/desktop/pages/install_page.dart',
         [("'https://rustdesk.com/privacy.html'", "'https://nrisp.ac.ir'")],
         'install_page.dart (نشانی حریم خصوصی)'),
        (repo / 'flutter/lib/mobile/pages/connection_page.dart',
         [("final url = 'https://rustdesk.com/download';",
           "final url = 'https://nrisp.ac.ir';")],
         'mobile/connection_page.dart (نشانی دریافت)'),
    ]
    for path, pairs, label in jobs:
        if not path.exists():
            note(MISS, label, 'فایل نبود')
            continue
        edit(path, pairs, label=label)


CORP_FA = 'موسسه تحقیقات سیاست علمی کشور'


def corporate_footer(repo: Path):
    """نام شرکت اصلی سازنده را از جاهایی که کاربر می‌بیند برمی‌دارد."""
    jobs = [
        (repo / 'flutter/lib/desktop/pages/desktop_setting_page.dart',
         [("'Copyright © ${DateTime.now().toString().substring(0, 4)} "
           "Purslane Tech Pte. Ltd.\\n$license'",
           "'حقوق © " + CORP_FA + " ۱۴۰۵\\n$license'")],
         'desktop_setting_page.dart (حق نشر)'),
        (repo / 'src/ui/index.tis',
         [('Copyright &copy; 2026 Purslane Tech Pte. Ltd.',
           'حقوق &copy; ' + CORP_FA + ' ۱۴۰۵')],
         'index.tis (حق نشر)'),
        (repo / 'src/auth_2fa.rs',
         [('const ISSUER: &str = "RustDesk";',
           'const ISSUER: &str = "' + FA_APP_NAME + '";')],
         'auth_2fa.rs (نام صادرکننده)'),
    ]
    for path, pairs, label in jobs:
        if not path.exists():
            note(MISS, label, 'فایل نبود')
            continue
        edit(path, pairs, label=label)


def hide_install_card(repo: Path):
    """کارت صورتی «برنامه را نصب کنید» از صفحهٔ اصلی برداشته می‌شود."""
    p = repo / 'flutter/lib/desktop/pages/desktop_home_page.dart'
    if not p.exists():
        note(MISS, 'desktop_home_page.dart', 'فایل نیست')
        return
    src = read(p)
    old = """    if (isWindows && !bind.isDisableInstallation()) {
      if (!bind.mainIsInstalled()) {"""
    new = """    if (isWindows && !bind.isDisableInstallation()) {
      // کارت راهنمای نصب برداشته شد؛ نصب از فایل نصبی رسمی انجام می‌شود
      if (false && !bind.mainIsInstalled()) {"""
    if old in src:
        write(p, src.replace(old, new, 1))
        note(OK, 'desktop_home_page.dart (کارت راهنمای نصب برداشته شد)')
    else:
        note(MISS, 'desktop_home_page.dart', 'قطعهٔ کارت نصب پیدا نشد')



def tabbar_theme(repo: Path):
    """رنگ آیکون‌های نوار بالای پنجره (پوستهٔ تیره)."""
    p = repo / 'flutter/lib/desktop/widgets/tabbar_widget.dart'
    if not p.exists():
        note(MISS, 'tabbar_widget.dart', 'فایل نیست')
        return
    edit(p, [
        ("""  static const dark = TabbarTheme(
      selectedTabIconColor: MyTheme.accent,
      unSelectedTabIconColor: Color.fromARGB(255, 30, 65, 98),""",
         """  static const dark = TabbarTheme(
      selectedTabIconColor: Color(0xFFFFB599),
      unSelectedTabIconColor: Color(0xFFFFB599),"""),
    ], label='tabbar_widget.dart (رنگ نوار بالا)')



def bundle_font(repo: Path):
    """فونت وزیرمتن را همراه برنامه می‌کند و فونت پیش‌فرض همهٔ نوشته‌ها می‌گذارد."""
    src_dir = BRAND_FONTS
    dst_dir = repo / 'flutter' / 'assets'
    if not src_dir.exists():
        note(MISS, 'bundle_font', 'پوشهٔ فونت‌ها پیدا نشد')
        return
    dst_dir.mkdir(parents=True, exist_ok=True)
    for name in ('Vazirmatn-Regular.ttf', 'Vazirmatn-Bold.ttf'):
        s_file = src_dir / name
        if s_file.exists():
            shutil.copyfile(s_file, dst_dir / name)
    pub = repo / 'flutter' / 'pubspec.yaml'
    txt = read(pub)
    if 'Vazirmatn' not in txt:
        anchor = '  fonts:\n'
        block = ('  fonts:\n'
                 '    - family: Vazirmatn\n'
                 '      fonts:\n'
                 '        - asset: assets/Vazirmatn-Regular.ttf\n'
                 '        - asset: assets/Vazirmatn-Bold.ttf\n'
                 '          weight: 700\n')
        if anchor in txt:
            txt = txt.replace(anchor, block, 1)
            write(pub, txt)
            note(OK, 'pubspec.yaml (فونت وزیرمتن)')
        else:
            note(MISS, 'pubspec.yaml', 'بخش فونت‌ها پیدا نشد')
    else:
        note(SKIP, 'pubspec.yaml (فونت وزیرمتن)', 'از قبل بود')

    common = repo / 'flutter' / 'lib' / 'common.dart'
    edit(common, [
        ("    useMaterial3: false,\n    brightness: Brightness.light,",
         "    useMaterial3: false,\n    fontFamily: 'Vazirmatn',\n    brightness: Brightness.light,"),
        ("    useMaterial3: false,\n    brightness: Brightness.dark,",
         "    useMaterial3: false,\n    fontFamily: 'Vazirmatn',\n    brightness: Brightness.dark,"),
    ], label='common.dart (فونت پیش‌فرض)')


def voice_call_hint(repo: Path):
    """ترجمهٔ فارسی راهنمای تماس صوتی که خالی بود."""
    p = repo / 'src' / 'lang' / 'fa.rs'
    if not p.exists():
        note(MISS, 'fa.rs', 'فایل نیست')
        return
    src = read(p)
    old = ('("To start a voice call, enable \\"Audio capture\\" on the '
           '\\"Screen share\\" page.", "")')
    new = ('("To start a voice call, enable \\"Audio capture\\" on the '
           '\\"Screen share\\" page.", "برای شروع تماس صوتی، گزینهٔ «ضبط صدا» '
           'را در صفحهٔ «اشتراک صفحه» فعال کنید.")')
    if old in src:
        write(p, src.replace(old, new, 1))
        note(OK, 'fa.rs (راهنمای تماس صوتی)')
    elif 'برای شروع تماس صوتی' in src:
        note(SKIP, 'fa.rs (راهنمای تماس صوتی)', 'از قبل بود')
    else:
        note(MISS, 'fa.rs (راهنمای تماس صوتی)', 'متن پیدا نشد')


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
    dorsan_look(repo)
    tabbar_title(repo)
    tabbar_theme(repo)
    drop_powered(repo)
    replace_links(repo)
    fa_brand_cleanup(repo)
    replace_visible_urls(repo)
    corporate_footer(repo)
    hide_install_card(repo)
    bundle_font(repo)
    voice_call_hint(repo)

    print('\n--- خلاصه ---')
    print(f"اعمال‌شده: {sum(1 for r in rows if r[0] == OK)}   "
          f"از قبل: {sum(1 for r in rows if r[0] == SKIP)}   "
          f"پیدا نشد: {sum(1 for r in rows if r[0] == MISS)}")
    if any(r[0] == MISS for r in rows):
        print('موارد پیدا نشده در بالا فهرست شده‌اند.')


if __name__ == '__main__':
    main()
