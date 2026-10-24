---
source: "The Quantum Insider"
prefix: tqi-
title: "Google Launches $150,000 AI Competition to Reduce Quantum Computing Demands"
url: "https://thequantuminsider.com/2026/10/23/google-launches-150000-ai-competition-to-reduce-quantum-computing-demands/"
published: 2026-10-23
chars: 9585
truncated: false
extraction: full
---

Insider Brief
- Google Quantum AI launched a $150,000 Kaggle competition to develop smaller, more efficient quantum circuits for calculations related to fusion energy, optimization and chemistry.
- Participants will reduce qubit and gate counts while meeting accuracy requirements, potentially lowering the hardware demands of useful quantum algorithms.
- The competition uses Google’s open-source kickmix software to efficiently test circuit designs on conventional computers, providing confidence in approximate correctness without proving exact equivalence.
Google Quantum AI is launching a competition to use artificial intelligence to shrink the circuits needed for useful quantum computing. The competition offers a total prize pool of $150,000, organizers said.
The competition, hosted on Kaggle, challenges participants to reduce the number of computing steps and quantum bits required for tasks related to fusion energy, mathematical optimization and chemistry. Google is providing starting circuits and software to check whether proposed improvements produce sufficiently accurate results.
The effort targets a central obstacle to practical quantum computing. Even as researchers build more capable processors, many potentially useful calculations remain too demanding for available hardware. Reducing the work required by an algorithm could lower the hardware requirements for running it.
According to Google’s announcement, the competition draws on a method that allows conventional computers to efficiently test a particular class of quantum circuits. That creates a way for AI systems to repeatedly propose changes, check their accuracy and search for further savings.
Reducing the Cost of a Calculation
A quantum circuit is a sequence of operations used to carry out a calculation. Those operations, called gates, act on qubits, the basic units of quantum information.
Current processors have limited numbers of qubits, and their gates can introduce errors. Quantum error correction is designed to protect calculations from those mistakes, but it requires additional qubits and operations.
That added burden makes circuit size an important factor in determining when an algorithm might become practical, Google said. Removing operations or reducing the number of qubits needed for a calculation can also reduce the resources required to protect it from errors.
The competition addresses this problem through circuit compilation, the process of translating a calculation into a sequence of operations that a quantum computer can execute. Different sequences can perform the same task while using different amounts of computing resources.
Google said specialists have traditionally improved such circuits through detailed manual work. AI agents — software systems that can propose changes, use tools and evaluate results — offer a way to automate parts of that search.
The difficulty is checking their work. For a general quantum circuit, a conventional computer may need to track an enormous number of possible states. That burden grows rapidly as qubits are added, making comprehensive simulation impractical for large circuits.
Google’s approach narrows the search to circuits that are easier to check.
A Faster Way to Test AI Designs
The competition uses an open-source software library called kickmix, available within Google’s Qualtran project. A companion paper, “Leveraging verifiable structure in quantum circuits to find more efficient compilations with agentic AI,” describes the method.
Kickmix circuits combine reversible logic, operations that adjust quantum phases and a measurement-based method for clearing temporary information. Reversible logic preserves enough information to undo a computation. Quantum phases help determine how different parts of a quantum calculation reinforce or cancel one another.
According to Google, these circuits take each input string of zeros and ones to a single output string and an associated phase without creating additional superpositions. A superposition allows a quantum state to contain contributions from multiple possible bit patterns.
That structure allows conventional computers to test randomly selected inputs efficiently, without tracking every possible component of a large quantum state.
The process, known as randomized fuzz testing, checks many inputs for evidence that a proposed circuit behaves as intended. Google said the method can establish approximate correctness with high confidence, including for the circuit’s behavior on quantum states.
It does not establish exact equivalence. Instead, the approach allows small, bounded differences, which Google said many quantum algorithms can tolerate. Accepting carefully controlled approximations can substantially reduce gate and qubit counts.
Google said the kickmix software can test circuits at a rate of 60 billion gates per second on a single processor core. That figure describes conventional-computer testing speed, rather than the operating speed of a quantum processor.
Three Scientific Targets
Each competition benchmark includes a reference circuit and a separate verification program, both released under the Apache 2.0 open-source license. Participants must submit circuits that pass the relevant verifier while reducing a score based on gate and qubit counts.
Google describes the three tasks as follows:
- Fusion energy: Designing inertial confinement fusion targets requires simulating how quickly charged particles slow down in a hot, dense plasma fuel (Proceedings of the National Academy of Sciences (PNAS)). The main bottleneck is computing the electric potential energy between every pair of particles, which is inversely proportional to their distance. The task is a quantum take on the classic fast inverse square root: given the squared distance x, apply a phase proportional to 1/√x, accurate to a tiny fraction of its exact value.
- Optimization: Decoded Quantum Interferometry (Nature) is a quantum algorithm for solving hard combinatorial optimization problems. On one such problem, Optimal Polynomial Intersection (OPI), it finds better solutions than any known efficient classical algorithm. The main arithmetic bottleneck in solving OPI is decoding a Reed-Solomon code in superposition. The task is to build this decoder as a quantum circuit.
- Chemistry: Fertilizer production depends on nitrogen fixation, which converts nitrogen gas from the air into ammonia. Industry does this at high temperature and pressure, using about 1–2% of the world’s energy supply, while bacteria do it at ambient conditions with the enzyme nitrogenase, whose active site is an iron-molybdenum cluster called FeMoCo. Understanding how FeMoCo works requires modeling its strongly correlated electrons, a long-standing target for quantum computers. Our recent algorithm (Physical Review X (PRX)) makes that quantum simulation cheaper by classically factorizing the molecule’s Hamiltonian into a compact sum of squares, so the quantum computer needs far fewer steps. At each step, the main bottleneck is a quantum lookup table that loads the parameters of that factorized Hamiltonian in superposition. The task is to co-design both parts: find an accurate factorization that needs fewer steps, and build compact circuits to load its parameters so each step costs less.
Google said internal experiments with its Gemini models have already produced improvements beyond circuits reported to date across all three benchmarks. The researchers published a digital fingerprint, or hash, of those circuits in their manuscript and plan to reveal them after the competition.
Prizes
Leaderboard Prizes
- 1st Place: $50,000
- 2nd Place: $25,000
- 3rd Place: $10,000
- 4th Place: $5,000
- 5th Place: $5,000
- 6th Place: $5,000
Additional Prizes: $50,000
- Mid-Competition Milestone Prize: $10,000
- Longest Leader Prize: $10,000
- Single Task Performance Prizes: $30,000
For each additional prize, the winning notebooks or submissions need to adhere to the same requirements and restrictions regarding licensing, reproducibility, and documentation to which the winning Submission is subject (see Competition Rules).
Mid-Competition Milestone Prize
Participants of this competition are encouraged to make publicly available their notebooks through the competition. At the end of the competition, $10,000 will be awarded to the team with the highest public leaderboard score at 11:59 PM UTC, November 20th. To be eligible for the Mid-Competition Milestone Prize, you will need to: publish a notebook and keep the notebooks and any datasets they use publicly available until the Final Submission Deadline.
Longest Leader Prize
Awarded to the team whose notebook(s) generates the best scoring submission on the leaderboard for the longest period of time between the competition start date and January 4th, 2027. The notebook(s) and any datasets used must be made publicly available at latest at January 4th, 2027 11:59 PM UTC and kept public until the end of the competition. In the event that a team has multiple public notebooks, each achieving the top leaderboard position at different times, those durations will be combined.
Single Task Performance Prizes
For each of the three tasks (combinatorial optimization, chemistry, and fusion), the selected submission with the best score for that specific task will receive a $10,000 prize.
Visit the competition page on Kaggle to read the full details, explore the resources, and submit your work.
Matt Swayne
Get the latest research, company news, and market intelligence every week.
MENTIONED IN THE ARTICLE
