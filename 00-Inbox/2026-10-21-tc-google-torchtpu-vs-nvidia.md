---
title: "GoogleがTorchTPUを公開、AmazonのTorchNeuronに続きPyTorch経由でNvidiaの牙城を崩しにかかる"
date: 2026-10-21
source: "https://techcrunch.com/2026/10/20/google-has-joined-amazon-in-attacking-nvidias-stronghold-with-ai-app-developers/"
source-type: article
domain: deeptech
tech-tags: [AI, semiconductor]
companies-mentioned: [Google, Amazon, Nvidia, Meta, Hugging Face]
investment-implication: "AIアプリの約85%が使うとされるPyTorchでNvidia依存を外す動きが、Googleに続きAmazonでも出そろった。移植コストが下がれば、TPUとTrainiumが推論・学習の代替先として現実味を増し、Nvidiaのソフトウェア面の囲い込みが最初に削られる。"
signal-strength: moderate
status: fleeting
landscape-position: "AI > Compute/Infra > AIアクセラレータ(GPU/TPU)"
---

## Key Claim
Googleが、自社AIチップTPU上でPyTorchアプリを動かせる**オープンソース「TorchTPU」を公開**し、前日のAmazon「TorchNeuron」に続いてNvidia依存の切り崩しに加わった。

## Evidence / Context
PyTorchはAIアプリの**約85%が使う**とされ、機能の多くがNvidia GPU向けに作られてきた。TorchTPUは設定変更だけで既存アプリをTPU（＝Google Cloud）へ移せる。GoogleはMeta、Hugging Face、vLLM開発元のInferact、SGLang開発元のRadixArkと連携して主要ツールとの互換を確保し、移行支援の「TPU agent suite」も出した。AmazonはTrainium向けのTorchNeuronを公開したうえ、PyTorch本体でもNvidia固有機能の切り離しコードを提出している。記事は、開発者がすぐNvidiaを捨てるわけではないとしている。

## My Take


## Links
