---
source: "The Quantum Insider"
prefix: tqi-
title: "Qblox Integrates NVIDIA DGX Spark With Quantum System Controller"
url: "https://thequantuminsider.com/2026/10/22/qblox-hybrid-quantum-computing-nvidia-dgx-spark-nvqlink/"
published: 2026-10-22
chars: 3876
truncated: false
extraction: full
---

Insider Brief
- Qblox has integrated NVIDIA DGX Spark with its quantum system controller using NVIDIA NVQLink, reporting round-trip latency below 4.0 microseconds on NVIDIA RTX PRO 6000 Blackwell and below 7.2 microseconds on DGX Spark.
- The integration connects GPU computing with quantum control to support real-time hybrid quantum-classical workloads, including GPU-accelerated calibration and quantum error correction.
- The system uses NVIDIA CUDA-Q to support development on desktop hardware, with the same code designed to transfer to GPU servers as quantum systems scale.
PRESS RELEASE — Qblox, a leader in scalable quantum control architecture, today announced the integration of NVIDIA DGX Spark with a quantum system controller using NVIDIA NVQLink, achieving measured roundtrip latency below 4.0 µs on NVIDIA RTX PRO 6000 Blackwell and below 7.2 µs on NVIDIA DGX Spark. This enables Qblox to support real-time hybrid quantum-classical applications, with a single desktop system that can host quantum, AI, and simulation workloads via NVIDIA CUDA-Q. The same code then carries over to data center graphics processing unit (GPU) servers as systems scale.
The integration brings GPU acceleration into the real-time control loop, a key building block for scaling quantum systems to support logical qubits. Qblox‘s Q1 sequence processors and LINQ deliver the low latency and high throughput the Qblox Cluster needs to work hand in hand with the GPU. GPU-accelerated calibration routines update qubit parameters while experiments run, instead of between them. For quantum error correction, syndrome data reaches GPU-based decoders with low latency, helping identify and correct errors in real time.
The milestone builds on the previous work from Qblox with NVIDIA NVQLink announced in October 2025 and on Qblox’s support for the NVIDIA CUDA-Q realtime API in March 2026. It moves the integration from architecture to measured hardware performance, demonstrating Qblox’s ability to deliver the low-latency performance needed to connect quantum control with GPU computing in real time.
“Quantum computers will scale only as fast as the classical control systems around them,” said Niels Bultink, CEO and Co-founder of Qblox. “With these developments, the GPUs become part of that control loop, giving quantum systems access to the computing power they need in real time. Qblox is proud to work with NVIDIA‘s NVQLink to advance GPU integration and bring faster calibration and error correction to the quantum industry.”
“DGX Spark puts an AI supercomputer on a quantum researcher’s desk,” said Sam Stanwyck, director of quantum product at NVIDIA. “Qblox‘s integration with NVQLink and CUDA-Q connects that computing power to quantum hardware, bringing simulation, real-time calibration and error correction into a single development platform. Researchers can build and test new approaches on their desktop, then scale the same code to GPU supercomputers as their quantum systems grow.”
Mohib Ur Rehman
Get the latest research, company news, and market intelligence every week.
MENTIONED IN THE ARTICLE
Qblox specializes in advancing quantum technology through scalable control electronics crucial for quantum computing. They are known for their modular quantum control stacks, which enable efficient qubit control and readout for diverse applications. The company is based in the Netherlands and is a spin-off of QuTech.
NVIDIA Corporation is an American multinational technology company and a global player in accelerated computing and Artificial Intelligence (AI). Founded in 1993, the company pushes the aerospace frontier with the Space-1 Vera Rubin Module, a platform for orbital data centers that delivers massive AI-compute Space Computing. This NVIDIA technology enables satellites and autonomous spacecraft to process and fuse sensor data rapidly Space Computing.
