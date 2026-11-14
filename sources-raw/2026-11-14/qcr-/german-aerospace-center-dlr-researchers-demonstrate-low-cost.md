---
source: "Quantum Computing Report"
prefix: qcr-
title: "German Aerospace Center (DLR) Researchers Demonstrate Low-Cost Benchmarked-Noise Error Mitigation Across 100-Qubit IBM and IQM Processors"
url: "https://quantumcomputingreport.com/german-aerospace-center-dlr-researchers-demonstrate-low-cost-benchmarked-noise-error-mitigation-across-100-qubit-ibm-and-iqm-processors/"
published: 2026-11-13
chars: 3195
truncated: false
extraction: full
---

Researchers at the German Aerospace Center (DLR) have demonstrated an extended quantum error mitigation protocol, termed randomized benchmarked-noise zero-noise extrapolation (bnZNE), that improves expectation-value accuracy over standard digital zero-noise extrapolation (ZNE) without increasing total measurement shot budgets. Detailed in a technical preprint on arXiv, the method was validated on both the 156-qubit IBM Quantum Heron r2 (ibm_fez) and 54-qubit IQM Emerald superconducting processors across workloads reaching 100 qubits and two-qubit gate depths up to 452.
| DLR Randomized bnZNE Architecture & Cross-Platform Benchmarks |  |  | 
|---|---|---|
| Evaluation Dimension | Technical Specification | Experimental & Resource Impact | 
| Core Extrapolation Mechanism | Structure-mirroring, classically simulable benchmark circuits | Replaces idealized integer folding factors (r = 1, 3, 5) with empirical error rates ε(r) ∈ [0, 1]. | 
| IBM Heron r2 Protocol | Replaces native √X gates with equivalent-error X gates (plus entangling layer-inversion variant) | Tested on ibm_fez across 100-qubit kicked Ising (1,980 CZ gates), 50-qubit QFT, and 5-qubit Grover circuits. | 
| IQM Emerald Protocol | Stochastic replacement of native R(θ, φ) gates with X or Y gates | Tested on 54-qubit grid QPU for 30-qubit kicked Ising dynamics up to 40 Trotter steps (1,160 CZ gates). | 
| Sampling Cost Parity | 196,608 total shots per application (32 randomizations × 3 noise levels) | Allocates 1,024 shots each to application and benchmark circuits, matching standard ZNE shot budgets. | 
Standard zero-noise extrapolation inflates circuit noise by inserting redundant gate folds and extrapolating measured expectation values back to a nominal zero-noise limit. At utility scale, however, single-qubit gate errors, temporal calibration drift, and noise saturation cause the relationship between integer folding factors and physical error rates to diverge, introducing systematic bias.
To anchor the classical extrapolation step to actual hardware noise conditions, the DLR team pairs each randomized application circuit with a compiled twin that preserves the exact physical gate layout while restricting state evolution to an efficiently computable classical bitstring or identity state. By incorporating Pauli twirling, dynamical decoupling, and twirled readout error extinction (TREX) across multiple randomizations, the protocol outperformed standard ZNE across every tested single-qubit observable and two-qubit correlation decay benchmark, while showing that circuit depth plays a stronger role in mitigation accuracy than total circuit area.
The study was supported by the DLR Quantum Computing Initiative (ALQU project), the German Federal Ministry of Research, Technology and Space, and the European Union’s Horizon Europe Q-Neko program.
The full preprint is available on arXiv here, alongside the authors’ foundational bnZNE paper here and open-source code on GitHub here. Related QCR coverage of low-overhead error mitigation and detection includes LTM’s AI-QEM release on IBM Quantum Functions here and IBM’s Qiskit Paulice spacetime error-detection framework here.
November 14, 2026
