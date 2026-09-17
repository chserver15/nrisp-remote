#!/usr/bin/env bash
# ثبت متن گزارش (معمولاً پیام خطا) روی شاخهٔ ci-status
# این روش مستقل از بخش Releases کار می‌کند و همیشه در دسترس است.
set -e
NOTE_FILE="${1:?مسیر فایل گزارش}"
TITLE="${2:-گزارش}"
REPO_URL="https://x-access-token:${GITHUB_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"
WORK="$(mktemp -d)"
cd "$WORK"
if ! git clone --quiet --depth 1 --branch ci-status "$REPO_URL" . >/dev/null 2>&1; then
  git init -q .; git remote add origin "$REPO_URL"; git checkout -q -b ci-status
fi
git config user.email "nrisp@nrisp.ac.ir"
git config user.name "NRISP Build"
mkdir -p ci-status
{
  echo "===== $TITLE | اجرا: ${GITHUB_RUN_NUMBER:-?} | کار: ${GITHUB_JOB:-?} | زمان: $(date -u '+%Y-%m-%d %H:%M:%S') ====="
  tail -n 200 "$NOTE_FILE" 2>/dev/null || echo "(فایل گزارش نبود)"
  echo
} >> ci-status/failure.txt
if [ "$(wc -l < ci-status/failure.txt)" -gt 800 ]; then tail -n 800 ci-status/failure.txt > ci-status/f.new && mv ci-status/f.new ci-status/failure.txt; fi
git add -f ci-status/failure.txt
git commit -q -m "$TITLE" >/dev/null 2>&1 || true
git push -f --quiet origin ci-status
echo "گزارش روی شاخهٔ وضعیت ثبت شد"
