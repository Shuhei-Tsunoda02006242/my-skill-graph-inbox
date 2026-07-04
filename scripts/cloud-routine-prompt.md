# claude.ai クラウドルーチン用プロンプト（貼り付け用）

claude.ai側のデイリーキャプチャルーチン(現在TechCrunch/Techmemeのみ)を全ソース+批評コメント対応にするための差し替えプロンプト。

運用手順（既存はTechmeme用/TechCrunch用の2本立て）:
1. どちらか片方のルーチンのプロンプト本文を以下に置き換える（実行時刻は毎朝7:00 JSTのまま）。編集できないUIなら以下で新規作成する
2. 新ルーチンが動くのを確認したら、**残ったもう片方（と旧ルーチン）を削除**する
3. 最終状態＝全ソース版ルーチン1本。先に2本とも削除しないこと（その日の朝キャプチャが飛ぶ）

---

デイリーキャプチャループを実行してください。

対象リポジトリ: https://github.com/Shuhei-Tsunoda02006242/my-skill-graph-inbox （mainブランチ）

手順:
1. リポジトリを取得し、CLAUDE.md を読んで最新のキャプチャ対象ソースとルールを確認する
2. CLAUDE.md のソーステーブルに記載された**全ソース**から、本日の注目記事を最大3件ずつ取得する（現在: TechCrunch `tc-` / Techmeme `tm-` / STAT News `sn-` / IEEE Spectrum Neuro `is-` / Quantum Computing Report `qcr-` / FierceBiotech `fb-` / Electrek `ek-`）
3. CLAUDE.md のフォーマット（frontmatter + 本文）に従い、日本語で `00-Inbox/YYYY-MM-DD-{prefix}-{slug}.md` を作成する
4. 批評コメント作成: 本日キャプチャした全記事をソース別にまとめ、`digests/YYYY-MM-DD-commentary.md` を作成する
   - ソースごとに「## {ソース正式名}」見出し（例: ## TechCrunch）+ 批評本文3〜5文
   - 観点: (1) 誇張・ハイプの可能性 (2) 記事に欠けている文脈 (3) 投資家として注意すべき点 (4) 記事間に共通するトレンド
   - このファイルは毎朝10:00 JSTのダイジェストメールにそのまま掲載される
5. git commit & push
   - ソースごとに1コミット: `daily: {Source} capture {YYYY-MM-DD} ({N} articles)`
   - 批評コメントは別コミット: `daily: digest commentary {YYYY-MM-DD}`
   - Author: `Claude <noreply@anthropic.com>`

ルール:
- signal-strength が moderate 以上になりそうな記事を優先する
- 過去7日以内に類似トピックをキャプチャ済みならスキップ（00-Inbox内の既存ファイルを確認）
- 該当記事が無いソースはスキップしてよい（no-updatesファイルは作らない）
- 必ず git push まで完了させること（途中で止めない）
- 新規ソース追加候補を見つけた場合は CLAUDE.md のソーステーブルを更新する
