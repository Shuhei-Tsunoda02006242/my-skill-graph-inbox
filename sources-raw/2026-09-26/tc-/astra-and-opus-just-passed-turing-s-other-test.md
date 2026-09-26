---
source: "TechCrunch"
prefix: tc-
title: "Astra and Opus just passed Turing’s other test"
url: "https://techcrunch.com/2026/09/25/astra-and-opus-just-passed-turings-other-test/"
published: 2026-09-25
chars: 2691
truncated: false
extraction: full
---

Computer pioneer Alan Turing is best known for his eponymous experiment to test whether artificial and human intelligence can be distinguished. However, the more important test he faced during his lifetime was cracking the Enigma code used by Nazi Germany during World War II.
Now, a pair of cryptanalysts say they’ve cracked two long-unsolved messages encoded by Enigma machines using LLMs built by OpenAI and Anthropic.
While Turing and his team of cryptanalysts built an early computer, dubbed the Bombe, that allowed the United Kingdom to translate Enigma messages during the war, a handful of archival messages remain unbroken — usually due to mistranscription or errors by the original encoders.
Carter Leffen, a developer, simply told OpenAI’s newest model, Astra, to search a database of Enigma messages for an unbroken message and decode it. The model was able to do just that, after doing its own archival research, finding context clues, building a simulator of the Enigma machine, and ultimately recovering the plaintext of a message that had baffled researchers since 2005. He even used Astra to build an interactive website explaining the whole problem.
Frode Weierud, a retired electrical engineer with a lifelong interest in cryptology, maintains the website Crypto Cellar, which includes a variety of resources and records and a database of messages. Last week, Weierud validated Leffen’s solution, which he said left him in “awe.”
Notably, given the lengths that AI agents will go to answer the questions in front of them, the Astra model’s logs include discussion of archived messages in a “private collection” that aren’t hosted by Weierud. He still isn’t sure if the model accessed them or not, but speculates they may have been shared by a different researcher somewhere online, or that the model was able to access the German government’s public archives.
“GPT–6 Astra is behaving like a very professional cryptanalyst and archive researcher,” he wrote. “What it has achieved in two days would take a human researcher weeks or even months. Personally, I spent several weeks researching the Bundesarchiv files GPT–6 Astra refers to.”
On September 21, another cryptanalyst, Jack Willis, a cybersecurity executive, reached out to Weierud, saying he had used Anthropic’s Claude Opus 5 model to break a different unsolved message. Willis provided significantly more guidance to Claude, which was ultimately able to use the known signature of a particular officer’s name to break the message.
Weierud notes that there are just seven unbroken Enigma messages remaining, along with one message where the plaintext is known but the code is still unbroken.
Perhaps not for long.
