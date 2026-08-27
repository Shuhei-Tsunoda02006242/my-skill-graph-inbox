# メール配信の仕様（GitHub Actions）

CLAUDE.md から切り出した記録。実装の正は `scripts/build_digest.py` と
`.github/workflows/daily-digest.yml` / `weekly-quantum-digest.yml`。
この文書はいつ何が送られるかを人間が把握するためのもので、
キャプチャの動作には影響しない。

## 配信タイミングと構成

`.github/workflows/daily-digest.yml` は**毎朝7:35 JSTにcron起動**（GitHub Actionsのスケジュール遅延込みで実配信は8:00 JST前後、2026-07-22〜。以前はcron 08:00 JST起動設定だったが毎時00分は混雑で40分超遅延することが実測されたため前倒し）し、さらに**8:20 JSTに保険のcronを1本持つ**（2026-08-26に本命が4時間54分遅延して12:29 JST着になり「朝メールが来ない」事象が発生したため2026-08-27に追加。全ステップが `if: count != '0'` でガードされているため、本命が成功していれば保険は検出0件で無送信に終わる）。前回送信以降（ルートの `.digest-state` マーカー以降）に追加された全ソースのノートを上記の**配信カテゴリ別**にグルーピングし、カテゴリごとのGemini批評コメント付きで **カテゴリごとに1通ずつ** メール送信する（2026-07-18〜、以前はソース別グルーピングだった。2026-07-05〜07-17はソース別1通ずつ、それ以前は1日1通にまとめていた）。

- Frontier（量子）カテゴリは日次送信の対象外。`.github/workflows/weekly-quantum-digest.yml` が**土曜7:35 JSTにcron起動**（cron `35 22 * * 5`、Actionsの遅延込みで実配信は土曜8:00 JST前後）で週次1通として送信する（`WEEKLY_QUANTUM=1 python3 scripts/build_digest.py` 起動。対象は `00-Inbox/*.md` をファイル名の日付でスキャンし過去7日以内のFrontier（量子）ノート。`.digest-state` には依存しない。対象0件なら送信せず正常終了）。週次本文は1行ヘッドライン形式（フルカードではない）＋Gemini週次総括＋末尾に量子ヒートマップ
- push時の都度送信は廃止済み（2026-07-04）
- 手動送信: 両ワークフローとも Actions の workflow_dispatch から実行可能
- 本文組み立て・SMTP送信ともに `scripts/build_digest.py` が実施（`smtplib.SMTP_SSL` で1ログイン後、カテゴリごとにループ送信。Gemini API失敗時はコメント無しで送信を継続）
- カテゴリメールは複数ソースが混在するため、各記事カードにソース名チップ（シグナルバッジの横にグレー文字で表示。例: `TechCrunch`）を表示する。plain版も各記事に `ソース: {ソース名}` の1行を追加
- 📍パンくずには市場規模注記が付く（`assets/market/market-sizes.json` の `breadcrumb-map` 由来。例: `📍 Quantum > PQC（市場$0.4B・急成長）`）。マップ不一致・データ無しなら注記なしでフォールバック
- メール末尾に**そのカテゴリに対応する領域の**市場規模ヒートマップPNGを1枚だけ埋め込む（`🗺 市場規模ヒートマップ` セクション。カテゴリ→domainの対応は「配信カテゴリ」表参照、その他はヒートマップ無し）。SVGをGitHub Actions上で `rsvg-convert` によりPNG化しCID埋め込み。環境変数 `INCLUDE_HEATMAPS=0` で画像埋め込みのみ無効化可能（📍注記は継続）
- `assets/market/` はvault側 `scripts/generate_market_treemaps.py` 実行時に自動同期される（Inboxリポジトリはvaultの非コミット物を直接読めないため）

---
