---
source: "The Quantum Insider"
prefix: tqi-
title: "Quantus Launches a Quantum-Secure Cold Wallet That Runs on Any Spare Phone"
url: "https://thequantuminsider.com/2026/11/20/quantus-quantum-secure-cold-wallet-spare-phone/"
published: 2026-11-20
chars: 4528
truncated: false
extraction: full
---

Insider Brief
- Quantus has released an open-source mobile cold wallet that turns a spare smartphone into an air-gapped device for storing and signing cryptocurrency transactions.
- The app uses smartphone security chips to store keys, supports ML-DSA post-quantum digital signatures and displays transaction details before users approve them.
- The wallet currently supports QTC, the native token of the Quantus network, with QR-code transfers between the offline device and a separate internet-connected phone or computer.
PRESS RELEASE — Quantus has released the Quantus Cold Wallet, an open-source mobile app that converts any spare smartphone into an entirely air-gapped, offline crypto wallet. The launch aims to eliminate the hidden vulnerabilities of traditional hardware wallets, which frequently expose buyers to both digital supply-chain tampering and physical home-address leaks.
The Quantus Cold Wallet installs on any phone, so nobody knows in advance which handset will hold the keys. During setup, users permanently disable all Wi-Fi and mobile data capabilities, and the app refuses to sign anything if a network connection is active.
The wallet also doesn’t look like a wallet. A hardware wallet tells anyone who finds it that its owner holds crypto, whether it sits on a desk or turns up during a robbery. A spare phone in a drawer gives nothing away.
Users can run the wallet from a second, everyday phone or a laptop. The two devices never connect. To send money, the everyday phone shows the transaction as a QR code, which the offline phone scans.
“We were not satisfied with the state of affairs in crypto where even large institutions regularly blind sign. They can’t verify what they’re signing,” said Nikolaus Heger, CTO of Quantus. “Modern phones have secure elements that can keep a secret safe even when the device is lost. So we decided to implement our own cold wallet; a phone always disconnected from the internet is very secure.”
The offline app natively decodes the payload and shows the exact transaction amount and destination address in plain text. This prevents “blind signing,” when users approve transactions they cannot read.
A phone also has far more computing power than a hardware wallet. Most hardware wallets lack the memory to handle zero-knowledge (zk) transactions, which use cryptographic proofs to confirm a payment without revealing its details. A smartphone can process them.
Keys are stored in the security chip built into modern iPhones and Android phones. The wallet signs transactions with ML-DSA, a post-quantum standard approved by the U.S. National Institute of Standards and Technology (NIST) to resist attacks from future quantum computers.
Quantus originally built the wallet for internal use. At launch, it supports QTC, the native token of the Quantus network, and developers can also sign transactions from a laptop with a command-line tool.
“Most people never think about all the ways a hardware wallet can be attacked, but by now every one of them has been used in the wild,” said Christopher Smith, co-founder and CEO of Quantus. “A phone you can buy in any shop, a device that doesn’t attract attention, that never goes online and shows you exactly what you are approving, that device closes off the attacks that have cost people the most.”
One of those attacks surfaced this month when Ledger confirmed that devices sold through CryptoBilis, a reseller in Southeast Asia, had been intercepted. Attackers installed physical implants in the hardware to read owners’ 24-word recovery phrases directly from the screens and silently transmit them over mobile networks.
Even an untampered device leaves a trail, because the shipping label ties the buyer’s name to their home address. Leaked personal records have been linked to “wrench attacks,” in which criminals use violence to force crypto holders to hand over their funds. In France, a tax official was detained in 2025 on suspicion of selling crypto holders’ home addresses to criminal networks.
Blind signing has proved just as costly. It was exploited in the $1.5 billion Bybit exchange hack, where staff approved a malicious transaction that looked routine on a compromised screen.
The Quantus Cold Wallet is free to download now from the App Store and Google Play. Users need only a spare phone to get started. More information, including a step-by-step setup guide, is available here.
Mohib Ur Rehman
Get the latest research, company news, and market intelligence every week.
MENTIONED IN THE ARTICLE
