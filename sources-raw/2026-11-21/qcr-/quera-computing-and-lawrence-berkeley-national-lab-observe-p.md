---
source: "Quantum Computing Report"
prefix: qcr-
title: "QuEra Computing and Lawrence Berkeley National Lab Observe Prethermal Dynamical Phase Transitions on 180 Qubits in Nature Study"
url: "https://quantumcomputingreport.com/quera-computing-and-lawrence-berkeley-national-lab-observe-prethermal-dynamical-phase-transitions-on-180-qubits-in-nature-study/"
published: 2026-11-21
chars: 4062
truncated: false
extraction: full
---

Researchers from the National Energy Research Scientific Computing Center (NERSC) at Lawrence Berkeley National Laboratory, QuEra Computing, Harvard University, and Boston University have published a peer-reviewed study in Nature demonstrating non-equilibrium quantum quench dynamics on arrays of up to 180 neutral-atom qubits. Using QuEra’s programmable analog neutral-atom processor Aquila via Amazon Braket alongside classical exact-diagonalization simulations on NERSC’s Perlmutter supercomputer, the team mapped far-from-equilibrium spin dynamics across one-dimensional chains of up to 52 rubidium-87 atoms and two-dimensional square lattices of up to 180 atoms.
| QuEra–NERSC Quantum Dynamics Experiment & Aquila Corpus Summary |  |  | 
|---|---|---|
| Experiment / Platform Dimension | Technical Parameters & Scale | Key Findings & Validation Metrics | 
| Quantum Hardware & Geometries | QuEra Aquila (87Rb neutral-atom array on Amazon Braket); 1D chains up to 52 atoms and 2D lattices up to 180 atoms. | Hardware-native sudden quenches up to 4 μs evolution time across detuning Δ/Ω ∈ [−4.0, 6.0] and blockade ratio Rb/a ∈ [1.2, 1.6]. | 
| Classical HPC Benchmarking | Exact diagonalization via QuEra’s open-source Bloqade.jl on NERSC’s Perlmutter supercomputer (up to N = 20 atoms, 100 μs evolution). | Validated prethermal blockade-subspace averages, site-disorder broadening (~0.1 μm), and finite-size scaling against hardware runs. | 
| 1D Prethermal & Resonance Physics | 52-atom periodic chains probing two-site correlators (⟨OZZ⟩), Hamming weights, and k-island excitation clusters. | Observed Floquet-like prethermal steady states (mean excitations scaling as N/4) and structured resonant melting at k = 2, 3 islands. | 
| 2D Dynamical Phase Transition | 2D square arrays scaling from 9, 16, and 64 atoms up to 180 atoms. | Uncovered a first-order dynamical phase transition driven by Néel-order defect proliferation, verified via a generalized Clausius–Clapeyron test. | 
| Four-Year Aquila Corpus (2023–2026) | 55 total publications surveyed (24 many-body physics, 16 optimization, 8 QML/applications, 7 benchmarking/tooling/characterization). | Demonstrations span 3 to 256 atoms (including 231-qubit MIS reduction and 108-atom reservoir learning) ahead of QuEra’s 2028 Libra system. | 
Following sudden parameter quenches from an all-ground initial state at a constant Rabi frequency of Ω/2π = 2.5 MHz, the experiments uncovered three distinct physical phenomena: long-lived Floquet-like prethermal steady states stabilized inside the Rydberg blockade subspace, structured resonant melting where prethermal order breaks down at predictable multi-excitation island resonances, and a first-order dynamical phase transition in two dimensions driven by Néel-order defect proliferation. Using a generalized Clausius-Clapeyron relation connecting the transition boundary slope to jumps in excitation density and second-neighbor correlations, the authors quantitatively verified that the two-dimensional transition sharpens with system size and lacks any counterpart in the system’s equilibrium phase diagram.
To construct and benchmark the hardware runs, NERSC researchers executed classical simulations using QuEra’s open-source Bloqade software package on Perlmutter before scaling experiments to 180 qubits on Aquila. Alongside the study, QuEra and Amazon Web Services released a four-year literature survey cataloging 55 research and application papers executed on Aquila since its November 2022 launch on Amazon Braket, spanning many-body physics, combinatorial optimization, and quantum reservoir learning ahead of QuEra’s planned fault-tolerant Libra system in 2028.
Read the Nature paper here, view the open-access preprint on arXiv here, read the joint announcement here, and explore the AWS Quantum Technologies technical blog post here. The four-year Aquila research survey is available here, and related QCR coverage of QuEra’s earlier Transversal STAR error-correction architecture with Los Alamos National Laboratory is available here.
