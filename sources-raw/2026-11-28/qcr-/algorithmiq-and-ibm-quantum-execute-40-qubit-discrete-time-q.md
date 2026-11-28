---
source: "Quantum Computing Report"
prefix: qcr-
title: "Algorithmiq and IBM Quantum Execute 40-Qubit Discrete-Time Quantum Walks on Biological Networks"
url: "https://quantumcomputingreport.com/algorithmiq-and-ibm-quantum-execute-40-qubit-discrete-time-quantum-walks-on-biological-networks/"
published: 2026-11-28
chars: 2984
truncated: false
extraction: full
---

Researchers at Algorithmiq and IBM Quantum have demonstrated discrete-time quantum walks (DTQWs) on irregular protein-protein interaction (PPI) networks using up to 40 qubits on superconducting hardware, publishing their experimental results in npj Quantum Information. Conducted within the Healthcare and Life Sciences Quantum Working Group, the study addresses a longstanding bottleneck in gate-based quantum walk algorithms, where conventional dense encodings require deep multi-controlled gate sequences that exceed the coherence limits of pre-fault-tolerant processors.
| Algorithmiq & IBM Quantum Biological Network DTQW Benchmarks |  | 
|---|---|
| Biological Subgraph (BioPlex 3.0) | Hardware, Circuit Depth & Experimental Fidelity | 
| Graph 1: 11 Nodes, 12 Edges (Asthma PPI motif; diameter 6) | 24 qubits on IBM Heron R2 ( ibm_kingston); 165 CZ gates/step (223 entangling layers at 7 steps); postselected Hellinger fidelity FH ≥ 0.95 (FHBC ≥ 0.71) | 
| Graph 2: 15 Nodes, 18 Edges (Asthma PPI motif; diameter 8) | 36 qubits on IBM Heron R3 ( ibm_pittsburgh); 286 CZ gates/step (264 entangling layers at 7 steps); postselected Hellinger fidelity FH ≥ 0.90 (FHBC ≥ 0.46) | 
| Graph 3: 17 Nodes, 20 Edges (Asthma PPI motif; diameter 8) | 40 qubits on IBM Heron R2 ( ibm_kingston); 322 CZ gates/step (287 entangling layers at 7 steps); postselected Hellinger fidelity FH ≥ 0.87 (FHBC ≥ 0.54) | 
| Algorithmic Architecture | 2\|E\|-qubit single-excitation (Hamming-weight-1) encoding, domain-wall basis rotation for degree ≤3 Grover coins, √iSWAP shift gates, and symmetry postselection | 
| Gene Prioritization Case Study | 9-step walk seeded at HLA-DQA1 ranked non-local asthma risk gene FLVCR1 4th via Quantum Interference Index (vs. 7th in PageRank and 9th in DIAMOnD) | 
Instead of compressing walker positions into logarithmic registers, the team mapped directed graph edges into a sparse single-excitation (Hamming-weight-1) subspace requiring twice as many qubits as undirected edges. Combining domain-wall basis rotations for local Grover coin operators with partial-swap shift gates cut two-qubit circuit depth by roughly two orders of magnitude on heavy-hex topologies, while symmetry-respecting postselection filtered out measurement bitstrings outside the single-excitation sector.
In a proof-of-principle biomedical application, the researchers extended the 11-node experiment to nine walk steps initialized at the asthma-associated seed gene HLA-DQA1 and scored nodes using a Quantum Interference Index comparing quantum and classical random-walk probability distributions. Alongside adjacent markers HLA-C, PON2, and HLA-G, constructive amplitude interference elevated the non-adjacent asthma susceptibility gene FLVCR1 to fourth place, outranking classical network baselines such as PageRank and DIAMOnD.
Read the open-access paper in npj Quantum Information here, view Algorithmiq’s announcement here, and access the circuit-construction code on Figshare here.
