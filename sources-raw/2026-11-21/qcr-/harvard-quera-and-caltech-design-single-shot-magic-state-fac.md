---
source: "Quantum Computing Report"
prefix: qcr-
title: "Harvard, QuEra, and Caltech Design Single-Shot Magic State Factories for Quantum LDPC Codes with 10–40x Lower Overhead"
url: "https://quantumcomputingreport.com/harvard-quera-and-caltech-design-single-shot-magic-state-factories-for-quantum-ldpc-codes-with-10-40x-lower-overhead/"
published: 2026-11-21
chars: 2606
truncated: false
extraction: full
---

Researchers from Harvard University, QuEra Computing, Caltech, the University of Maryland, and MIT have introduced a fault-tolerant magic state factory architecture for high-rate quantum low-density parity-check (qLDPC) codes that reduces space-time resource costs by 10× to 40× compared to state-of-the-art surface-code and color-code magic state cultivation. The design pairs three-dimensional balanced-product tricycle codes, which generate parallel non-Clifford magic states via transversal controlled-controlled-Z (CCZ) gates, with four-dimensional balanced-product quadcycle codes identified through an AI-assisted algebraic search.
| Magic State Factory Performance Comparison (Circuit-Level Noise p = 10−3) |  |  |  |  | 
|---|---|---|---|---|
| Protocol & Fault Distance | Output State & Target Code | Single-Shot | \|CCZ⟩-Converted Error Rate | Expected Space-Time Volume / \|CCZ⟩ | 
| 3D–4D qLDPC Factory (f = 3) | 2 \|CCZ⟩ in [[54, 6, 6]] Quadcycle | Yes | 1.2 × 10−5 | 4.3 × 103 | 
| Surface / Color Cultivation (f = 3) | \|T⟩ in Surface / Grafted Code | No | 1.2 × 10−5 | 80.4 × 103 / 162.8 × 103 | 
| 3D–4D qLDPC Factory (f = 4) | 2 \|CCZ⟩ in [[72, 6, 8]] Quadcycle | Yes | 1.2 × 10−6 | 8.6 × 103 | 
| Surface Code Cultivation (f = 5) | \|T⟩ in Surface Code | No | 1.2 × 10−6 | 83.8 × 103 | 
| 3D–4D qLDPC Factory (f = 5) | 2 \|CCZ⟩ in [[162, 6, 14]] Quadcycle | Yes | 1.6 × 10−8 | 6.7 × 104 | 
| Color Code Cultivation (f = 5) | \|T⟩ in Grafted Color Code | No | 1.6 × 10−8 | 228.6 × 104 | 
To overcome the asymmetric distances of tricycle codes without deep syndrome-extraction cycles, the protocol uses a distance-2 repetition fan-out gadget to execute the transversal CCZ in a single Rydberg pulse, followed by a depth-1 homomorphic CNOT that teleports the nine-qubit hypergraph magic state into paired quadcycle blocks. Because quadcycle codes possess redundant metachecks in both Pauli bases, they support constant-depth single-shot state preparation and error correction while transversal X measurements of the tricycle blocks enable postselection, pushing logical error rates down to 10−9 at a physical error rate of 10−3 and yielding two disjoint |CCZ⟩ states directly inside high-rate memory blocks.
The authors also mapped the factory onto reconfigurable neutral-atom arrays, showing that the shared quasi-cyclic structure of matched tricycle-quadcycle pairs allows uniform parallel atom shuttling, overlaid CNOT teleportation, and constant-depth homomorphic extraction and Clifford feed-forward gadgets within 33 array-traversal steps.
Read the full research paper on arXiv here.
