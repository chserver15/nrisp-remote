# -*- coding: utf-8 -*-
"""ویدیو/تصویر: نه — این وصله «نمایش شناسهٔ ذخیره‌شده» را چپ‌به‌راست می‌کند.

کادر تایپ شناسه پیش‌تر چپ‌به‌راست شد و درست کار می‌کند، اما نمایش شناسه در
فهرست دستگاه‌های ذخیره‌شده (پایین صفحه)، پیشنهادهای جست‌وجو و صفحهٔ «درباره»
در بستر راست‌به‌چپ برعکس دیده می‌شد. با نویسه‌های کنترلی جهت (LRI/PDI) و
textDirection، فقط خودِ شناسه چپ‌به‌راست نمایش داده می‌شود؛ متن فارسی اطراف
راست‌به‌چپ می‌ماند.

اجرای دوباره بی‌خطر است (اگر وصله باشد رد می‌شود).
"""
import argparse
import io
import re
import sys
from pathlib import Path

OK, SKIP, MISS = '[+]', '[-]', '[!]'
MARK = 'nrisp_id_ltr2'
rows = []

# در کد دارت این‌ها به شکل \u2066 و \u2069 نوشته می‌شوند
LRI = '\\u2066'
PDI = '\\u2069'


def note(kind, where, detail=''):
    rows.append((kind, where, detail))
    print(f'{kind} {where}' + (f'   ->  {detail}' if detail else ''))


def read(p: Path):
    with io.open(p, encoding='utf-8') as f:
        return f.read()


def write(p: Path, s: str):
    with io.open(p, 'w', encoding='utf-8', newline='') as f:
        f.write(s)


def patch(repo: Path, rel: str, rx: str, repl: str, label: str):
    """هر جا الگو بود، شناسه را در نویسه‌های جهت می‌پیچد."""
    p = repo / rel
    if not p.exists():
        note(MISS, label, 'فایل نیست')
        return
    s = read(p)
    if LRI in s and label in s:
        note(SKIP, label, 'از قبل درست شده')
        return
    n = len(re.findall(rx, s))
    if n == 0:
        if LRI in s:
            note(SKIP, label, 'از قبل درست شده')
        else:
            note(MISS, label, 'جای الگو پیدا نشد')
        return
    s2 = re.sub(rx, lambda m: repl, s)
    if s2 == s:
        note(SKIP, label, 'تغییری لازم نبود')
        return
    write(p, s2)
    note(OK, label, f'{n} مورد')


def patch_plain(repo: Path, rel: str, old: str, new: str, label: str):
    p = repo / rel
    if not p.exists():
        note(MISS, label, 'فایل نیست')
        return
    s = read(p)
    if new in s or (LRI in s and old not in s):
        note(SKIP, label, 'از قبل درست شده')
        return
    if old not in s:
        note(MISS, label, 'جای متن پیدا نشد')
        return
    write(p, s.replace(old, new, 1))
    note(OK, label)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    a = ap.parse_args()
    repo = Path(a.repo).resolve()
    print(f'سورس: {repo}')

    # ۱) فهرست دستگاه‌های ذخیره‌شده (پایین صفحهٔ اتصال) — هر دو کارت
    patch(
        repo,
        'flutter/lib/common/widgets/peer_card.dart',
        r'peer\.alias\.isEmpty \? formatID\(peer\.id\) : peer\.alias',
        "peer.alias.isEmpty ? '" + LRI + "${formatID(peer.id)}" + PDI +
        "' : peer.alias",
        'کارت دستگاه ذخیره‌شده (peer_card)',
    )

    # ۲) پیشنهادهای جست‌وجوی شناسه
    patch(
        repo,
        'flutter/lib/common/widgets/autocomplete.dart',
        r"formatID\(\s*widget\.peer\.id\)",
        "'" + LRI + "${formatID(widget.peer.id)}" + PDI + "'",
        'پیشنهادهای جست‌وجو (autocomplete)',
    )

    # ۳) شناسهٔ این دستگاه در تنظیمات گوشی
    patch_plain(
        repo,
        'flutter/lib/mobile/pages/settings_page.dart',
        'child: Text(_myId)',
        'child: Text(_myId, textDirection: TextDirection.ltr)',
        'تنظیمات اندروید (_myId)',
    )

    # ۴) شناسهٔ این دستگاه در صفحهٔ دربارهٔ ویندوز
    patch_plain(
        repo,
        'flutter/lib/desktop/pages/desktop_setting_page.dart',
        "child: Text('${translate('ID')}: $myId')",
        "child: Text('${translate('ID')}: " + LRI + "$myId" + PDI + "')",
        'دربارهٔ ویندوز (myId)',
    )

    print('\n--- خلاصه ---')
    print('اعمال‌شده:', sum(1 for r in rows if r[0] == OK),
          ' از قبل:', sum(1 for r in rows if r[0] == SKIP),
          ' پیدا نشد:', sum(1 for r in rows if r[0] == MISS))
    return 0 if not any(r[0] == MISS for r in rows) else 0


if __name__ == '__main__':
    sys.exit(main())
