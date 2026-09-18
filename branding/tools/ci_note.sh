#!/usr/bin/env bash
# ثبت گزارش خطا روی شاخهٔ ci-status (مستقل از بخش Releases)
set +e
NOTE_FILE="${1:-}"
TITLE="${2:-گزارش خطا}"
REPO_URL="https://x-access-token:${GITHUB_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"
WORK="$(mktemp -d)"
TMP_BODY="$WORK/body.txt"
{
  echo "===== $TITLE | اجرا: ${GITHUB_RUN_NUMBER:-?} | کار: ${GITHUB_JOB:-?} | زمان: $(date -u '+%Y-%m-%d %H:%M:%S') ====="
  if [ -n "$NOTE_FILE" ] && [ -f "$NOTE_FILE" ]; then
    tail -n 250 "$NOTE_FILE"
  else
    echo "(فایل گزارش نبود؛ گردآوری مستقیم از لاگ‌ها)"
    for f in branding-log.txt build-log.txt packaging-log.txt android-source-log.txt android-deps-log.txt android-branding-log.txt android-build-log.txt; do
      echo "----- $f -----"
      tail -n 120 "$GITHUB_WORKSPACE/$f" 2>/dev/null || echo "(نیست)"
    done
    echo "----- فهرست فضای کار -----"
    ls -la "$GITHUB_WORKSPACE" 2>/dev/null | head -40
    echo "----- پوشهٔ سورس -----"
    ls -la "$GITHUB_WORKSPACE/${SRC_DIR:-rustdesk-src}" 2>/dev/null | head -40
  fi
  echo
} > "$TMP_BODY" 2>/dev/null

cd "$WORK" || exit 0
if ! git clone --quiet --depth 1 --branch ci-status "$REPO_URL" . >/dev/null 2>&1; then
  git init -q . ; git remote add origin "$REPO_URL" ; git checkout -q -b ci-status
  # شاخه از پیش هست؟ پیش از افزودن، محتوای موجود را بگیر
  git fetch --quiet --depth 1 origin ci-status >/dev/null 2>&1 && git reset --soft FETCH_HEAD >/dev/null 2>&1
fi
git config user.email "nrisp@nrisp.ac.ir"
git config user.name "NRISP Build"
mkdir -p ci-status
cat "$TMP_BODY" >> ci-status/failure.txt 2>/dev/null
if [ "$(wc -l < ci-status/failure.txt 2>/dev/null || echo 0)" -gt 900 ]; then
  tail -n 900 ci-status/failure.txt > ci-status/f.new && mv ci-status/f.new ci-status/failure.txt
fi
git add -f ci-status/failure.txt
git commit -q -m "$TITLE" >/dev/null 2>&1 || true
git push -f --quiet origin ci-status
echo "گزارش ثبت شد"
