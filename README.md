# Agile Leadership Summit 2027 / Women in Agile Tokyo 2027 LP

`site/` が元ファイル(HTML/CSS のみ)。`./build.sh` で 2 サイトに分けて `dist/` に書き出し、それぞれ別の Cloudflare Pages プロジェクトで公開する。

- `site/shared/`:共通の CSS・画像(両サイトのルートにコピーされる)
- `site/als/` → `dist/als`:トップ = ALS 2027、過去イベント `/als-2019/` `/eaf-2024/`
- `site/wia/` → `dist/wia`:トップ = WIA Tokyo 2027、過去イベント `/2026/` `/osaka-2025/` `/2025/` `/2024/`

WIA の過去イベントページは `python3 tools/gen_wia_past.py` で生成する(元データは `reference/wia-past/`)。
ページ内のパスはルート基準(`/style.css` など)。過去イベントはヘッダーの「過去イベント」プルダウンから辿れる(追加したら各ページのプルダウンにも足す)。
相手サイトへのリンクは `build.sh` の既定 URL で書いてあり、`ALS_URL` / `WIA_URL` を指定するとビルド時に置き換わる。
`reference/` は Wix から保存した参照用ファイルで、公開も Git 管理もしない(`.gitignore` 済み)。

## ローカル確認

```sh
./build.sh
npx serve dist/als   # WIA は dist/wia
```

## デプロイ(Cloudflare Pages / Direct Upload)

```sh
npx wrangler login                                                     # 初回のみ
npx wrangler pages project create als-2027 --production-branch main --force  # 初回のみ(作成済み)
npx wrangler pages project create wia-2027 --production-branch main --force  # 初回のみ(作成済み)
./build.sh
npx wrangler pages deploy dist/als --project-name als-2027 --branch main
npx wrangler pages deploy dist/wia --project-name wia-2027 --branch main
```

公開先: `https://als-2027-b95.pages.dev` / `https://wia-2027.pages.dev`

## 独自ドメイン

ドメインは未定。決まったら各 Pages プロジェクトの Custom domains に追加し、`ALS_URL` / `WIA_URL` を指定して `./build.sh` からデプロイし直す。
Wix 上のスクラム祭り2025 のページは移行しない。

## TODO

`site/index.html` 内の `<!-- TODO -->` を埋める(日時・会場・チケットURL・参加費・基調講演・協力コミュニティ・問い合わせフォーム)。
