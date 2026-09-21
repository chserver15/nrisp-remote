# -*- coding: utf-8 -*-
"""رکورد و تماس صوتی: هر دو داخل برنامه درست می‌شوند (بدون تنظیم دستی).

۱) تماس صوتی روی اندروید ۶ تا ۱۰ هم فعال می‌شود (پیش‌فرض راست‌دسک فقط از
   اندروید ۱۱ به بعد اجازه می‌داد؛ در نتیجه در گوشی‌های قدیمی‌تر فقط چت
   در دسترس بود).
۲) اجازهٔ رکورد جلسه از سمت میزبان همیشه داده می‌شود و دکمهٔ «رکورد» در فهرست
   جلسهٔ موبایل همیشه دیده می‌شود.
۳) مسیر ذخیرهٔ فایل ضبط در ویندوز/اندروید مطمئن و بی‌ردپا می‌شود؛ اگر پوشه
   ساخته نشود، مسیر جایگزین امتحان می‌شود تا رکورد بی‌صدا شکست نخورد.

اجرای دوباره بی‌خطر است (هر تغییر فقط یک بار اعمال می‌شود).
"""
import argparse
import io
import re
import sys
from pathlib import Path

OK, SKIP, MISS = '[+]', '[-]', '[!]'
rows = []

PAIRS = [
    # ---- ۱) تماس صوتی روی اندروید قدیمی‌تر ----
    ('flutter/android/app/src/main/kotlin/com/carriez/flutter_hbb/AudioRecordHandle.kt',
     '''        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.Q) {
            return false
        }''',
     '''        // NRISP: مسیر ضبط صدای صفحه به اندروید ۱۰+ نیاز دارد، اما ضبط صدای
        // میکروفون برای تماس صوتی روی نسخه‌های قدیمی‌تر هم کار می‌کند.
        if (!inVoiceCall && Build.VERSION.SDK_INT < Build.VERSION_CODES.Q) {
            return false
        }''',
     'AudioRecordHandle.kt (میکروفون روی اندروید قدیمی‌تر)'),

    # ---- ۲) اجازهٔ رکورد جلسه از سمت میزبان ----
    ('src/server/connection.rs',
     'recording: Self::permission(keys::OPTION_ENABLE_RECORD_SESSION, &control_permissions),',
     'recording: true, // NRISP: اجازهٔ رکورد جلسه همیشه داده می‌شود تا رکورد کار کند',
     'connection.rs (اجازهٔ رکورد جلسه)'),

    # ---- ۲ب) دکمهٔ رکورد در فهرست جلسهٔ موبایل ----
    ('flutter/lib/common/widgets/toolbar.dart',
     '''  if (!(isDesktop || isWeb) &&
      bind.mainGetLocalOption(key: kOptionHideRecordingButton) != 'Y' &&
      (ffi.recordingModel.start || (perms["recording"] != false))) {''',
     '''  // NRISP: دکمهٔ رکورد همیشه در فهرست جلسهٔ موبایل دیده می‌شود.
  if (!(isDesktop || isWeb)) {''',
     'toolbar.dart (دکمهٔ رکورد در موبایل)'),

    # ---- ۳) مسیر ذخیرهٔ ضبط (ویندوز) ----
    ('src/ui_interface.rs',
     '''            let drive = std::env::var("SystemDrive").unwrap_or("C:".to_owned());
            let dir =
                std::path::PathBuf::from(format!("{drive}\\\\ProgramData\\\\{appname}\\\\recording",));
            return dir.to_string_lossy().to_string();''',
     '''            let drive = std::env::var("SystemDrive").unwrap_or("C:".to_owned());
            let dir =
                std::path::PathBuf::from(format!("{drive}\\\\ProgramData\\\\{appname}\\\\recording",));
            // NRISP: اگر سرویس نتواند این پوشه را بسازد، به مسیر کاربر می‌رویم
            // تا رکورد بی‌دلیل شکست نخورد.
            let created = try_create(dir.as_path());
            if !created.is_empty() {
                return created;
            }''',
     'ui_interface.rs (مسیر ضبط در ویندوز)'),
    # ---- ۴) رکورد خودکار (بدون کار دستی) ----
    ('src/client/io_loop.rs',
     '            let auto_record = LocalConfig::get_bool_option(keys::OPTION_ALLOW_AUTO_RECORD_OUTGOING);',
     '''            // NRISP: رکورد جلسه به‌صورت خودکار فعال است (بدون کار دستی کاربر).
            // اگر کاربر خودش گزینه را خاموش کرده باشد، همان مقدار رعایت می‌شود.
            let auto_record = match LocalConfig::get_option(keys::OPTION_ALLOW_AUTO_RECORD_OUTGOING) {
                v if v.is_empty() => true,
                _ => LocalConfig::get_bool_option(keys::OPTION_ALLOW_AUTO_RECORD_OUTGOING),
            };''',
     'io_loop.rs (رکورد خودکار جلسه‌های خروجی)'),
]



REGEX_RULES = [
    # تماس صوتی در اندروید به‌صورت پیش‌فرض فعال است؛ پیش‌فرض راست‌دسک فقط
    # اندروید ۱۱+ را قبول می‌کرد و در بقیهٔ گوشی‌ها فقط «چت» می‌ماند.
    ('flutter/android/app/src/main/kotlin/com/carriez/flutter_hbb/common.kt',
     re.compile(r'fun isSupportVoiceCall\(\): Boolean \{[^}]*\}'),
     'fun isSupportVoiceCall(): Boolean {\n'
     '    // NRISP: تماس صوتی به‌صورت پیش‌فرض فعال است (بدون توجه به نسخهٔ اندروید);\n'
     '    // اجازهٔ میکروفون در هنگام تماس از کاربر گرفته می‌شود.\n'
     '    return true\n'
     '}',
     'common.kt (تماس صوتی پیش‌فرض فعال)'),
]


def apply_regex_rules(repo: Path):
    for rel, rx, new, label in REGEX_RULES:
        fp = resolve(repo, rel)
        if not fp.exists():
            note(MISS, label, 'فایل نیست: ' + rel)
            continue
        with io.open(fp, encoding='utf-8') as f:
            t = f.read()
        new_t, n = rx.subn(new, t, count=1)
        if n == 0:
            if 'NRISP: تماس صوتی به‌صورت پیش‌فرض فعال است' in t:
                note(SKIP, label, 'از قبل بود')
            else:
                note(MISS, label, 'جای تابع پیدا نشد')
            continue
        with io.open(fp, 'w', encoding='utf-8', newline='') as f:
            f.write(new_t)
        note(OK, label)



def resolve(repo: Path, rel: str) -> Path:
    """مسیر پرونده را پیدا می‌کند؛ اگر بستهٔ کاتلین جابه‌جا شده باشد (تغییر نام
    بسته در برندسازی)، پرونده را از روی نامش پیدا می‌کند."""
    direct = repo / rel
    if direct.exists():
        return direct
    name = rel.split('/')[-1]
    hits = sorted(repo.glob('**/' + name))
    for h in hits:
        if 'kotlin' in str(h) or 'flutter' in str(h) or str(h).endswith(name):
            return h
    return direct


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
        p = resolve(repo, rel)
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
    apply_regex_rules(repo)
    print('\n--- خلاصه ---')
    print('اعمال‌شده:', sum(1 for r in rows if r[0] == OK),
          ' از قبل:', sum(1 for r in rows if r[0] == SKIP),
          ' پیدا نشد:', sum(1 for r in rows if r[0] == MISS))
    return 0


if __name__ == '__main__':
    sys.exit(main())
