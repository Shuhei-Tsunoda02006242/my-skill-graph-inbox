---
source: "Quantum Computing Report"
prefix: qcr-
title: "Qoro Quantum Signs MoU with STFC Hartree Centre to Build UK Quantum-HPC Demonstrator"
url: "https://quantumcomputingreport.com/qoro-quantum-signs-mou-with-stfc-hartree-centre-to-build-uk-quantum-hpc-demonstrator/"
published: 2026-09-12
chars: 2908
truncated: false
extraction: full
---

Quantum middleware startup Qoro Quantum has signed a Memorandum of Understanding (MoU) with the STFC Hartree Centre to construct an enterprise-grade hybrid quantum-HPC demonstrator. Backed by the UK’s Science and Technology Facilities Council (STFC), the collaboration will integrate Qoro’s automated software stack directly into the Hartree Centre’s high-performance computing (HPC) cluster infrastructure to serve UK industry and public sector research workloads.
The technical integration utilizes the open-source Quantum Resource Management Interface (QRMI) to establish tightly coupled execution pathways between classical HPC schedulers and multi-QPU resources. Sitting above the interface, Qoro’s open-source Python SDK, Divi, automatically partitions, serializes, and parallelizes complex quantum circuits, routing them as native Slurm jobs into the Hartree Centre scheduler. Below the interface, Qoro’s unified simulation engine, Maestro, operates alongside physical quantum processing units (QPUs) from hardware partners including IBM and Pasqal to provide automated auto-scaling simulation and execution backends.
| [ Qoro Quantum & STFC Hartree Centre Software Stack Integration ] |  |  | 
|---|---|---|
| Stack Layer | Qoro Software Module | Hartree HPC Integration Role | 
| Application & SDK | • Divi Open-Source Python SDK | • Application-Aware Circuit Parallelization • Slurm Job Generation & Circuit Dispatch | 
| Interface & Middleware | • QRMI Open-Source Management Plugin • Dedicato Private Infrastructure Stack | • Standardized Multi-QPU Resource Routing • Sovereign Quantum-HPC Value Chain | 
| Execution Backends | • Maestro Auto-Scaling Simulation Engine | • Multi-Node Classical Simulation Substrate • Heterogeneous QPU Access (IBM, Pasqal) | 
Initial demonstrator workflows will target practical challenges in electronic structure theory, physical sciences modeling, and quantum chemistry, establishing documented reference benchmarks for the UK quantum research community. The collaboration aligns with broader sovereign UK computing initiatives—including the Edinburgh Parallel Computing Centre (EPCC) and the National Quantum Computing Centre (NQCC)—with planned future extensions into physical QPU pilots across energy, finance, and pharmaceuticals.
The partnership builds on Qoro’s commercial momentum following the launch of its Solo cloud platform and previous Quantum-HPC demonstrator pilots with Spain’s CESGA. Under Director Kate Royse and CEO Dan Holme, the joint effort aims to deliver a “build once, run everywhere” software model that eliminates custom integration code for industrial supercomputing users.
Review the official news release on Qoro Quantum here, listen to our Podcast with Stephen DiAdamo, Co-founder and CTO of Qoro Quantum here, and examine our previous analysis of Qoro’s Launch of Solo for Parallelized Quantum Simulation here.
September 11, 2026
