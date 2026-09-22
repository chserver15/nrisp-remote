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
          border: Border.all(
              color: Theme.of(context).brightness == Brightness.dark
                  ? const Color(0xFF2A2F37)
                  : const Color(0xFFF6C4AC)),
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
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                  colors: Theme.of(context).brightness == Brightness.dark
                      ? [
                          const Color(0xFFFB4201).withOpacity(0.16),
                          const Color(0xFFFB4201).withOpacity(0.02),
                        ]
                      : [
                          const Color(0xFFFFD9C2),
                          const Color(0xFFFFF3EC),
                        ],
                ),
                borderRadius: BorderRadius.circular(22),
                border: Border.all(
                    color: Theme.of(context).brightness == Brightness.dark
                        ? const Color(0xFF2A2F37)
                        : const Color(0xFFF6C4AC)),
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

# متن‌هایی که ترجمهٔ اصلی راست‌دسک در فارسی جابه‌جا/نادرست است و مستقیم اصلاح می‌شوند
FA_TEXT_OVERRIDES = {
    'ID/Relay Server': 'سرور شناسه و رله',
    'Relay Server': 'سرور رله',
    'API Server': 'سرور API',
    'Your new ID': 'شناسهٔ جدید شما',
    'Socks5 Proxy': 'پروکسی Socks5',
    'Socks5/Http(s) Proxy': 'پروکسی Socks5/Http',
    'RDP Settings': 'تنظیمات RDP',
    'Direct IP Access': 'دسترسی مستقیم',
    'Enable direct IP access': 'دسترسی مستقیم را فعال کنید',
    'IP Whitelisting': 'فهرست مجاز',
    'Use IP Whitelisting': 'استفاده از فهرست مجاز',
    'Invalid IP': 'نشانی وارد\u200cشده نامعتبر است',
    'whitelist_tip': 'فقط نشانی\u200cهای فهرست مجاز می\u200cتوانند به این دسکتاپ متصل شوند',
    'whitelist_cidr_tip': 'نمونهٔ الگوی شبکهٔ مجاز: 192.168.1.0/24',
    'id_whitelist_caveat_tip': 'شناسه توسط کلاینت متصل\u200cشونده گزارش می\u200cشود',
    'id_input_tip': 'برای دسترسی به سرورهای عمومی نیازی به کلید نیست؛ نمونه: <id>@public',
    'TCP tunneling': 'تانل TCP',
    'Enable TCP tunneling': 'فعال\u200cسازی تانل TCP',
    'Disable UDP': 'غیرفعال\u200cکردن UDP',
    'Use WebSocket': 'استفاده از WebSocket',
    'websocket_tip': 'فقط اتصال از طریق رله پشتیبانی می\u200cشود (WebSocket)',
    'Enable RDP session sharing': 'فعال\u200cسازی اشتراک\u200cگذاری نشست RDP',
    'Legacy mode': 'حالت قدیمی',
    'Map mode': 'حالت نقشهٔ کلید',
    'Relay Connection': 'اتصال از طریق رله',
    'Relayed and encrypted connection': 'اتصال از طریق رله و رمزگذاری\u200cشده',
    'Relayed and unencrypted connection': 'اتصال از طریق رله و بدون رمزگذاری',
    'Always connect via relay': 'همیشه از طریق رله متصل شو',
    'Failed to connect to relay server': 'اتصال به سرور رله برقرار نشد',
    'Failed to connect via relay server': 'اتصال از طریق سرور رله انجام نشد',
    'Please wait for confirmation of UAC...': 'منتظر تأیید کاربر بمانید…',
    'wait_accept_uac_tip': 'منتظر بمانید تا کاربر سمت راه دور درخواست دسترسی را بپذیرد.',
    'accept_and_elevate_btn_tooltip': 'اتصال را بپذیرید و دسترسی مدیر بدهید',
    'Capture screen using DirectX': 'تصویربرداری از صفحه با DirectX',
    'Use D3D rendering': 'استفاده از رندر D3D',
    'd3d_render_tip': 'فعال\u200cکردن رندر D3D برای کارکرد بهتر',
    'Adaptive bitrate': 'نرخ بیت تطبیقی',
    'Enable IPv6 P2P connection': 'فعال\u200cسازی اتصال همتا\u200cبه\u200cهمتا IPv6',
    'Enable WebRTC P2P connection': 'فعال\u200cسازی اتصال همتا\u200cبه\u200cهمتا WebRTC',
    'Enable UDP hole punching': 'فعال\u200cسازی تکنیک سوراخ\u200cکنی UDP',
    'Enable TCP hole punching': 'فعال\u200cسازی تکنیک سوراخ\u200cکنی TCP',
    'API Token': 'توکن API',
    'Fingerprint': 'اثر انگشت',
    'HSV Color': 'رنگ HSV',
    'Remove wallpaper during incoming sessions': 'حذف تصویر پس\u200cزمینه در جلسه\u200cهای ورودی',
    'Allow insecure TLS fallback': 'اجازهٔ جایگزینی ناامن TLS',
    'allow-insecure-tls-fallback-tip': 'به\u200cطور پیش\u200cفرض گواهی سرور بررسی می\u200cشود؛ با فعال\u200cکردن این گزینه، در نبود گواهی معتبر اتصال برقرار می\u200cماند.',
    'disable-udp-tip': 'تعیین می\u200cکند اتصال فقط از طریق TCP انجام شود یا نه.',
    'default_proxy_tip': 'پیش\u200cفرض، پروکسی Sock5 روی پورت ۱۰۸۰ است',
    'elevation_username_tip': 'نام کاربری را به شکل کامل وارد کنید (کاربر یا دامنه/کاربر)',
    'enable-2fa-desc': 'بارکد را اسکن کنید و کد نمایش\u200cداده\u200cشده در برنامه را وارد کنید',
    'relay_hint_tip': 'در صورت نیاز شناسه را دستی وارد کنید یا گزینهٔ اتصال همیشگی از طریق رله را فعال کنید',
    'invalid_http': 'نشانی نامعتبر است؛ نمونه: https://example.com',
    'length %min% to %max%': 'طول باید بین %min% و %max% باشد',
    'config_acc': 'برای کنترل دسکتاپ از راه دور، اجازهٔ دسترس\u200cپذیری را بدهید.',
    'config_screen': 'برای کنترل دسکتاپ از راه دور، اجازهٔ تصویربرداری از صفحه را بدهید.',
    'config_input': 'برای کنترل دسکتاپ با صفحه\u200cکلید، اجازهٔ پایش ورودی را بدهید.',
    'config_microphone': 'برای صحبت در تماس صوتی، اجازهٔ ضبط صدا را بدهید.',
    'install_tip': 'برای راحتی استفاده، برنامه را نصب کنید و پنجرهٔ تأیید ویندوز را بپذیرید.',
    'still_click_uac_tip': 'کاربر سمت راه دور همچنان باید پنجرهٔ تأیید را بپذیرد.',
    'verify_rustdesk_password_tip': 'رمز عبور برنامه را تأیید کنید',
    'allow-only-conn-window-open-tip': 'اتصال فقط زمانی برقرار می\u200cشود که این پنجره باز باشد',
    'floating_window_tip': 'به فعال\u200cماندن سرویس در پس\u200cزمینه کمک می\u200cکند',
    'server-oss-not-support-tip': 'توجه: سرور عمومی این ویژگی را ندارد.',
    'android_input_permission_tip1': 'برای کنترل دستگاه با ماوس یا لمس، اجازهٔ دسترس\u200cپذیری را به برنامه بدهید.',
    'android_input_permission_tip2': 'در تنظیمات اندروید به بخش دسترس\u200cپذیری بروید و گزینهٔ ورودی برنامه را روشن کنید.',
    'android_start_service_tip': 'برای شروع، دکمهٔ شروع سرویس را بزنید و اجازهٔ تصویربرداری از صفحه را بدهید.',
    'upgrade_remote_rustdesk_client_to_{}_tip': 'لطفاً برنامه را در سمت راه دور به نسخهٔ {} یا جدیدتر ارتقا دهید',
    'upgrade_rustdesk_server_pro_to_{}_tip': 'لطفاً سرور را به نسخهٔ {} یا جدیدتر ارتقا دهید',
    'About RustDesk': 'دربارهٔ دسترسی راه دور موسسه',
    'Show RustDesk': 'نمایش پنجرهٔ برنامه',
    'Keep RustDesk background service': 'سرویس دسترسی راه دور در پس\u200cزمینه فعال بماند',
    'RustDesk cannot reach the desktop session on the remote device, check that a desktop session is running and that RustDesk can use it': 'برنامه نمی\u200cتواند به نشست میزکار دستگاه راه دور دسترسی پیدا کند؛ بررسی کنید نشست میزکار در حال اجرا باشد.',
    'RustDesk could not obtain a usable screen from the XDG Desktop Portal, the PipeWire library may be too old': 'برنامه نتوانست صفحهٔ قابل استفاده\u200cای بگیرد؛ ممکن است سرویس درگاه میزکار نصب یا فعال نباشد.',
    'RustDesk could not load a GStreamer component needed for screen capture ({})': 'برنامه نتوانست مؤلفهٔ لازم برای ضبط صفحه را بارگذاری کند.',
    'x11 expected': 'نیازمند X11',
    'wayland-requires-higher-linux-version': 'نیازمند نسخهٔ بالاتر لینوکس است؛ یا X11 را انتخاب کنید',
    'xdp-portal-unavailable': 'ضبط صفحه ناموفق بود؛ سرویس درگاه میزکار از کار افتاده است',
    'wayland_experiment_tip': 'پشتیبانی Wayland آزمایشی است؛ در صورت نیاز به دسترسی بهتر X11 را انتخاب کنید',
    'software_render_tip': 'اگر کارت گرافیک Nvidia دارید و پنجرهٔ راه دور بسته می\u200cشود، حالت رندر نرم\u200cافزاری را انتخاب کنید',
    'selinux_tip': 'سرویس امنیتی سیستم روی دستگاه شما فعال است و ممکن است جلوِ کار برنامه را بگیرد',
    'Clear Wayland screen selection': 'پاک کردن انتخاب صفحه',
    'Login screen using Wayland is not supported': 'ورود به سیستم با Wayland پشتیبانی نمی\u200cشود',
    'empty_recent_tip': 'هیچ جلسهٔ اخیری وجود ندارد! زمان برنامه\u200cریزی جلسهٔ جدید است',
    'empty_favorite_tip': 'هنوز همتای مورد علاقه\u200cای ندارید؟ بیایید فردی را برای ارتباط پیدا کنیم',
    'Your ip is blocked by the peer': 'نشانی شما توسط طرف مقابل مسدود شده است',
    'conn-e2ee-unavailable-tip': 'رمزنگاری سرتاسری قابل تأیید نیست. ممکن است دستگاه راه دور هنوز آماده نشده باشد.',
    'ubuntu-21-04-required': 'نیازمند نسخهٔ جدیدتر سیستم\u200cعامل است',
}


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
        if key in FA_TEXT_OVERRIDES:
            counter['n'] += 1
            fixed = FA_TEXT_OVERRIDES[key].replace('"', '\\"')
            return m.group(0).replace('"' + val + '"', '"' + fixed + '"', 1)
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
    """کارت نصب باید سر جایش باشد تا کاربر پرتابل بتواند برنامه را روی ویندوز نصب کند
    (نصب همان چیزی است که سرویس، قوانین فایروال و ثبت در کنترل پنل را می‌سازد)."""
    p = repo / 'flutter/lib/desktop/pages/desktop_home_page.dart'
    if not p.exists():
        note(MISS, 'desktop_home_page.dart (کارت نصب)', 'فایل نیست')
        return
    s = read(p)
    old = "      if (false && !bind.mainIsInstalled()) {"
    if old in s:
        s = s.replace(old, "      if (!bind.mainIsInstalled()) {", 1)
        write(p, s)
        note(OK, 'desktop_home_page.dart (کارت نصب برگشت)')
    else:
        note(SKIP, 'desktop_home_page.dart (کارت نصب)', 'از قبل درست')


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
         "    useMaterial3: false,\n    fontFamilyFallback: const ['Vazirmatn'],\n    brightness: Brightness.light,"),
        ("    useMaterial3: false,\n    brightness: Brightness.dark,",
         "    useMaterial3: false,\n    fontFamilyFallback: const ['Vazirmatn'],\n    brightness: Brightness.dark,"),
    ], label='common.dart (فونت پیش‌فرض)')


def settings_font(repo: Path):
    """اندازهٔ نوشته‌های صفحهٔ تنظیمات دست‌نخورده می‌ماند.

    کوچک/بزرگ‌کردن اندازه‌ها باعث می‌شد برچسب زبانه‌ها (مثل «تنظیمات») در
    کادر خودش جا نشود و بریده شود؛ پس همان اندازهٔ اصلی برنامه حفظ می‌شود.
    """
    note(SKIP, 'settings_font', 'اندازه‌های اصلی حفظ شد')


def window_title(repo: Path):
    """عنوان پنجره در نوار وظیفه، نام کامل و زیبا باشد."""
    p = repo / 'flutter' / 'lib' / 'main.dart'
    if not p.exists():
        note(MISS, 'main.dart', 'فایل نیست')
        return
    src = read(p)
    old = "              : bind.mainGetAppNameSync(),"
    new = "              : 'NRISP Remote Access',"
    if old in src:
        write(p, src.replace(old, new, 1))
        note(OK, 'main.dart (عنوان پنجره)')
    else:
        note(SKIP, 'main.dart (عنوان پنجره)', 'از قبل یا پیدا نشد')


def menu_side(repo: Path):
    """منوی سه‌نقطه باید مثل قبل از نقطهٔ کلیک باز شود؛ در حالت راست‌به‌چپ
    جهت باز شدن و چیدمان منو برمی‌گشت و به سمت دیگر می‌رفت."""
    p = repo / 'flutter' / 'lib' / 'desktop' / 'widgets' / 'material_mod_popup_menu.dart'
    if not p.exists():
        note(MISS, 'material_mod_popup_menu.dart', 'فایل نیست')
        return
    src = read(p)
    if 'double x = position.left;' in src:
        note(SKIP, 'منوی سه‌نقطه (جهت باز شدن)', 'از قبل بود')
        return
    pairs = [
        ("""    // Find the ideal horizontal position.
    double x;
    // if (position.left > position.right) {
    //   // Menu button is closer to the right edge, so grow to the left, aligned to the right edge.
    //   x = size.width - position.right - childSize.width;
    // } else if (position.left < position.right) {
    //   // Menu button is closer to the left edge, so grow to the right, aligned to the left edge.
    //   x = position.left;
    // } else {
    // Menu button is equidistant from both edges, so grow in reading direction.
    switch (textDirection) {
      case TextDirection.rtl:
        x = size.width - position.right - childSize.width;
        break;
      case TextDirection.ltr:
        x = position.left;
        break;
    }
    //}""",
         """    // موقعیت افقی منو همیشه مثل نسخهٔ اصلی برنامه: از نقطهٔ کلیک به سمت راست
    double x = position.left;"""),
        ("            child: Align(\n              alignment: AlignmentDirectional.topEnd,",
         "            child: Align(\n              alignment: Alignment.topLeft,"),
    ]
    ok = 0
    for old, new in pairs:
        if old in src:
            src = src.replace(old, new, 1)
            ok += 1
        else:
            note(MISS, 'منوی سه‌نقطه', 'بخشی پیدا نشد')
    if ok:
        write(p, src)
        note(OK, 'منوی سه‌نقطه (جهت باز شدن و چیدمان)')


def line_height_fix(repo: Path):
    """تغییر ارتفاع خط لازم نیست: فونت وزیرمتن فقط پشتیبان است و ارتفاع خط
    پیش‌فرض دست‌نخورده می‌ماند (تحمیل ارتفاع، منوها و کادرها را به‌هم می‌ریخت)."""
    note(SKIP, 'line_height_fix', 'لازم نیست (پشتیبان فونت کافی است)')


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



def bump_version(repo: Path):
    """شمارهٔ نسخه را بالا می‌برد تا نسخه‌ها از هم قابل تشخیص باشند."""
    import re as _re
    ver = '1.5.2'
    ct = repo / 'Cargo.toml'
    cl = repo / 'Cargo.lock'
    src = read(ct)
    new = _re.sub(r'(?m)^version = "1[.]5[.]0"', f'version = "{ver}"', src, count=1)
    if new != src:
        write(ct, new)
        note(OK, 'Cargo.toml (شمارهٔ نسخه)', ver)
    else:
        note(SKIP, 'Cargo.toml (شمارهٔ نسخه)', 'از قبل')
    if cl.exists():
        src = read(cl)
        old = 'name = "rustdesk"\nversion = "1.5.0"'
        if old in src:
            write(cl, src.replace(old, f'name = "rustdesk"\nversion = "{ver}"', 1))
            note(OK, 'Cargo.lock (شمارهٔ نسخه)', ver)
        else:
            note(SKIP, 'Cargo.lock (شمارهٔ نسخه)', 'از قبل')



def window_buttons(repo: Path):
    """دکمه‌های کوچک/بزرگ/بستن مثل همهٔ برنامه‌های ویندوز بالا-راست می‌مانند.

    تنها «نوار بالای پنجره» چپ‌به‌راست می‌شود تا دکمه‌ها سمت راست بنشینند؛
    محتوای صفحه (متن‌ها و تنظیمات) دست‌نخورده و راست‌به‌چپ فارسی می‌ماند.
    """
    p = repo / 'flutter/lib/desktop/widgets/tabbar_widget.dart'
    if not p.exists():
        note(MISS, 'tabbar_widget.dart', 'فایل نیست')
        return
    src = read(p)
    old = """  Widget _buildBar() {
    final isIncomingHomePage = bind.isIncomingOnly() && isInHomePage();
    return Row(
      children: ["""
    new = """  Widget _buildBar() {
    final isIncomingHomePage = bind.isIncomingOnly() && isInHomePage();
    // NRISP: نوار بالای پنجره چپ‌به‌راست است تا دکمه‌ها بالا-راست بمانند
    return Row(
      textDirection: TextDirection.ltr,
      children: ["""
    done = 0
    if old in src:
        src = src.replace(old, new, 1)
        done += 1
    elif 'return Row(\n      textDirection: TextDirection.ltr,\n      children: [' in src:
        done += 1
    else:
        note(MISS, 'tabbar_widget.dart (_buildBar)', 'قطعه پیدا نشد')
    # ترتیب آیکون‌های داخل ردیف دکمه‌ها هم چپ‌به‌راست استاندارد بماند
    # داخل ناحیهٔ تب‌ها راست‌به‌چپ بماند (متن تب‌ها مثل بقیهٔ صفحه)
    t_old = """        Expanded(
            child: GestureDetector("""
    t_new = """        Expanded(
          child: Directionality(
            textDirection: TextDirection.rtl,
            child: GestureDetector("""
    c_old = """                  ],
                ))),
        // hide simulated action buttons"""
    c_new = """                  ],
                )))),
        // hide simulated action buttons"""
    if t_old in src:
        src = src.replace(t_old, t_new, 1).replace(c_old, c_new, 1)
        done += 1
    elif t_new in src:
        done += 1
    else:
        note(MISS, 'tabbar_widget.dart (ناحیهٔ تب‌ها)', 'قطعه پیدا نشد')
    marker = """  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.end,
      children: ["""
    add = """  Widget build(BuildContext context) {
    return Row(
      textDirection: TextDirection.ltr,
      mainAxisAlignment: MainAxisAlignment.end,
      children: ["""
    if marker in src:
        src = src.replace(marker, add, 1)
        done += 1
    elif add in src:
        done += 1
    else:
        note(MISS, 'tabbar_widget.dart (ردیف دکمه‌ها)', 'قطعه پیدا نشد')
    write(p, src)
    note(OK if done >= 1 else MISS, 'tabbar_widget.dart (دکمه‌های پنجره بالا-راست)')


def remove_extras(repo: Path):
    """حذف شعار، پیوندهای بی‌مصرف و بخش حساب کاربری."""
    # ۱) شعار «ساخته شده با عشق»
    p = repo / 'flutter/lib/desktop/pages/desktop_setting_page.dart'
    src = read(p)
    old_slogan = """                          Text(
                            translate('Slogan_tip'),
                            style: TextStyle(
                                fontWeight: FontWeight.w800,
                                color: Colors.white),
                          )"""
    if old_slogan in src:
        src = src.replace(old_slogan, """                          const SizedBox.shrink()""", 1)
        note(OK, 'desktop_setting_page.dart (شعار ساخت با عشق برداشته شد)')
    else:
        note(MISS, 'desktop_setting_page.dart', 'شعار پیدا نشد')

    # ۲) پیوندهای حریم خصوصی و وب‌سایت
    for block in ["""              InkWell(
                  onTap: () {
                    launchUrlString('https://nrisp.ac.ir/privacy.html');
                  },
                  child: Text(
                    translate('Privacy Statement'),
                    style: linkStyle,
                  ).marginSymmetric(vertical: 4.0)),""",
                  """              InkWell(
                  onTap: () {
                    launchUrlString('https://nrisp.ac.ir');
                  },
                  child: Text(
                    translate('Website'),
                    style: linkStyle,
                  ).marginSymmetric(vertical: 4.0)),"""]:
        if block in src:
            src = src.replace(block, '', 1)
            note(OK, 'desktop_setting_page.dart (پیوند برداشته شد)')
    write(p, src)

    # ۳) بخش حساب کاربری از فهرست تنظیمات
    src = read(p)
    old_tab = """              _TabInfo(tab, 'Account', Icons.person_outline, Icons.person));"""
    if old_tab in src:
        src = src.replace(old_tab, '              _TabInfo(tab, "\\u200c", Icons.person_outline, Icons.person));', 1)
    write(p, src)
    note(OK, 'desktop_setting_page.dart (پیوندها و شعار پاک شد)')



def disable_account(repo: Path):
    """بخش حساب کاربری و ورود را کامل از برنامه برمی‌دارد."""
    p = repo / 'libs/hbb_common/src/config.rs'
    if not p.exists():
        note(MISS, 'config.rs (حساب کاربری)', 'فایل نیست')
        return
    edit(p, [
        ("fn is_some_hard_opton(name: &str) -> bool {\n    HARD_SETTINGS\n        .read()\n        .unwrap()\n        .get(name)\n        .map_or(false, |x| x == (\"Y\"))",
         "fn is_some_hard_opton(name: &str) -> bool {\n    if name == \"disable-account\" || name == \"disable-ab\" {\n        return true;  // حساب کاربری و ورود در این نسخه برداشته شده است\n    }\n    HARD_SETTINGS\n        .read()\n        .unwrap()\n        .get(name)\n        .map_or(false, |x| x == (\"Y\"))"),
    ], label='config.rs (حساب کاربری خاموش)')


def connect_card_fixes(repo: Path):
    """اصلاح کارت اتصال: کادر هم‌رنگ کارت شناسه، دکمهٔ کنار اتصال قرمز."""
    import re as _re
    p = repo / 'flutter/lib/desktop/pages/connection_page.dart'
    if not p.exists():
        note(MISS, 'connection_page.dart (کارت اتصال)', 'فایل نیست')
        return
    src = read(p)
    changed = 0

    # ۱) کادر ورودی: رنگ روشن/تیره‌پذیر به‌جای تیرهٔ ثابت
    new_field = """filled: true,
                              fillColor: Theme.of(context).brightness ==
                                      Brightness.dark
                                  ? const Color(0xFF262B33)
                                  : const Color(0xFFF5F6F8),
                              hintStyle: TextStyle(
                                  color: Theme.of(context).brightness ==
                                          Brightness.dark
                                      ? const Color(0xFF98A2B0)
                                      : const Color(0xFF77808C)),
                              enabledBorder: OutlineInputBorder(
                                borderRadius: BorderRadius.circular(12),
                                borderSide: BorderSide(
                                    color: Theme.of(context).brightness ==
                                            Brightness.dark
                                        ? const Color(0xFF2C323B)
                                        : const Color(0xFFE3E7EE)),
                              ),
                              focusedBorder: OutlineInputBorder(
                                borderRadius: BorderRadius.circular(12),
                                borderSide: const BorderSide(
                                    color: Color(0xFFFB4201), width: 1.4),
                              ),"""
    if _re.search(r'fillColor:\s*const Color\(0xFF24282F\)', src):
        src = _re.sub(r'filled:\s*true,\s*\n\s*fillColor:\s*const Color\(0xFF24282F\),',
                      new_field, src, count=1)
        changed += 1

    # ۲) دکمهٔ کنار دکمهٔ اتصال: قرمز به‌جای تیره
    if _re.search(r'color:\s*const Color\(0xFF24282F\),\s*\n\s*border:\s*Border\.all\(color:\s*const Color\(0xFF2A2F37\)\),', src):
        src = _re.sub(r'color:\s*const Color\(0xFF24282F\),\s*\n\s*border:\s*Border\.all\(color:\s*const Color\(0xFF2A2F37\)\),',
                      'color: const Color(0xFFFB4201),\n                    border: Border.all(color: const Color(0xFFFB4201)),',
                      src, count=1)
        changed += 1

    # ۳) آیکون آن دکمه: سفید و درشت‌تر
    n_icon = len(_re.findall(r'Icon\(IconFont\.more, size: 14\)', src))
    if n_icon:
        src = src.replace('Icon(IconFont.more, size: 14)',
                          'Icon(IconFont.more, size: 19, color: Colors.white)')
        changed += 1

    if changed:
        write(p, src)
        note(OK, 'connection_page.dart (کارت اتصال: کادر روشن و دکمهٔ قرمز)', f'{changed} مورد')
    else:
        note(SKIP, 'connection_page.dart (کارت اتصال)', 'از قبل')



def final_tweaks(repo: Path):
    """اصلاحات نهایی: دکمه‌های پنجره سمت راست، متن‌های خوانا، برداشتن متن‌های پایین صفحه."""
    # ۱) دکمه‌های پنجره: در تابع window_buttons با جهت چپ‌به‌راستِ همان ردیف
    #    درست شده‌اند؛ اینجا دیگر چیزی به نوار بالای صفحه تحمیل نمی‌شود.
    note(SKIP, 'tabbar_widget.dart (_buildBar)', 'لازم نیست (فقط ردیف دکمه‌ها)')

    # ۲) عنوان کارت: رنگ خوانا در هر دو پوسته
    p = repo / 'flutter/lib/common/widgets/connection_page_title.dart'
    if p.exists():
        s = read(p)
        old = """            style: Theme.of(context)
                .textTheme
                .titleLarge
                ?.merge(TextStyle(height: 1)),"""
        new = """            style: Theme.of(context).textTheme.titleLarge?.merge(TextStyle(
                  height: 1,
                  fontSize: 18,
                  fontWeight: FontWeight.w700,
                  color: Theme.of(context).brightness == Brightness.dark
                      ? const Color(0xFFF3F5F8)
                      : const Color(0xFF1E2430),
                )),"""
        if old in s:
            s = s.replace(old, new, 1)
            write(p, s)
            note(OK, 'عنوان کارت اتصال (رنگ خوانا)')
        else:
            note(MISS, 'عنوان کارت اتصال', 'لنگر پیدا نشد')

    # ۳) متن و راهنمای کادر شناسه: رنگ روشن و خوانا
    p = repo / 'flutter/lib/desktop/pages/connection_page.dart'
    if p.exists():
        s = read(p)
        n = 0
        old = """                          style: const TextStyle(
                            fontFamily: 'WorkSans',
                            fontSize: 19,
                            height: 1.5,
                            color: Color(0xFFF2F4F7),
                          ),"""
        new = """                          style: TextStyle(
                            fontFamily: 'WorkSans',
                            fontSize: 19,
                            height: 1.5,
                            color:
                                Theme.of(context).brightness == Brightness.dark
                                    ? const Color(0xFFF3F5F8)
                                    : const Color(0xFF1E2430),
                          ),"""
        if old in s:
            s = s.replace(old, new, 1); n += 1
        old2 = """                                      ? const Color(0xFF98A2B0)
                                      : const Color(0xFF77808C)),"""
        new2 = """                                      ? const Color(0xFFB4BCC8)
                                      : const Color(0xFF5C6673)),"""
        if old2 in s:
            s = s.replace(old2, new2, 1); n += 1
        old3 = """            offstage: !(!_svcStopped.value &&
                stateGlobal.svcStatus.value == SvcStatus.ready &&
                _svcIsUsingPublicServer.value),"""
        if old3 in s:
            s = s.replace(old3, """            offstage: true, // متن راهنمای سرور برداشته شد""", 1); n += 1
        if n:
            write(p, s)
            note(OK, 'connection_page.dart (خوانایی متن و برداشتن متن پایین)', f'{n} مورد')
        else:
            note(MISS, 'connection_page.dart (خوانایی)', 'لنگر پیدا نشد')


def silent_installer(repo: Path):
    """نصب‌کننده بدون صفحهٔ پرسش: با دوبار کلیک، خودش نصب می‌کند (فقط تأیید مدیریت ویندوز)."""
    p = repo / 'libs/portable/src/main.rs'
    if not p.exists():
        note(MISS, 'libs/portable/src/main.rs', 'فایل نیست')
        return
    s = read(p)
    old = """        if click_setup {
            args = vec!["--install".to_owned()];"""
    new = """        if click_setup {
            // نصب مستقیم و بی‌صفحه: کاربر فقط تأیید مدیریت را می‌زند
            args = vec!["--silent-install".to_owned()];"""
    if old in s:
        s = s.replace(old, new, 1)
        write(p, s)
        note(OK, 'libs/portable/src/main.rs (نصب بی‌صفحه)')
    else:
        note(SKIP, 'libs/portable/src/main.rs', 'از قبل یا پیدا نشد')

    # دوبار کلیک روی فایل نصبی، با هر نامی، باید نصب کند (به‌جز نسخهٔ portable)
    s = read(p)
    old2 = ('    let click_setup = args.is_empty() '
            '&& arg_exe.to_lowercase().ends_with("install.exe");')
    new2 = ('    // نام فایل مهم نیست: هر فایل نصبی (به‌جز portable) با دوبار کلیک نصب می‌کند\n'
            '    let click_setup = args.is_empty() '
            '&& !arg_exe.to_lowercase().contains("portable");')
    if old2 in s:
        write(p, s.replace(old2, new2, 1))
        note(OK, 'libs/portable/src/main.rs (نصب مستقل از نام فایل)')
    else:
        note(SKIP, 'libs/portable/src/main.rs (نام فایل)', 'از قبل یا پیدا نشد')

    # پس از نصب بی‌صفحه، پنجرهٔ برنامه هم باز شود (وگرنه کاربر فکر می‌کند نصب نشده)
    r = repo / 'src' / 'core_main.rs'
    if r.exists():
        t = read(r)
        old4 = 'let res = platform::install_me(options, "".to_owned(), true, debug);'
        new4 = ('// پس از نصب، پنجرهٔ برنامه هم باز شود\n'
                '                let res = platform::install_me(options, "".to_owned(), false, debug);')
        if old4 in t:
            write(r, t.replace(old4, new4, 1))
            note(OK, 'src/core_main.rs (باز شدن پنجره پس از نصب)')
        else:
            note(SKIP, 'src/core_main.rs', 'از قبل یا پیدا نشد')

    # کارت «نصب» داخل برنامه هم مستقیماً نصب کند، نه اینکه صفحهٔ دو‌دکمه‌ای را باز کند
    q = repo / 'src/ui_interface.rs'
    if q.exists():
        t = read(q)
        old3 = 'allow_err!(crate::run_me(vec!["--install"]));'
        new3 = 'allow_err!(crate::run_me(vec!["--silent-install"]));'
        if old3 in t:
            write(q, t.replace(old3, new3, 1))
            note(OK, 'src/ui_interface.rs (نصب مستقیم از کارت برنامه)')
        else:
            note(SKIP, 'src/ui_interface.rs', 'از قبل یا پیدا نشد')



def id_fields_ltr(repo: Path):
    """کادر شناسهٔ راه‌دور چپ‌به‌راست شود؛ وگرنه تایپ عدد در رابط راست‌به‌چپ برعکس دیده می‌شود."""
    cases = [
        (
            repo / 'flutter' / 'lib' / 'mobile' / 'pages' / 'connection_page.dart',
            "                      return AutoSizeTextField(\n"
            "                        controller: fieldTextEditingController,\n",
            "                      return AutoSizeTextField(\n"
            "                        textDirection: TextDirection.ltr,\n"
            "                        textAlign: TextAlign.left,\n"
            "                        controller: fieldTextEditingController,\n",
            'کادر شناسهٔ گوشی (چپ‌به‌راست)',
        ),
        (
            repo / 'flutter' / 'lib' / 'desktop' / 'pages' / 'connection_page.dart',
            "                          controller: fieldTextEditingController,\n"
            "                          inputFormatters: [IDTextInputFormatter()],\n",
            "                          textDirection: TextDirection.ltr,\n"
            "                          textAlign: TextAlign.left,\n"
            "                          controller: fieldTextEditingController,\n"
            "                          inputFormatters: [IDTextInputFormatter()],\n",
            'کادر شناسهٔ ویندوز (چپ‌به‌راست)',
        ),
    ]
    for path, old, new, label in cases:
        if not path.exists():
            note(MISS, label, f'فایل موجود نیست: {path}')
            continue
        t = read(path)
        if new in t:
            note(SKIP, label, 'از قبل اعمال شده')
            continue
        if old not in t:
            note(MISS, label, 'جای کادر شناسه پیدا نشد')
            continue
        write(path, t.replace(old, new, 1))
        note(OK, label, '1 تغییر')


def error_hook(repo: Path):
    """اگر خطایی در ساخت صفحه رخ داد، به جای صفحهٔ خاکستری متن خطا نشان داده شود"""
    m = repo / 'flutter/lib/main.dart'
    s = read(m)
    if 'nrispErrorHook' in s:
        note(SKIP, 'main.dart', 'قلاب خطا از قبل هست')
        return
    fn = """
// NRISP: نمایش متن خطا به جای صفحهٔ خاکستری
void nrispErrorHook() {
  ErrorWidget.builder = (FlutterErrorDetails details) => Material(
        color: const Color(0xFFFFFFFF),
        child: Directionality(
          textDirection: TextDirection.ltr,
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(14),
            child: Text(
              'NRISP-ERROR\\n${details.exception}\\n\\n${details.stack ?? ''}',
              style: const TextStyle(color: Color(0xFFC0392B), fontSize: 12),
            ),
          ),
        ),
      );
}

"""
    s = s.replace('Future<void> main(List<String> args) async {',
                  fn + 'Future<void> main(List<String> args) async {\n  nrispErrorHook();', 1)
    if 'nrispErrorHook();' not in s:
        note(MISS, 'main.dart', 'جای تابع main پیدا نشد')
        return
    write(m, s)
    note(OK, 'main.dart', 'قلاب نمایش خطا اضافه شد')



HELP_LTR = (
    "// NRISP: جهت پایهٔ متن راست‌به‌چپ (فارسی) است تا جمله‌های فارسی درست بچینند.\n"
    "// نوشته‌های انگلیسی داخل جمله‌ها با الگوریتم دوجهتهٔ استاندارد درست نشان داده می‌شوند.\n"
    "Widget nrispTextBase(Widget? child) => Directionality(\n"
    "      textDirection: TextDirection.rtl,\n"
    "      child: child ?? Container(),\n"
    "    );\n\n"
)


def ltr_text_base(repo: Path):
    """پایهٔ جهت متن برنامه راست‌به‌چپ (فارسی) می‌شود.

    چپ‌چین‌کردن کل برنامه اشتباه بود و جمله‌های فارسی را به سمت چپ می‌برد.
    اکنون پایه روی راست‌به‌چپ است و تنها متن‌های لاتینِ تک‌واژه‌ای (شناسه و
    مانند آن) جهت چپ‌به‌راست خودشان را نگه می‌دارند.
    """
    path = repo / 'flutter' / 'lib' / 'main.dart'
    if not path.exists():
        note(MISS, 'main.dart', 'فایل نیست')
        return
    src = read(path)
    helper = HELP_LTR
    if 'nrispTextBase' in src:
        note(SKIP, 'main.dart (پایهٔ متن راست‌به‌چپ)', 'از قبل بود')
        return
    pairs = [
        ('Future<void> main(List<String> args) async {',
         helper + 'Future<void> main(List<String> args) async {'),
        ('        child = botToastBuilder(context, child);\n        return child;',
         '        child = botToastBuilder(context, child);\n        return nrispTextBase(child);'),
        ('                  if (isLinux) {\n                    return buildVirtualWindowFrame(context, child);\n                  } else {\n                    return workaroundWindowBorder(context, child);\n                  }',
         '                  if (isLinux) {\n                    return nrispTextBase(buildVirtualWindowFrame(context, child));\n                  } else {\n                    return nrispTextBase(workaroundWindowBorder(context, child));\n                  }'),
        ('    child: child ?? Container(),\n  );\n}\n\n_registerEventHandler() {',
         '    child: nrispTextBase(child),\n  );\n}\n\n_registerEventHandler() {'),
    ]
    hits = 0
    for old, new in pairs:
        if old in src:
            src = src.replace(old, new, 1)
            hits += 1
        else:
            note(MISS, 'main.dart (پایهٔ متن)', 'بخشی پیدا نشد')
    write(path, src)
    note(OK if hits == len(pairs) else MISS,
         'main.dart (پایهٔ متن راست‌به‌چپ)', '%d از %d' % (hits, len(pairs)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    args = ap.parse_args()
    repo = Path(args.repo).resolve()
    if not (repo / 'Cargo.toml').exists() or not (repo / 'flutter').exists():
        print(f'ERROR: پوشهٔ سورس راست‌دسک نیست: {repo}')
        sys.exit(2)

    print(f'سورس: {repo}')
    # NRISP: وصلهٔ «زبان فارسی اجباری» برداشته شد.
    # همین وصله (localeName=fa و Locale('fa')) تصویر اندروید را سیاه می‌کرد و در
    # ویندوز چیدمان راست‌به‌چپ را روی همه‌چیز تحمیل می‌کرد و متن منوها را
    # به‌هم می‌ریخت. زبان فارسی از سیستم/تنظیمات خود برنامه خوانده می‌شود.
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
    window_buttons(repo)
    remove_extras(repo)
    disable_account(repo)
    connect_card_fixes(repo)
    final_tweaks(repo)
    silent_installer(repo)
    bundle_font(repo)
    window_title(repo)
    ltr_text_base(repo)
    menu_side(repo)
    settings_font(repo)
    line_height_fix(repo)
    bump_version(repo)
    voice_call_hint(repo)
    id_fields_ltr(repo)
    error_hook(repo)

    print('\n--- خلاصه ---')
    print(f"اعمال‌شده: {sum(1 for r in rows if r[0] == OK)}   "
          f"از قبل: {sum(1 for r in rows if r[0] == SKIP)}   "
          f"پیدا نشد: {sum(1 for r in rows if r[0] == MISS)}")
    if any(r[0] == MISS for r in rows):
        print('موارد پیدا نشده در بالا فهرست شده‌اند.')


if __name__ == '__main__':
    main()
