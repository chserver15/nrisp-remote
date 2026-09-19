#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""پیش‌فرض‌های خودِ برنامه (اندروید) — بدون نیاز به تنظیم دستی:
   ۱) رمزگشای نرم‌افزاری (رمزگشای سخت‌افزاری روی بعضی گوشی‌ها تصویر خاکستری می‌دهد)
   ۲) کدک پیش‌فرض VP9 (مطمئن‌ترین کدک روی گوشی)
   این تنظیم فقط پیش‌فرض است؛ کاربر می‌تواند از تنظیمات عوضش کند.
"""
import io
import re
import sys
from pathlib import Path

REPO = Path(sys.argv[1] if len(sys.argv) > 1 else '.')
F = REPO / 'libs/hbb_common/src/config.rs'

HELPER = '''
// NRISP: پیش‌فرض‌های خودِ برنامه (بدون نیاز به تنظیم دستی)
fn nrisp_default_option(k: &str) -> String {
    #[cfg(any(target_os = "android", target_os = "ios"))]
    {
        match k {
            // رمزگشای سخت‌افزاری روی برخی گوشی‌ها فریم را نشان نمی‌دهد (صفحهٔ خاکستری)
            "enable-hwcodec" => return "N".to_string(),
            // مطمئن‌ترین کدک برای گوشی
            "codec-preference" => return "vp9".to_string(),
            _ => {}
        }
    }
    let _ = k;
    String::new()
}
'''

OLD = '''    pub fn get_option(k: &str) -> String {
        get_or(
            &OVERWRITE_LOCAL_SETTINGS,
            &LOCAL_CONFIG.read().unwrap().options,
            &DEFAULT_LOCAL_SETTINGS,
            k,
        )
        .unwrap_or_default()
    }'''

NEW = '''    pub fn get_option(k: &str) -> String {
        get_or(
            &OVERWRITE_LOCAL_SETTINGS,
            &LOCAL_CONFIG.read().unwrap().options,
            &DEFAULT_LOCAL_SETTINGS,
            k,
        )
        .unwrap_or_else(|| nrisp_default_option(k))
    }'''


def main():
    if not F.exists():
        print('فایل پیدا نشد:', F)
        return 1
    t = io.open(F, encoding='utf-8').read()
    if 'nrisp_default_option' in t:
        print('پیش‌فرض‌ها قبلاً اعمال شده — رد شد')
        return 0
    if OLD not in t:
        print('!!! محل مورد نظر در config.rs پیدا نشد')
        return 2
    t = t.replace(OLD, NEW, 1)
    # تابع کمکی را پیش از impl یا انتهای فایل اضافه کن
    m = re.search(r'\nimpl Config \{', t)
    if m:
        t = t[:m.start()] + '\n' + HELPER + t[m.start():]
    else:
        t += '\n' + HELPER
    io.open(F, 'w', encoding='utf-8').write(t)
    print('پیش‌فرض‌های اندروید اعمال شد: hwcodec=N و codec=vp9')
    return 0


if __name__ == '__main__':
    sys.exit(main())
