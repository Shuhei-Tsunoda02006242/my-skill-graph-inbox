---
source: "Quantum Computing Report"
prefix: qcr-
title: "Qubit Pharmaceuticals and Sorbonne Université Develop Polynomial-Time Lie Algebra Generator Pool Construction for Quantum Chemistry"
url: "https://quantumcomputingreport.com/qubit-pharmaceuticals-and-sorbonne-universite-develop-polynomial-time-lie-algebra-generator-pool-construction-for-quantum-chemistry/"
published: 2026-11-21
chars: 2345
truncated: false
extraction: full
---

Researchers from Qubit Pharmaceuticals and Sorbonne Université (CNRS Laboratoire de Chimie Théorique) have published a peer-reviewed paper in Communications Physics introducing a polynomial-scaling algebraic framework to construct and verify Minimal Complete Pools (MCPs) for variational quantum eigensolvers (VQE). By mapping sets of Pauli operators to binary anti-commutation adjacency matrices over 𝔽2, the team proved that Lie-algebraic completeness can be certified directly via matrix rank in O(N3) time, eliminating the exponential overhead of explicitly computing nested commutators or product-group dimensions.
| Operator Pool Dimensionality Reduction Across Molecular Benchmarks |  |  |  | 
|---|---|---|---|
| Molecular System | Qubit Count (N) | Standard QEB Pool Size | Constructed MCP / Augmented Pool (MCP + Starters) | 
| LiH (R = 1.3 Å, STO-3G) | 12 qubits | 561 operators | 20 (MCP) / 34 (Augmented) | 
| H6 Chain (R = 3.0 Å, STO-3G) | 12 qubits | 561 operators | 20 (MCP) / 59 (Augmented) | 
| H8 Chain (R = 0.8 Å, STO-3G) | 16 qubits | 1,940 operators | 28 (MCP) / 174 (Augmented) | 
| H2O (6-31G basis) | 26 qubits | 15,275 operators | 48 (MCP) / 667 (Augmented) | 
For symmetry-preserving molecular Hamiltonians, the authors showed that generating pools attain a target rank of 2N − 4 while scaling linearly in qubit count rather than the O(N4) scaling of standard unitary coupled-cluster or qubit-excitation-based (QEB) pools. Because a strictly minimal pool can limit optimization directions in practice, the authors augmented the mathematically verified MCP core with physics-informed starter excitations and paired it with a batched adaptive algorithm, MB-ADAPT-VQE, as well as the fixed-ansatz non-iterative NI-DUCC-VQE method.
In GPU-accelerated statevector benchmarks on the Jean Zay supercomputer up to 26 qubits, MB-ADAPT-VQE reduced energy-evaluation overhead by up to two orders of magnitude on strongly correlated and multi-orbital molecules compared with standard QEB-based ADAPT-VQE, while NI-DUCC-VQE scaled beyond its prior 14-qubit ceiling to reach chemical accuracy on 26-qubit H2O. The authors have open-sourced the C++ and CUDA routines for rank-based MCP verification on GitHub.
Read the open-access paper in Communications Physics here, and access the open-source MCP verification code on GitHub here.
