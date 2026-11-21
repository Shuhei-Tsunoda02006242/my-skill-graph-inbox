---
source: "The Quantum Insider"
prefix: tqi-
title: "Google’s Quantum Chip Beats Classical Limits in Tests of Teamwork"
url: "https://thequantuminsider.com/2026/11/19/googles-quantum-chip-beats-classical-limits-in-tests-of-teamwork/"
published: 2026-11-19
chars: 7218
truncated: false
extraction: full
---

Insider Brief
- Google Quantum AI used its Willow processor to show that quantum contextuality can beat classical limits in cooperative games and help identify hardware errors.
- The chip won the four-qubit magic square game 98.3% of the time against a classical ceiling of 88.9% and beat the classical limit in a separate game with up to 71 qubits.
- A 105-qubit experiment returned valid answers to a mathematical problem more than half the time, though the classical benchmark at that scale remains unproven.
It turns out teamwork can indeed make the dream work, even when the team isn’t allowed to talk. It helps to have a few entangled qubits, though.
In a study, a Google-led team of researchers used a quantum chip to beat the best classical strategies in games that barred players from communicating, demonstrating a way to test what might give quantum computers an edge over classical systems.
The experiments tested a property called quantum contextuality, which is how the results of certain quantum measurements depend on which other measurements are made alongside them, according to the study that Google Quantum AI researchers and collaborators published in the journal Science. In one game designed to test quantum textuality, the researchers reported four quantum bits, or qubits, produced a winning rate of 98.3%, compared with a classical ceiling of 88.9%. In another, the researchers beat the classical limit with as many as 71 qubits, each standing in for a player.
The team also used up to 105 qubits to tackle a mathematical problem designed to test how much work a quantum computer can do in a few steps. The chip returned a valid answer more than half the time at that scale. The researchers’ estimate of how many steps a classical computer would need relies on a conjecture, leaving the size of any quantum advantage in that experiment an open question.
The two games offered a firmer comparison because the rules set a precise limit on how often an ordinary strategy could win. They also gave the researchers a way to measure how much of the quantum effect survived as more qubits were brought into play. The study has implications in quantum error correction, as well, because it suggests that these tests could help engineers spot errors that other checks on quantum hardware can miss.
A game with a built-in contradiction
Admittedly, this game isn’t exactly Uno on the fun scale, but here’s the gist of the assignment:
In the first experiment, two players are given separate assignments on the same three-by-three grid. A referee picks a row for one player and a column for the other. Each player fills their three squares with either +1 or −1. The row must contain an even number of minus signs, including zero, and the column must contain an odd number. The row and column share exactly one square. To win, the players have to put the same number in that square without talking or knowing which row or column the other player was assigned.
The players can agree on a strategy before getting their assignments. Once the referee chooses the row and column, each player has to answer independently. A shared cheat sheet with a fixed answer for each square would run into a contradiction. Each row needs an even number of minus ones, which makes the total for the grid even. Each column needs an odd number, which makes the total for the same grid odd. The best classical strategy can therefore win on eight of nine equally likely assignments.
Google’s team gave each player one qubit from each of two entangled pairs. Entanglement links the results of measurements on the qubits. Depending on the assignment, each player made a different set of measurements on their two qubits. In an ideal system, the resulting answers would agree at the intersection every time. On Google’s Willow hardware, the team ran each of the nine assignments 100,000 times and won 98.3% overall.
The researchers separately measured contextuality using the same arrangement of rows and columns. They carried out sequences of measurements on two qubits, using a third to record the results. On that test, a model in which every measurement has a fixed value independent of what else is measured can score at most 4. The chip scored 5.59, compared with an ideal quantum score of 6. The team attributed the gap to experimental errors.
Adding more players
The second game tested how well the effect held up across a larger part of the chip.
Each player received a zero or a one and returned a zero or a one. The referee guaranteed that the number of ones sent out was even. To win, the players had to make the number of ones they returned odd if half the input total was odd, and even if half that total was even. Each player saw only their own input.
The players could use a shared quantum state known as a GHZ state, short for Greenberger-Horne-Zeilinger. Each player measured their qubit in one of two ways, depending on the number they received. With error-free hardware, the shared state would produce the right combination every time. On the Willow processor, the winning rate stayed above the classical ceiling through 71 players, though the margin shrank as the team added qubits.
In a separate analysis, the researchers verified that as many as 45 qubits were genuinely entangled as a group. That figure measures how many qubits the team could confirm shared a single entangled state. The 71-qubit result measures how far the team could scale the game and still beat the classical winning rate.
A harder test for the hardware
The final experiment moved from games to a problem known as the two-dimensional hidden linear function. The chip received a table of zeros and ones that specified a set of mathematical relationships. Its job was to return a string of zeros and ones that satisfied those relationships.
The researchers encoded each table in a grid of qubits, ran four layers of operations that linked neighboring qubits and checked the answers using a classical simulation.
A 2018 theoretical study showed that, for sufficiently large versions of the problem, a quantum circuit can solve it in a fixed number of layers while a restricted kind of classical circuit needs more layers as the problem grows. A layer is a group of operations that can run at the same time. The earlier proof gives a meaningful comparison at tens of thousands of qubits, according to the Google study.
For the experiments at up to 105 qubits, the team proposed an estimate of the classical requirement. Establishing a mathematical bound at that scale would let researchers determine how much of the predicted advantage survives on hardware with errors.
The tests also gave Google a way to look for small, systematic errors in how the chip carries out its instructions. The team reported that the larger experiments detected errors that had escaped tests based on randomly chosen operations.
For future work, the researchers proposed using the games and the mathematical problem to track hardware improvements. The narrower winning margin at 71 qubits offers one measure of the gap engineers would need to close.
Matt Swayne
Get the latest research, company news, and market intelligence every week.
MENTIONED IN THE ARTICLE
