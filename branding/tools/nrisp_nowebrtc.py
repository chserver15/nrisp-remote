# -*- coding: utf-8 -*-
"""خاموش‌کردن مسیر WebRTC در نسخهٔ ما (داخل خود برنامه، نه تنظیم دستی).

یافته: در شاخهٔ master راست‌دسک، گزینهٔ «enable-webrtc» روی سرور عمومی
پیش‌فرض روشن است؛ پس برنامهٔ کنترل‌کننده (گوشی) اول مسیر WebRTC را می‌سازد
و آن را ترجیح می‌دهد. در نسخهٔ رسمی ۱.۴.۹ این مسیر وجود ندارد. نتیجهٔ دیده‌شده
در حالت WebRTC: جلسه برقرار می‌شود و موس کار می‌کند ولی تصویر نمی‌آید.

این وصله همان تابع را خاموش می‌کند تا مسیر کلاسیک (همان مسیر نسخهٔ رسمی)
بازگردد. اجرای دوباره بی‌خطر است.
"""
import argparse
import io
import sys
from pathlib import Path

OK, SKIP, MISS = '[+]', '[-]', '[!]'
rows = []
MARK = 'NRISP_NO_WEBRTC'

REL = 'src/common.rs'
OLD = '''pub fn get_webrtc_enabled() -> bool {
    config::option2bool(
        keys::OPTION_ENABLE_WEBRTC,
        &get_local_option(keys::OPTION_ENABLE_WEBRTC),
    )
}'''
NEW = '''pub fn get_webrtc_enabled() -> bool {
    // NRISP_NO_WEBRTC: مسیر WebRTC در نسخهٔ ما خاموش است؛ جلسه برقرار می‌شد و
    // موس کار می‌کرد ولی تصویر نمی‌آمد، در حالی که نسخهٔ رسمی ۱.۴.۹ این مسیر
    // را ندارد و تصویر می‌آید. مسیر کلاسیک استفاده می‌شود.
    false
}'''


def note(kind, where, detail=''):
    rows.append((kind, where, detail))
    print(f'{kind} {where}' + (f'   ->  {detail}' if detail else ''))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    a = ap.parse_args()
    repo = Path(a.repo).resolve()
    p = repo / REL
    print(f'سورس: {repo}')
    if not p.exists():
        note(MISS, 'src/common.rs', 'فایل نیست')
        return 0
    with io.open(p, encoding='utf-8') as f:
        s = f.read()
    if MARK in s:
        note(SKIP, 'get_webrtc_enabled', 'از قبل خاموش بود')
        return 0
    if OLD not in s:
        note(MISS, 'get_webrtc_enabled', 'جای تابع پیدا نشد')
        return 0
    with io.open(p, 'w', encoding='utf-8', newline='') as f:
        f.write(s.replace(OLD, NEW, 1))
    note(OK, 'get_webrtc_enabled', 'خاموش شد')
    print('\n--- خلاصه ---')
    print('اعمال‌شده:', sum(1 for r in rows if r[0] == OK))
    return 0


if __name__ == '__main__':
    sys.exit(main())
