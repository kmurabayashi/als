#!/bin/sh
# site/ から 2 つの公開用サイトを dist/ に書き出す
#   site/shared : 共通の CSS・画像(両サイトのルートにコピー)
#   site/als    → dist/als : トップ = ALS 2027、/als-2019/ /eaf-2024/
#   site/wia    → dist/wia : トップ = WIA Tokyo 2027、/2026/ /osaka-2025/ /2025/ /2024/
# ページ内のパスはルート基準(/style.css など)。相手サイトへのリンクは下記の既定 URL で書いてあり、
# ALS_URL / WIA_URL を指定するとビルド時に置き換える(独自ドメインを付けたとき用)。
set -eu
cd "$(dirname "$0")"

DEFAULT_ALS_URL="https://als-2027-b95.pages.dev/"
DEFAULT_WIA_URL="https://wia-2027.pages.dev/"
ALS_URL="${ALS_URL:-$DEFAULT_ALS_URL}"
WIA_URL="${WIA_URL:-$DEFAULT_WIA_URL}"

rm -rf dist
for s in als wia; do
  mkdir -p "dist/$s"
  cp -R site/shared/. "dist/$s/"
  cp -R "site/$s/." "dist/$s/"
done

if [ "$ALS_URL" != "$DEFAULT_ALS_URL" ] || [ "$WIA_URL" != "$DEFAULT_WIA_URL" ]; then
  find dist -name '*.html' -exec sed -i.bak \
    -e "s|$DEFAULT_ALS_URL|$ALS_URL|g" \
    -e "s|$DEFAULT_WIA_URL|$WIA_URL|g" {} +
  find dist -name '*.bak' -delete
fi

echo "built: dist/als ($ALS_URL) / dist/wia ($WIA_URL)"
