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

## メール配信（GitHub Actions）

`.github/workflows/daily-digest.yml` が **毎朝08:00 JST** に実行され、前回送信以降（ルートの `.digest-state` マーカー以降）に追加された **全ソース** のノートをソース別にグルーピングし、ソースごとのGemini批評コメント付きで **ソースごとに1通ずつ** メール送信する（2026-07-05〜、以前は1日1通にまとめて送信していた）。

- push時の都度送信は廃止済み（2026-07-04）
- 手動送信: Actions の workflow_dispatch から実行可能
- 本文組み立て・SMTP送信ともに `scripts/build_digest.py` が実施（`smtplib.SMTP_SSL` で1ログイン後、ソースごとにループ送信。Gemini API失敗時はコメント無しで送信を継続）

---

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
