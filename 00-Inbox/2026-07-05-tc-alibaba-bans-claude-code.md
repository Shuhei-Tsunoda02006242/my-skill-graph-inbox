---
title: "アリババ、Anthropicの「Claude Code」の社内利用を7月10日から禁止、スパイウェア疑惑と蒸留攻撃が背景"
date: 2026-07-05
source: "https://techcrunch.com/2026/07/04/alibaba-reportedly-bans-employees-from-using-claude-code/"
source-type: article
domain: both
tech-tags: [AI]
companies-mentioned: [Alibaba, Anthropic, Qwen]
investment-implication: "米中両陣営がAI開発ツールを相互に禁止し合う「AIデカップリング」が実務レベルまで進行していることを示し、Anthropicの中国関連ビジネス機会の縮小と、代替として自国製コーディングエージェント（Qoderなど）への需要シフトを示唆する。"
signal-strength: moderate
status: fleeting
---

## Key Claim
アリババは7月10日付でAnthropicのコーディングツール「Claude Code」の社内利用を高リスクソフトウェアとして禁止し、代替として自社製の「Qoder」を推奨する。

## Evidence / Context
- 発端は6月30日、あるユーザーがClaude Codeを逆解析し、2026年4月2日リリースのv2.1.91以降に密かに含まれていた難読化コードを発見。タイムゾーンやプロキシ情報など環境情報を検査し、Anthropicサーバーへのプロンプトに識別マーカーを挿入していた
- Anthropic社員は、この仕組みは3月に開始した実験の一部で「不正リセラーによるアカウント濫用の防止」と「蒸留（distillation）攻撃対策」が目的だったと説明
- 背景にはAnthropic側の主張もある：アリババのQwen AIラボに関連するとされる主体が、約2万5000件の不正アカウントを使い4〜6月の間に2880万回のやり取りでClaudeへの大規模な蒸留攻撃を行ったとされる
- 米中両国でAI開発ツールの相互禁止（太平洋の両岸での「Claude Code問題」）が進んでおり、AI供給網のデカップリングが加速している

## My Take


## Links
- [[2026-07-03-tm-anthropic-china-claude-loopholes]]
