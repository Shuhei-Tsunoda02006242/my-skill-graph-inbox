---
source: "The Quantum Insider"
prefix: tqi-
title: "Stanford Physicist Uses AI to Tackle Quantum Gravity Problem"
url: "https://thequantuminsider.com/2026/11/26/stanford-physicist-uses-ai-to-tackle-quantum-gravity-problem/"
published: 2026-11-26
chars: 7627
truncated: false
extraction: full
---

Insider Brief
- Stanford physicist Venkatesa Chandrasekaran proposed a quantum theory of gravity that uses the paths of light to calculate how spacetime can fluctuate.
- The approach yielded a finite result for a graviton-pair calculation that diverges under an approximation and reproduced a known quantum correction to black hole entropy.
- Chandrasekaran said he developed several calculations and proofs through months of work with OpenAI’s GPT-6 Astra, using about 400 million tokens.
A Stanford physicist has proposed a quantum theory of gravity that uses the paths of light to get a finite answer for a calculation that can otherwise run to infinity.
If the approach holds up, it could help reconcile quantum mechanics, which governs the behavior of matter and energy at small scales, with Einstein’s general relativity, which describes gravity as the curvature of spacetime. The study also reproduces a known quantum correction to the entropy of a black hole.
In a preprint posted on arXiv, Venkatesa Chandrasekaran calculated what happens when two gravitons, the hypothetical quantum units of gravitational waves, are created and then disappear. The calculation gave a finite answer even after accounting for waves of arbitrarily short wavelength. An approximation applied to the same calculation produced an infinity.
Chandrasekaran said in the paper’s acknowledgments that he developed several of its calculations and proofs through months of back-and-forth work with GPT-6 Astra, an OpenAI model. He put the total at about 400 million tokens, the units of text AI models process, and said OpenAI provided the computing resources.
The work addresses a problem of reconciling general relativity with quantum theory, a problem that, as mentioned, has vexed top physicists for decades. General relativity treats gravity as the curvature of spacetime. In plain terms, quantum theory allows physical quantities to fluctuate. If spacetime itself fluctuates, the geometry that ordinarily tells physicists where and when something happens also becomes part of what they have to calculate.
Chandrasekaran’s proposal uses the boundaries of finite regions of spacetime to set up those calculations. The boundaries follow paths that light could take, and their shape can change with the gravitational field. That gives the calculation a way to specify where something happens even as the geometry changes.
The study also finds that a region bounded this way, with a specified maximum size, can hold only a finite number of mutually distinguishable quantum states. In a separate calculation for a large black hole, the approach recovered both the standard relationship between a black hole’s entropy and its surface area and a previously calculated quantum correction.
It’s important to note that the paper is theoretical and presents no experimental test.
Using Light to Set the Boundaries
To calculate how gravity behaves when spacetime itself can fluctuate, Chandrasekaran starts by defining the region he wants to study. He uses the paths light can take between two events to set its boundaries.
One way to envision this is to imagine a flash going off and a detector set to record light at a particular moment later. Light spreading out from the flash marks one boundary. Tracing the possible paths of light backward from the detector at that moment marks the other. The two boundaries enclose a region called a causal diamond. Any point inside it can receive a signal from the flash and send one in time to reach the detector.
In general relativity, gravitational waves can distort those boundaries. The paper treats the surface where they meet as part of the system and locates quantities relative to it. Chandrasekaran first solves the classical equations that constrain which combinations of boundary data are possible. He then applies quantum rules to the remaining variables, which include the two ways a gravitational wave can be polarized.
To describe a larger stretch of spacetime, the paper joins regions along shared boundaries. It matches the gravitational data on the two sides and sums over the quantum states that can occur at an intermediate stage. Chandrasekaran shows that these intermediate sums converge within the construction. In fact, they converge even when the set of possible states is infinite.
The order of operations matters, as the graviton-pair calculation shows.
In practice, physicists often start with a rough answer and refine it by adding corrections based on the strength of the interaction.
In this example, expanding in Newton’s gravitational constant before adding the contributions from different wavelengths produces a term that grows without bound. Keeping the constant at its physical, nonzero value and doing the sum first gives a finite answer. At very short wavelengths, contributions that would otherwise drive the divergence partly cancel.
Counting States Inside a Black Hole
For the state-counting result, Chandrasekaran imposes a maximum size on a macroscopic causal diamond using what he calls a gravitational clock. The clock is a distance-like reading defined along the paths of light. Gravitational radiation changes that reading by affecting how neighboring light paths converge. Putting an upper limit on the reading also restricts which wave states can fit within the region.
The study concludes that a causal diamond with a fixed size limit can contain only a finite number of distinct quantum states. That means the area where the two light cones meet can take only certain values, with gaps between them.
The black hole calculation uses a surface where a bundle of outward-directed light rays momentarily stops spreading. The local gravitational data are enough to identify that surface and begin counting states on its interior side.
By summing over interior states, Chandrasekaran recovers the leading term in the Bekenstein-Hawking formula, which makes a black hole’s entropy proportional to its horizon area. Entropy describes how much microscopic information is compatible with the same large-scale description.
For a large, nonrotating black hole, the study also found a small adjustment to the standard entropy formula that grows slowly as the black hole’s surface area increases. The result matches an earlier calculation by physicist Ashoke Sen that held the black hole’s mass fixed and accounted for small variations in its spin.
Next Steps
A lot of work remains.
The four-dimensional theory covers gravity in a vacuum, where gravitational waves can propagate. Extending it to include matter would widen its scope. The calculation also recovers Einstein’s equations in the low-energy limit for initial quantum states concentrated around a classical geometry. It calculates the first quantum correction in that regime, including how fluctuations in gravity in turn affect the average geometry.
One question Chandrasekaran leaves for future work is whether different choices in building the quantum state space lead to equivalent theories for the same range of clock readings. Another test would be to carry the black hole and low-energy calculations beyond the first quantum correction.
For a deeper, more technical dive, please review the paper on arXiv. It’s important to note that arXiv is a pre-print server, which allows researchers to receive quick feedback on their work. However, it is not — nor is this article, itself — official peer-review publications. Peer-review is an important step in the scientific process to verify results.
Matt Swayne
Get the latest research, company news, and market intelligence every week.
MENTIONED IN THE ARTICLE
