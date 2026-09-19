# -*- coding: utf-8 -*-
"""تنظیمات ویژهٔ نسخهٔ اندروید: پیش‌فرض «مقیاس تطبیقی» تا تصویر تمام‌صفحه بیاید."""
import argparse
import io
import sys
from pathlib import Path

OK, SKIP, MISS = '[+]', '[-]', '[!]'
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


def default_view_style(repo: Path):
    """مقدار پیش‌فرض سبک نمایش در سمت راست = adaptive (مقیاس تطبیقی)."""
    p = repo / 'libs' / 'hbb_common' / 'src' / 'config.rs'
    if not p.exists():
        note(MISS, 'config.rs', 'فایل نیست')
        return
    s = read(p)
    old = ('            #[cfg(not(any(target_os = "android", target_os = "ios")))]\n'
           '            keys::OPTION_VIEW_STYLE => self.get_string(key, "original", vec!["adaptive"]),')
    new = ('            #[cfg(not(any(target_os = "android", target_os = "ios")))]\n'
           '            // پیش‌فرض موسسه: مقیاس تطبیقی (تصویر تمام‌صفحه، بدون نیاز به اسکرول)\n'
           '            keys::OPTION_VIEW_STYLE => self.get_string(key, "adaptive", vec!["original"]),')
    if new in s:
        note(SKIP, 'پیش‌فرض مقیاس تطبیقی', 'از قبل بود')
        return
    if old in s:
        write(p, s.replace(old, new, 1))
        note(OK, 'config.rs (پیش‌فرض مقیاس تطبیقی)')
    else:
        note(MISS, 'config.rs', 'جای پیش‌فرض سبک نمایش پیدا نشد')


def settings_order(repo: Path):
    """در صفحهٔ تنظیمات اندروید، گزینهٔ تطبیقی اول بیاید."""
    p = repo / 'flutter' / 'lib' / 'mobile' / 'pages' / 'settings_page.dart'
    if not p.exists():
        note(MISS, 'settings_page.dart', 'فایل نیست')
        return
    s = read(p)
    bad = ("                _RadioEntry('Scale adaptive', kRemoteViewStyleAdaptive),\n"
           "                _RadioEntry('Scale adaptive', kRemoteViewStyleAdaptive)")
    good = "                _RadioEntry('Scale adaptive', kRemoteViewStyleAdaptive),"
    if bad in s:
        write(p, s.replace(bad, good, 1))
        note(OK, 'settings_page.dart (رفع گزینهٔ تکراری)')
    else:
        note(SKIP, 'settings_page.dart', 'نیازی به اصلاح نبود')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    a = ap.parse_args()
    repo = Path(a.repo).resolve()
    print(f'سورس: {repo}')
    default_view_style(repo)
    settings_order(repo)
    print('\n--- خلاصه ---')
    print('اعمال‌شده:', sum(1 for r in rows if r[0] == OK),
          ' از قبل:', sum(1 for r in rows if r[0] == SKIP),
          ' پیدا نشد:', sum(1 for r in rows if r[0] == MISS))


if __name__ == '__main__':
    main()
