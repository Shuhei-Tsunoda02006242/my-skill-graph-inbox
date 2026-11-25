---
title: "日常業務ベンチマーク「ShellBench」、最先端AIエージェントでも3回に1回以上失敗"
date: 2026-11-25
source: "https://techcrunch.com/2026/11/24/even-the-best-ai-agents-struggle-with-everyday-life/"
source-type: article
domain: deeptech
tech-tags: [AI]
companies-mentioned: [OpenAI, Anthropic, Meta, Hugging Face, Red Hat, UC Berkeley]
investment-implication: "首位のGPT-6 Astraでも3回連続成功は半分未満、全試行の15.7%で安全要件違反。Muse（登録1,000万人超）などパーソナルエージェントの普及が先行するなか、信頼性と実行基盤（ハーネス）の出来が差別化要因になる"
signal-strength: moderate
status: fleeting
landscape-position: "AI > Orchestration/Tooling > 監視/評価/ガバナンス"
---

## Key Claim
1,000万件超の実利用ログをもとに作られた日常業務ベンチマーク「ShellBench」で、OpenAI・Anthropic・Metaの最先端モデルでも**3回に1回以上タスクに失敗**し、成功率は同じモデルでも実行基盤（ハーネス）によって大きく変わった。

## Evidence / Context
- 全モデル合計で15.7%の試行が少なくとも1つの安全要件に違反。正解した試行でも約10%は安全基準を満たさなかった
- 首位のGPT-6 Astraでも、同条件3回の試行をすべて成功させた割合は半分未満
- 個別タスク: 子どもの送迎予定の考慮漏れ79.5%、銀行アップロード用トークンの秘匿失敗18.6%、請求書の二重・誤支払いの推奨40.3%
- **ハーネス依存**: Meta Muse Wonder FullはPiで56%、Claude Codeでは38.1%。GPT-6 AstraとClaude Fable 5.2の優劣もハーネスによって逆転した
- 各社の純正ハーネス（Muse・Dots・Claude Duet）では評価していない。Museは開始6週間で米加1,000万人超が登録

## My Take

## Links
