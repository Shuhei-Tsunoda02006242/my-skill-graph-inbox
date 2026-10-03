---
source: "Quantum Computing Report"
prefix: qcr-
title: "Fermilab SQMS Center Identifies Microscopic Origins of Qubit Performance Variance Across Superconducting Transmons"
url: "https://quantumcomputingreport.com/fermilab-sqms-center-identifies-microscopic-origins-of-qubit-performance-variance-across-superconducting-transmons/"
published: 2026-10-02
chars: 3126
truncated: false
extraction: full
---

Researchers at the Fermi National Accelerator Laboratory-led Superconducting Quantum Materials and Systems Center (SQMS), in collaboration with Rigetti Computing, the National Institute of Standards and Technology (NIST), Ames National Laboratory, Northwestern University, and the National Physical Laboratory (NPL), have published a comprehensive multi-institution study isolating the microscopic materials defects responsible for device-to-device performance variation in superconducting transmon qubits. Published in Applied Physics Reviews, the findings establish direct correlations between nanoscale fabrication geometries, surface oxides, and energy relaxation times (T1).
A primary bottleneck in scaling fault-tolerant superconducting quantum processing units (QPUs) is performance variance among identically designed qubits co-fabricated on the same substrate. To eliminate observer bias, the study evaluated 22 transmon devices using a double-blind protocol: characterization teams cataloged structural and chemical features across seven non-destructive and invasive spectroscopy and microscopy techniques without prior knowledge of the qubits’ coherence metrics. Coherence measurements conducted in the SQMS Quantum Garage were correlated with materials data only after characterization was completed.
| [ SQMS Materials Characterization Drivers & Qubit Coherence Impact ] |  |  | 
|---|---|---|
| Material / Geometry Feature | Physical Measurement & Fabrication Metric | Coherence Impact & Engineering Guidance | 
| • Etched Sidewall Angle | • Sharp 10°–15° angle vs. broad 30° tapered etch slope | • 10°–15° angles reduce electric field storage in lossy surface oxides, predicting a 20%–30% T1 improvement | 
| • Substrate Trench Depth | • Vertical depth of etched substrate recesses adjacent to metal electrodes (<20 nm) | • Variations below 20 nm drive sharp performance fluctuations; effects saturate at deeper trench profiles | 
| • Surface Oxide Thickness | • Single-nanometer shifts in ambient surface oxide layers | • Dominates dielectric loss tangent; single-nm shifts directly drive up to a 2x variation in T1 relaxation times | 
| • Macroscopic Imperfections | • Visible surface scratches, dust particulates, and macroscopic defects | • Exhibited no statistical correlation with T1 variance; nanoscale interfaces dictate coherence spread | 
The analysis demonstrated that single-nanometer shifts in surface oxide thickness, substrate trench depths below 20 nanometers, and sidewall etch profiles account for up to a twofold variation in T1 lifetimes across neighboring qubits on the same chip. Conversely, macroscopic surface defects showed no clear statistical correlation with performance degradation. Industry partner Rigetti Computing is leveraging these empirical parameters to optimize lithographic etching and surface passivation protocols, providing a predictive framework to enforce yield uniformity across multi-qubit processors.
Review the full laboratory release on the Fermilab Newsroom here and inspect the peer-reviewed research manuscript in Applied Physics Reviews here.
October 1, 2026
