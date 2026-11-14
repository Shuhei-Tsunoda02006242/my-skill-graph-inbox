---
source: "Quantum Computing Report"
prefix: qcr-
title: "JIJ Launches SQOA Solver in IBM Quantum Functions Catalog to Tackle Combinatorial Optimization Beyond Qubit Counts"
url: "https://quantumcomputingreport.com/jij-launches-sqoa-solver-in-ibm-quantum-functions-catalog-to-tackle-combinatorial-optimization-beyond-qubit-counts/"
published: 2026-11-14
chars: 2944
truncated: false
extraction: full
---

Tokyo-based optimization software developer JIJ Inc. has deployed its SQOA Solver (jij/sqoa-solver) in the IBM Quantum Functions Catalog, enabling IBM Quantum Premium, Flex, and On-Prem Plan users to solve combinatorial optimization problems containing more decision variables than available physical qubits. Built on the company’s Sampling-based Quantum Optimization Algorithm with Quantum Relaxation (SQOA-QR), the function combines variable-compression encoding with classical subspace diagonalization to eliminate iterative variational parameter loops on quantum hardware.
| JIJ SQOA Solver Architecture & IBM Heron r2 Benchmarks |  |  | 
|---|---|---|
| System Dimension | Technical Specification | Measured Benchmark / Platform Impact | 
| Encoding & Compression | (3,1) Quantum Random Access Code (QRAC) relaxation | Maps up to three binary variables per physical qubit using Pauli X, Y, and Z operators. | 
| Execution Paradigm | Single-pass quantum sampling + classical SQD diagonalization | Removes iterative QPU optimization loops; state-preparation parameters are computed classically. | 
| IBM Heron r2 Benchmarks | QOBLIB Maximum Independent Set & 3-regular MaxCut instances | Solved 384-node MaxCut on 129 qubits (98.5% AR, 12.0 s QPU) and 200-node MIS on 67 qubits (100% AR). | 
| Modeling & Sizing Tiers | Supports QUBO dictionaries, qiskit-addon-opt-mapper, and OMMX | Offers Small (≤50 vars), Medium (≤100 vars), and Large (up to 48 vCPU / 768 GB RAM) compute profiles. | 
Conventional variational algorithms such as the Quantum Approximate Optimization Algorithm (QAOA) typically require one physical qubit per binary variable and rely on repeated quantum-classical optimization loops that accumulate hardware noise as circuit depth grows. SQOA Solver addresses both constraints by packing multiple non-interacting variables onto shared qubits and restricting the quantum processor to sampling bitstrings from a non-diagonal relaxed Hamiltonian.
In the post-processing stage, classical compute nodes project the relaxed Hamiltonian onto the subspace spanned by the sampled bitstrings, diagonalize the reduced system, and apply rounding and local-search refinement to recover feasible classical assignments. The solver natively ingests Open Mathematical Programming eXchange (OMMX) instances compiled via JIJ’s JijModeling 2 library, allowing enterprise teams to transition models between classical solvers and IBM Quantum hardware.
Official announcement details are available via JIJ here, with catalog access here, technical documentation here, API reference here, and a Maximum Independent Set tutorial hosted on the IBM Quantum Platform here. The underlying SQOA-QR paper presented at IEEE Quantum Week 2025 is accessible via IEEE Xplore here and arXiv here. Related QCR coverage of QOBLIB benchmarks and recent IBM Quantum Functions additions includes our QOBLIB report here and Kipu Quantum’s Rimay catalog launch here.
