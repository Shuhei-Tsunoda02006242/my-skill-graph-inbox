# メール配信の仕様（GitHub Actions）

CLAUDE.md から切り出した記録。実装の正は `scripts/build_digest.py` と
`.github/workflows/daily-digest.yml` / `weekly-quantum-digest.yml` / `weekly-healthcare-digest.yml` / `weekly-fusion-digest.yml`。
この文書はいつ何が送られるかを人間が把握するためのもので、
キャプチャの動作には影響しない。

## 配信タイミングと構成

`.github/workflows/daily-digest.yml` は**毎朝7:35 JSTにcron起動**（GitHub Actionsのスケジュール遅延込みで実配信は8:00 JST前後、2026-07-22〜。以前はcron 08:00 JST起動設定だったが毎時00分は混雑で40分超遅延することが実測されたため前倒し）し、さらに**8:20 JSTに保険のcronを1本持つ**（2026-08-26に本命が4時間54分遅延して12:29 JST着になり「朝メールが来ない」事象が発生したため2026-08-27に追加。全ステップが `if: count != '0'` でガードされているため、本命が成功していれば保険は検出0件で無送信に終わる）。前回送信以降（ルートの `.digest-state` マーカー以降）に追加された全ソースのノートを上記の**配信カテゴリ別**にグルーピングし、カテゴリごとのGemini批評コメント付きで **カテゴリごとに1通ずつ** メール送信する（2026-07-18〜、以前はソース別グルーピングだった。2026-07-05〜07-17はソース別1通ずつ、それ以前は1日1通にまとめていた）。

- Frontier（量子）カテゴリは日次送信の対象外。`.github/workflows/weekly-quantum-digest.yml` が**土曜7:35 JSTにcron起動**（cron `35 22 * * 5`、Actionsの遅延込みで実配信は土曜8:00 JST前後）で週次1通として送信する（`WEEKLY_QUANTUM=1 python3 scripts/build_digest.py` 起動。対象は `00-Inbox/*.md` をファイル名の日付でスキャンし過去7日以内のFrontier（量子）ノート。`.digest-state` には依存しない。対象0件なら送信せず正常終了）。週次本文は1行ヘッドライン形式（フルカードではない）＋Gemini週次総括＋末尾に量子ヒートマップ
- Healthcare（2026-10-19〜）は日次と週次で中身が違う:
  - **日次**: 「💰 お金が動いた」「🧪 臨床の結果」の2つの表だけ（1記事=1行。カード・批評コメント・ヒートマップは付けない）。行はノートの frontmatter の追加欄（`indication` / `approach` / `players` / `deal-*` / `trial-*`。仕様は CLAUDE.md「Healthcare（Biotech）ノートの追加欄」）から機械的に作る。振り分けは `classify_healthcare()`: `deal-type` が funding/ipo/license/ma → money（臨床と両方に当たる記事も money）、`trial-result` が非空 → clinical、追加欄のキーが1つも無い → missing、それ以外（`fund` を含む）→ other。件名は `📥 [Healthcare] デイリーダイジェスト {日付}（{money+clinical}件）`。末尾に「その他のヘルスケア記事N件は土曜の週次まとめに回しました」を出し、missing があれば「分類欄が未記入の記事N件も週次に回しました（キャプチャ側が新しい欄を書いていない可能性）」も出す。money と clinical が0件でも missing が1件以上あれば、0件のまま注記つきで送る（キャプチャ側の不具合に気づくため）。missing も0件ならそのカテゴリのメールは送らない
  - 金額セルの1行目は前払い・調達額（`$103M（約155億円）`、$1=150円の概算）。総額が前払いと違えば「・総額最大$1.16B」を足す。前払いが無く総額だけなら「最大$500M」。並びは前払い（無ければ総額）の大きい順。臨床の結果は「✗ 第3相 未達」の形で、相の高い順
  - **週次**: `.github/workflows/weekly-healthcare-digest.yml` が**土曜7:50 JSTにcron起動**（cron `50 22 * * 5`。量子の7:35とずらしている）し、`WEEKLY_HEALTHCARE=1 python3 scripts/build_digest.py` でHealthcareの週次まとめ1通を送る。対象期間は実行時刻ではなく「JSTで今日より前（当日は含めない）の直近の金曜日」を end とした end-6日（土）〜end（金）のファイル名日付（Actionsの遅延で日曜にずれ込んでも同じ週を指し、金曜に手動実行すると前週の金曜になる。`.digest-state` には依存しない）。金曜までなのは、ファイル名の日付Dのノートが D日17:00 UTC＝JSTでD+1日2:00にキャプチャされるため。土曜日付のノートは日曜2:00まで存在せず、「土曜まで」の窓だと土曜朝の週次に載らず、翌週の窓からも外れて永久に漏れる。対象0件なら送信せず正常終了。本文は(1)「💰 今週お金が集まった領域」= 病気別・アプローチ別の集計表（件数・前払い・調達計・総額計。前払い・調達計の大きい順。グループキーは値の「（」より前の部分、空は「（記載なし）」）、(2)「🧪 臨床結果」の「○2 ✗3 △1」集計、(3)「📰 その他の動き」= other と missing の記事を1行ずつ、(4)末尾にbiotechのヒートマップ。件名は `📅 [Healthcare] 週次まとめ {start}〜{end}（{N}件）`。Geminiは使わない
  - 集計は前払い・調達額を主にする。提携の「最大$1.16B」のほとんどは後払いのマイルストンで、総額で集計すると実態とずれるため
- Fusion（核融合、2026-10-25〜）は量子と同じく日次送信の対象外で、`.github/workflows/weekly-fusion-digest.yml` が**土曜8:05 JSTにcron起動**（cron `5 23 * * 5`。量子7:35・Healthcare7:50とずらしている）し、`WEEKLY_FUSION=1 python3 scripts/build_digest.py` で週次1通を送る
  - **振り分け**: `landscape-position` に `核融合` か `Fusion` を含むノートは、第1セグメント（Energy）より優先して Fusion に入る（`tc-`/`tm-`/`ek-` 経由の核融合記事も日次の Climate & Energy から外れる）。positionが空なら prefix `fia-`・`tcf-` でフォールバック。判定は `categorize()` / `FUSION_POSITION_RE`
  - **対象期間**: Healthcare週次と同じ窓（実行時刻ではなく「JSTで今日より前の直近の金曜日」を end とした end-6日（土）〜end（金）のファイル名日付。`healthcare_week_window()` を共有。理由はHealthcare週次の項を参照）。対象0件なら送信せず、`No fusion articles this week (...): count=0, no mail sent` をログに出して正常終了する
  - **本文**: (1)「💰 資金調達」= `deal-type` が funding/ipo/ma/grant のノートを1行ずつ（誰が・種別（`deal-note`、無ければ種別ラベル）・調達額（`deal-upfront-usd-m` を円併記、非公表は「—」）。調達額の大きい順）、(2)「方式別」= `fusion-approach` ごとの件数と調達額の合計（空は「不明」で最後）、(3)「🏛 政策・規制」（`fusion-topic: policy`）と「🔬 技術・その他」（tech / supply-chain / other / 空）を1行ずつ並べた一覧、(4)末尾に追加欄が未記入のノートの件数注記。資金調達の行は(3)の一覧には重ねて出さない。Geminiもヒートマップも使わない（非上場の会社が多く市場タイルが無いため）。件名は `📅 [Fusion] 週次まとめ {start}〜{end}（{N}件）`
  - 追加欄の仕様は CLAUDE.md「Fusion（核融合）ノートの追加欄」。`players` / `deal-type` / `deal-upfront-usd-m` / `deal-note` は Healthcare と同じキー名なので `parse_note()` の同じフィールドを共有する
  - 金額の整形は Healthcare の `fmt_usd_with_yen()` などを再利用（$1=150円の概算）
- push時の都度送信は廃止済み（2026-07-04）
- 手動送信: 各ワークフローとも Actions の workflow_dispatch から実行可能
- 本文組み立て・SMTP送信ともに `scripts/build_digest.py` が実施（`smtplib.SMTP_SSL` で1ログイン後、カテゴリごとにループ送信。Gemini API失敗時はコメント無しで送信を継続）
- カテゴリメールは複数ソースが混在するため、各記事カードにソース名チップ（シグナルバッジの横にグレー文字で表示。例: `TechCrunch`）を表示する。plain版も各記事に `ソース: {ソース名}` の1行を追加
- 📍パンくずには市場規模注記が付く（`assets/market/market-sizes.json` の `breadcrumb-map` 由来。例: `📍 Quantum > PQC（市場$0.4B・急成長）`）。マップ不一致・データ無しなら注記なしでフォールバック
- メール末尾に**そのカテゴリに対応する領域の**市場規模ヒートマップPNGを1枚だけ埋め込む（`🗺 市場規模ヒートマップ` セクション。カテゴリ→domainの対応は「配信カテゴリ」表参照、その他はヒートマップ無し）。SVGをGitHub Actions上で `rsvg-convert` によりPNG化しCID埋め込み。環境変数 `INCLUDE_HEATMAPS=0` で画像埋め込みのみ無効化可能（📍注記は継続）
- `assets/market/` はvault側 `scripts/generate_market_treemaps.py` 実行時に自動同期される（Inboxリポジトリはvaultの非コミット物を直接読めないため）

---
