---
source: "TechCrunch"
prefix: tc-
title: "Elorian’s first AI model wants to reason with images, not just about them"
url: "https://techcrunch.com/2026/10/16/elorians-first-ai-model-wants-to-reason-with-images-not-just-about-them/"
published: 2026-10-16
chars: 2865
truncated: false
extraction: full
---

Elorian, the Palo Alto AI startup that raised a $55 million seed round at a $300 million valuation before it launched a product, released its first model on Friday, TechCrunch has exclusively learned.
The model, Glimpse, is launching as a research preview with API access and a chat interface. The thesis? Today’s AI models, for all their skill with language and code, still can’t really see.
Most multimodal models look at an image once, convert it to tokens, and then reason about it in text — like describing a photo from memory. Glimpse keeps going back to the source. Mid-reasoning, it can crop into a region, pull specific frames from a video, or run code to measure or compare what it’s looking at, a mechanism Elorian calls a “visual scratch space.” Think of someone pinching to zoom on a phone photo to double-check what they thought they saw.
For former Google DeepMind researcher and Elorian CEO Andrew Dai, one of the clearest signs that AI still couldn’t really see came on game night.
Last year he photographed a board game he’d just finished with friends and asked a frontier model who was winning. It couldn’t say. Board games “each have their own visual language, each have their own iconography, symbols,” he told TechCrunch. “To an adult, it’s quite easy to understand what’s going on with minimal text, but these models aren’t able to intuit what the symbols mean.”
“Humans can look at Ikea diagrams, with no text, and assemble Ikea furniture, right? Why can’t AI models?” he said.
The approach isn’t completely new — OpenAI added crop-and-zoom during reasoning to its o-series models in 2025 — but Elorian’s pitch is that it built the whole model around it, cheaply. The company says a small team trained Glimpse on a few hundred GPUs and that the model is substantially smaller than the frontier systems it’s benchmarked against.
Glimpse costs $0.60 per million tokens in and $3 per million tokens out — cheaper than mid-level models like Sonnet and Sol but more expensive than lightweight models like Haiku and Luna.
But according to Elorian’s evaluations, Glimpse outperforms even GPT-6 Astra on scientific chart reasoning and short-form video captioning, with competitive results on other visual reasoning tasks.
Elorian came out of stealth six months ago with a round co-led by Striker Venture Partners, Menlo Ventures, and Altimeter Capital, with participation from Nvidia and Google chief scientist Jeff Dean.
The initial targets are companies sitting on lots of video: robotics firms, scientific labs, media, and creative companies. Longer term, Elorian wants to move from seeing to doing. That means building a model of a scene using that to choose an action, including directly controlling robots. Next year, Dai said, the company aims to build “the world’s best visual reasoning model,” one that leads on every visual reasoning test.
