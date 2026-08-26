# 領域マップ（パンくず用タクソノミー）

ノートの frontmatter `landscape-position` を埋めるための階層タクソノミー。
`大分類 > 中分類 > 葉` の形式で最も近い葉を選ぶ。ぴったりの葉が無ければ
最も近い中分類まででよい。複数領域にまたがる場合は主たる方を1つだけ。

**このファイルが唯一の正**（CLAUDE.md には書き写さない）。


<!-- 出典: My-Skill-Graph/_maps/*-landscape.md（四半期ごとに同期） -->

- AI
  - Compute/Infra
    - AIアクセラレータ(GPU/TPU)
    - 推論特化チップ/ネオクラウド
    - DC電力/冷却
    - メモリ/HBM需要
  - Foundation Models
    - フロンティアLLM
    - 効率化/低コストモデル
    - World Models/マルチモーダル
    - 音声/動画生成
    - 解釈可能性/内部表現研究
  - Orchestration/Tooling
    - エージェント実行基盤
    - コンテキスト/データ接続
    - 監視/評価/ガバナンス
    - AIセキュリティ
  - Application
    - 水平SaaS/エンタープライズエージェント
    - 垂直特化(科学/ヘルス/気象)
    - コンシューマ/デバイス統合
    - 産業/ロボティクス垂直(ロボタクシー/ヒューマノイド/製造)
    - 金融/クオンツトレーディング
  - Data/Training
    - 学習データ/ラベリング
    - 強化学習(RL)
    - 物理AI/ロボットデータ
  - Governance/Geopolitics
    - 輸出規制/人材
    - AI規制/安全性
    - エコシステム/アクセラレーター

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
    - 先端基板材料(ダイヤモンド等の超ワイドバンドギャップ)
  - 製品カテゴリ
    - ロジック(CPU/GPU/SoC)
    - メモリ(DRAM/HBM/NAND)
    - アナログ/パワー
    - 先端パッケージング(熱・冷却ソリューションを含む)
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
    - シリコンスピン方式
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
    - 政府R&D資金/補助金(CHIPS法等)

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
