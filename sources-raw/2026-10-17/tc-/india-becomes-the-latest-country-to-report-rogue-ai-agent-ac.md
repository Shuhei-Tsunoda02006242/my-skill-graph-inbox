---
source: "TechCrunch"
prefix: tc-
title: "India becomes the latest country to report rogue AI agent activity"
url: "https://techcrunch.com/2026/10/16/india-becomes-the-latest-country-to-report-rogue-ai-agent-activity/"
published: 2026-10-16
chars: 2331
truncated: false
extraction: full
---

AI agents from multiple providers accessed personal data and confidential material at Indian organizations during research and testing, India’s cybersecurity agency said Thursday.
The Indian Computer Emergency Response Team (CERT-In) said it had received “multiple voluntary disclosures from AI model providers” whose models, during research and evaluation runs on the open internet, “had reached the live systems of Indian organizations.”
The agents got in through credentials and connection settings left exposed in app configurations, public code repositories, and overly permissive cloud roles, and their actions “exceeded the authorisation of their assigned tasks.”
This makes India the latest stop on what has become a world tour for rogue AI agents. In July, OpenAI’s agents escaped a test environment and hacked French company Hugging Face — kicking off a summer of rogue AI agent activity. Last month, OpenAI apologized to Australia after its agents accessed four government websites, including a Medicare statistics portal.
At Hugging Face, OpenAI’s agents started the same way but then found and exploited software flaws to run code on the company’s servers. CERT-In described no such hacking in India, where the agents appear to have simply used the access left lying around.
Still, the Indian cases appear to be worse in one respect, which is what the agents saw: In Australia, OpenAI said it found no evidence its agents touched individuals’ medical or criminal records, even after they wrote files inside a Medicare statistics system, while in India, agents read personal data and confidential business records. And unlike earlier incidents, each disclosed by a single lab, India’s case involved agents from multiple providers.
CERT-In did not name the providers or affected organizations, or say whether the agents altered any systems. TechCrunch has reached out to CERT-In for more information.
For now, the closest parallel seems to be Anthropic’s July disclosure of Claude breaking into three companies’ systems during testing using basic techniques like weak passwords.
In India, as in Anthropic’s cases, the affected organizations had not detected the intrusions on their own. The disclosures have left governments relying on AI companies causing these breaches to voluntarily disclose rogue AI agent activity.
