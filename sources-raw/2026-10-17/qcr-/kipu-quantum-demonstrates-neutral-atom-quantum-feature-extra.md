---
source: "Quantum Computing Report"
prefix: qcr-
title: "Kipu Quantum Demonstrates Neutral-Atom Quantum Feature Extraction for Molecular Toxicity Classification on QuEra Hardware"
url: "https://quantumcomputingreport.com/kipu-quantum-demonstrates-neutral-atom-quantum-feature-extraction-for-molecular-toxicity-classification-on-quera-hardware/"
published: 2026-10-17
chars: 2491
truncated: false
extraction: full
---

In a technical release, quantum application software developer Kipu Quantum detailed experimental results demonstrating analog quantum feature extraction on QuEra Computing’s 256-qubit Aquila neutral-atom quantum processor, achieving performance gains in molecular toxicity classification for drug discovery and chemical safety.
Authored by Kipu Quantum engineers Antonio Ferrer Sánchez, Carlos Flores, and Alejandro Gómez Cadavid (“Reading Toxicity of Molecules with Neutral-Atom Quantum Processors“), the study deployed 200-qubit neutral-atom arrays to generate high-dimensional quantum features that significantly outperformed traditional classical molecular descriptors on imbalanced dataset benchmarks.
| [ Feature Set Benchmark Comparison (Molecular Toxicity Dataset) ] |  |  |  |  | 
|---|---|---|---|---|
| Feature Set / Pipeline | Raw Accuracy | Balanced Accuracy | F1-Score | AUC Score | 
| • Classical Baseline Features | • ~ 0.74 | • ~ 0.55 | • ~ 0.30 | • ~ 0.68 | 
| • Combined (Classical + Quantum) | • ~ 0.77 | • ~ 0.68 | • ~ 0.58 | • ~ 0.77 | 
| • Quantum Features Only (SVM Top) | • ~ 0.78 | • ~ 0.70 | • ~ 0.60 (2x Boost) | • ~ 0.81 | 
Traditional digital quantum machine learning (QML) algorithms require deep, gate-based circuits that suffer from noise on current hardware. Kipu Quantum avoided discrete gate overhead by utilizing analog Rydberg-state continuous dynamics on QuEra’s neutral-atom QPU, accessed via the Kipu Quantum Hub platform. For each candidate molecule in the UCI Molecular Toxicity dataset, 200 neutral atoms were arranged on a 14×15 grid spaced a few micrometers apart. Applying smooth driving pulses for under 4 microseconds allowed collective quantum interactions to evolve across the array, generating ~1,000 quantum features per molecule across 500 independent readout shots per sample.
The extracted quantum features were evaluated across 100 random dataset splits using a suite of classical machine learning models, including XGBoost, CatBoost, Random Forest, Support Vector Machines (SVM), and Google Research’s zero-shot tabular foundation model (TabFM). On imbalanced dataset metrics where classical models struggle—often achieving flattering raw accuracy by simply predicting the majority non-toxic class—quantum features raised Balanced Accuracy from 0.55 to 0.70 and doubled the F1-score from ~0.30 to ~0.60, with an SVM classifier achieving the top overall AUC score (~0.81).
Review the technical report on the Kipu Quantum Portal here.
