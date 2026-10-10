---
source: "Quantum Computing Report"
prefix: qcr-
title: "Quantinuum and HQS Simulate 21-Spin NMR Spectrum on 42 Qubits With 1,400+ Two-Qubit Gate Circuits"
url: "https://quantumcomputingreport.com/quantinuum-and-hqs-simulate-21-spin-nmr-spectrum-on-42-qubits-with-1400-two-qubit-gate-circuits/"
published: 2026-10-09
chars: 2529
truncated: false
extraction: full
---

Quantum hardware developer Quantinuum, in partnership with German software vendor HQS Quantum Simulations, has demonstrated an end-to-end digital Nuclear Magnetic Resonance (NMR) spectroscopy simulation on the Quantinuum System Model H2-1 trapped-ion quantum computer. The benchmark modeled the liquid-state proton NMR spectrum of 1,2-di-tert-butyl-diphosphane, a classically challenging 22-spin heteronuclear molecule containing two 31P nuclei and twenty 1H nuclei.
To map the molecular spin network onto trapped-ion hardware, the joint team applied a hardware-efficient projection of the two-phosphorus subsystem into its singlet-triplet (|S⟩, |T0⟩) subspace. This reduced the system from 22 physical spins to a 21-spin effective Hamiltonian, reducing two-qubit gate requirements per Trotter step from 69 to 20 native ZZPhase gates.
| [ Quantinuum H2-1 NMR Simulation Technical Parameters ] |  |  | 
|---|---|---|
| Parameter / Domain | Hardware Execution Metric | Operational & Circuit Function | 
| • Qubit Allocation | • 42 Qubits total (21 system + 21 ancilla) | • Ancillas dedicated to mid-circuit leakage detection gadgets. | 
| • Trotterized Time Evolution | • 70 Trotter steps (discrete time step Δt = 0.42 ms) | • Total physical evolution time: 29.4 ms. | 
| • Circuit Depth & Gate Metrics | • Maximum 2-qubit gate depth: 1,442 gates | • Native gateset: Rz, PhasedX, and parameterized ZZPhase. | 
| • Error Suppression Stack | • Echo compiling, DD, & leakage filtering | • Full-Trotter step Pauli twirling, server-side dynamical decoupling, and ancilla-assisted leakage post-selection. | 
Previous 22-qubit hardware experiments on superconducting and trapped-ion systems struggled to resolve the 3.9–4.3 ppm region of diphosphane, which contains a subtle double-peak structure requiring up to fourth-order coupled-spin correlation tracking. By maintaining high gate fidelity across all-to-all connected ionic channels and mitigating idle memory errors, the H2-1 hardware run successfully reproduced the double-peak structure with a spectral resolution of approximately 0.07 ppm.
While the authors note that classical solvers like Spinach remain more computationally efficient for routine high-field liquid-state spectroscopy today, the result validates the viability of deep digital Hamiltonian simulation workflows for zero- to ultralow-field (ZULF) NMR and solid-state materials characterization.
Review the full pre-print manuscript on arXiv here and examine vendor performance analysis in the Quantinuum Blog here.
