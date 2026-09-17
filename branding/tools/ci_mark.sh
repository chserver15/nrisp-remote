#!/usr/bin/env bash
# ثبت وضعیت پیشرفت ساخت روی شاخهٔ ci-status
# این کار باعث می‌شود پیشرفت ساخت از بیرون گیت‌هاب هم قابل پیگیری باشد.
# نکته: برای پرهیز از دست‌خوردن پوشهٔ کاری اصلی، اینجا یک نسخهٔ جداگانه از
# مخزن در پوشهٔ موقت ساخته می‌شود.
set -e
MSG="${1:-به‌روزرسانی وضعیت}"
REPO_URL="https://x-access-token:${GITHUB_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"
WORK="${RUNNER_TEMP:-/tmp}/nrisp-ci-status"
rm -rf "$WORK"
mkdir -p "$WORK"
cd "$WORK"
if ! git clone --quiet --depth 1 --branch ci-status "$REPO_URL" . >/dev/null 2>&1; then
  git init -q .
  git remote add origin "$REPO_URL"
  git checkout -q -b ci-status
fi
git config user.email "nrisp@nrisp.ac.ir"
git config user.name "NRISP Build"
mkdir -p ci-status
echo "زمان: $(date -u '+%Y-%m-%d %H:%M:%S') | اجرا: ${GITHUB_RUN_NUMBER:-?} | کار: ${GITHUB_JOB:-?} | وضعیت: $MSG" >> ci-status/log.txt
if [ "$(wc -l < ci-status/log.txt)" -gt 80 ]; then
  tail -n 80 ci-status/log.txt > ci-status/log.new && mv ci-status/log.new ci-status/log.txt
fi
git add -f ci-status/log.txt
git commit -q -m "وضعیت: $MSG" >/dev/null 2>&1 || true
git push -f --quiet origin ci-status
echo "ثبت شد: $MSG"
