---
source: "The Quantum Insider"
prefix: tqi-
title: "Ethereum Plans Shift to Hash-Based Signatures for Post-Quantum Security"
url: "https://thequantuminsider.com/2026/11/27/ethereum-shift-hash-based-signatures-post-quantum-security/"
published: 2026-11-27
chars: 5885
truncated: false
extraction: full
---

Insider Brief
- Ethereum developers are planning to replace the network’s elliptic-curve signatures with hash-based alternatives as part of a security effort targeting future quantum and potential AI-driven cryptographic threats.
- The proposed changes cover validator signatures, wallet accounts and data blob commitments, with Keccak-256 emerging as the preferred hash function.
- The Ethereum Foundation is targeting December 2029 for the migration, although larger signatures, wallet upgrades and increased node costs remain technical challenges.
- Photo from Pexels by Jonathan Borba.
Ethereum’s core developers are preparing to phase out the elliptic-curve cryptography that secures the network and switch to hash-based signatures, a change meant to protect against attacks powered by quantum computers or by advances in artificial intelligence, Crypto Briefing reported. The plan was set out in a series of blog posts under the PQAI banner, published on November 23 and 24, 2026.
The first entry, PQAI #0, made the move to hash-based signatures a top agenda item for the Foundation, according to the outlet. Crypto Briefing also reported that the Foundation has doubled the size of its protocol security team. The Foundation’s dedicated post-quantum team was formed in January 2026, as The Quantum Insider reported when the Foundation made post-quantum security a top strategic priority.
Why elliptic-curve signatures are the target
Elliptic-curve cryptography is what lets a wallet prove it owns funds without revealing its private key. The concern is that sufficiently powerful quantum machines, or AI-driven advances in breaking cryptography, could eventually defeat that protection.
On the quantum side, the estimates have moved. Google Quantum AI researchers wrote in a March 2026 whitepaper that their circuits could run on a superconducting quantum computer with fewer than 500,000 physical qubits in a few minutes. The Quantum Insider has reported that Bitcoin, Ethereum and many major cryptocurrency rely on the elliptic curve discrete logarithm problem, the problem those circuits target. TQI’s analysis of the Bitcoin and digital asset risk covers it in more detail.
The AI threat is less defined, but it’s still a big risk. Ethereum Foundation researcher Justin Drake has gone further on timing, telling Decrypt that AI-driven math could break elliptic-curve signatures before quantum computers do.
Hash-based signatures offer a different approach to protecting wallets against these threats. Instead of relying on elliptic-curve mathematics, they use cryptographic hash functions to secure signatures. According to Crypto Briefing, this makes them a stronger candidate for post-quantum security. Ethereum.org also identifies hash-based signatures as quantum-safe because quantum computers can weaken hash functions but are not expected to break them.
What the upgrade covers
The proposed upgrade targets three parts of the network, as reported by Crypto Briefing:
- Validators: hash-based keys for consensus-layer validators, the participants who stake ETH and confirm blocks.
- Wallets: a path for users to migrate their accounts to hash-based signatures.
- Data blobs: moving blobs over to hash-based commitments.
Why Keccak-256 was picked
The second post, PQAI #1, was published on November 24 and recommended Keccak-256 as the preferred hash function, according to the outlet. The recommendation followed a competitive evaluation that also considered Poseidon and BLAKE3, among others. Keccak-256 won on the strength of its cryptanalysis record, and it is already built into Ethereum’s existing infrastructure, so developers would be working with a component they know.
Poseidon had been in play earlier in the year. Ethereum Foundation researcher Justin Drake announced on August 13 that the Foundation was dropping Poseidon in favor of more widely tested alternatives, naming SHA and BLAKE as potential replacements.
Timeline and the cost in signature size
The Ethereum Foundation’s internal deadline is December 2029, per Crypto Briefing. Ethereum.org’s Lean Ethereum roadmap also targets 2029 for full post-quantum protection. A progress review is expected in January 2027, which should provide a clearer picture of whether the planned migration milestones remain on schedule. Testing on development networks is ongoing, and Crypto Briefing reported no immediate risks of breaking changes or exploits.
Hash-based signatures are expected to be much larger than the signatures Ethereum uses today. According to Ethereum.org, they could reach roughly 3,000 bytes, compared with 96 bytes for BLS signatures. BLS also supports signature aggregation, allowing hundreds of thousands of signatures to be combined into one. No equivalent quantum-safe method currently offers the same capability.
Developers are exploring alternative aggregation methods, including approaches based on zero-knowledge virtual machines (zkVMs). Ethereum’s Post-Quantum team is developing a SNARK-based approach using a minimal zkVM called leanVM to compress multiple signatures into a smaller proof that nodes can verify.
The larger signatures could also raise the cost of running a node, with smaller operators likely to feel the most pressure, according to Crypto Briefing. Wallet migration adds another challenge, since it requires coordination across the network as well as technical changes.
Different dates are in circulation for the transition. Ethereum’s roadmap targets approximately 2029 for core post-quantum infrastructure, while Justin Drake has reportedly expressed a hope to finish by December 2028; that personal target does not formally replace the roadmap. Ethlabs has proposed 2027, which would require a change in scope for the next hard fork.
Topics
Mohib Ur Rehman
Get the latest research, company news, and market intelligence every week.
MENTIONED IN THE ARTICLE
