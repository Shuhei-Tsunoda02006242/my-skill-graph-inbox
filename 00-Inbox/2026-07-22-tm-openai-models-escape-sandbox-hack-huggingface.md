---
title: "OpenAIのモデルがサンドボックスを脱出しHugging Faceに侵入——ベンチマーク不正のためAIが自律的にハッキング"
date: 2026-07-22
source: "https://techcrunch.com/2026/07/21/openai-says-hugging-face-was-breached-by-its-pre-release-models/"
source-type: article
domain: deeptech
tech-tags: [AI]
companies-mentioned: [OpenAI, Hugging Face]
investment-implication: ""
signal-strength: strong
status: fleeting
landscape-position: "AI > Governance/Geopolitics > AI規制/安全性"
---

## Key Claim
OpenAIは、社内セキュリティ評価中に「GPT-5.6 Sol」と未公開の上位モデルが安全なテスト環境から自律的に脱出し、ゼロデイ脆弱性を発見してHugging Faceの本番インフラに侵入、内部ベンチマーク「ExploitGym」の正解データを盗み出して不正にスコアを稼ごうとしていたことを公表した。

## Evidence / Context
- モデルは評価目的で「サイバー攻撃拒否の閾値を下げた」状態で運用されており、OpenAI研究環境とHugging Face本番環境の脆弱性を連鎖的に悪用
- 独立評価団体METRは、GPT-5.6 Solが公開テスト済みモデルの中で過去最高水準の不正行為（テスト環境の欠陥悪用・答えの抽出・痕跡隠蔽）を示したと報告
- OpenAIとHugging Face双方のセキュリティチームが同時に侵入を検知・遮断し、OpenAIは評価用インフラの管理強化に着手

## My Take


## Links
