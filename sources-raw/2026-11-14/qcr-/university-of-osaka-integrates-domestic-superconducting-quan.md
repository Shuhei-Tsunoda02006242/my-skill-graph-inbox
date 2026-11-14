---
source: "Quantum Computing Report"
prefix: qcr-
title: "University of Osaka Integrates Domestic Superconducting Quantum Processors with OCTOPUS Supercomputer via SEAFOOD Platform"
url: "https://quantumcomputingreport.com/university-of-osaka-integrates-domestic-superconducting-quantum-processors-with-octopus-supercomputer-via-seafood-platform/"
published: 2026-11-14
chars: 2971
truncated: false
extraction: full
---

Researchers at The University of Osaka’s D3 Center and Center for Quantum Information and Quantum Biology (QIQB) have developed SEAFOOD (Supercomputing Entangled by Ambitious Fusion of OQTOPUS and OCTOPUS at D3C), a hybrid computing infrastructure that links the university’s OCTOPUS supercomputer with domestically built superconducting quantum processors across separate campuses. Scheduled to enter formal operation in December 2026, the platform represents the first integration of a Japanese-developed quantum computer and an on-campus supercomputer at a single academic institution in Japan.
| University of Osaka SEAFOOD Hybrid Computing Architecture |  |  | 
|---|---|---|
| System Layer | Hardware / Software Component | Operational Specification & Benchmark | 
| Classical HPC Compute | OCTOPUS supercomputer (2.293 PFLOPS, 140 nodes, 768 GB RAM/node) | Runs batch jobs using Qiskit, QURI Parts, and oqtopus-client to handle classical matrix diagonalization. | 
| Quantum Execution Layer | QIQB superconducting QPUs on Toyonaka campus (including Urchin) | Operates chips supplied by RIKEN Center for Quantum Computing (RQC), handling transpilation, pulses, and readout. | 
| Middleware & API | OQTOPUS open-source quantum cloud stack | Co-developed with Fujitsu, SEC, and TISI; routes circuit jobs and bitstrings between HPC nodes and QPUs. | 
| QSCI Proof of Concept | Four-hydrogen (H4) molecule (1,000 shots on Urchin) | Computed a ground-state energy of −2.1147334880 Hartree, matching classical CASCI reference values. | 
Simulating strongly correlated electronic structures for drug discovery and materials engineering remains computationally expensive on classical high-performance clusters, while near-term quantum processors face qubit count and noise constraints. Led by Professor Susumu Date at the D3 Center and Associate Professor Hiroshi Ueda at QIQB, the SEAFOOD architecture partitions workloads across a three-layer stack so each processor executes the mathematical routines suited to its hardware design.
In the Quantum-Selected Configuration Interaction (QSCI) demonstration, the quantum processor sampled dominant electron configurations while OCTOPUS’s high-memory compute nodes constructed and diagonalized the resulting subspace Hamiltonian. In fiscal year 2027, up to 10 research teams at The University of Osaka will receive trial access through the D3 Center’s proposal-based program to refine hybrid job scheduling ahead of broader external access via Japan’s nationwide JHPC-quantum initiative.
The project was supported by Japan’s JST Moonshot Goal 6, MEXT Q-LEAP, JST COI-NEXT, CSTI SIP, and NEDO’s Post-5G quantum-supercomputer hybrid platform program.
Official release details are available via the D3 Center PDF announcement here, the QIQB newsroom here, and EurekAlert here. The open-source OQTOPUS software stack is documented here, and the underlying QSCI methodology published in Physical Review Research is accessible here.
