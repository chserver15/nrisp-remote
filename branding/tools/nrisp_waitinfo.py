# -*- coding: utf-8 -*-
"""نوار «در انتظار تصویر» در صفحهٔ جلسهٔ گوشی.

تا وقتی اولین تصویر از کامپیوتر نرسیده، روی صفحهٔ سیاه نوشته می‌شود که
طرف مقابل چه کدکی را انتخاب کرده، چند نمایشگر و چه وضوحی گزارش کرده و
نسخه‌اش چیست. با این اطلاعات معلوم می‌شود خرابی از طرف کامپیوتر است یا گوشی.

اجرای دوباره بی‌خطر است.
"""
import argparse
import io
import shutil
import sys
from pathlib import Path

OK, SKIP, MISS = '[+]', '[-]', '[!]'
rows = []

SRC_REL = 'flutter/lib/nrisp/nrisp_waiting_info.dart'
PAGE_REL = 'flutter/lib/mobile/pages/remote_page.dart'

IMPORT_LINE = "import '../../models/model.dart';"
IMPORT_NEW = ("import '../../models/model.dart';\n"
              "import '../../nrisp/nrisp_waiting_info.dart';")

ANCHOR = "          final paints = [\n            ImagePaint(ffiModel: gFFI.ffiModel),"
ANCHOR_NEW = ("          final paints = [\n"
              "            ImagePaint(ffiModel: gFFI.ffiModel),\n"
              "            const NrispWaitingInfo(),")


def note(kind, where, detail=''):
    rows.append((kind, where, detail))
    print(f'{kind} {where}' + (f'   ->  {detail}' if detail else ''))


def read(p: Path):
    with io.open(p, encoding='utf-8') as f:
        return f.read()


def write(p: Path, s: str):
    with io.open(p, 'w', encoding='utf-8', newline='') as f:
        f.write(s)


def copy_widget(repo: Path):
    here = Path(__file__).resolve().parent.parent.parent  # ریشهٔ مخزن برند
    src = here / 'ui' / 'flutter' / 'lib' / 'nrisp' / 'nrisp_waiting_info.dart'
    dst = repo / SRC_REL
    if not src.exists():
        note(MISS, 'nrisp_waiting_info.dart', 'فایل منبع در مخزن برند نیست')
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() and read(dst) == read(src):
        note(SKIP, 'nrisp_waiting_info.dart', 'از قبل بود')
        return
    shutil.copyfile(str(src), str(dst))
    note(OK, 'nrisp_waiting_info.dart')


def patch_page(repo: Path):
    p = repo / PAGE_REL
    if not p.exists():
        note(MISS, 'remote_page.dart', 'فایل نیست')
        return
    s = read(p)
    changed = False
    if 'nrisp/nrisp_waiting_info.dart' not in s:
        if IMPORT_LINE in s:
            s = s.replace(IMPORT_LINE, IMPORT_NEW, 1)
            changed = True
            note(OK, 'import در remote_page.dart')
        else:
            note(MISS, 'import در remote_page.dart', 'جای import پیدا نشد')
    else:
        note(SKIP, 'import در remote_page.dart', 'از قبل بود')

    if 'const NrispWaitingInfo()' not in s:
        if ANCHOR in s:
            s = s.replace(ANCHOR, ANCHOR_NEW, 1)
            changed = True
            note(OK, 'نوار انتظار تصویر در صفحهٔ جلسه')
        else:
            note(MISS, 'نوار انتظار تصویر', 'جای افزودن پیدا نشد')
    else:
        note(SKIP, 'نوار انتظار تصویر', 'از قبل بود')

    if changed:
        write(p, s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    a = ap.parse_args()
    repo = Path(a.repo).resolve()
    print(f'سورس: {repo}')
    copy_widget(repo)
    patch_page(repo)
    print('\n--- خلاصه ---')
    print('اعمال‌شده:', sum(1 for r in rows if r[0] == OK),
          ' از قبل:', sum(1 for r in rows if r[0] == SKIP),
          ' پیدا نشد:', sum(1 for r in rows if r[0] == MISS))
    return 0


if __name__ == '__main__':
    sys.exit(main())
