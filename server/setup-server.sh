#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# راه‌اندازی سرور اختصاصی (رایگان) روی یک سرور لینوکسی
# روی Ubuntu 22.04 / 24.04 یا Debian 12 تست می‌شود.
#
#   sudo bash setup-server.sh
#
# کاری که می‌کند: نصب داکر، بالا آوردن دو سرویس، باز کردن پورت‌ها،
# و در پایان کلید عمومی سرور را چاپ می‌کند.
# ---------------------------------------------------------------------------
set -euo pipefail

DOMAIN="${DOMAIN:-rd.yourcompany.ir}"
DIR="${DIR:-/opt/rd-server}"

say() { printf '\n\033[1;36m==> %s\033[0m\n' "$1"; }

if [ "$(id -u)" -ne 0 ]; then
  echo "این اسکریپت باید با sudo اجرا شود."
  exit 1
fi

say "۱) نصب پیش‌نیازها"
apt-get update -qq
apt-get install -y -qq curl ca-certificates ufw >/dev/null

say "۲) نصب داکر (اگر نصب نباشد)"
if ! command -v docker >/dev/null 2>&1; then
  curl -fsSL https://get.docker.com | sh
  systemctl enable --now docker
else
  echo "داکر از قبل نصب است."
fi

say "۳) ساخت پوشه‌ی سرور در $DIR"
mkdir -p "$DIR/data"
cd "$DIR"

cat > docker-compose.yml <<EOF
services:
  hbbs:
    container_name: rd-hbbs
    image: rustdesk/rustdesk-server:latest
    command: hbbs -r ${DOMAIN}:21117
    network_mode: host
    volumes:
      - ./data:/root
    restart: always

  hbbr:
    container_name: rd-hbbr
    image: rustdesk/rustdesk-server:latest
    command: hbbr
    network_mode: host
    volumes:
      - ./data:/root
    restart: always
EOF

say "۴) بالا آوردن سرویس‌ها"
docker compose up -d

say "۵) باز کردن پورت‌ها در فایروال"
for p in 21114 21115 21116 21117 21118 21119; do
  ufw allow "$p"/tcp >/dev/null 2>&1 || true
  ufw allow "$p"/udp >/dev/null 2>&1 || true
done
# اگر پورت ۸۰ و ۴۴۳ برای پنل وب و گواهی امنیتی لازم دارید:
ufw allow 80/tcp >/dev/null 2>&1 || true
ufw allow 443/tcp >/dev/null 2>&1 || true

say "۶) صبر برای تولید کلید سرور"
for i in $(seq 1 30); do
  if [ -s "$DIR/data/id_ed25519.pub" ]; then break; fi
  sleep 1
done

say "تمام شد"
echo
if [ -s "$DIR/data/id_ed25519.pub" ]; then
  echo "کلید عمومی سرور شما (این را در فایل branding.json بگذارید):"
  echo
  echo "    $(cat "$DIR/data/id_ed25519.pub")"
  echo
else
  echo "کلید ساخته نشد. لاگ را ببینید:  docker compose -f $DIR/docker-compose.yml logs"
fi

cat <<EOF

مرحله‌های بعدی:
  ۱. دامنه‌ی ${DOMAIN} را به آی‌پی همین سرور وصل کنید (رکورد A).
  ۲. مقدار server  را در branding.json روی همین دامنه بگذارید.
  ۳. مقدار public_key را روی کلیدی که بالا چاپ شد بگذارید.
  ۴. روی کامپیوتر خودتان اسکریپت ساخت را اجرا کنید.

بررسی سلامت:
  docker compose -f $DIR/docker-compose.yml ps
  ss -tulnp | grep 2111
EOF
