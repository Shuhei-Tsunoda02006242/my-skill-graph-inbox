---
source: "Quantum Computing Report"
prefix: qcr-
title: "Quantum Motion and NVIDIA Integrate CUDA-Q Backend into QUICHE for End-to-End Quantum Chemistry Workflows"
url: "https://quantumcomputingreport.com/quantum-motion-and-nvidia-integrate-cuda-q-backend-into-quiche-for-end-to-end-quantum-chemistry-workflows/"
published: 2026-11-21
chars: 1765
truncated: false
extraction: full
---

Quantum Motion and NVIDIA have demonstrated an end-to-end quantum chemistry simulation and resource-estimation pipeline by adding NVIDIA CUDA-Q as a prototype backend to QUICHE, the open-source interface co-developed by Quantum Motion, FACCTs, and Riverlane to connect quantum algorithms with the ORCA quantum chemistry package. Leveraging the CUDA-Q Algorithms layer, the integration automates the transition from classical molecular integral generation to GPU-accelerated quantum phase estimation (QPE) without requiring manual circuit construction.
In the unified workflow, researchers run classical electronic-structure calculations in ORCA to export active-space integrals in a standard FCIDUMP file, which QUICHE ingests alongside high-level specifications for the Hamiltonian, QPE protocol, and target energy precision. CUDA-Q Algorithms then constructs the qubit Hamiltonian and dispatches QPE kernels directly onto NVIDIA GPUs, using the same problem specification that drives fault-tolerant resource estimation.
To validate the pipeline, the teams modeled the spin-state energetics of the iron-sulfur complex Fe(SH)4−, a minimal representation of the active site in the protein rubredoxin, within a five-electron, five-orbital active space on a single GPU, verifying QPE energy outputs against exact complete active space self-consistent field (CASSCF) benchmarks.
Read Quantum Motion’s technical announcement here, and access the open-source QUICHE codebase here and the SC26 demonstration Jupyter notebook here. Related QCR coverage includes our reports on the launch of the QUICHE consortium here, Quantum Motion’s silicon-spin integration with the CUDA-Q logical compiler stack here, and the Quantum Motion-NVIDIA state-preparation collaboration here.
