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
import sys
from pathlib import Path

OK, SKIP, MISS = '[+]', '[-]', '[!]'
rows = []

PAIRS = [
    # ---- ۱) تماس صوتی روی اندروید قدیمی‌تر ----
    ('flutter/android/app/src/main/kotlin/com/carriez/flutter_hbb/common.kt',
     '''fun isSupportVoiceCall(): Boolean {
    // https://developer.android.com/reference/android/media/MediaRecorder.AudioSource#VOICE_COMMUNICATION
    return Build.VERSION.SDK_INT >= Build.VERSION_CODES.R
}''',
     '''fun isSupportVoiceCall(): Boolean {
    // NRISP: تماس صوتی از اندروید ۶ به بالا فعال است (پیش‌فرض راست‌دسک فقط
    // اندروید ۱۱+ را قبول می‌کرد و در گوشی‌های قدیمی‌تر تنها «چت» می‌ماند).
    return Build.VERSION.SDK_INT >= Build.VERSION_CODES.M
}''',
     'common.kt (پشتیبانی تماس صوتی اندروید ۶+)'),

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
