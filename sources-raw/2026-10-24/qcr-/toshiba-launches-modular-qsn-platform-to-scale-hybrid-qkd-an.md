---
source: "Quantum Computing Report"
prefix: qcr-
title: "Toshiba Launches Modular QSN Platform to Scale Hybrid QKD and PQC Across Lit Fiber Networks"
url: "https://quantumcomputingreport.com/toshiba-launches-modular-qsn-platform-to-scale-hybrid-qkd-and-pqc-across-lit-fiber-networks/"
published: 2026-10-24
chars: 4832
truncated: false
extraction: full
---

Toshiba Corporation (TYO: 6502) has launched its carrier-grade Quantum-Safe Networking (QSN) Platform, introducing a modular hardware and software architecture engineered to scale quantum-secured communications across telecommunications, enterprise, and data center infrastructures. The platform shifts quantum key deployment away from rigid, expensive point-to-point dark-fiber connections toward dynamic, multi-tenant optical topologies.
Designed to mitigate “Harvest Now, Decrypt Later” (HNDL) cyber risks across critical infrastructure, the QSN Platform integrates hardware-level Quantum Key Distribution (QKD) and Quantum Random Number Generation (QRNG) with algorithmic Post-Quantum Cryptography (PQC). By incorporating active optical switching and dense wavelength-division multiplexing (DWDM), the architecture allows quantum channels to coexist with high-capacity classical data traffic on standard lit optical fiber.
| [ Toshiba Quantum-Safe Networking (QSN) Architecture & Component Matrix ] |  |  | 
|---|---|---|
| Hardware / Software Layer | System Component | Operational Role & Technical Function | 
| • Optical Routing & Multiplexing | • QSN Hub 1550/1310 | • Employs active optical switching to connect a single central hub to hundreds of remote sites, eliminating dedicated point-to-point hardware stacks. | 
|  | • QSN Multiplexer | • Multiplexes quantum signals (1550 nm or 1310 nm) and QKD service channels onto active, third-party DWDM lit fiber, bypassing dark-fiber requirements. | 
| • Node & Endpoint Hardware | • QSN Transceiver 1550/1310 | • Combines a Quantum Transmitter (QTx) and Quantum Receiver (QRx) inside a single unified chassis for core network links and key relaying. | 
|  | • QSN Spoke & QSN Link | • Compact, low-footprint endpoints for remote branch sites and dedicated high-performance point-to-point links. | 
| • Cryptographic & Key Management | • QSN Key Delivery System (KDS) | • Appliance-integrated software layer delivering QKD, PQC, and hybrid key materials with automated dynamic re-routing. | 
|  | • QSN Key Management System (Q-KMS) | • Standalone x86 software engine providing network-wide key lifecycle management, security policies, and cryptographic auditing. | 
|  | • QSN Controller | • Centralized Software-Defined Networking (SDN) interface delivering live topology mapping, link performance telemetry, and automated provisioning. | 
Addressing Dark Fiber Constraints and Hardware Sprawl
A primary bottleneck in scaling quantum communication has been the operational overhead of point-to-point QKD. Conventional deployments demand dedicated pairs of transmitter and receiver units for every point-to-point link, often requiring costly dedicated dark fiber to prevent classical photon bleed from swamping single-photon quantum detectors.
Toshiba’s platform addresses these economics through optical concentration. The QSN Hub uses active optical switching to allow a single central terminal to service hundreds of client nodes (QSN Spokes) across hub-and-spoke, ring, or mesh topologies. Concurrently, the QSN Multiplexer provides advanced optical filtering, enabling quantum signals to travel alongside multi-terabit classical DWDM channels without performance degradation.
The control plane is managed via an integrated, crypto-agile software stack. The Key Delivery System (KDS) routes hybrid key material combining physical QKD key streams with NIST-standardized PQC algorithms, providing defense-in-depth protection in compliance with evolving government mandates across North America, EMEA, and APAC.
Enterprise Validation: Securing IPsec VPNs with HPE and SpeQtral
Highlighting the platform’s real-world integration, Toshiba Asia Pacific recently partnered with Singapore quantum communications firm SpeQtral and Hewlett Packard Enterprise (HPE) to demonstrate a validated quantum-safe enterprise networking solution.
Showcased at GovWare 2026 in Singapore, the implementation integrated Toshiba’s QSN Platform directly with HPE Networking SRX Next Generation Firewalls via SpeQtral’s key orchestration software. The configuration injects hybrid QKD and PQC key material into standard enterprise IPsec VPN tunnels, securing inter-data-center and branch communications without requiring enterprises to re-architect existing IP network infrastructure.
Toshiba, which chairs the ETSI Industry Specification Group on Quantum Key Distribution, confirmed that the QSN Platform is currently being rolled out to commercial telecommunications operators, defense contractors, and cloud service providers globally.
Review the commercial product release via the Toshiba Global Newsroom here, examine the enterprise architecture overview on the Toshiba Quantum Solutions Portal here, and read the HPE/SpeQtral deployment announcement on the Toshiba Asia Pacific Portal here.
