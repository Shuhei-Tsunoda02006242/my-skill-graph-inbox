---
source: "Quantum Computing Report"
prefix: qcr-
title: "IQM Verifies Full-Chip Entanglement Across 54-Qubit Emerald Superconducting Processor"
url: "https://quantumcomputingreport.com/iqm-verifies-full-chip-entanglement-across-54-qubit-emerald-superconducting-processor/"
published: 2026-10-31
chars: 1780
truncated: false
extraction: full
---

IQM Quantum Computers (Nasdaq: IQMX) has demonstrated simultaneous Greenberger–Horne–Zeilinger (GHZ) state entanglement across all 54 transmon qubits of its cloud-accessible IQM Emerald processor. The achievement validates full-lattice coherence on commercial hardware where users previously operated within ~30-qubit active partitions. The milestone builds on the company’s autonomous tuning initiatives reported in QCR’s previous coverage of IQM’s agentic calibration with NVIDIA Ising.
| IQM Emerald Full-Chip Entanglement Benchmarks |  |  | 
|---|---|---|
| System Scale | Mitigation Protocol | Measured State Fidelity | 
| 40 Qubits | Raw (Unmitigated) | 0.515 (Exceeds genuine multipartite entanglement threshold of 0.500) | 
| 54 Qubits (Full Chip) | Readout Error Mitigation (REM) | 0.516 (> 0.500 classical boundary separating entanglement from separable noise) | 
| Processor Topology | 54 Transmons in Square Lattice | Native two-qubit CZ gates enabled by tunable couplers | 
The state preparation relied on an automated scheduling compiler that balances individual two-qubit CZ gate fidelities against cumulative qubit idling times, cutting overall processor error rates by up to 50% alongside dynamical decoupling. While exceeding the 0.500 threshold confirms genuine multipartite entanglement across the full register, the narrow fidelity margin highlights the steep scaling challenge of deep circuit execution on unencoded physical QPUs. Maintaining full-chip coherence will require further gate-speed optimizations and continuous calibration to prevent localized cross-talk from degrading algorithmic sampling.
Technical details are available in the official IQM Announcement here, with architecture specifications detailed on the IQM Emerald Platform Portal here.
