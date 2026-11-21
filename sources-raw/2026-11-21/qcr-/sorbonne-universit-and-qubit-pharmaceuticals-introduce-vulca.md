---
source: "Quantum Computing Report"
prefix: qcr-
title: "Sorbonne Université and Qubit Pharmaceuticals Introduce VULCAN Hybrid Framework for Scalable Quantum Chemistry"
url: "https://quantumcomputingreport.com/sorbonne-universite-and-qubit-pharmaceuticals-introduce-vulcan-hybrid-framework-for-scalable-quantum-chemistry/"
published: 2026-11-21
chars: 3218
truncated: false
extraction: full
---

Researchers from Sorbonne Université (CNRS Laboratoire de Chimie Théorique) and Qubit Pharmaceuticals have introduced VULCAN (Variational Upbuilding, Layered Compression, Adaptive N-body perturbation), a hybrid quantum-classical electronic-structure framework designed to eliminate the Hamiltonian gradient-measurement bottleneck of adaptive variational quantum eigensolvers (ADAPT-VQE). Detailed in a preprint on arXiv, VULCAN combines dynamic Lie-algebraic operator pool generation, state-overlap circuit compression, active-subspace projection, and GPU-accelerated second-order perturbation theory to reach chemical accuracy with substantially lower quantum resource demands.
| VULCAN Pipeline Architecture & Benchmark Performance |  |  | 
|---|---|---|
| Pipeline Stage / Metric | Technical Mechanism | Key Benchmark Results | 
| Gradient-Free Layered Growth | Generates pool via Variational Double Bracket Flow (VDBF) commutator + 2N − 4 MCP; appends complete layers without energy-gradient screening. | Pools 4×–25× smaller than QEB (e.g., 1,480 vs. 36,456 on 32-qubit C3H6); reaches chemical accuracy at 5%–20% of batched ADAPT-VQE measurements. | 
| Overlap-Guided Compression | Prunes circuit depth by ranking operators via single-measurement state-overlap gradients against the uncompressed layer. | Cuts CNOT counts below batched ADAPT-VQE on 4 of 7 benchmarks, reaching 0.14× baseline CNOTs on stretched H10. | 
| Adaptive Subspace Projection | Projects Hamiltonian onto 2k dominant determinants guided by a perturbative stopping criterion. | Reduces required qubits by 23%–50% (e.g., 26 → 20 qubits on H2O) and Pauli terms by 60%–88%, with 40%–74% fewer CNOTs after basis optimization. | 
| Stochastic ENPT2 Post-Processing | Importance-sampled second-order Epstein–Nesbet perturbation theory on classical GPUs enables early VQE termination. | Reaches chemical accuracy in 1 layer on 26-qubit H2O (0.05% baseline measurements) and 32-qubit C3H6 (1.0 × 10−3 Ha error), where batched ADAPT-VQE fails to converge. | 
Rather than screening thousands of candidate operators via energy gradients at every iteration, VULCAN derives physically relevant excitations in seconds from a one-body Variational Double Bracket Flow (VDBF) commutator with the molecular Hamiltonian, completes them into a linearly scaling Minimal Complete Pool, and appends full layers simultaneously. To control circuit depth and register size, users can apply single-measurement state-overlap compression or project the Hamiltonian onto a compact dominant-determinant subspace before running quantum optimization.
In GPU-accelerated statevector benchmarks up to 32 qubits, VULCAN achieved chemical accuracy at 5% to 20% of the measurement cost of batched ADAPT-VQE across hydrogen chains, BeH2, and H2O, while pairing a single quantum layer with stochastic Epstein-Nesbet perturbation theory achieved chemical accuracy on 32-qubit C3H6 where batched ADAPT-VQE stalled. The authors also reported an initial proof-of-principle hardware validation on a Quantinuum System Model H2 trapped-ion processor for molecular hydrogen, measuring a ground-state energy within 1.7 × 10−3 Ha of the exact reference.
Read the full preprint on arXiv here.
