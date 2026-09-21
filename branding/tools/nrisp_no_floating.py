# -*- coding: utf-8 -*-
"""آیکون شناور روی صفحهٔ گوشی حذف می‌شود.

راست‌دسک وقتی برنامه به پس‌زمینه می‌رود یک آیکون شناور روی صفحه می‌گذارد.
این آیکون در نسخهٔ موسسه نمایش داده نمی‌شود؛ بنابراین نه چیزی روی صفحه
می‌افتد و نه لازم است کاربر «توقف سرویس» بزند تا آن را ببندد.

اجرای دوباره بی‌خطر است.
"""
import argparse
import io
import sys
from pathlib import Path

OK, SKIP, MISS = '[+]', '[-]', '[!]'

OLD = '        val disableFloatingWindow = FFI.getLocalOption("disable-floating-window") == "Y"'
NEW = ('        // NRISP: آیکون شناور روی صفحهٔ گوشی هرگز نمایش داده نمی‌شود؛\n'
       '        // کاربر نباید برای بستن آن کاری انجام دهد.\n'
       '        val disableFloatingWindow = true')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    a = ap.parse_args()
    repo = Path(a.repo).resolve()
    cands = sorted(repo.glob('flutter/android/**/MainActivity.kt'))
    if not cands:
        print(f'{MISS} MainActivity.kt پیدا نشد')
        return 0
    hits = 0
    for p in cands:
        with io.open(p, encoding='utf-8') as f:
            s = f.read()
        if NEW in s:
            print(f'{SKIP} آیکون شناور ({p.name})', '-> از قبل بود')
            continue
        if OLD not in s:
            print(f'{MISS} آیکون شناور ({p.name})', '-> جای متن پیدا نشد')
            continue
        with io.open(p, 'w', encoding='utf-8', newline='') as f:
            f.write(s.replace(OLD, NEW, 1))
        print(f'{OK} آیکون شناور روی صفحه حذف شد ({p.name})')
        hits += 1
    print('\n--- خلاصه ---')
    print('اعمال‌شده:', hits)
    return 0


if __name__ == '__main__':
    sys.exit(main())
