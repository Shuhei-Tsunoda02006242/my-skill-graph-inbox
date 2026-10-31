---
source: "Quantum Computing Report"
prefix: qcr-
title: "University of Stuttgart Deploys Quantum Dot QKD Link Using Frequency Conversion Over Campus Fiber"
url: "https://quantumcomputingreport.com/university-of-stuttgart-deploys-quantum-dot-qkd-link-using-frequency-conversion-over-campus-fiber/"
published: 2026-10-31
chars: 3212
truncated: false
extraction: full
---

In a preprint titled Deployed entanglement-based BBM92 quantum key distribution using frequency-converted photons emitted by a quantum dot, a collaborative team led by the University of Stuttgart alongside Saarland University and Leibniz IFW Dresden has demonstrated field-deployed entanglement-based quantum key distribution (QKD) using an epitaxial quantum dot photon source. Operating under a 1 GHz optical excitation rate over a 1.59 km installed fiber link on the Stuttgart-Vaihingen campus, the system generated 14.2 Mbit of secure key material to perform one-time pad image encryption.
| Stuttgart Deployed Quantum Dot QKD Operational Parameters |  |  | 
|---|---|---|
| System Dimension | Reported Specification | Network & Cryptographic Role | 
| Quantum Dot Emitter | Epitaxial droplet-etched GaAs (779.8 nm) | Generates polarization-entangled pairs via resonant two-photon biexciton-exciton (XX–X) cascade. | 
| Fine-Structure Splitting (δ) | 2.1 ± 0.3 μeV | Yields a 91.4% fidelity to the \|Φ+⟩ Bell state within a 275 ps coincidence window. | 
| Wavelength Conversion | Sagnac QFC (779.8 nm → 1515 nm) | Translates biexciton photons to the telecom C-band with up to 50% internal efficiency. | 
| Deployed Fiber Channel | 1.59 km campus link (1.09 dB total loss) | Connects IHFG lab to a 19-inch receiver rack at TIK with automated motorized polarization tracking. | 
| Throughput & Error Rate | Raw: 504 Hz \| Secure: 206 Hz | Maintains an average QBER of 4.70% (well below the 11% BBM92 security threshold). | 
| Post-Processing Pipeline | 5,000-bit LDPC blocks & Toeplitz hashing | Achieves an effective error correction and privacy amplification retention ratio of 40.87%. | 
Most field-deployed QKD networks rely on Poisson-distributed sources—such as attenuated lasers or spontaneous parametric down-conversion (SPDC)—which face intrinsic trade-offs between emitter brightness and multi-photon emission probabilities. While epitaxial quantum dots provide deterministic, sub-Poissonian emission, their native wavelengths lie outside standard telecommunication windows. The Stuttgart team bridged this gap by integrating a broadband antenna-coupled GaAs quantum dot with a polarization-preserving Sagnac frequency converter, transferring one photon of each entangled pair into low-loss silica fiber while preserving polarization correlations.
The network executed the entanglement-based BBM92 protocol using passive 50:50 beam splitters to select between conjugate (Z) and (X) measurement bases, with a multi-photon squashing model to mitigate side-channel risks. Coincidence window optimization identified an operational balance at 275 ps: widening the gate captures more radiative decay events but elevates error rates from fine-structure precession and conversion noise. Motorized waveplates executing hourly polarization probes maintained Stokes parameters above 0.995 throughout 19 hours of continuous operation, with minor throughput declines isolated to thermal detuning in a 25 GHz volume Bragg grating filter. The experiment establishes quantum dots paired with frequency conversion as viable transmitters for metropolitan quantum key networks.
The manuscript is available on arXiv here.
