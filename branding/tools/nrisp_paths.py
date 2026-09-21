# -*- coding: utf-8 -*-
"""بستن ردپای «راست‌دسک» در نام پوشه‌ها و فایل‌های ساختهٔ برنامه.

دو کار:
۱) نام پیش‌فرض خودِ برنامه در هستهٔ راست‌دسک («RustDesk») به نام موسسه تغییر
   می‌کند؛ در نتیجه پوشهٔ ضبط تصویر، پوشهٔ سرویس ویندوز و متن‌های ترجمه‌شده
   دیگر «RustDesk» نشان نمی‌دهند.
۲) پوشهٔ ضبط تصویر در اندروید با نام کوتاه و بی‌ردپا ساخته می‌شود: nrisp

اجرای دوباره بی‌خطر است.
"""
import argparse
import io
import sys
from pathlib import Path

OK, SKIP, MISS = '[+]', '[-]', '[!]'
APP_NAME = 'NRISP Remote Access'
rows = []

PAIRS = [
    ('libs/hbb_common/src/config.rs',
     'pub static ref APP_NAME: RwLock<String> = RwLock::new("RustDesk".to_owned());',
     'pub static ref APP_NAME: RwLock<String> = RwLock::new("%s".to_owned());' % APP_NAME,
     'نام پیش‌فرض برنامه در هسته (RustDesk → نام موسسه)'),
    ('src/ui_interface.rs',
     'path.push_str(format!("/{appname}/ScreenRecord").as_str());',
     'path.push_str("/nrisp/ScreenRecord");  // NRISP: پوشهٔ ضبط بدون ردپای نام سازنده',
     'پوشهٔ ضبط در اندروید (ScreenRecord)'),
]


def note(kind, where, detail=''):
    rows.append((kind, where, detail))
    print(f'{kind} {where}' + (f'   ->  {detail}' if detail else ''))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    a = ap.parse_args()
    repo = Path(a.repo).resolve()
    print(f'سورس: {repo}')
    for rel, old, new, label in PAIRS:
        p = repo / rel
        if not p.exists():
            note(MISS, label, 'فایل نیست: ' + rel)
            continue
        with io.open(p, encoding='utf-8') as f:
            s = f.read()
        if new in s:
            note(SKIP, label, 'از قبل بود')
            continue
        if old not in s:
            note(MISS, label, 'جای متن پیدا نشد')
            continue
        with io.open(p, 'w', encoding='utf-8', newline='') as f:
            f.write(s.replace(old, new, 1))
        note(OK, label)
    print('\n--- خلاصه ---')
    print('اعمال‌شده:', sum(1 for r in rows if r[0] == OK),
          ' از قبل:', sum(1 for r in rows if r[0] == SKIP),
          ' پیدا نشد:', sum(1 for r in rows if r[0] == MISS))
    return 0


if __name__ == '__main__':
    sys.exit(main())
