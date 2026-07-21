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

`.github/workflows/daily-digest.yml` は**毎朝7:35 JSTにcron起動**（GitHub Actionsのスケジュール遅延込みで実配信は8:00 JST前後、2026-07-22〜。以前はcron 08:00 JST起動設定だったが毎時00分は混雑で40分超遅延することが実測されたため前倒し）し、前回送信以降（ルートの `.digest-state` マーカー以降）に追加された全ソースのノートを上記の**配信カテゴリ別**にグルーピングし、カテゴリごとのGemini批評コメント付きで **カテゴリごとに1通ずつ** メール送信する（2026-07-18〜、以前はソース別グルーピングだった。2026-07-05〜07-17はソース別1通ずつ、それ以前は1日1通にまとめていた）。

- Frontier（量子）カテゴリは日次送信の対象外。`.github/workflows/weekly-quantum-digest.yml` が**土曜7:35 JSTにcron起動**（cron `35 22 * * 5`、Actionsの遅延込みで実配信は土曜8:00 JST前後）で週次1通として送信する（`WEEKLY_QUANTUM=1 python3 scripts/build_digest.py` 起動。対象は `00-Inbox/*.md` をファイル名の日付でスキャンし過去7日以内のFrontier（量子）ノート。`.digest-state` には依存しない。対象0件なら送信せず正常終了）。週次本文は1行ヘッドライン形式（フルカードではない）＋Gemini週次総括＋末尾に量子ヒートマップ
- push時の都度送信は廃止済み（2026-07-04）
- 手動送信: 両ワークフローとも Actions の workflow_dispatch から実行可能
- 本文組み立て・SMTP送信ともに `scripts/build_digest.py` が実施（`smtplib.SMTP_SSL` で1ログイン後、カテゴリごとにループ送信。Gemini API失敗時はコメント無しで送信を継続）
- カテゴリメールは複数ソースが混在するため、各記事カードにソース名チップ（シグナルバッジの横にグレー文字で表示。例: `TechCrunch`）を表示する。plain版も各記事に `ソース: {ソース名}` の1行を追加
- 📍パンくずには市場規模注記が付く（`assets/market/market-sizes.json` の `breadcrumb-map` 由来。例: `📍 Quantum > PQC（市場$0.4B・急成長）`）。マップ不一致・データ無しなら注記なしでフォールバック
- メール末尾に**そのカテゴリに対応する領域の**市場規模ヒートマップPNGを1枚だけ埋め込む（`🗺 市場規模ヒートマップ` セクション。カテゴリ→domainの対応は「配信カテゴリ」表参照、その他はヒートマップ無し）。SVGをGitHub Actions上で `rsvg-convert` によりPNG化しCID埋め込み。環境変数 `INCLUDE_HEATMAPS=0` で画像埋め込みのみ無効化可能（📍注記は継続）
- `assets/market/` はvault側 `scripts/generate_market_treemaps.py` 実行時に自動同期される（Inboxリポジトリはvaultの非コミット物を直接読めないため）

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

---

## 領域マップ（パンくず用タクソノミー）

<!-- 出典: My-Skill-Graph/_maps/*-landscape.md（四半期ごとに同期） -->

- AI
  - Compute/Infra
    - AIアクセラレータ(GPU/TPU)
    - 推論特化チップ/ネオクラウド
    - DC電力/冷却
  - Foundation Models
    - フロンティアLLM
    - 効率化/低コストモデル
    - World Models/マルチモーダル
    - 音声/動画生成
  - Orchestration/Tooling
    - エージェント実行基盤
    - コンテキスト/データ接続
    - 監視/評価/ガバナンス
    - AIセキュリティ
  - Application
    - 水平SaaS/エンタープライズエージェント
    - 垂直特化(科学/ヘルス/気象)
    - コンシューマ/デバイス統合
  - Data/Training
    - 学習データ/ラベリング
    - 強化学習(RL)
    - 物理AI/ロボットデータ
  - Governance/Geopolitics
    - 輸出規制/人材
    - AI規制/安全性

- Semiconductor
  - 設計(Design)
    - EDA
    - IP(Arm/RISC-V)
    - ファブレス/ロジック
    - 内製ASIC(ハイパースケーラー)
  - 製造(Manufacturing)
    - 先端ファウンドリ
    - メモリIDM
    - OSAT(後工程)
  - 装置(Equipment)
    - リソグラフィ(EUV)
    - 成膜/エッチング/計測
  - 材料(Materials)
    - シリコンウェハ
    - フォトレジスト/ガス/スラリー
    - 化合物半導体(SiC/GaN)
  - 製品カテゴリ
    - ロジック(CPU/GPU/SoC)
    - メモリ(DRAM/HBM/NAND)
    - アナログ/パワー
    - 先端パッケージング
    - エッジ/組み込み推論チップ
  - 次世代素材/方式
    - 光チップ/フォトニクス
    - バレートロニクス
    - CXL/近メモリ計算

- Quantum
  - Computing
    - 超伝導方式
    - イオントラップ方式
    - 中性原子方式
    - フォトニック方式
    - トポロジカル方式
    - 誤り訂正/フォールトトレランス
    - コンパイラ/ミドルウェア
    - 量子アルゴリズム/アプリ
  - Communication/Security
    - QKD/量子インターネット
    - 分散量子
    - PQC(耐量子暗号)
  - Sensing
    - 量子計測/センサー
  - 資本/立地
    - 量子IPO/SPAC
    - 政府量子キャンパス
    - 研究拠点/人材

- Biotech
  - Tools/Platforms
    - ゲノム編集(CRISPR)
    - 合成生物学
    - AI創薬
    - シーケンシング/オミクス
  - Modality
    - 低分子
    - 抗体/バイオ医薬
    - 遺伝子治療
    - 細胞治療(CAR-T)
    - 核酸/mRNA
    - 中枢神経/サイケデリック
  - Development/Regulatory
    - 臨床試験/CRO
    - FDA承認/審査高速化
  - Supply/Industrialization
    - CDMO/バイオ製造
    - 農業バイオ
  - Neurotech/BMI
    - 侵襲/低侵襲BMI
    - 双方向BMI/触覚
    - EEG/センサー
    - 音声合成BMI
  - 資本/M&A
    - Pharma大型M&A
    - バイオIPO/ライセンス

- Energy
  - Generation
    - 核融合(Fusion)
    - 次世代原子力/SMR
    - 太陽光
    - 風力
    - 地熱(次世代/海洋)
  - Storage
    - リチウムイオン/次世代化学
    - グリッド蓄電/セカンドライフ
    - 長時間貯蔵(LDES)
    - 水素/合成燃料
  - Grid/T&D
    - 送電網/変圧器
    - グリッド安定化/需給調整
  - Demand/Efficiency
    - データセンター電力/冷却
    - EV/電動化
    - 省エネ/デマンドレスポンス
  - AIデータセンター電力(横断)
    - オフグリッド電源
    - 電力調達(PPA)/電力REIT
