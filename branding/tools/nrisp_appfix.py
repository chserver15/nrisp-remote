#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""پیش‌فرض کدک روی گوشی — بدون کار دستی:
   روی اندروید/آی‌اواس، اگر کدکی انتخاب نشده باشد، برنامه از طرف مقابل
   کدک VP9 را می‌خواهد؛ راست‌دسک رمزگشای نرم‌افزاری VP9 را همیشه دارد،
   پس تصویر روی گوشی‌هایی که رمزگشای سخت‌افزاری‌شان مشکل دارد هم می‌آید.
"""
import io
import sys
from pathlib import Path

REPO = Path(sys.argv[1] if len(sys.argv) > 1 else '.')
F = REPO / 'libs/scrap/src/common/codec.rs'
MARK = 'nrisp_video_prefer'

HELPER = '''
// NRISP: روی گوشی، کدک مطمئن (VP9 نرم‌افزاری) پیش‌فرض شود تا تصویر همیشه بیاید
fn nrisp_video_prefer() -> PreferCodec {
    #[cfg(any(target_os = "android", target_os = "ios"))]
    {
        PreferCodec::VP9
    }
    #[cfg(not(any(target_os = "android", target_os = "ios")))]
    {
        PreferCodec::Auto
    }
}
'''

ANCHOR_EMPTY = '''        if id.is_empty() {
            return (PreferCodec::Auto, Chroma::I420);
        }'''
NEW_EMPTY = '''        if id.is_empty() {
            return (nrisp_video_prefer(), Chroma::I420);
        }'''

ANCHOR_CHROMA = '        let chroma = if options.get("i444") == Some(&"Y".to_string()) {'
NEW_CHROMA = '''        // NRISP: اگر کدکی انتخاب نشده، کدک مطمئن خودمان (VP9)
        #[cfg(any(target_os = "android", target_os = "ios"))]
        let codec = match codec {
            PreferCodec::Auto => PreferCodec::VP9,
            other => other,
        };
        let chroma = if options.get("i444") == Some(&"Y".to_string()) {'''


def main():
    if not F.exists():
        print('!!! فایل پیدا نشد:', F)
        return 1
    t = io.open(F, encoding='utf-8').read()
    if MARK in t:
        print('پیش‌فرض کدک قبلاً اعمال شده — رد شد')
        return 0
    if ANCHOR_EMPTY not in t:
        print('!!! محل اول پیدا نشد')
        return 2
    t = t.replace(ANCHOR_EMPTY, NEW_EMPTY, 1)
    if ANCHOR_CHROMA not in t:
        print('!!! محل دوم پیدا نشد')
        return 3
    t = t.replace(ANCHOR_CHROMA, NEW_CHROMA, 1)
    t = t.rstrip() + '\n' + HELPER
    io.open(F, 'w', encoding='utf-8').write(t)
    print('پیش‌فرض کدک VP9 برای گوشی اعمال شد')
    return 0


if __name__ == '__main__':
    sys.exit(main())
