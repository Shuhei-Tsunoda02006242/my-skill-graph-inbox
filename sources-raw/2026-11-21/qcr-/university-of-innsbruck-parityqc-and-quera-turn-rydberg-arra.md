---
source: "Quantum Computing Report"
prefix: qcr-
title: "University of Innsbruck, ParityQC, and QuEra Turn Rydberg Array Embeddings into Intrinsic Error-Correcting Codes"
url: "https://quantumcomputingreport.com/university-of-innsbruck-parityqc-and-quera-turn-rydberg-array-embeddings-into-intrinsic-error-correcting-codes/"
published: 2026-11-21
chars: 1813
truncated: false
extraction: full
---

Researchers from the University of Innsbruck, Parity Quantum Computing (ParityQC), and QuEra Computing have demonstrated that the auxiliary qubits required to embed arbitrary combinatorial optimization problems onto neutral-atom processors simultaneously form an intrinsic classical error-correcting code. Focusing on the Rydberg-Parity embedding, the team showed that LINK and 3BODY atomic gadgets decompose into overlapping dimer and trimer superatoms governed by an exact single-excitation Rydberg blockade rule, enabling local syndrome extraction simply by counting Rydberg excitations without additional hardware overhead.
Because number-check syndromes produce a strictly nonlinear code incompatible with standard linear decoders, the authors developed an iterative Cluster decoder that groups violated superatoms into local clusters, resolves unique gadget configurations via lookup tables against frozen boundary atoms, and dynamically expands and merges unresolved clusters. Under an independent bit-flip noise model, the co-designed Rydberg-Parity code and Cluster decoder achieved error-correction thresholds of 27.5% on complete graphs and 26.3% on bipartite graphs, and generalized directly to crossing-lattice (23.5% threshold) and 3D quantum-wire (24.1% threshold) embeddings.
Validated on experimental adiabatic optimization runs from QuEra’s Aquila processor across complete and bipartite QUBO instances up to 107 atoms, the Cluster decoder consistently outperformed both raw hardware readouts and standard GreedyMIS post-processing. On the largest 107-atom bipartite layouts, the decoder recovered exact optimal solutions at an average success rate exceeding 8% in regimes where both raw hardware measurements and GreedyMIS found zero valid solutions.
Read the full research paper on arXiv here.
