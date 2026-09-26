---
source: "Quantum Computing Report"
prefix: qcr-
title: "ETSI Identifies Technical Limitations and Implementation Vulnerabilities in Quantum Random Number Generators (ETSI TR 104 171)"
url: "https://quantumcomputingreport.com/etsi-identifies-technical-limitations-and-implementation-vulnerabilities-in-quantum-random-number-generators-etsi-tr-104-171/"
published: 2026-09-26
chars: 2635
truncated: false
extraction: full
---

The European Telecommunications Standards Institute (ETSI) Technical Committee Cyber Security (TC CYBER) has released a Technical Report, ETSI TR 104 171 (Implementation Guidelines for Quantum Random Number Generators). The document addresses a key vulnerability in quantum cybersecurity: while quantum physical processes are non-deterministic, practical hardware implementations, detector dead times, thermal noise, and side-channel leakage can reintroduce predictability into Quantum Random Number Generator (QRNG) outputs if not properly audited and conditioned.
The report establishes guidelines spanning the complete QRNG lifecycle, including physical modeling of the Quantum Entropy Source (QES), real-time conditional min-entropy estimation, randomness extraction (using seeded Toeplitz hashing or multi-source extractors), operational health monitoring, and physical tamper resistance. To mitigate side-channel vectors—such as optical injection “blinding” attacks, RF electromagnetic interference, and power-analysis probing—ETSI introduces the Entropy Zero Trust (EZT) framework. Under EZT, every stage of the entropy pipeline is treated as untrusted and subject to continuous hardware verification, runtime attestation, and cryptographic signing.
| [ ETSI TR 104 171 Framework & Classification Matrix ] |  |  | 
|---|---|---|
| Standardization Domain | Core Requirement & Engineering Controls | Classification & Metrics | 
| Entropy Zero Trust (EZT) | • Layered verification across QES, hardware RoT, drivers, and API • Hardware Root of Trust (TPM/eFuse) for boot attestation | • TL-0: Raw unverified source • TL-2: EZT-compliant platform • TL-3: Critical/military grade | 
| Side-Channel Defense | • Optical isolators against photodetector blinding • EMI/magnetic shielding and voltage regulation monitoring | • Active power/voltage fault monitoring • Continuous statistical sampling (≥1 Hz) | 
| SWaP & Performance | • Common command interface & op-codes for control plane • PQC + QRNG integration architectures | • Throughput: Class I (≤100k) to Class V (≥1G) • Power: Class A (≤100mW) to Class D (2-10W) | 
Chaired by Mark Pecen (ETSI TC Quantum), the committee outlined priorities for subsequent normative Technical Specifications, including standardized API command sets, logging protocols, Common Criteria/FIPS 140-3 alignment, and integration models pairing certified QRNG entropy pools with post-quantum cryptography (PQC) standards such as ML-KEM and ML-DSA.
Review the press release via ETSI Newsroom here and download the complete publication via the ETSI TR 104 171 Standard Document PDF here.
September 26, 2026
