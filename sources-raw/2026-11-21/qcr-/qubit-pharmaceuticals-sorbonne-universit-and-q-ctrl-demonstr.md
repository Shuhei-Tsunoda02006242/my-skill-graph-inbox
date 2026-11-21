---
source: "Quantum Computing Report"
prefix: qcr-
title: "Qubit Pharmaceuticals, Sorbonne Université, and Q-CTRL Demonstrate 3D Protein Hydration-Site Prediction on IBM Heron Processors"
url: "https://quantumcomputingreport.com/qubit-pharmaceuticals-sorbonne-universite-and-q-ctrl-demonstrate-3d-protein-hydration-site-prediction-on-ibm-heron-processors/"
published: 2026-11-21
chars: 3231
truncated: false
extraction: full
---

Researchers from Qubit Pharmaceuticals, Sorbonne Université (CNRS Laboratoire de Chimie Théorique), and Q-CTRL have published a peer-reviewed study in Physical Review Research demonstrating three-dimensional protein-pocket hydration-site prediction on 156-qubit IBM Heron quantum processors. By fitting continuous 3D Reference Interaction Site Model (3D-RISM) water densities to a Gaussian Mixture Model (GMM) cast as a Quadratic Unconstrained Binary Optimization (QUBO) problem, the team executed hardware experiments up to 123 qubits across five FDA-approved drug-target protein structures using Q-CTRL’s Fire Opal optimization solver.
| 3D Protein Hydration-Site Quantum Optimization & Resource Scaling Summary |  |  | 
|---|---|---|
| Benchmark / Regime | Scale & Hardware / Solver | Key Findings & Resource Metrics | 
| 11-Instance Protein Benchmark Set | 41 to 116 qubits across 5 PDB targets (1f9g, 1×70, 2f9w, 3b7e, 4h2f/3beq) on IBM Kingston (Heron r2) | Q-CTRL Fire Opal identified exact CPLEX-verified optimal water placements across all 11 instances, reaching ~9% optimal sampling probability at 116 qubits (vs. ~2% for simulated annealing). | 
| 123-Qubit Hard QUBO Benchmark | 123 qubits (PDB 3b7e with ligand at 1.9 Å grid spacing) on IBM Pittsburgh (Heron r3) | Found a lower-cost solution (C = −321.32) in 25 minutes on QPU than CPLEX reached before timing out at 3 hours (C = −319.90, 40% optimality gap). | 
| Classical Scale-Up & Comparison | 900 to 6,824 binary variables via simulated annealing vs. Hydraprot, Watgen, Placevent, and Dowser++ | Crystal-water recovery rose from ~60% at 123 variables to ~90% at ≥1,450 variables, matching Hydraprot precision and outperforming Placevent, Watgen, and Dowser++. | 
| Quantum Utility Forecast | Quadratic two-qubit gate scaling extrapolated from 156-qubit Heron compilations | Projects ~900 qubits and ~100,000 two-qubit gates (reducible to ~15,000 with higher connectivity) for practical drug-discovery utility. | 
Across 11 discretized protein-ligand test instances ranging from 41 to 116 variables on the IBM Kingston Heron r2 processor, Q-CTRL’s automated error-suppressed variational solver recovered the exact classically verified ground-state water configurations in every case, achieving roughly 9% sampling probability for the optimal solution on the 116-qubit instance compared with 2% for classical simulated annealing. Scaling the 3b7e protein-ligand complex to 123 qubits on IBM’s newer Heron r3 processor (IBM Pittsburgh) yielded a lower-energy solution in 25 minutes of QPU runtime than the exact classical solver CPLEX achieved before hitting a three-hour timeout.
To chart the path toward practical computer-aided drug discovery (CADD) utility, the authors evaluated larger problem grids classically up to 6,824 variables and extrapolated circuit compilation requirements from Heron hardware. Their analysis indicates that hydration-site prediction becomes competitive with leading classical tools at roughly 900 qubits and 100,000 two-qubit gates, placing full-pocket water placement for molecular docking and lead optimization within reach of early error-corrected quantum processors.
Read the open-access paper in Physical Review Research here.
