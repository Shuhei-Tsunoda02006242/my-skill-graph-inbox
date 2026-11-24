---
title: "Anthropic、コードの承認までAIエージェントに任せる「Claude Ship」を発表"
date: 2026-11-24
source: "https://techcrunch.com/2026/11/23/anthropic-launches-claude-ship-letting-ai-agents-review-fix-and-approve-code-changes/"
source-type: article
domain: both
tech-tags: [AI]
companies-mentioned: [Anthropic, GitHub]
investment-implication: "コード生成の次のボトルネックであるレビュー・承認工程にAIが入り、人間の承認を前提にしたコードレビュー/CIツール各社の価値提案が揺らぐ。Team・Enterpriseプラン向けで、上場直後のAnthropicにとって開発者向け有料機能の上積みになる"
signal-strength: moderate
status: fleeting
landscape-position: "AI > Orchestration/Tooling > エージェント実行基盤"
---

## Key Claim
Anthropicが、コードレビュー・修正に加えて**チームが定めたポリシーに基づきAIが変更を自動承認する**エージェント群「Claude Ship」を発表した。

## Evidence / Context
- 構成は、一般提供済みのCode Reviewと、ベータの2エージェント。PR StewardはCI失敗・マージ競合・レビュー指摘に対応し、毎回の変更内容と戻し方をコメントする。Claude Approvalsはリポジトリ内のファイルに自然言語で書いた承認ポリシーを適用する
- 背景は**AIがコードを大量に書くようになり、人間によるレビューと承認が詰まっている**こと。同社は「Claude Codeチームではコードの大半をClaudeが書いている」としている
- ベータのため、まず観察のみのモードで動かすことを推奨。対象リポジトリを1つに絞る、月額上限を設けるといった制御も可能。GitHub上のリポジトリで、Claude Team・Enterpriseプランに順次提供

## My Take

## Links
