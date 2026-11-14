---
source: "Quantum Computing Report"
prefix: qcr-
title: "QodeX Quantum, NVIDIA, RTX BBN, and U.S. Navy Researchers Forecast Unstructured PDEs on 52-Qubit IBM Hardware"
url: "https://quantumcomputingreport.com/qodex-quantum-nvidia-rtx-bbn-and-u-s-navy-researchers-forecast-unstructured-pdes-on-52-qubit-ibm-hardware/"
published: 2026-11-13
chars: 3308
truncated: false
extraction: full
---

A research team from QodeX Quantum, the University of South Carolina, the Naval Surface Warfare Center Panama City Division, NVIDIA, and RTX BBN has demonstrated gradient-free forecasting of nonlinear partial differential equations (PDEs) on unstructured engineering meshes using up to 52 qubits on an IBM Quantum Heron r3 (ibm_boston) processor. Detailed in a technical preprint on arXiv, the hybrid quantum reservoir network (QRN) executed circuits up to 24 times longer than median qubit coherence times and reduced forecast error by 21% to 41% on physical hardware compared to classical latent linear baselines.
| Quantum Reservoir Network (QRN) Hardware & Simulation Benchmarks |  |  | 
|---|---|---|
| Benchmark Dimension | 2D Cylinder Flow (ReD = 1000) | Gray-Scott Reaction-Diffusion | 
| Spatial Discretization | 33,824-cell unstructured hex-dominant mesh (OpenFOAM) | 128 × 128 uniform grid (two interacting chemical species) | 
| Quantum Register Scale | 26 qubits (13 memory, 13 readout) | 26 qubits and 52 qubits (26 memory, 26 readout) | 
| Compiled Circuit Depth | 14,234 layers (38,670 CZ gates across 300 steps) | 53,322 layers on 52 qubits (272,827 CZ gates across 1,001 steps) | 
| One-Step Error Reduction | 33.2% NRMSE reduction on QPU (0.081 vs. 0.121 baseline); 21.2% on pressure observer | 41.1% NRMSE reduction on 26- and 52-qubit QPUs (0.133 vs. 0.225 baseline) | 
| QPU vs. H100 Sampling | 75 s on ibm_boston vs. 2.5 × 105 s on NVIDIA H100 (~3,300× faster QPU sampling) | 222 s on 52-qubit QPU (beyond exact classical statevector simulation) | 
Conventional gate-based quantum solvers for computational fluid dynamics have historically been restricted to uniform grids, low Reynolds numbers, or shallow variational circuits susceptible to barren plateaus and heavy measurement overheads. To decouple complex boundary geometries from quantum circuit topology, the authors paired a pretrained graph neural network autoencoder with a fixed, untrained quantum reservoir split into dedicated memory and readout registers.
At each time step, latent flow variables are encoded into the memory register via data-reuploading rotations, coupled to readout qubits through tunable partial-SWAP gates, and followed by mid-circuit measurement and reset of the readout register. This controlled amplitude-damping channel establishes a tunable fading memory that sustains continuous evolution for up to 28 times median qubit T1 and 24 times median T2 without collapsing the memory register, while a post-hoc Pauli-weight truncation method controls readout shot requirements.
In 10-step closed-loop autoregressive rollouts on the cylinder flow dataset, physical hardware noise acted as an effective regularizer, achieving a test NRMSE of 0.257 compared to 0.707 in noiseless CUDA-Q simulation and 1.126 for a classical persistence baseline. According to Chicago-based QodeX Quantum, the study also served to develop and validate modules of AlphaPsi, its agentic quantum workflow platform.
The full technical manuscript is available on arXiv here, with open-source implementation code hosted on GitHub here and product details on QodeX Quantum’s website here. Related QCR coverage of quantum fluid dynamics and reservoir computing includes Q-CTRL’s 12× Nighthawk r2 dynamics simulation speedup here.
