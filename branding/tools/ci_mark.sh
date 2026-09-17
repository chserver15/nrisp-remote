#!/usr/bin/env bash
# ثبت وضعیت پیشرفت ساخت روی شاخهٔ ci-status
# این کار باعث می‌شود پیشرفت ساخت از بیرون گیت‌هاب هم قابل پیگیری باشد.
set -e
MSG="${1:-به‌روزرسانی وضعیت}"
cd "${GITHUB_WORKSPACE:-.}"
git config user.email "nrisp@nrisp.ac.ir" >/dev/null 2>&1 || true
git config user.name "NRISP Build" >/dev/null 2>&1 || true
git fetch --depth 1 origin ci-status >/dev/null 2>&1 || true
git checkout -B ci-status origin/ci-status >/dev/null 2>&1 || git checkout -B ci-status >/dev/null 2>&1
mkdir -p ci-status
{
  echo "زمان: $(date -u '+%Y-%m-%d %H:%M:%S') | اجرا: ${GITHUB_RUN_NUMBER:-?} | کار: ${GITHUB_JOB:-?} | وضعیت: $MSG"
} >> ci-status/log.txt
if [ "$(wc -l < ci-status/log.txt)" -gt 80 ]; then tail -n 80 ci-status/log.txt > ci-status/log.new && mv ci-status/log.new ci-status/log.txt; fi
git add -f ci-status/log.txt
git commit -q -m "وضعیت: $MSG" >/dev/null 2>&1 || true
git push -f -q origin ci-status
echo "ثبت شد: $MSG"
