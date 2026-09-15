---
source: "Quantum Computing Report"
prefix: qcr-
title: "QC Design Integrates Plaquette Platform with NVIDIA CUDA-Q Logical for Hardware-Realistic FTQC Simulation"
url: "https://quantumcomputingreport.com/qc-design-integrates-plaquette-platform-with-nvidia-cuda-q-logical-for-hardware-realistic-ftqc-simulation/"
published: 2026-09-15
chars: 2775
truncated: false
extraction: full
---

Fault-tolerant quantum design automation developer QC Design has announced an integration between its flagship platform, Plaquette, and NVIDIA CUDA-Q Logical. Announced on September 14, 2026, the integration connects high-level quantum error correction (QEC) circuit compilation with device-specific physical noise models, enabling hardware engineering teams to simulate lattice surgery and logical gate protocols under realistic, physics-based error channels.
The joint workflow addresses a systematic discrepancy in fault-tolerant quantum computing (FTQC) resource estimation: traditional QEC compilation tools rely on idealized Clifford assumptions and simplified Pauli noise approximations, which obscure the operational impact of complex physical device dynamics. By interfacing Plaquette’s physical simulation samplers—including its proprietary XPauli and near-Clifford engines—with CUDA-Q Logical’s extensible compilation layer, developers can evaluate compiled QEC code structures under continuous non-Pauli noise models, such as multi-state leakage, coherent over-rotations, and shuttling-induced decoherence.
| [ QC Design Plaquette & NVIDIA CUDA-Q Logical Integration Parameters ] |  |  | 
|---|---|---|
| Simulation Layer | Hardware Noise & Physics Modeling | CUDA-Q Logical Software Function | 
| QEC Protocol & Geometry | • Surface Code & Lattice Surgery CX Gates • Hardware-Specific Kraus Operators & Channels | • High-Level Logical Workload Expression • Standardized Code & Gadget Compilation | 
| Physical Noise Dynamics | • 0.2% Two-Qubit Entangling Gate Leakage • Multi-State Leakage & Coherent Over-Rotations | • Integrated Error Accounting & Placement • Automated Pipeline-Level Noise Injection | 
| Operational Benchmark Impact | • 60% Reduction in Circuit Noise Threshold • Non-Pauli Threshold Shift Quantification | • Data-Backed Physical-to-Logical Resource Estimates • Cross-Platform Hardware Architecture Verification | 
In an initial verification study, QC Design modeled a lattice-surgery CX gate between two surface-code logical qubits subject to multi-state leakage dynamics. The simulation demonstrated that introducing a 0.2% leakage rate on physical two-qubit entangling gates degraded the fault-tolerant circuit noise threshold by approximately 60%. The outcome quantifies how unmitigated physical imperfections alter theoretical code thresholds, providing a data-backed baseline for hardware manufacturers to allocate error budgets and validate FTQC deployment roadmaps.
Review the news release via QC Design here, examine the underlying physics engine via arXiv here, and read our prior coverage of QC Design’s Plaquette Hardware-Aware Simulation Framework here and Gauge Theoretical Error-Correction Benchmarking here.
September 14, 2026
