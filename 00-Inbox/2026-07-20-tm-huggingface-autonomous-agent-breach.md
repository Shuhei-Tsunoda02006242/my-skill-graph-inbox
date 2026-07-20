---
title: "Hugging Face、自律型AIエージェントによる侵入を受けたと公表——検知もAIが担う"
date: 2026-07-20
source: "https://www.techmeme.com/260719/p12"
source-type: article
domain: deeptech
tech-tags: [AI]
companies-mentioned: [Hugging Face]
investment-implication: ""
signal-strength: none
status: fleeting
landscape-position: "AI > Orchestration/Tooling > AIセキュリティ"
---

## Key Claim
AIモデル共有大手のHugging Faceが、悪意あるデータセットを起点に自律型AIエージェント群が週末をかけて内部クラスターと認証情報にアクセスした侵入事件を公表した。攻撃・検知の両面でAIが主体的役割を担った点が注目される。

## Evidence / Context
- 攻撃者はデータローダーの任意コード実行脆弱性とテンプレートインジェクションを悪用し、使い捨てのサンドボックス群から数千のアクションを自動実行
- 侵入はHugging Face自社のLLMベース異常検知パイプラインが検知し対応
- 公開モデル・データセット・Spacesの改ざん証拠はなく、ソフトウェアサプライチェーンもクリーンと確認
- 攻撃者は利用ポリシーに縛られない一方、防御側は商用APIのガードレールに阻まれる非対称性が浮き彫りに

## My Take
<!-- fill in later -->

## Links
<!-- fill in later -->
