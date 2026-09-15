---
source: "Quantum Computing Report"
prefix: qcr-
title: "IQM Adopts NVIDIA CUDA-Q Logical Framework to Drive Open-Architecture Fault-Tolerant System Benchmarking"
url: "https://quantumcomputingreport.com/iqm-adopts-nvidia-cuda-q-logical-framework-to-drive-open-architecture-fault-tolerant-system-benchmarking/"
published: 2026-09-15
chars: 2744
truncated: false
extraction: full
---

Superconducting quantum computer manufacturer IQM Quantum Computers has adopted NVIDIA CUDA-Q Logical as a primary logical orchestration layer within its full-stack hardware environment. Announced at IEEE Quantum Week 2026, the integration connects CUDA-Q’s open-source fault-tolerant compilation stack to IQM’s on-premises Halocene quantum error correction (QEC) product line, decoupling high-level logical algorithm benchmarking from proprietary vendor-specific control software and low-level FPGA firmware.
By standardizing high-level logical circuit descriptions within CUDA-Q Logical, the compilation layer allows QEC algorithm workloads—ranging from high-rate qLDPC codes to planar surface codes—to be compiled, benchmarked, and executed across heterogeneous physical backends without altering underlying operational metrics. The integrated stack provides auditable multi-layer resource estimates, quantifying runtime overhead across decoding latency, inter-component quantum interconnect transport, and control electronics bandwidth. On the hardware layer, IQM’s 150-qubit Halocene system pairs square-lattice superconducting QPU architectures (featuring native CZ gates and tunable couplers) with NVIDIA NVQLink for microsecond-scale real-time GPU decoding co-processing.
| [ IQM Halocene & NVIDIA CUDA-Q Logical Stack Integration ] |  |  | 
|---|---|---|
| System Layer | Hardware & Interconnect Infrastructure | Software & QEC Orchestration Layer | 
| Physical QPU & Topology | • IQM Halocene Processor (150 Physical Qubits) • Square-Lattice Geometry with Tunable Couplers | • Native Single-Qubit (X/Y) & Two-Qubit (CZ) Gates • Calibrated for Direct Surface Code Execution | 
| Control & Hardware Acceleration | • Open On-Premises Control Electronics • NVIDIA NVQLink Ultra-Low Latency Interconnect | • Pulse-Level Control & Real-Time FPGA Interface • Sub-Microsecond GPU-Based QEC Decoding Loops | 
| Fault-Tolerant Compilation Stack | • Heterogeneous HPC-QPU Co-Processor Integration • Target Support for Up to 5 Logical Qubits | • NVIDIA CUDA-Q Logical Orchestration Layer • Auditable Cross-Vendor Resource Estimation | 
The operational framework establishes a standardized architecture for academic, national laboratory, and enterprise supercomputing deployments to evaluate and validate QEC designs on physical testbed hardware. Under ecosystem software management led by Max Haeberlein, the integration builds on IQM’s deployment roadmap for Halocene and expands its hardware-agnostic software compatibility across European HPC infrastructure centers.
Review the technical commentary via IQM Blog here and examine our previous analysis of NVIDIA’s NVQLink Integration Across European Supercomputing Hubs here.
September 14, 2026
