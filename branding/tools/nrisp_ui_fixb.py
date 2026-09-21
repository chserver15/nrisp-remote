# -*- coding: utf-8 -*-
"""اجرای وصله‌های رابط کاربری جز فهرست حذف‌شده."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('nrisp_ui', str(HERE / 'nrisp_ui.py'))
ui = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ui)

ALL = ['persian_default','restyle_theme','dorsan_look','tabbar_title','tabbar_theme','drop_powered',
       'replace_links','fa_brand_cleanup','replace_visible_urls','corporate_footer','hide_install_card',
       'window_buttons','remove_extras','disable_account','connect_card_fixes','final_tweaks',
       'silent_installer','bundle_font','window_title','menu_side','settings_font','line_height_fix',
       'bump_version','voice_call_hint','id_fields_ltr','error_hook']
EXCLUDE = ['persian_default']

repo = Path(sys.argv[1]).resolve()
print('سورس:', repo)
for fn in ALL:
    if fn in EXCLUDE:
        print('--- حذف‌شده:', fn)
        continue
    print('---', fn)
    getattr(ui, fn)(repo)
print('تمام')
