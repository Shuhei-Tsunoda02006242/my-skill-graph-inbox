---
source: "Quantum Computing Report"
prefix: qcr-
title: "Researchers Propose Fault-Tolerant Quantum Processor Architecture Controlled by 20 or Fewer External Wires"
url: "https://quantumcomputingreport.com/researchers-propose-fault-tolerant-quantum-processor-architecture-controlled-by-20-or-fewer-external-wires/"
published: 2026-11-28
chars: 3186
truncated: false
extraction: full
---

Researchers from the Simons Institute for the Theory of Computing at UC Berkeley, Stanford University, Google Quantum AI, the California Institute of Technology (Caltech), and Oratomic have introduced a theoretical blueprint for a universal fault-tolerant quantum processor modeled on classical central processing units. Detailed in a paper posted to arXiv, the architecture replaces per-qubit external control lines and centralized off-chip syndrome decoders with a fixed, clocked planar array in which encoded quantum data flows through hard-wired operation tiles driven by at most 20 external wires.
| Minimal-Control Fault-Tolerant Quantum Processor Specifications |  | 
|---|---|
| Architectural Dimension | Theoretical Bound & Implementation Mechanism | 
| External Control Interface | Constant ≤20 external wires (13 controlled qubits in the concrete construction; reducible to 1 via time-multiplexing), independent of physical qubit count n or logical error rate ε | 
| Chip Layout & Gate Locality | 2D square lattice (spacing 1) with two-qubit gates acting within Euclidean distance ≤√5; fixed depth-3 periodic circuit (two SWAP transport layers plus one gate layer) | 
| Fault-Tolerant Encoding | Level-l concatenated 1D measurement-free quantum computation code unrolled into 2D tiles, concatenated with a rate-1/4 classical expander program/readout code and metronome framing | 
| All-Quantum Scaling (Theorem 5.7) | n/polylog(n/ε) logical qubits with n·polylog(n/ε) time per logical gate; tolerates arbitrary initial states and static fabrication defects below threshold | 
| Classical-Wire RAQM Variant (Theorem 6.4) | Unit-density classical broadcast wires and L×L teleportation memory cells reduce logical gate time from n/polylog(n/ε) to polylog(n/ε) | 
Except for the small fixed set of interface qubits coupled to external lines, every physical qubit on the two-dimensional lattice executes the same fabrication-fixed, depth-3 sequence of swap and gate layers on each tick of a global clock, allowing arbitrary initial states to self-initialize via a program-independent startup stream. To prevent physical noise on the narrow external wire interface from corrupting incoming instructions or outgoing results, the design concatenates a classical expander code on top of a measurement-free quantum error-correcting code, decoding instructions fault-tolerantly on-chip at the logical level while using a majority-voted metronome signal to track codeword boundaries.
While the baseline local architecture incurs a linear-in-n routing delay as logical data blocks circulate along a single memory tape, partitioning storage into a two-dimensional grid of random-access quantum memory cells linked by unit-density classical broadcast wires and Bell-pair teleportation cuts per-gate time overhead to polylogarithmic scaling. The authors highlight two-dimensional semiconductor spin-qubit shuttling arrays co-integrated with cryo-CMOS electronics and merged-element transmons paired with single-flux-quantum logic as promising physical platforms for realizing such fixed-function quantum chips.
Access the technical paper on arXiv here and view BlueQubit’s summary post here.
