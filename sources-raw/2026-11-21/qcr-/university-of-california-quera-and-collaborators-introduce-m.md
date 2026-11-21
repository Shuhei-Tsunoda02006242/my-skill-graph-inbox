---
source: "Quantum Computing Report"
prefix: qcr-
title: "University of California, QuEra, and Collaborators Introduce Multi-Agent LLM Compiler Qubrio for Neutral-Atom Processors"
url: "https://quantumcomputingreport.com/university-of-california-quera-and-collaborators-introduce-multi-agent-llm-compiler-qubrio-for-neutral-atom-processors/"
published: 2026-11-21
chars: 2726
truncated: false
extraction: full
---

Researchers from the University of California, San Diego, Rice University, QuEra Computing, Rochester Institute of Technology, and the University of Wisconsin–Madison have introduced Qubrio, a multi-agent large language model (LLM) framework for neutral-atom quantum circuit compilation accepted to NeurIPS 2026. Rather than relying on hand-engineered heuristics that must be rewritten whenever processor layouts or transport capabilities change, Qubrio pairs specialized LLM proposal agents with deterministic constraint verifiers and a physical hardware simulator to automate qubit placement, acousto-optic deflector (AOD) routing, and schedule optimization.
| Qubrio Compilation Performance & Hardware Adaptability Summary |  |  | 
|---|---|---|
| Evaluation Dimension | Baseline / Configuration | Key Results | 
| Overall Speedup & Fidelity | vs. SOTA compiler PowerMove (QFT, QAOA, GHZ, Ising up to 78 qubits) | 4.7× average runtime reduction (5.9× at ~60 qubits) and 1.3× average fidelity gain (9.9× including QFT-63). | 
| LLM Backbone Comparison | GPT-5.4, DeepSeek-V3.2, and Qwen-3.5 vs. PowerMove | Runtime speedups of 4.7× (GPT-5.4), 2.5× (DeepSeek-V3.2), and 2.1× (Qwen-3.5) with ~$0.29–$0.59 per-stage API cost. | 
| Convoy-Style Shuttling | LLM-discovered buffer-trap & continuous-motion heuristic | Packs up to 30.3 qubits per AOD move on GHZ-78; distilling rules into PowerMove recovers 38% of runtime savings. | 
| Architectural Adaptability | Multi-AOD (kAOD = 1–4), Zoned Arrays, and Fixed-Lane Layouts | Adapted via declarative constraints without algorithmic rewrites; yields 2,263× fidelity gain on zoned QFT-63. | 
To prevent single-pass LLM failures on long, tightly constrained circuits, Qubrio applies a three-level decomposition: partitioning circuits into sequential controlled-Z (CZ) gate stages, separating spatial placement from sequential trajectory routing and schedule refinement across dedicated agents, and providing localized spatio-temporal error diagnostics alongside decoupled transfer and decoherence feedback. Analyzing the agents’ reasoning logs revealed that the system autonomously discovered convoy-style shuttling, using buffer traps and continuous multi-round motion to move compatible qubits in lockstep and minimize spatial-light-modulator to AOD transfer penalties.
Evaluated across QASMBench workloads up to 78 qubits and compared against both heuristic compilers and simulated annealing with 10,000× larger evaluation budgets, Qubrio consistently delivered faster execution schedules and higher circuit fidelity while compiling batches of stages in roughly five minutes.
Read the full research paper on arXiv here, and access the open-source Qubrio codebase on GitHub here.
