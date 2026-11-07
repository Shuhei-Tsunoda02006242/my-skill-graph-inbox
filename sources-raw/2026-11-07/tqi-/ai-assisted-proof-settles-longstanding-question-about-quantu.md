---
source: "The Quantum Insider"
prefix: tqi-
title: "AI-Assisted Proof Settles Longstanding Question About Quantum Speedups"
url: "https://thequantuminsider.com/2026/11/06/ai-assisted-proof-settles-longstanding-question-about-quantum-speedups/"
published: 2026-11-06
chars: 12000
truncated: true
extraction: full
---

Insider Brief
- A proof of the Aaronson-Ambainis conjecture establishes that exponential quantum advantages in input reads require structure when answering yes-or-no questions on most randomly generated inputs.
- PSI said its research system used a non-public Anthropic model to find the proof, which was checked in the Lean proof assistant and reviewed by researchers.
- The theorem limits data reads rather than total computing time, leaving room for practical quantum advantages and further work to strengthen its mathematical bounds.
A mathematical proof has resolved a conjecture open since 2008 about when quantum computers can achieve enormous advantages over conventional machines, establishing a limit on their ability to outperform classical algorithms on unstructured inputs.
The result proves the Aaronson-Ambainis conjecture, which connects a question about mathematical functions to whether dramatic speedups require special structure in the problems being solved, a central issue in quantum computing, namely.
For quantum computing, the practical implication is a clearer direction for quantum algorithm research toward problems whose mathematical or physical structure offers an advantage. The theorem strengthens the theoretical basis for that approach, although it does not ultimately determine which applications will deliver useful speedups.
According to a paper posted on git hub by David Turturean of Physical Superintelligence, or PSI, the answer is yes within a widely used framework that measures how often an algorithm accesses its input. For yes-or-no computations, a classical algorithm can approximate a quantum algorithm’s probability of answering yes on most uniformly random inputs without needing exponentially more accesses.
PSI said in an accompanying blog post that an internally developed research system, using instances of a non-public Anthropic model, found a complete proof during the third day of a run. The paper says the main theorem and its formulation of the original conjecture were formalized in Lean, a proof assistant, and checked by its kernel, the software component that verifies the logical steps.
The Boundary Between Quantum and Classical
The finding sharpens the theoretical boundary between quantum and classical computing. It establishes a limit on how often a computer must read the data supplied to a problem, known as its input. That measure does not account for all the work needed to process the data, so the theorem does not establish a general limit on total computing time or the commercial value of quantum machines.
The conjecture takes its name from Scott Aaronson and Andris Ambainis, whose work connected the quantum computing question to a statement about polynomials. The new paper traces the conjecture to a 2008 lecture by Aaronson and builds on a series of results from mathematics and theoretical computer science.
One reason the question matters is that quantum computing’s best-known potential advantages exploit patterns.
Peter Shor’s factoring algorithm, introduced in 1994, uses quantum computation to find the period of a repeating mathematical function. That approach offers a route to factoring large numbers far faster than any known classical method. As PSI’s blog explains, the periodic pattern supplies structure that a quantum algorithm can exploit.
The Aaronson-Ambainis question concerns what happens when such favorable conditions are absent. Can a quantum algorithm still gain an exponential advantage when presented with a uniformly random string of zeros and ones?
The Query Model
To study that question, researchers use the query model. Instead of counting every operation a computer performs, the model counts its requests for information about an input. A classical query reads a bit at a selected position. A quantum query can act on a superposition of positions, allowing the algorithm to use interference as it processes information.
If that sounds a bit esoteric, imagine the input as a row of closed boxes, each holding a zero or a one. A classical query opens one box and reads its contents. A quantum query can interact with several boxes at once, but it does not reveal everything inside them. Instead, a quantum algorithm combines the effects of those interactions to uncover information about the collection, such as a hidden pattern.
If even that sounds a bit esoteric, it may be better to know that the framework gives researchers a precise way to compare the information each kind of machine needs. It also makes the result narrower than a claim that conventional computers can efficiently reproduce everything quantum computers do.
The paper establishes that, for a quantum algorithm making a given number of queries, there is a deterministic classical algorithm that approximates its acceptance probability — its probability of answering yes — on all but a chosen small fraction of inputs. For fixed accuracy and a fixed allowance for exceptional inputs, the classical query count grows as a fixed power of the quantum query count.
In other words, for most randomly generated inputs, a conventional computer can estimate the quantum algorithm’s probability of answering yes without needing vastly more reads of the data. The finding concerns those reads, rather than the total time needed to produce an answer.
Earlier research supplied a crucial link between quantum computing and mathematics. It showed that a quantum algorithm’s probability of answering yes can be described by a mathematical formula, with the formula’s complexity limited by how often the algorithm reads its input.
The formula translates the input data into the probability that the quantum algorithm will answer yes. It also captures how different pieces of that data work together to affect the answer.
Aaronson and Ambainis proposed that, for the mathematical formulas describing these quantum algorithms, there must be at least one piece of input data with a measurable effect on the result whenever that result varies meaningfully across inputs.
That would give a conventional computer a way to decide what information to read next. Rather than examine every bit of data, it could focus on bits that most affect the quantum algorithm’s probability of answering yes.
The method described in PSI’s blog assumes the conventional computer already knows the formula describing that probability. It reads an influential bit, updates its assessment and then selects another. Once the unread data has little effect on the prediction, it stops and estimates the probability by averaging over the remaining possibilities.
The conjecture was the missing guarantee that this process could make sufficient progress without requiring exponentially more reads of the data.
Supplying the Guarantee
Turturean’s paper supplies that guarantee. It establishes a minimum effect that at least one input bit must have, based on the complexity of the formula and how much its result varies. Crucially, adding more input bits does not, by itself, weaken the guarantee.
According to the paper, earlier mathematical results offered guarantees that became too weak as the formulas grew more complex. The new result overcomes that obstacle and establishes the relationship needed to prove the conjecture.
The proof builds on an approach developed by Shachar Lovett and Jiapeng Zhang. Their strategy examines which inputs produce results above or below a series of thresholds, providing a way to study how changes in the data affect the outcome.
A central advance is a new method of matching different arrangements of input data, according to the study. The matching follows restrictions on where the arrangements agree or differ, allowing the proof to connect changes in individual bits to the behavior of the formula as a whole. It strengthens an earlier mathematical result known as David Reimer’s Butterfly Lemma.
The paper also finds that one mathematical claim proposed by Lovett and Zhang does not hold in its stated general form. The new proof retains their broader strategy while replacing that claim with a different result.
The advance follows recent progress on a narrower version of the quantum computing question. According to PSI’s blog, Stanford University researchers Guy Blanc, Jordan Docter, Carmen Strassle and Li-Yang Tan showed in August 2026 that quantum algorithms could not achieve exponential savings in data reads on random inputs when restricted to a fixed number of rounds, with multiple reads allowed in each round.
PSI said those researchers have been reading the full proof, providing comments and preparing a shorter explanation for experts. The paper acknowledges their contributions.
That work complements the checks performed by Lean. The software verifies that the formalized proof follows its mathematical rules, while researchers can examine the reasoning, explain why it works and assess its implications.
The paper also describes how AI contributed to the discovery. Multiple instances of the Anthropic model searched existing research, proposed ideas, combined approaches and tested arguments. Some instances coordinated work among others within the research system Turturean developed.
Turturean selected and defined the problem, operated the system and prompted a model to assemble the results into a first draft. According to the paper’s disclosure, he personally reviewed and edited the draft and takes responsibility for its correctness.
The first complete proof emerged during the third day of the run, according to the paper’s discovery timeline. It settled the conjecture with a weaker guarantee than the final version.
After the model instances were directed to investigate related open problems, they twice improved the mathematical bound. The initial proof and both improvements were checked in Lean, according to the appendix.
The account documents a substantial AI-assisted discovery, although it does not establish how consistently the system could solve other longstanding problems. The model used in the run is non-public, and the work relied on a research system developed and operated by humans.
Limits and Future Work
The quantum computing result also has important limits.
It allows a conventional computer to estimate a quantum algorithm’s probability of answering yes for most randomly generated inputs, within a chosen margin of error. It does not guarantee an accurate estimate for every input or show how to reproduce every kind of quantum computation.
The result also concerns how often a computer needs to read its data. It does not account for all the work required to decide which bits to read or calculate an answer.
This might bear out in practice when a conventional computer might need relatively few reads but still perform a large amount of computation between them. The paper’s explicit guarantee also permits a substantial number of reads, particularly when a highly accurate estimate is required. Establishing that the cost avoids exponential growth does not necessarily make the method practical.
The theorem therefore leaves room for substantial quantum advantages, including more moderate speedups on unstructured inputs and dramatic gains on problems with useful structure.
As for further mathematical questions, the paper does not establish the strongest possible guarantee for how influential an input bit must be. Improving that guarantee could tighten the resulting limits on how many reads a conventional computer needs.
The manuscript also asks whether its central matching step can be achieved through a direct construction. The current proof establishes that a suitable matching exists through an algebraic argument. A direct method could make that part of the reasoning easier to understand and use.
With the conjecture resolved, researchers may take part in future research to pursue those sharper limits and investigate what the proof’s methods reveal about other problems in mathematics and computing.
Matt Swayne
Get the latest research, com
