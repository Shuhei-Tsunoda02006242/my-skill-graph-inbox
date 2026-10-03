---
source: "Quantum Computing Report"
prefix: qcr-
title: "ORNL Develops LuGo Algorithm on Frontier Supercomputer, Reducing Quantum Circuit Gate Counts by 95% for Computational Fluid Dynamics"
url: "https://quantumcomputingreport.com/ornl-develops-lugo-algorithm-on-frontier-supercomputer-reducing-quantum-circuit-gate-counts-by-95-for-computational-fluid-dynamics/"
published: 2026-10-02
chars: 3344
truncated: false
extraction: full
---

Computational scientists at the Oak Ridge National Laboratory (ORNL) have introduced LuGo, an enhanced Quantum Phase Estimation (QPE) algorithmic framework designed to mitigate circuit-depth bottlenecks in quantum computational fluid dynamics (CFD). Developed using the Department of Energy’s (DOE) Frontier exascale supercomputer at the Oak Ridge Leadership Computing Facility (OLCF) and validated via the Quantum Computing User Program (QCUP), the algorithm achieves a greater than 95% reduction in total quantum gate operations required to solve fluid flow differential equations.
A primary bottleneck in applying the Harrow-Hassidim-Lloyd (HHL) quantum linear system solver to fluid dynamics—such as the Hele-Shaw flow equation governing viscous fluids between parallel plates—is the high circuit depth associated with conventional QPE encoding. Standard implementations for these fluid equations required approximately 2,000,000 logic gates, introducing severe noise and decoherence risks. LuGo restructures the hybrid workflow by shifting heavy initialization routines onto classical HPC nodes prior to quantum state mapping. By performing classical preprocessing on a single node of the 2-exaflop Frontier system, the team compressed the required quantum gate count down to 91,000 gates.
| [ ORNL LuGo Algorithm Benchmark & Execution Specifications ] |  |  | 
|---|---|---|
| Technical Metric / Resource | Operational Parameters & Performance | Engineering Impact & CFD Scope | 
| • Quantum Gate Compression | • Reduced from 2,000,000 to 91,000 logic gates • >95% reduction in quantum circuit depth | • Mitigates gate-induced noise and phase decoherence in QPE routines | 
| • Classical Preprocessing HPC | • OLCF Frontier (2 exaflops peak, 1 node used) • NERSC Perlmutter (113 petaflops) | • Streamlines state preparation before state encoding onto quantum registers | 
| • QPU Hardware Validation | • Quantinuum H-1 (Trapped-Ion) • IBM Marrakesh & Sherbrooke (Superconducting) • IQM Garnet & Sirius (Superconducting) | • Evaluated cross-platform QPE performance across trapped-ion and superconducting QPUs via QCUP | 
| • Peer Review & Recognition | • Published in Future Generation Computer Systems (Vol. 178, 2026) • Awarded 2026 R&D 100 Award | • Establishes scalable pre-processing baseline for fault-tolerant linear system solvers | 
The team validated LuGo across multiple commercial quantum hardware platforms provided through the DOE Quantum User Expansion for Science and Technology (QUEST) initiative. Experimental evaluations were executed on Quantinuum’s H-1 trapped-ion processor alongside IBM (Marrakesh, Sherbrooke) and IQM (Garnet, Sirius) superconducting devices. Shifting the data-transformation load to classical pre-processing provides a practical route toward executing high-dimensional fluid, aerodynamics, microfluidics, and groundwater flow simulations on early error-corrected and error-mitigated quantum processors.
Review the full laboratory release on the Oak Ridge Leadership Computing Facility Newsroom here, inspect the peer-reviewed research manuscript in Future Generation Computer Systems here, examine comprehensive academic literature via the Quantum Algorithms for CFD Review on arXiv here, and read our previous coverage on the Department of Energy’s national laboratory quantum access calls here.
