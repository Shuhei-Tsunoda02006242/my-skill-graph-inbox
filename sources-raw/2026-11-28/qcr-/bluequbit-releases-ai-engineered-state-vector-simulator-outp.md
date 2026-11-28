---
source: "Quantum Computing Report"
prefix: qcr-
title: "BlueQubit Releases AI-Engineered State-Vector Simulator Outperforming NVIDIA cuStateVec Benchmarks"
url: "https://quantumcomputingreport.com/bluequbit-releases-ai-engineered-state-vector-simulator-outperforming-nvidia-custatevec-benchmarks/"
published: 2026-11-28
chars: 1501
truncated: false
extraction: full
---

BlueQubit has introduced bluesv, an exact quantum state-vector simulator engineered entirely through automated agentic coding workflows to serve as a drop-in replacement for NVIDIA’s cuStateVec library. Built in weeks rather than a typical multi-quarter development cycle using Anthropic’s Claude Code verified against deterministic numerical oracles, the library provides direct API compatibility with Qiskit, Cirq, and PennyLane across single and double floating-point precision without requiring user code changes.
In benchmark tests against qsim on an NVIDIA A100 GPU across randomly generated circuits spanning 22 to 30 qubits and depths from 10 to 100, bluesv outperformed cuStateVec at every measured point and achieved more than a 1.4× speedup on the largest, deepest circuits. On a 10-core Intel Xeon processor, bluesv outpaced qsim‘s CPU backend across all tested sizes, delivering 1.5× to 1.6× speedups at depth 10 and roughly 1.8× speedups at depth 30 for circuits of 26 qubits or more while matching reference outputs to machine precision.
Packaged as a self-contained binary to eliminate setup overhead for high-throughput batches of smaller circuits, bluesv is now live in production powering the BlueQubit SDK and hosted cloud platform. BlueQubit stated that bluesv will be released as open-source software and represents the first of several core SDK components the company plans to build through specification-driven agentic engineering.
Read BlueQubit’s technical announcement here.
