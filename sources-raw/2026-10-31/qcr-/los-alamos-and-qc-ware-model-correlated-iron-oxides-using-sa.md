---
source: "Quantum Computing Report"
prefix: qcr-
title: "Los Alamos and QC Ware Model Correlated Iron Oxides Using Sample-Based Quantum Diagonalization on IBM Hardware"
url: "https://quantumcomputingreport.com/los-alamos-and-qc-ware-model-correlated-iron-oxides-using-sample-based-quantum-diagonalization-on-ibm-hardware/"
published: 2026-10-31
chars: 2993
truncated: false
extraction: full
---

In a preprint titled Towards Quantum Computation of Bulk FeO, researchers from Los Alamos National Laboratory (LANL) and QC Ware present a hybrid workflow simulating strongly correlated transition metal oxides on quantum processors. Benchmarked on diatomic iron monoxide (FeO) and rhombic iron oxide dimers (Fe2O2), the team coupled ab initio-informed d–p tight-binding models with Sample-based Quantum Diagonalization (SQD) on IBM Quantum’s ibm_miami system, using near-term hardware purely as a Fock-space sampler to reach chemical accuracy where standalone Variational Quantum Eigensolver (VQE) optimizations stall.
| LANL / QC Ware Correlated Electronic Structure Benchmarks |  |  | 
|---|---|---|
| System Dimension | FeO Diatomic Molecule | Fe2O2 Rhombic Dimer | 
| Active Space & Qubit Footprint | 12 electrons in 16 spin orbitals (16 qubits) | 24 electrons in 32 spin orbitals (32 qubits) | 
| Hardware Multiplexing ( ibm_miami) | 6 parallel instances across 96 qubits | 3 parallel instances across 96 qubits | 
| Ansatz Architecture | 1-layer LUCJ (120 variational parameters) | 1-layer LUCJ (496 variational parameters) | 
| Raw VQE Performance | Residual error ΔE ≈ 173 meV (exceeds 43 meV limit) | Trapped in nonlinear variational parameter manifold | 
| SQD Post-Processing | Ground doublet recovered in 184 determinants (< 43 meV) | Chemical accuracy achieved via 1-shell expansion | 
| Physical State Recovered | Experimental quintet (5Δi); ΔEexc ≈ 2,167 cm−1 | Nonet magnetic ground state (MS = 4 sector) | 
Bulk FeO is an archetypal Mott insulator whose strong electronic correlations cause conventional density functional theory (DFT) to mischaracterize it as metallic. To make these open-shell systems computationally tractable, the authors extracted localized Wannier functions from non-spin-polarized DFT calculations to build multi-orbital d–p Hamiltonians. Variational states were parameterized using a one-layer Local Unitary Cluster Jastrow (LUCJ) ansatz, which restricts two-mode Givens rotations to nearest-neighbor connectivity to eliminate non-local SWAP overheads.
To bypass on-hardware barren plateaus, circuit parameters were optimized in classical statevector simulations and deployed to frozen QPUs strictly for configuration sampling. Measured bitstrings post-selected for particle-number conservation were then expanded into one- and two-shell Fock-space graphs based on non-zero Hamiltonian matrix elements. Classical exact diagonalization of the resulting projected Hamiltonian converged rapidly: two connectivity shells recovered the experimental 5Δi quintet state for FeO within a compressed subspace of 184 determinants, yielding an excitation energy of 2,167 cm−1 (substantially outperforming prior multireference configuration interaction baselines that predicted 300 cm−1). The methodology establishes a blueprint for modeling bulk periodic FeO by distributing SQD sub-blocks across Brillouin zone k-points.
The preprint is accessible on arXiv here.
