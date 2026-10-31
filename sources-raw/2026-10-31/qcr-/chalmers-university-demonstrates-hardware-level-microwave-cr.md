---
source: "Quantum Computing Report"
prefix: qcr-
title: "Chalmers University Demonstrates Hardware-Level Microwave Crosstalk Suppression via Parasitic Capacitance Engineering"
url: "https://quantumcomputingreport.com/chalmers-university-demonstrates-hardware-level-microwave-crosstalk-suppression-via-parasitic-capacitance-engineering/"
published: 2026-10-31
chars: 3450
truncated: false
extraction: full
---

Physicists at Chalmers University of Technology have demonstrated an architectural layout method to eliminate classical microwave drive crosstalk in superconducting processors by engineering on-chip parasitic capacitances. Detailed in a preprint titled Suppressing microwave crosstalk in superconducting quantum processors by designing parasitic drive capacitances, the study challenges conventional assumptions by showing that microwave crosstalk suppression does not originate from cancelling effective exchange coupling (Jeff = 0), but from multi-path destructive interference among parasitic capacitive channels across drive lines, qubits, and tunable couplers.
In multi-qubit superconducting architectures, pulsing an XY drive line to control a target qubit induces spurious excitations and AC Stark phase shifts in neighboring victim qubits. Standard design heuristics assume that tuning a coupler to eliminate the exchange interaction (Jeff = 0) concurrently minimizes drive crosstalk. Using a test chip with two fixed-frequency floating transmons (Q1 at 4.752 GHz, Q2 at 4.658 GHz) linked via a flux-tunable grounded transmon coupler, the Chalmers team found that the cross-Rabi minimum occurred roughly 300 MHz away from the Jeff = 0 operating frequency (3.665 GHz).
| Chalmers Two-Qubit Transmon Device & Crosstalk Model Parameters |  |  | 
|---|---|---|
| Architecture Dimension | Measured / Extracted Parameter | Hardware & Modeling Role | 
| Qubit Frequencies | Q1: 4.752 GHz \| Q2: 4.658 GHz | Fixed-frequency floating transmons with ~240 MHz negative anharmonicity. | 
| Tunable Coupler | Grounded transmon (max ωc / 2π = 4.93 GHz) | Mediates static ZZ coupling and exchange interactions via flux bias. | 
| Crosstalk vs. Jeff Shift | Δf ≈ 0.3 GHz offset | Confirms cross-Rabi null occurs independently of qubit-qubit coupling cancellation. | 
| Parasitic Capacitance Scale | Cdc ≈ 18–30 aF \| Cd,victim ≈ 2–10 aF | Attofarad-scale paths whose interference dictates the crosstalk null. | 
| Off-Resonant Suppression | Pmax reduced by orders of magnitude | Suppresses unwanted state populations on victim qubits during single-qubit gates. | 
Using a time-independent Hamiltonian derived via a first-order high-frequency expansion, the authors modeled the dressed drive amplitude at the victim qubit (Θm) as a coherent sum of three distinct channels: direct drive-to-target coupling, stray drive-to-coupler capacitance (Cdc), and stray drive-to-victim capacitance (Cd,victim). Sizing these parasitic capacitances allows the direct and coupler-mediated signals to arrive at the victim qubit with opposing phases, yielding a complete destructive cancellation (Θvictim = 0).
The comparative analysis highlighted a pronounced practical advantage for floating transmons over grounded architectures. In floating configurations, the crosstalk-null frequencies for opposing drive lines shift with the same slope sign as parasitic capacitances vary, providing the lithographic leeway needed to align bidirectional nulls. In grounded transmons, the null frequencies shift in opposite directions, requiring impractically tight fabrication margins. Furthermore, because tunable couplers possess bias points where static ZZ interactions vanish, parasitic capacitances can be laid out geometrically so that the classical microwave crosstalk null aligns with the quantum ZZ null at the identical operating flux.
The preprint is available on arXiv here.
