#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# اجرای کل فرایند برندسازی، از ساخت آیکون تا اعمال روی سورس.
#
#   bash run.sh ../rustdesk                 # برندسازی پایه
#   bash run.sh ../rustdesk --check-only    # فقط بررسی سورس
#   bash run.sh ../rustdesk --ui            # نصب لایهٔ ظاهری اختصاصی موسسه
#   bash run.sh ../rustdesk --full          # همه‌چیز: ظاهر + نام فایل اجرایی + بسته‌ها
# ---------------------------------------------------------------------------
set -euo pipefail
cd "$(dirname "$0")"

REPO="${1:-../rustdesk}"
shift || true

EXTRA=()
for a in "$@"; do
  case "$a" in
    --full) EXTRA+=(--rename-exe --android-package --ui) ;;
    *) EXTRA+=("$a") ;;
  esac
done

if [ ! -d "$REPO" ]; then
  echo "پوشهٔ سورس پیدا نشد: $REPO"
  echo "نمونه:  bash run.sh ../rustdesk"
  exit 1
fi

echo "== مرحله ۱: ساخت آیکون‌ها و لوگوها =="
python3 branding/tools/generate_icons.py

echo
echo "== مرحله ۲: اعمال برند روی سورس =="
python3 branding/tools/apply_branding.py --repo "$REPO" "${EXTRA[@]}"

echo
echo "== تمام شد =="
echo "برای ساخت فایل نصبی، راهنمای docs/2-build-windows.md را ببینید."
