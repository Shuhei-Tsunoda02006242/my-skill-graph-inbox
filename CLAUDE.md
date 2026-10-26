# My-Skill-Graph-Inbox: Capture Rules

自律キャプチャループの動作仕様。新しいソースを追加するときはここを先に更新する。

---

## ループの起動条件

このファイル（`CLAUDE.md`）が存在しないとループは再起動できない。
ループ再起動時は **必ずこのファイルの存在を確認してから** CronCreate を呼ぶ。

---

## キャプチャ対象ソース

| prefix | ソース | URL | フィード | ドメイン |
|--------|--------|-----|----------|---------|
| `tc-` | TechCrunch | `https://techcrunch.com/category/startups/` | `https://techcrunch.com/feed/` | AI・半導体・スタートアップ資金調達 |
| `tm-` | Techmeme | `https://www.techmeme.com/` | `https://www.techmeme.com/feed.xml` | テック業界全般のヘッドライン集約 |
| `sn-` | STAT News | `https://www.statnews.com/category/biotech/` | `https://www.statnews.com/feed/` | バイオテック・CRISPR・遺伝子治療・創薬 |
| `is-` | IEEE Spectrum Neuro | `https://spectrum.ieee.org/tag/brain-computer-interface` | `https://spectrum.ieee.org/feeds/topic/biomedical.rss` | BMI・ニューロテック・脳科学×エンジニアリング |
| `qcr-` | Quantum Computing Report | `https://quantumcomputingreport.com/` | `https://quantumcomputingreport.com/feed/` | 量子コンピューター全般・商用化動向・資金調達 |
| `fb-` | FierceBiotech | `https://www.fiercebiotech.com/` | `https://www.fiercebiotech.com/rss/xml` | バイオテックM&A・FDA承認・臨床試験結果 |
| `ek-` | Electrek | `https://electrek.co/` | `https://electrek.co/feed/` | エネルギー技術・EV・再生可能エネルギー・電力インフラ |
| `tqi-` | The Quantum Insider | `https://thequantuminsider.com/` | `https://thequantuminsider.com/feed/` | 量子コンピューター・研究・PQC・上場/資金調達（qcr-の補完） |
| `fia-` | Fusion Industry Association | `https://www.fusionindustryassociation.org/` | `https://www.fusionindustryassociation.org/feed/` | 核融合（政策・資金・業界団体発表） |
| `tcf-` | TechCrunch Fusion | `https://techcrunch.com/tag/fusion-power/` | `https://techcrunch.com/tag/fusion-power/feed/` | 核融合スタートアップの資金調達・技術 |

---

## ソース記事の取得方法（2026-09-10〜）

**WebFetch でソースサイトを直接取得してはならない。** 実行環境のegressは2026-09-07以降、
全ドメインへの接続が403で拒否されており、直接取得は必ず失敗する。
設定画面を3箇所（デスクトップアプリの「許可されたサイト」／ルーチン編集の「動作」タブ／
設定→機能→コード実行とファイル作成のドメイン許可リスト）確認したが、**この実行環境の
egressを利用者が変更できる設定は存在しなかった**（vaultのKNOWLEDGE.md 2026-09-10の項）。

代わりに GitHub Actions（`fetch-sources.yml`、毎日1:50 JST＝ルーチンの10分前）が
全ソースのフィードと記事本文を取得し、`sources-raw` ブランチへ置いている。
**github.com はegress遮断日でも到達できる**ため（遮断日でもルーチンはcommit/pushに
成功していた）、この経路なら環境の状態に依存しない。

### 手順

1. `git fetch origin sources-raw`（**mainへマージしないこと**。履歴を持たない別系統のブランチ）
2. `git show origin/sources-raw:sources-raw/fetch-log.md` — ソース別の取得結果
3. `git show origin/sources-raw:sources-raw/{当日}/index.md` — 記事一覧（prefix・公開日・タイトル・ファイルパス・URL）
4. 本文は `git show origin/sources-raw:sources-raw/{当日}/{prefix}/{slug}.md`
   frontmatter に `source` `title` `url` `published` が入っている。
   **`url` をそのままノートの `source:` に使う**（重複チェックもこのURLで行う）

### 注意

- **`extraction: summary` の記事は本文ではなくフィードの要約**（300字前後）。ページ本文が取れない
  ソース（Techmemeのような集約サイト、ペイウォール記事）で使われる。Evidence / Context に
  書けることが限られるので、**要約に書いていないことを推測で補わないこと**。`extraction: full` なら通常どおり
- **`truncated: true` の記事は末尾が切れている。** 重要な数字が末尾にある可能性があるため、
  Key Claim に断定を書くときは本文中に根拠があることを確認する
- `index.md` には3日前までの記事が載っている。障害日のさかのぼり取得はここから拾える
- Actions側が取得に失敗したソースは `fetch-log.md` の「取得」列が `失敗` になる。
  巡回ログの「取得」列はこの表をそのまま転記してよい（従来の自己申告より事実に近い）
- **当日の `index.md` が無ければ、`sources-raw` にある最新の日付フォルダを使う。**
  `git ls-tree -d --name-only origin/sources-raw:sources-raw/` で日付フォルダを一覧し、最新のものを選ぶ。
  取得は3日前まで遡って行われているので、1日古いフォルダでも当日分の記事は入っている。
  日付が一致することを前提にしてはいけない——Actionsのスケジュール実行は実測で50〜148分遅れ、
  UTC日付を跨ぐことがある（2026-09-10の初回実行は16:50 UTC指定に対し19:18 UTC起動だった）
- **最新フォルダの日付が2日以上前なら、Actionsが止まっている。** その場合は記事を作らず、
  巡回ログに「sources-raw が N 日前で停止」と書いて終える

### egress疎通の記録（毎回1行）

元の直接取得経路が復活したかを記録に残すため、巡回ログの末尾に次を1行書く。

```
egress疎通: OK (200)      または      egress疎通: 失敗 (403)
```

判定は次のコマンドを**1回だけ**実行して得る。記事の取得には使わない（取得は `sources-raw` 経由が正）。

```
curl -sS -o /dev/null -w '%{http_code}' --max-time 10 https://techcrunch.com/
```

これは環境が復旧した日を記録するためだけの1リクエストである。
復旧が確認できても取得経路は自動では戻さない。戻すかどうかはユーザーが判断する。

---

## ファイル命名規則

```
YYYY-MM-DD-{prefix}-{slug}.md
```

- `{slug}`: 記事タイトルを英語で3〜5単語にケバブケース化
- 例: `2026-06-20-sn-crispr-liver-disease-phase3.md`
- 例: `2026-06-20-is-neuralink-100ch-implant-trial.md`

---

## frontmatter フォーマット

```yaml
---
title: "記事タイトル（日本語）"
date: YYYY-MM-DD
source: "https://..."
source-type: article  # article | newsletter | report
domain: deeptech      # deeptech | investment | both
tech-tags: []         # AI | semiconductor | quantum | biotech | neurotech | energy
companies-mentioned: []
investment-implication: ""
signal-strength: none # none | weak | moderate | strong
status: fleeting
landscape-position: ""  # 領域タクソノミーのパンくず（下記「領域マップ」参照）
---
```

---

## 本文フォーマット

```markdown
## Key Claim
<!-- この記事・情報の最重要ポイントを1文で（日本語） -->

## Evidence / Context
<!-- 数字・引用・根拠（日本語） -->

## My Take
<!-- 1行の自分の見解（空欄でよい） -->

## Links
<!-- [[関連ノート]] -->
```

### 本文の書き方ルール

- **自然な日本語で書く**: 直訳調（不自然な語順・逐語訳のカタカナ表現）を避け、日本のビジネスメディアの文体で要約する
- **金額には日本円換算を併記する**: 米ドル等の金額の直後に `（約◯億円）` を付ける。レートは概算でよい（$1≒150円目安）。例: `$600M（約900億円）`、`$135M（約200億円）`。桁の直感を掴むことが目的なので厳密なレートより桁感を優先。frontmatterの `investment-implication` 内の金額も同様
- **landscape-position を必ず埋める**: 記事内容に最も近い葉ノードを下記「領域マップ（パンくず用タクソノミー）」から選び、`大分類 > 中分類 > 葉` 形式で書く（例: `Semiconductor > 製造(Manufacturing) > 先端ファウンドリ`）。ぴったりの葉が無ければ最も近い中分類まででよい。複数領域にまたがる場合は主たる方を1つだけ
- **frontmatterの値を書き直すときは sed を使わない**: Edit ツールか Python で該当行を丸ごと書き換える。sed の置換文字列では `&` が「マッチした部分そのもの」に展開されるため、`資本/M&A`・`政府R&D資金` のように `&` を含む値へ置換すると、旧い行が新しい値の `&` の位置に埋め込まれて壊れる（2026-10-06に4件発生: `"Biotech > 資本/Mlandscape-position: \"Biotech > 創薬...\"A > バイオIPO/ライセンス"`）。書き直した後は `grep -c "landscape-position" <file>` が1であることを確認する
- **`investment-implication` に書いた金額・数値は、`Evidence / Context` にも必ず1行入れる。** 含意は記事全文（最大12,000字）を読んで書けるが、`Evidence / Context` は数行の要約なので、**含意にだけ数字があるとノート上で出所を追えなくなる**。`sources-raw` は3日で入れ替わるため、それ以降は検証する手段が消える
  - 2026-10-04に実際に起きた: Zealandのノートの含意に「最大€315Mのマイルストン」とあったが Evidence に無く、一次記事を取りに行って初めて裏付け（`up to 315 million euros ($355 million) in milestones`）が確認できた。記事が消えていれば確認できなかった
  - 対象は**金額・比率・件数・期日**など、後から検証しうる具体的な数字。「競争優位が動く」のような解釈は対象外
  - 同じ数字を二重に書くことになるが、**含意はメールの【投資含意】に、Evidenceはノートの根拠欄に出る**ので読み手が違う
- **signal-strength が `moderate` 以上なら `investment-implication` を必ず書く**: この2つは連動している。金額・評価額・契約規模が記事にあればそれを、無ければ**何がどう変わるのか**（誰の競争優位が動くか、どの市場の前提が崩れるか）を1〜2文で書く。「重要だが投資的な含意が思いつかない」場合は、含意を空にするのではなく **signal-strength を下げる**のが正しい。**空のまま moderate 以上を付けない。** 理由: Vault側の `/inbox` 処理は「`investment-implication` が非空 **かつ** `signal-strength` が moderate 以上」でクロスドメインのブリッジノートを生成するため、片方が欠けると**ルーチン自身が最重要と判定した記事が機械的にブリッジ生成から漏れる**（2026-09-06までに実際に4件発生: テキサス州の送電網接続凍結、Merck/Modernaのメラノーマ再発49%抑制、ブタ腎臓異種移植271日、GPT-6 Astraの初Critical判定）
- **本文の要点マークアップ**: Key Claim・Evidence / Context の本文中で、その記事で最も重要な語句や事実を `**〜**` で囲んで強調する。**1セクションにつき1〜2箇所まで**（強調が多すぎると効果が消える）。強調するのは「金額の大きさ」ではなく「なぜ重要か」が伝わる部分を優先する（金額・パーセントはメール側で自動的に太字になるため、二重に囲む必要はない）。**frontmatter（`title`・`investment-implication`）には `**` を使わない**（YAMLの可読性が落ちるため。本文セクションのみ）

### Healthcare（Biotech）ノートの追加欄（2026-10-19〜）

Healthcare の日次メールは「💰 お金が動いた」「🧪 臨床の結果」の2つの表（1記事=1行）だけになった。
表の行は frontmatter の下記の欄から機械的に作られる（本文は読まれない）。そのため、
**landscape-position が `Biotech` で始まるノートだけ**、`landscape-position:` の直後に次の欄を
**必ずすべて書く**。該当しない欄も **キーは残して値を空文字（`""`）にする**。
キーが1つも無いノートは「未記入」と判定され、日次メールの末尾に警告が出る。

```yaml
indication: ""          # 対象の病気（日本語。例: 肥満 / 多発性嚢胞腎 / がん（HER2陽性））。主たる1つ。記事に無ければ空。推測で埋めない
approach: ""            # アプローチ＝モダリティ＋標的を短く（例: siRNA / 遺伝子治療（AAV） / ALK7阻害 / FcRn阻害抗体 / AI創薬）
players: ""             # 主役の企業。提携・買収は「買い手 ← 売り手」（例: Roche ← Rona）。臨床結果は開発企業
deal-type: ""           # funding | ipo | license | ma | fund | 空（お金が動いた記事のみ）
deal-total-usd-m: ""    # 総額（マイルストン込み）を百万ドル単位の数値で（例: 1160）。非公表なら空
deal-upfront-usd-m: ""  # 前払い・実際の調達額（百万ドル）。シリーズ調達とIPOは調達額をここに入れる。非公表なら空
deal-note: ""           # 種類を短く（例: シリーズA / 上方修正IPO / 前払い非公表）
trial-phase: ""         # 1 | 1/2 | 2 | 2/3 | 3 | 空（臨床結果の記事のみ）
trial-result: ""        # success（主要評価項目を達成） | fail（未達・中止） | mixed（一部達成・用量で割れる・評価が割れる） | 空
trial-note: ""          # 結果の補足を20字程度で（例: PFS未達、OSは継続）
```

- **記事に書いてあることだけを入れる。** 記事に無い値は空にする（推測で埋めない）。病名・モダリティ・金額を、記事に書かれていない知識で補わない
- 金額はドル以外なら概算でドルに換算する。記事に無い額は空にする（推測禁止）。既存ルールのとおり、`Evidence / Context` にも同じ数字を入れる
- **総額と前払いを混ぜない。** 提携の「最大$1.16B」のほとんどは後払いのマイルストンで、実態とずれる。集計は前払い・調達額（`deal-upfront-usd-m`）を主に使うので、前払いが記事に無いときは空にする（総額で代用しない）
- お金と臨床結果の両方に当てはまる記事は、両方を埋める（日次メールでは「お金が動いた」の表に出る）
- `deal-*` は**その記事で新たに動いたお金**だけ。過去の取引への言及（例: 数年前の買収額）は入れない。`trial-*` は**試験の結果**だけ。FDAの審査日程・承認・安全性の報告・規制は臨床結果ではないので空にする
- `deal-type: fund` はVCなどのファンド組成。日次の表には出ず、週次にまわる
- `indication` と `approach` は週次の集計で **「（」または「(」より前の部分** で束ねられる。詳細は括弧の中に書く（例: `遺伝子治療（AAV）`）
- 値の書き換えに sed を使わない（上の「frontmatterの値を書き直すときは sed を使わない」を参照）。書き直したら、各キーが1行ずつであることを確認する

---

## キャプチャ基準（フィルタリング）

### 含める
- 資金調達・製品発表・研究ブレークスルーのニュース
- signal-strength が `moderate` 以上になりそうなもの
- CRISPR・遺伝子治療・合成生物学・BMI・神経インターフェース関連
- AI・半導体・量子コンピューティングのメジャーニュース

### 除外する
- 単純な人事・採用ニュース（技術的インパクトなし）
- プレスリリースのみで独自情報なし
- 既にキャプチャ済み（下記「重複チェック」参照）

### 重複チェック（2段階・このルールが唯一の正）

判定は**2種類あり、それぞれ探す範囲が違う**。混同しないこと。

| 判定 | 探す範囲 | 判定方法 | 一致したら |
|---|---|---|---|
| **① URL完全一致** | **全期間（`00-Inbox/` の全ファイル）** | 記事URLで既存ノートの `source:` を検索 | **必ずスキップ** |
| **② 類似トピック** | 過去7日以内 | タイトル・企業名・主題の重なりで判断 | スキップ（判断は書き手に委ねる） |

- **①に期間の制限を設けてはいけない。** `00-Inbox/` は処理後も削除されず全件（2026-05-22以降の800件超）が残っており、全件grepは一瞬で終わる。**期間で区切る理由がない**
- 期間の窓（過去7日）が必要なのは②の曖昧な判定だけ。①の厳密な一致判定にまで窓を掛けると、**時間を空けて蒸し返された記事が二重にキャプチャされる**（2026-09-05に実際に発生: `ability-neurotech-bci-human-trial` を8/23と9/5で13日空けて二重取得）
- **プロンプト側に「過去7日以内に…記事URLで検索」という旧い書き方が残っている場合は、このCLAUDE.mdのルールが優先する**

### 量子ソース（qcr-/tqi-）の軽量化ルール（2026-07-18〜）
Frontier（量子）は日次配信から外れ週次サマリーに集約されたため、キャプチャ自体も全体感把握用に軽量化する（使用量削減も兼ねる）。

- `qcr-`・`tqi-` は**1日合計最大2記事まで**（両ソース合わせて2件。個別ソースごとに2件ではない）
- **枠は先着順で埋めない。** ソーステーブルの順に処理すると `qcr-` が先に来るため、素朴に処理すると `qcr-` が2件取った時点で `tqi-` が構造的に0件になる。必ず**両ソースの候補をいったん出し切ってから、重要度の高い順に2件を選ぶ**こと（片方から2件になっても、両方から1件ずつになってもよい）
  - 2026-09-06の回で実際に起きた: `qcr-` が2件取り、`tqi-` の「NEC、量子計算機ハードウェアの開発を中止」が枠切れで落ちた。重要度では明らかにNECの方が上であり、先着順は選定として機能していない
- 本文は **Key Claim中心に3行以内**で簡潔に書く（Evidence / Contextを詳細に掘り下げない）
- 詳細な深掘りは不要。週次ダイジェストは1行ヘッドライン形式で潮流を見るためのものなので、個別記事の情報量より広く拾うことを優先する

### 核融合ソース（fia-/tcf-）の軽量化ルール（2026-10-25〜）
Fusion（核融合）は日次配信から外れ、土曜の週次1通に集約される。量子と同じ形で軽量化する。

- `fia-`・`tcf-` は**1日合計最大3記事まで**（両ソース合わせて3件。個別ソースごとに3件ではない）
- **枠は先着順で埋めない。** ソーステーブルの順に処理すると `fia-` が先に来るため、素朴に処理すると `fia-` が3件取った時点で `tcf-` が構造的に0件になる。必ず**両ソースの候補をいったん出し切ってから、重要度の高い順に3件を選ぶ**こと
- `fia-` は **FIA ドメイン（`fusionindustryassociation.org`）の自社記事を優先**する。FIA のフィードには外部サイト（Reuters・FT・各国メディア等）の記事へのリンクが混ざっており、`url` のドメインで区別できる。**外部リンク記事は、`sources-raw` のファイルが `extraction: full`（本文が取れている）のときだけ採用する。** ペイウォールで本文が取れず `extraction: summary`（フィード要約）になった記事は採らない（Evidence を書く根拠が無く、推測で補うことになるため）
- `tcf-` の記事は `tc-` と同じURLで出ることがある。重複チェック①（URL完全一致・全期間）でそのままスキップされるので、特別扱いは要らない
- `tc-`/`tm-`/`ek-` など**他ソースから来た核融合の記事も、同じ扱い**にする。ソースに関係なく、核融合の記事の landscape-position は葉 `Energy > Generation > 核融合(Fusion)`（`docs/taxonomy.md`）にする。`build_digest.py` は landscape-position に `核融合` を含むノートを（第1セグメントが Energy でも）Fusion カテゴリに入れ、日次から外す
- 本文は **Key Claim中心に3行以内**で簡潔に書く（週次は1行ヘッドライン＋表が中心）。ただし下の追加欄は必ず書く

### Fusion（核融合）ノートの追加欄（2026-10-25〜）

Fusion の週次メールは「💰 資金調達」の表・方式別の集計・政策/技術の一覧から成り、
frontmatter の下記の欄から機械的に作られる（本文は読まれない）。そのため、
**landscape-position に `核融合` を含むノートだけ**、`landscape-position:` の直後に次の欄を
**必ずすべて書く**。該当しない欄も **キーは残して値を空文字（`""`）にする**。
キーが無いノートは「未記入」と判定され、週次メール末尾に件数の注記が出る。

```yaml
fusion-approach: ""     # tokamak | stellarator | frc | inertial | z-pinch | magnetized-target | mirror | other | 空
fusion-topic: ""        # funding | policy | tech | supply-chain | other
players: ""             # 主役の企業・機関
deal-type: ""           # funding | ipo | ma | grant | 空
deal-upfront-usd-m: ""  # 実際の調達額・交付額（百万ドル）。非公表なら空
deal-note: ""           # 例: シリーズB / DOEマイルストン
```

- **記事に書いてあることだけを入れる。** 記事に無い値は空にする（推測で埋めない）。方式（tokamak 等）を、記事に書かれていない知識で補わない
- 金額はドル以外なら概算でドルに換算する。既存ルールのとおり、`Evidence / Context` にも同じ数字を入れる
- `deal-*` は**その記事で新たに動いたお金**だけ。過去の取引への言及は入れない。`deal-type` が空でない記事は「資金調達」の表に出て、`fusion-topic` に関係なく政策/技術の一覧には出ない
- `players` は Healthcare と同じキー名。核融合ノートでは主役の企業・機関（提携・買収は「買い手 ← 売り手」）
- 値の書き換えに sed を使わない（「frontmatterの値を書き直すときは sed を使わない」を参照）

---

## 巡回ログ（毎回必ず出力する）

キャプチャ処理の最後に `digests/YYYY-MM-DD-sources.md` を作成し、**全ソース1行ずつ**の巡回結果を記録する。
`daily: source log {YYYY-MM-DD}` としてコミットする（配信対象は `00-Inbox/*.md` のみなので、このファイルはメールに影響しない）。

なぜ必要か: 「該当記事が無いソースはスキップしてよい」というルールのため、**スキップは何の痕跡も残さない**。
その結果「取得したが採らなかった」のか「取得に失敗した」のかを事後に切り分けられず、キャプチャ件数が急に減った日の原因調査ができない
（2026-09-07の朝、5件/3ソースまで落ちた回で実際に切り分け不能になった）。

フォーマット（ソーステーブルの**全行**を必ず1行ずつ書く。0件のソースこそ重要なので省略しない）:

```markdown
# 巡回ログ 2026-09-06

| prefix | 取得 | 候補 | 採用 | 不採用の理由 |
|--------|------|------|------|--------------|
| `tc-` | OK | 5 | 2 | 3件はキャプチャ基準の対象外 |
| `fb-` | OK | 2 | 0 | 量子枠とは無関係。判断ミスならここに残る |
| `tqi-` | OK | 3 | 0 | 量子枠を`qcr-`が使用済み |
| `ek-` | 失敗 | - | - | EGRESS_BLOCKED |
```

- 取得: `OK` / `失敗`（失敗時は理由を「不採用の理由」列に書く。`EGRESS_BLOCKED`・タイムアウト・404など）
- 候補: そのソースで見た当日記事のうち、キャプチャ基準に一致しそうだったものの件数
- 採用: 実際に `00-Inbox/` へ書き出した件数
- 不採用の理由: 候補>採用のとき**必ず書く**。「重複（既出URL）」「signal-strength不足」「量子枠切れ」など

---

## 障害日のさかのぼり取得（実行開始時に必ず判定する）

前日が全ソース取得失敗（egress遮断など）で0件だった場合、**その日の記事は誰も拾わないまま消える**。
翌日の実行時点でも各ソースのRSS/一覧には3〜4日前の記事が残っているため、取得自体は可能である。
取りに行っていないだけなので、障害の翌日に限りさかのぼって拾う。

### 判定（ソース取得を始める前に行う）

前日を D とする。次のどちらかに当てはまれば **D は障害日**:

1. `digests/{D}-sources.md` が存在し、**全行の「取得」列が「失敗」**
2. `digests/{D}-sources.md` が存在せず、かつ `00-Inbox/` に `{D}-` で始まる記事ノートが**1件もない**（巡回ログ導入前や、ログを書く前に落ちた回）

### 障害日だったときの取得

通常の本日分に加えて、**D の記事を各ソース最大2件**さかのぼって取得する（本日分の最大3件とは別枠）。

- ファイル名は `00-Inbox/{D}-{prefix}-{slug}.md`、frontmatter の `date:` も `{D}` にする（実際の記事日付に合わせる。捏造しない）
- 量子ソースの2記事上限は **D の分と本日分でそれぞれ独立**に適用する（Dで2件、本日で2件まで）
- 重複チェックは通常どおり（URL完全一致は全期間）。翌日の一覧に同じ記事が残っていても既出なら当然スキップされる
- コミットは通常どおりソースごと1コミット。`daily: {Source} capture {D} ({N} articles)` とDの日付で切る
- 批評コメントは**本日分1本にまとめる**（`digests/{本日}-commentary.md`）。さかのぼり分も同じファイルに含めてよい。
  `build_digest.py` は実行日基準でcommentaryを探すため、Dの日付でファイルを作ると読まれない
- **`digests/{D}-sources.md` は書き換えない。** 障害の記録として残す価値があるため。
  代わりに本日の巡回ログの末尾に「{D}分のさかのぼり取得: N件採用」を1行書く

### やらないこと

- **さかのぼるのは直近1日分だけ。** 2日以上前は追わない（フィードから溢れて取得が不確実になり、
  「取れなかった」のか「無かった」のかが判別できなくなる）
- 2日連続で障害日だった場合も、拾うのは直近のDのみ

---

## signal-strength 判定基準

| strength | 条件 |
|----------|------|
| `strong` | 評価額$1B以上、または業界構造を変えるブレークスルー |
| `moderate` | $100M〜$1Bの資金調達、または有望な技術進展 |
| `weak` | $10M〜$100M、または参考情報 |
| `none` | 投資含意なし、または動向ウォッチのみ |

---

## git 操作

1ソースにつき1コミット。コミットメッセージ形式：

```
daily: {Source} capture {YYYY-MM-DD} ({N} articles)
```

例: `daily: STAT News capture 2026-06-20 (2 articles)`

プッシュ先: `https://github.com/Shuhei-Tsunoda02006242/my-skill-graph-inbox.git`
Author: `Claude <noreply@anthropic.com>`

1回のループで最大ソース×3記事まで（合計最大12記事/日）。

※ コミット・pushはキャプチャ後に `scripts/daily-capture.sh` がフォールバックとして必ず実行するので、Claude側でgitが実行できなくてもノート作成さえ完了していればよい。

---

## 配信カテゴリ（Sequoia風アレンジ）

メールはソース別ではなく、Sequoia Capital「Our Companies」風にアレンジした5カテゴリ＋その他でグルーピングする（2026-07-18〜）。振り分けは `landscape-position` の第1セグメントを優先し、空欄ならソースprefixでフォールバックする。

| カテゴリ（表示名） | landscape-position第1セグメント | ソースprefixフォールバック | 配信頻度 |
|---|---|---|---|
| AI | AI | `tc-`, `tm-` | 日次 |
| Hardware（半導体） | Semiconductor | （フォールバック無し） | 日次 |
| Climate & Energy | Energy | `ek-` | 日次 |
| Healthcare | Biotech | `sn-`, `is-`, `fb-` | 日次（資金・臨床結果のみ1行）＋週次（土曜） |
| Frontier（量子） | Quantum | `qcr-`, `tqi-` | **週次（土曜8:00 JST前後）** |
| Fusion（核融合） | （第1セグメントを問わず、landscape-position に `核融合` / `Fusion` を含むもの。Energy より優先） | `fia-`, `tcf-` | **週次（土曜8:05 JST起動）** |
| その他 | （どれにも該当しない/position無し） | 不明なprefix | 日次 |

Frontier（量子）と Fusion（核融合）は日次配信から外れ、それぞれ `weekly-quantum-digest.yml`・`weekly-fusion-digest.yml` が土曜朝に週次1通としてまとめて送る（詳細は次節と `docs/mail-delivery.md`）。

---

## メール配信（GitHub Actions）

配信タイミング・カテゴリ構成・ヒートマップ埋め込みの詳細は **`docs/mail-delivery.md`** を参照。
キャプチャの動作には影響しないため、ここには要点のみ置く:

- 日次ダイジェストは毎朝7:35 JST起動（実配信8:00前後）、カテゴリごとに1通
- Frontier（量子）は土曜7:35 JST起動の週次1通
- Fusion（核融合）は土曜8:05 JST起動の週次1通。資金調達の表・方式別の集計・政策/技術の一覧（Geminiとヒートマップは無し）。表は上記「Fusion（核融合）ノートの追加欄」から作られる
- Healthcare は日次では「お金が動いた」「臨床の結果」の2表（1記事=1行）だけ。それ以外の記事は土曜7:50 JST起動の週次1通にまとまる。表は上記「Healthcare（Biotech）ノートの追加欄」から作られる
- 本文組み立て・SMTP送信とも `scripts/build_digest.py` が実施

## tech-tags マッピング（ソース別）

| ソース | 主な tech-tags |
|--------|----------------|
| TechCrunch | AI, semiconductor |
| Techmeme | AI, semiconductor, quantum（記事内容による） |
| STAT News | biotech |
| IEEE Spectrum Neuro | neurotech |
| Quantum Computing Report | quantum |
| FierceBiotech | biotech |
| Electrek | energy |
| Fusion Industry Association | energy |
| TechCrunch Fusion | energy |

---

## 領域マップ（パンくず用タクソノミー）

**`docs/taxonomy.md` を読むこと。** frontmatter の `landscape-position` を
埋めるときは必ずそのファイルを参照する（ここには書き写さない——二重管理になり
実態とズレるため）。`大分類 > 中分類 > 葉` の形式で最も近い葉を選ぶ。
