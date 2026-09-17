#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# فرستادن پروژه به گیت‌هاب و گرفتن فایل نصبی ساخته‌شده
#
# پیش‌نیاز: git و gh (ابزار خط فرمان گیت‌هاب)
#   نصب gh در ویندوز:  winget install GitHub.cli
#   ورود یک‌بار:       gh auth login
#
# اجرا:
#   bash tools/push-to-github.sh                    # نام مخزن پیش‌فرض
#   bash tools/push-to-github.sh my-repo-name       # نام دلخواه
# ---------------------------------------------------------------------------
set -euo pipefail
cd "$(dirname "$0")/.."

REPO_NAME="${1:-nrisp-remote-desktop}"
WORKFLOW="build-windows.yml"
ARTIFACT="NRISP-Remote-installer"
OUT_DIR="output"

say() { printf '\n\033[1;36m==> %s\033[0m\n' "$1"; }

command -v git >/dev/null || { echo "git نصب نیست."; exit 1; }
command -v gh  >/dev/null || { echo "gh نصب نیست: winget install GitHub.cli"; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "اول وارد شوید: gh auth login"; exit 1; }

say "۱) آماده‌سازی مخزن محلی"
if [ ! -d .git ]; then
  git init -q
  git branch -M main
fi
cat > .gitignore <<'GI'
output/
rustdesk-src/
*.exe
*.zip
GI
git add -A
git commit -qm "هویت بصری و ظاهر اختصاصی موسسه" 2>/dev/null || echo "  چیزی برای ثبت نبود"

say "۲) ساخت مخزن روی گیت‌هاب و فرستادن فایل‌ها"
if gh repo view "$REPO_NAME" >/dev/null 2>&1; then
  echo "  مخزن از قبل هست؛ فقط می‌فرستیم."
  git remote get-url origin >/dev/null 2>&1 || \
    git remote add origin "$(gh repo view "$REPO_NAME" --json sshUrl -q .sshUrl)"
  git push -u origin main --quiet
else
  gh repo create "$REPO_NAME" --public --source=. --push \
    --description "نرم‌افزار دسترسی راه دور موسسه تحقیقات سیاست علمی کشور"
fi

say "۳) شروع ساخت روی ماشین ابری"
gh workflow run "$WORKFLOW" --repo "$(gh repo view "$REPO_NAME" --json nameWithOwner -q .nameWithOwner)" 2>/dev/null || true
sleep 10

say "۴) پیگیری ساخت (حدود یک ساعت)"
gh run watch "$(gh run list --workflow "$WORKFLOW" --limit 1 --json databaseId -q '.[0].databaseId')" || true

say "۵) برداشتن فایل نصبی"
mkdir -p "$OUT_DIR"
gh run download --name "$ARTIFACT" --dir "$OUT_DIR" 2>/dev/null || \
  gh run download "$(gh run list --workflow "$WORKFLOW" --limit 1 --json databaseId -q '.[0].databaseId')" \
     --name "$ARTIFACT" --dir "$OUT_DIR"

echo
echo "فایل نصبی اینجاست:"
ls -la "$OUT_DIR"
echo
echo "بعدی: فایل exe را روی سیستم‌ها نصب کنید."
