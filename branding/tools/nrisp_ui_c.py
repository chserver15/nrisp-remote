# -*- coding: utf-8 -*-
"""اجرای بخشی از وصله‌های رابط کاربری (برای پیدا کردن وصلهٔ مقصر تصویر)."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('nrisp_ui', str(HERE / 'nrisp_ui.py'))
ui = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ui)

repo = Path(sys.argv[1]).resolve()
print('سورس:', repo)
for fn in ['disable_account']:
    print('---', fn)
    getattr(ui, fn)(repo)
print('تمام')
