---
source: "Quantum Computing Report"
prefix: qcr-
title: "QuTech Demonstrates Weight-Four Stabilizer Parity Checks in a Silicon Spin-Shuttling Processor"
url: "https://quantumcomputingreport.com/qutech-demonstrates-weight-four-stabilizer-parity-checks-in-a-silicon-spin-shuttling-processor/"
published: 2026-11-28
chars: 3194
truncated: false
extraction: full
---

Researchers at QuTech and the Kavli Institute of Nanoscience at Delft University of Technology, working with TNO, have demonstrated weight-four X- and Z-type quantum error-correction parity checks and five-qubit Greenberger-Horne-Zeilinger (GHZ) entanglement in a sparse silicon spin-qubit processor using coherent electron shuttling, publishing their experimental results in Nature. Fabricated in an isotopically purified 28Si/SiGe heterostructure with a four-layer Ti:Pd gate stack and an on-chip cobalt micromagnet, the device organizes a readout zone, a 15-gate shuttling bus, and four isolated quantum-dot “bus stops” hosting stationary data qubits (D1 through D4) alongside a mobile ancilla spin (A1) and a readout ancilla (R1).
| QuTech Silicon Spin-Shuttling Processor Architecture & Benchmarks |  | 
|---|---|
| Parameter / Metric | Experimental Value & Configuration | 
| Device Architecture | Sparse 5-qubit array in a 7 nm strained 28Si/SiGe quantum well with a 4-phase conveyor bus (gates C0–C14), 4 bus stops (D1–D4), and an on-chip Ti:Co micromagnet (no external magnetic field) | 
| Conveyor Shuttling Performance | 1.8 m/s conveyor transport across a 1.2 μm round-trip path (730 ns) with 97.7(1)% single-qubit shuttling fidelity and negligible (<10 kHz) residual inter-qubit exchange crosstalk | 
| Single- & Two-Qubit Fidelities | Data-qubit single-qubit X90 gate fidelities of 99.958% to 99.978% (EDSR); decoupled CZ (DCZ) two-qubit exchange fidelities of 90.1% to 95.4% across the 4 bus stops | 
| Weight-Four Parity Checks | 4.84 μs circuit duration; 72.2(6)% accuracy for ZZZZ checks and 67.0(7)% accuracy for XXXX checks (with >93% per-round retention over 35 repeated weight-two parity checks) | 
| Multi-Qubit Entanglement | 62.9(1.8)% fidelity for post-selected ⟦4, 1, 2⟧ surface-code logical state preparation; up to 76.6(1.6)% 4-qubit GHZ fidelity and genuine 5-qubit GHZ entanglement (>50% threshold) | 
Because direct charge sensing via the single-electron transistor (S1) reaches only the first bus stop, the researchers pioneered a remote-tuning protocol that shuttles a superposition-prepared ancilla spin along the conveyor to map electrostatic crosstalk and calibrate all four bus stops without local charge sensors. During multi-qubit operation at 200 mK, a four-phase traveling-wave potential shuttles the ancilla between bus stops to execute decoupled controlled-Z (DCZ) interactions with each data qubit while dynamical decoupling pulses refocus phase pickup from the micromagnet’s field gradient.
Using parity-mode Pauli spin blockade readout and quantum non-demolition (QND) initialization, the team verified genuine entanglement across all qubit combinations in the array and executed repeated stabilizer cycles up to 35 rounds. Error-budget analysis confirms that incoherent noise in the two-qubit exchange pulses accounts for the largest share of residual error rather than electron transport, indicating that sparse shuttling channels can support remote calibration of roughly 100 qubits per sensor and near-term fault-tolerant surface-code modules.
Read QuTech’s announcement here, view the Nature paper here, and access the preprint on arXiv here.
