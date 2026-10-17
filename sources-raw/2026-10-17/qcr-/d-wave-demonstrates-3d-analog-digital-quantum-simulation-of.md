---
source: "Quantum Computing Report"
prefix: qcr-
title: "D-Wave Demonstrates 3D Analog-Digital Quantum Simulation of Higher-Order Topological Insulators Using 728 Qubits"
url: "https://quantumcomputingreport.com/d-wave-demonstrates-3d-analog-digital-quantum-simulation-of-higher-order-topological-insulators-using-728-qubits/"
published: 2026-10-17
chars: 3096
truncated: false
extraction: full
---

In a research study published on arXiv, scientists at D-Wave Quantum (Pratik Sathe, Andrew D. King, and collaborators) have demonstrated the realization and characterization of 1D, 2D, and 3D higher-order topological insulators (HOTIs) on an Advantage2 superconducting quantum annealing processor using up to 728 qubits.
Detailed in the paper (“Measuring higher-order bulk topology in a programmable quantum simulator“), the team deployed new analog-digital quantum control protocols to measure localized boundary modes and extract 3D bulk topological invariants via band projector tomography.
| [ Experimental Performance & Topological Benchmark Comparison ] |  |  |  | 
|---|---|---|---|
| Topological Model / Dimension | Qubit Count / Setup | Boundary Measurement (LDOS) | Bulk Topological Invariant | 
| • 1D SSH Model | • 64 Qubits (L = 32 Chain) | • In-Gap Fractional End Modes | • Zak Phase (γ = π) | 
| • 2D BBH Quadrupole Insulator | • 364 Dimers (L = 13 Skew) | • Localized Zero-D Corner Modes | • 2D Quadrupole Moment (pxy = 1/2) | 
| • 3D BBH Octupole Insulator | • 432 Qubits (3x3x3 Lattice) | • Gapped Bulk/Face/Hinge + Corners | • 3D Octupole Moment (1/2) | 
Analog-Digital Control Protocols & Dimerized 3D Lattices
Traditional quantum annealing applications rely on slow global quenches or static ground-state sampling. D-Wave’s new analog-digital architecture combines pulse-level state initialization, coherent static Hamiltonian evolution, and high-frequency time-series measurements:
- Qubit Dimerization: To embed dense 2D and 3D connectivity onto the processor graph, physical qubits were paired into strongly coupled dimers (Jd = 2.5 GHz, Δ = 3.0 GHz), acting as effective two-level systems to realize Benalcazar-Bernevig-Hughes (BBH) tight-binding models.
- Complex Wavefunction Tomography: By time-shifting σrx(t) measurements by 1/(4Δ) = 125 ps, the system reconstructed the complex-valued propagator Ψr(t) = σrx(t) + iσry(t) with a temporal resolution of δt = 62.5 ps.
- First Experimental Extraction of 3D Bulk Topology: By calculating three successive nested Wilson loops from experimentally reconstructed occupied-band projectors {Pν(k)}, the team measured the quantized 3D electric octupole moment (1/2 invariant), verifying the bulk-boundary correspondence in a 3D quantum simulator.
- Fractionalized Charge Deficits: Ingesting real-space return amplitudes into local density of states (LDOS) integrals revealed fractionalized charge deficits (≈ 1/2) localized at zero-dimensional corner modes.
- Insensitivity to Local Disorder: Bootstrapping over physical lattice symmetries proved that the bulk topological invariants remain quantized near 1/2 even without enforcing ideal spatial symmetries, demonstrating topological protection against mild hardware disorder.
The demonstration confirms that analog-digital quantum annealing hardware can serve as a programmable simulator for multi-dimensional condensed matter physics and non-interacting topological materials.
Review Andrew King’s summary on LinkedIn here and inspect the technical manuscript on arXiv here.
