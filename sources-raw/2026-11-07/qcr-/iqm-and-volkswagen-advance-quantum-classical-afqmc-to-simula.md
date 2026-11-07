---
source: "Quantum Computing Report"
prefix: qcr-
title: "IQM and Volkswagen Advance Quantum-Classical AFQMC to Simulate Next-Generation Battery Chemistry"
url: "https://quantumcomputingreport.com/iqm-and-volkswagen-advance-quantum-classical-afqmc-to-simulate-next-generation-battery-chemistry/"
published: 2026-11-06
chars: 3677
truncated: false
extraction: full
---

European quantum hardware manufacturer IQM Quantum Computers (Nasdaq: IQMX) and Volkswagen Group Innovation have demonstrated algorithmic and experimental advances in Quantum-Classical Auxiliary-Field Quantum Monte Carlo (QC-AFQMC), reducing the classical post-processing runtime scaling of the hybrid electronic structure algorithm by an order of magnitude. Detailed in a technical study titled Quantum-Classical Auxiliary-Field Quantum Monte Carlo at the Edge of Practicability, the collaboration achieved up to a 124× reduction in classical execution time for a 50-orbital benchmark and validated the workflow on IQM’s commercial Emerald superconducting processor.
| QC-AFQMC Algorithmic & Experimental Benchmarks |  |  | 
|---|---|---|
| Computational Dimension | Previous Implementation Baseline | IQM & Volkswagen Demonstration | 
| Per-Step Classical Scaling | Õ(N5.5) via standard shadow interpolation | Õ(N4.5) using Aitken’s block transformation on singular Pfaffians and automatic differentiation for force bias. | 
| Classical Time-to-Solution Speedup | Years on large clusters for ≥ 50 orbitals | Up to 124× speedup at 50 orbitals; up to 248× estimated speedup at 100 orbitals. | 
| Experimental Hardware Validation | Unmitigated small toy models | Ground-state calculation of stretched H8 on IQM Emerald using MPS-based tensor-network error filtering. | 
| Industrial Materials Benchmark | ≤ 20 qubits for active-space models | 40-qubit simulation of Li2O4 lithium superoxide dimer rearrangement (26 electrons in 20 orbitals). | 
Simulating complex chemical reactions—such as the intermediate stages of lithium-air battery cycles—presents severe challenges for classical electronic structure methods due to the exponential growth of Slater determinants needed to capture strong electron correlation. Standard classical phaseless AFQMC (ph-AFQMC) mitigates sign problems by projecting random walks against a trial wavefunction; however, the method incurs systematic bias if that trial state cannot accurately represent multi-reference character. While QC-AFQMC leverages a quantum computer to prepare high-fidelity multi-determinant trial states, calculating the overlaps between the quantum trial state and classical Monte Carlo walkers has historically created a prohibitive computational bottleneck.
Rather than using deep modified Hadamard test circuits (which the authors estimate would require millenia of execution time for even modest systems), the team utilized matchgate shadow tomography to reconstruct state overlaps via classical post-processing. By applying Aitken’s block transformation to resolve the singular Pfaffians that naturally arise in matchgate shadow kernels, the researchers reduced per-snapshot overlap evaluation from O(N4) to O(N3). Combined with algorithmic differentiation for Jacobian-vector products in the force bias calculations, the overall per-step classical post-processing dropped from Õ(N5.5) to Õ(N4.5).
To validate the workflow against physical hardware noise, the team calculated the ground-state energy of an H8 hydrogen chain on the 54-qubit IQM Emerald processor, applying matrix product state (MPS) filtering to discard noisy measurements. The researchers then scaled the methodology in classical simulation to model the rearrangement pathway of a lithium superoxide dimer (Li2O4) across a 40-qubit active space, accurately capturing the activation barrier and transition-state geometry governing battery charge/discharge mechanisms.
Technical whitepaper summaries are accessible on the IQM Case Study Portal here and the Direct Whitepaper Document here, with the full peer-reviewed preprint available on arXiv here.
