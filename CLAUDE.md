# My-Skill-Graph-Inbox: Capture Rules

自律キャプチャループの動作仕様。新しいソースを追加するときはここを先に更新する。

---

## ループの起動条件

このファイル（`CLAUDE.md`）が存在しないとループは再起動できない。
ループ再起動時は **必ずこのファイルの存在を確認してから** CronCreate を呼ぶ。

---

## キャプチャ対象ソース

| prefix | ソース | URL | ドメイン |
|--------|--------|-----|---------|
| `tc-` | TechCrunch | `https://techcrunch.com/category/startups/` | AI・半導体・スタートアップ資金調達 |
| `tm-` | Techmeme | `https://www.techmeme.com/` | テック業界全般のヘッドライン集約 |
| `sn-` | STAT News | `https://www.statnews.com/category/biotech/` | バイオテック・CRISPR・遺伝子治療・創薬 |
| `is-` | IEEE Spectrum Neuro | `https://spectrum.ieee.org/tag/brain-computer-interface` | BMI・ニューロテック・脳科学×エンジニアリング |
| `qcr-` | Quantum Computing Report | `https://quantumcomputingreport.com/` | 量子コンピューター全般・商用化動向・資金調達 |
| `fb-` | FierceBiotech | `https://www.fiercebiotech.com/` | バイオテックM&A・FDA承認・臨床試験結果 |
| `ek-` | Electrek | `https://electrek.co/` | エネルギー技術・EV・再生可能エネルギー・電力インフラ |
| `tqi-` | The Quantum Insider | `https://thequantuminsider.com/` | 量子コンピューター・研究・PQC・上場/資金調達（qcr-の補完） |

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
- **本文の要点マークアップ**: Key Claim・Evidence / Context の本文中で、その記事で最も重要な語句や事実を `**〜**` で囲んで強調する。**1セクションにつき1〜2箇所まで**（強調が多すぎると効果が消える）。強調するのは「金額の大きさ」ではなく「なぜ重要か」が伝わる部分を優先する（金額・パーセントはメール側で自動的に太字になるため、二重に囲む必要はない）。**frontmatter（`title`・`investment-implication`）には `**` を使わない**（YAMLの可読性が落ちるため。本文セクションのみ）

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
- 既に過去7日以内に類似トピックをキャプチャ済み

### 量子ソース（qcr-/tqi-）の軽量化ルール（2026-07-18〜）
Frontier（量子）は日次配信から外れ週次サマリーに集約されたため、キャプチャ自体も全体感把握用に軽量化する（使用量削減も兼ねる）。

- `qcr-`・`tqi-` は**1日合計最大2記事まで**（両ソース合わせて2件。個別ソースごとに2件ではない）
- 本文は **Key Claim中心に3行以内**で簡潔に書く（Evidence / Contextを詳細に掘り下げない）
- 詳細な深掘りは不要。週次ダイジェストは1行ヘッドライン形式で潮流を見るためのものなので、個別記事の情報量より広く拾うことを優先する

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
| Healthcare | Biotech | `sn-`, `is-`, `fb-` | 日次 |
| Frontier（量子） | Quantum | `qcr-`, `tqi-` | **週次（土曜8:00 JST前後）** |
| その他 | （どれにも該当しない/position無し） | 不明なprefix | 日次 |

Frontier（量子）だけは日次配信から外れ、`weekly-quantum-digest.yml` が土曜朝に週次1通としてまとめて送る（詳細は次節）。

---

## メール配信（GitHub Actions）

配信タイミング・カテゴリ構成・ヒートマップ埋め込みの詳細は **`docs/mail-delivery.md`** を参照。
キャプチャの動作には影響しないため、ここには要点のみ置く:

- 日次ダイジェストは毎朝7:35 JST起動（実配信8:00前後）、カテゴリごとに1通
- Frontier（量子）だけは土曜7:35 JST起動の週次1通
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

---

## 領域マップ（パンくず用タクソノミー）

**`docs/taxonomy.md` を読むこと。** frontmatter の `landscape-position` を
埋めるときは必ずそのファイルを参照する（ここには書き写さない——二重管理になり
実態とズレるため）。`大分類 > 中分類 > 葉` の形式で最も近い葉を選ぶ。
