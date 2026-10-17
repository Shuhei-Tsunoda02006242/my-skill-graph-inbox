---
source: "The Quantum Insider"
prefix: tqi-
title: "Google Demonstrates Method to Cut Errors in Quantum Computing’s ‘Magic States’"
url: "https://thequantuminsider.com/2026/10/16/google-demonstrates-method-to-cut-errors-in-quantum-computings-magic-states/"
published: 2026-10-16
chars: 9480
truncated: false
extraction: full
---

Insider Brief
- Google demonstrated magic-state cultivation on its Willow quantum processor, reducing state-preparation errors about 40-fold and reporting 99.99% logical fidelity, potentially lowering resource demands for error-corrected computing.
- The team used reinforcement learning to improve processor calibration and developed a measurement technique to avoid overstating the prepared states’ quality.
- Researchers transferred prepared states between two error-correcting codes, but larger demonstrations remain necessary, and a storage test produced errors about seven times higher than simulations predicted.
Google researchers reduced errors in a crucial quantum computing resource about 40-fold, demonstrating a method that could lower the hardware demands of useful, error-corrected machines.
The experiment, published in Science, showed that a technique called magic-state cultivation works on Google’s Willow processor, according to a Google Quantum AI blog post written by Emma Rosenfeld, research scientist and Craig Gidney, quantum software engineer. The team reported producing states known as T-states with a logical fidelity of 99.99%, which is a measure of how closely a protected quantum state matches its intended form.
The result addresses a problem in quantum computing that preparing these states could consume much of a future machine’s resources and leave less capacity for the calculations it is meant to perform. Google’s demonstration moves a proposed way to reduce that burden from theory to hardware.
The researchers were also able to transfer these prepared states between two forms of quantum error correction as an early test of whether the preparation method can connect with the architecture intended to support larger computations.
The work does not necessarily establish that the resource problem has been solved at a practical scale.
Ultimately, then, this looks to be an important, incremental advance toward practical quantum computing that demonstrates a way to prepare essential quantum states with fewer errors and potentially lower hardware demands. It addresses a significant obstacle, but the researchers expect that translating the advance into useful computations will require larger-scale tests and better methods for storing and using the prepared states.
Why Magic States Matter
Quantum computers process information using qubits, which are vulnerable to disturbances that can corrupt a calculation. Things like heat and electromagnetic interference can throw off a computation. To compensate, error correction spreads information across multiple physical qubits to create a protected unit called a logical qubit.
But protecting information is only part of the task. A useful quantum computer must also perform the full range of operations required by its programs.
Magic states provide a resource for implementing certain operations that are difficult to carry out directly within an error-correcting code with T-states serving as one such resource. They are consumed when used, requiring a computer running a lengthy calculation to keep producing replacements.
According to Google’s post, some estimates suggest that making magic states could occupy as much as 95% of a quantum computer’s capacity. That figure describes the potential burden in resource estimates, rather than a measured allocation on Willow.
The question is therefore not simply whether researchers can prepare a sufficiently accurate state, but can they find a way to produce those states with manageable demands on hardware and time.
Google researchers Gidney, Noah Shutty and Cody Jones developed their cultivation approach in 2024, building on an idea from earlier research, according to the post. The method starts with an imperfect state encoded in a small group of qubits and applies checks designed to detect faulty preparation attempts.
Attempts that fail the checks are discarded while those that pass provide the cultivated states.
Think of this as quality control in a factory. Researchers prepare a quantum state and run it through a series of checks, rejecting attempts that fail and keeping those that pass for use in computation.
That filtering process, known as postselection, is central to the result. The reported quality applies to accepted attempts, making the proportion retained an important consideration alongside fidelity when assessing the method’s eventual computing cost.
Testing the Method on Willow
The experiments used a Willow processor containing 105 superconducting qubits arranged in a square lattice, according to the paper.
Cultivation requires a coordinated sequence of operations and measurements that checks the desired logical state while looking for errors in the physical qubits that support it. The paper also describes additional consistency checks intended to catch faults that could otherwise pass through the preparation process.
Making the protocol work also required substantial calibration and the team leaned into a form of artificial intelligence — AI — to accomplish. In this case, the researchers used reinforcement learning, a form of machine learning that adjusts controls based on feedback, as a final calibration step. The main objective of this step was to reduce the rate at which the circuit detected errors.
For the experiment associated with an error of roughly one part in 10,000, training ran for about four hours immediately before data collection, according to the supplement. The researchers report that adding this calibration improved both the full circuit’s logical error probability and the proportion of retained attempts by about an order of magnitude.
Repeated experiments, including fresh training runs, produced results consistent within their statistical uncertainty, the researchers write.
The headline improvement of about 40-fold compares cultivated states with states prepared without cultivation, according to Google’s post. It is a result for this state-preparation task, rather than a 40-fold improvement in the performance of the processor as a whole.
A Measurement Problem
Establishing the quality of the cultivated states proved to be a completely different ballgame.
Google’s post describes how Rosenfeld encountered measurements that appeared inconsistent with the laws of physics. The paper explains why the team’s original approach could produce misleading results.
The technique, called logical state tomography, estimates a quantum state by combining measurements taken in different ways. The researchers also discarded attempts when error checks indicated a problem.
In the presence of certain noise, however, those different measurements could retain different subsets of attempts. Combining them could then produce an estimate that did not correspond to a physically possible state.
Intriguingly, the same problem could overstate fidelity without producing an obviously impossible answer, the researchers explain in the supplement.
They attributed the behavior to low-frequency phase noise. Possible sources included slow changes in qubit frequencies, residual magnetic fields from control lines and interference from microwave controls. According to the blog post, equipment drift and temperature variation contributed to the measurement difficulty.
The team developed a method called kickback tomography to avoid combining inconsistent measurements. It uses cultivation-based preparation, measurement and checking stages to obtain a self-consistent assessment.
The paper also describes this method as measuring a lower bound on T-state fidelity. Simulations supported its behavior at noise levels relevant to the device, although the researchers identified possible error mechanisms at much lower noise levels as a subject for further investigation.
Connecting Preparation to Computation
Google also tested transferring cultivated states from a distance-3 color code to a distance-5 surface code, according to the post.
Both are methods of encoding quantum information so errors can be detected and managed. Code distance refers to a measure of how many physical qubit errors must combine in certain patterns to cause an undetected logical error. A distance-3 code requires at least three, while a distance-5 code requires at least five, providing stronger protection.
The transfer, which the researchers call grafting, connects an encoding suited to cultivation with another intended for broader use in the computing architecture.
The supplementary material describes the distance-5 grafting experiment as involving 54 qubits.
That transfer is an important step, but the states must also remain useful while waiting for future operations. To investigate that requirement, the researchers extended the number of error-correction cycles after grafting and measured how errors accumulated.
The observed logical error rate was about seven times higher than predicted by simulations, according to the supplement. The researchers identified leakage as the likely main cause, meaning that qubits had moved outside the two states used to encode quantum information.
The simulations did not include leakage, and the experimental circuits lacked dedicated leakage-removal operations. The researchers also reported that readout controls had not been optimized for a configuration change within the grafting circuit.
For future work, the researchers expect better calibration, leakage removal, a simpler circuit arrangement and larger codes to improve performance.
