# ルルカ ホームページ Ver.4

Ver.3をベースに、SF6 BucklerのMRを自動取得する仕組みを追加した版です。

## 仕組み
GitHub Actionsが30分ごとにBucklerプロフィールを取得し、`mr.json` を更新します。
サイトは `mr.json` を読み込み、現在MR / BEST / 目標までの進捗を表示します。

Bucklerは一般公開REST APIではなく、Next.jsのページデータを使う仕組みです。
既存のコミュニティ実装でも、`fighter_banner_info.favorite_character_league_info.master_rating`
からMRを取得することが確認されています。

## 安全性
- `BUCKLER_ID` はGitHub Secretsに保存します。
- HTMLやJavaScriptにはCookieを記載しません。
- Cookieはサイト訪問者には公開されません。
- Cookieが期限切れになると自動更新は止まります。その場合はSecretを更新します。

## ユーザーが次にすること
1. GitHubアカウントを用意
2. 新しいリポジトリを1つ作成
3. このフォルダの中身をアップロード
4. GitHubのSettings → Secrets and variables → Actions → New repository secret
5. Name: `BUCKLER_ID`
6. Value: Bucklerの自分の `buckler_id` Cookie
7. Actionsから `Update SF6 MR` を手動実行してテスト
8. 問題なければGitHub Pagesを有効化

Cookieをチャットへ送らないでください。
