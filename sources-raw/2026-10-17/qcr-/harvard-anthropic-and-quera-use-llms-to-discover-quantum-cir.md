---
source: "Quantum Computing Report"
prefix: qcr-
title: "Harvard, Anthropic, and QuEra Use LLMs to Discover Quantum Circuits with Up to 9,100x Lower Resource Costs"
url: "https://quantumcomputingreport.com/harvard-anthropic-and-quera-use-llms-to-discover-quantum-circuits-with-up-to-9100x-lower-resource-costs/"
published: 2026-10-17
chars: 4198
truncated: false
extraction: full
---

In a research study published on arXiv, scientists from Harvard University, Anthropic, and QuEra Computing have introduced an evolutionary AI framework where Large Language Models (LLMs) automatically discover, write, and optimize fault-tolerant quantum circuits.
Detailed in the paper (“Discovering state-of-the-art quantum circuits with large language models“), the authors demonstrate that pairing LLM code proposals with an independent classical evaluator reduces the space-time resource costs (T × Q-cost) of core computational primitives by 4.1x to over 9,100x relative to hand-crafted baselines.
| [ Resource Improvements Across Eight Compilation Subroutines ] |  |  |  | 
|---|---|---|---|
| Compilation Subroutine / Task | Baseline (T, Q) | Discovered (T, Q) | TQ-Cost Gain (G_TQ) | 
| • Reed–Solomon DQI Decoder | • (5.1 × 106, 1,938) | • (4.4 × 105, 1,837) | • 12x Reduction | 
| • Hermitian DQI Decoder | • (1.0 × 108, 1.9 × 105) | • (9.3 × 105, 2,395) | • > 9,100x Reduction | 
| • HHL Rotation Angle (arcsin) | • (1.6 × 104, 300) | • (1,348, 115) | • 32x Reduction | 
| • Coulomb Potential (1/√\|\|x\|\|²) | • (6,355, 252) | • (1,140, 142) | • 9.9x Reduction | 
| • Fixed-Point Gaussian (e-x²) | • (2.4 × 104, 362) | • (1,583, 139) | • 39x Reduction | 
| • Fe&sub2;S&sub2; Alias–Select (Chemistry) | • (5.5 × 104, 139) | • (1.5 × 104, 126) | • 4.1x Reduction | 
| • Non-Abelian Lattice-Gauge Sim. | • (1.3 × 106, 1,927) | • (1.7 × 105, 1,859) | • 7.7x Reduction | 
| • Prime-Field Modular Inversion | • (1.9 × 106, 1,446) | • (4.0 × 106, 935) | • New Divsteps Architecture | 
Evolutionary LLM Framework and Reversible Design Principles
Unlike traditional automated circuit optimizers that perform local, gate-level rewrites on fixed circuit graphs, the Harvard-Anthropic-QuEra framework allows an LLM (Claude) to propose complete Python programs across distinct algorithmic families. A classical evaluator tests candidate circuits using the kickmix model—simulating basis trajectories and tracking phase kickback—to verify exact correctness while scoring candidates by their TQ-cost (Toffoli count T × peak qubit footprint Q).
The evolutionary search repeatedly uncovered three fundamental co-design principles:
- Conditional Routing over Conditional Arithmetic: Replacing separate, expensive conditional arithmetic blocks for every execution branch with inexpensive controlled SWAP gates that route selected data through a single shared, uncontrolled arithmetic block.
- Branch Decoding from Evolving Arithmetic State: Eliminating massive qubit history stacks by decoding intermediate branch choices directly from mathematical invariants present in the updated arithmetic registers during the uncomputation pass.
- Bounded Resource Allocation via Failure Budgets: Allocating history stack space and loop bounds to match typical inputs rather than worst-case limits, permitting a controlled failure rate (ε ~ 10-4) to save hundreds of ancilla qubits.
Key Breakthroughs and Modular Inversion Architecture
In the eighth task—prime-field modular inversion for cryptography and number theory—the framework discovered a new reversible architecture for divsteps, a classical, constant-time modular inversion algorithm previously considered unusable for quantum computing due to history storage overhead. By deriving a 2-adic mathematical invariant, the circuit decodes 87.6% of ambiguous branch decisions directly from the updated registers, storing only 12.4% on a small 60-qubit stack and establishing a smooth trade-off frontier between Toffoli count and qubit footprint.
For the Hermitian code DQI decoder (>9,100x savings), the AI replaced raw null-space matrix storage with an in-place Lanczos recurrence and a striped phase scan, dropping the peak qubit count from 190,000 to 2,395 and Toffolis from 100 million to 930,000. Similarly, for numerical functions (HHL angle evaluation, Coulomb potentials, and Gaussian basis functions), the AI replaced wide fixed-point multiplications with dyadic power-of-two aligned lookups and direct accumulator updates, reducing TQ-costs by 9.9x to 39x.
Review Yuval Boger’s post on LinkedIn here and inspect the technical manuscript on arXiv here.
