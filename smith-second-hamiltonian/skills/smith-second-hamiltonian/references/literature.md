# Literature: Smith's problem and the lollipop algorithm

Last literature sweep: October 2026 (session 2: nothing new resolves Eppstein's question or
PPA-completeness of SMITH). Entries marked **[verify]** have details not yet
checked against the original source.

## Contents
1. Foundations and complexity classes
2. Algorithms for a second Hamiltonian cycle
3. Running time of the lollipop algorithm
4. Path-following algorithms and PSPACE: the template for target T1
5. Related structural results

## 1. Foundations and complexity classes

- **Smith (1946), via Tutte.** In a cubic graph, every edge lies in an even number of
  Hamiltonian cycles. Hence every Hamiltonian cubic graph has at least three Hamiltonian
  cycles. Proof is a non-constructive parity argument.
- **Thomason (1978)**, "Hamiltonian cycles and uniquely edge colourable graphs", Ann.
  Discrete Math. 3:259–268. Constructive proof: the lollipop walk. The states are
  Hamiltonian paths starting with a fixed edge; each state has degree ≤ 2, and the
  degree-1 states are exactly those that close to a Hamiltonian cycle. This pairs up the
  Hamiltonian cycles through the edge.
- **Papadimitriou (1994)**, "On the complexity of the parity argument and other inefficient
  proofs of existence", JCSS 48(3):498–532. Defines PPA using this example; SMITH ∈ PPA.
  PPA-completeness of SMITH is open.
- **Eppstein**, "The Complexity of Iterated Reversible Computation", arXiv 2112.11607,
  published in TheoretiCS (2023). Shows connected-leaf problems (find the other leaf of the
  same path in an implicit graph of max degree 2) are FP^PSPACE-complete in general, and
  that LOLLIPOP-OUTPUT is in FP^PSPACE. Explicitly states that FP^PSPACE-completeness of
  LOLLIPOP-OUTPUT is **open**, as is PPA-completeness of SMITH.

## 2. Algorithms for a second Hamiltonian cycle

- **Bazgan, Santha, Tuza (1999)**, J. Algorithms. Longest path is not constant-factor
  approximable in cubic Hamiltonian graphs unless P = NP, but given a Hamiltonian cycle
  there is a PTAS (linear time) for finding another cycle of length (1 − ε)n.
- **Deligkas, Mertzios, Spirakis, Zamaraev (MFCS 2020)**, "Exact and Approximate Algorithms
  for Computing a Second Hamiltonian Cycle", arXiv 2004.06036. Deterministic
  O(n · 2^{0.299862744n}) = O(1.23103^n), linear space; O(1.22876^n) without induced C6.
  Structural lemma: the lollipop output C1 satisfies C0 Δ C1 connected. Also a linear-time
  algorithm for a long second cycle in general Hamiltonian graphs.
- **Algorithmica 86:2766–2785 (2024)**: randomized algorithm for a second Hamiltonian cycle
  in Hamiltonian graphs of large minimum degree via red-independent/green-dominating sets.
  **[verify authors; likely the DMSZ group]**
- **Thomassen (1998)**, JCTB: every Hamiltonian r-regular graph with r ≥ 300 has a second
  Hamiltonian cycle, with a polynomial algorithm via independent dominating sets.
  **[verify; later improvements to smaller r by Haxell–Seamone–Verstraete]**
- **Björklund, Kaski, Nederlof (ICALP 2024)**, "Another Hamiltonian Cycle in Bipartite
  Pfaffian Graphs", arXiv 2308.01574. In bipartite Pfaffian graphs of min degree 3 (where
  Hamiltonicity is NP-complete), another Hamiltonian cycle is found in linear time and in
  logspace. The lollipop walk takes at most n steps in cubic bipartite Pfaffian graphs,
  confirming Haddadan's conjecture for cubic bipartite planar graphs. They know of no
  other graph class with a polynomial bound on the lollipop walk.

## 3. Running time of the lollipop algorithm

- **Krawczyk (1999)**, "The complexity of finding a second Hamiltonian cycle in cubic
  graphs", JCSS 58(3):641–647. First exponential lower bound (planar family).
- **Cameron (2001)**, Discrete Math. 235:69–77. Exponential on Krawczyk's graphs, through a
  given edge.
- **Thomassen's observation** (via Zhong; IML problem collection, arXiv 1511.00270,
  Problem 5.5): a polynomial algorithm for cyclically 4-edge-connected cubic graphs would
  give one for all cubic graphs. Problem 5.5 asked for cyclically 4-edge-connected
  families with superpolynomial lollipop walks.
- **Zhong (2018)**, "The complexity of Thomason's algorithm for finding a second Hamiltonian
  cycle". Answers Problem 5.5: cyclically 4-edge-connected cubic **bipartite** graphs with
  16(i + 1) vertices where the walk takes 12(2^i − 1) + 3 steps, i.e. Θ(2^{n/16}). Unlike
  earlier families, these have exponentially many Hamiltonian cycles.
- **Briański, Szady (2022)**, "A short note on graphs with long Thomason chains", Discrete
  Math. 345(1):112624, arXiv 1903.02515. 3-connected planar cubic family with
  Ω(1.1812^n) steps; best known base.
- **Open (IML problems 5.3, 5.4)**: existence of 3-connected cubic bipartite graphs with an
  edge in exactly two Hamiltonian cycles, or with exactly four Hamiltonian cycles.

## 4. Path-following algorithms and PSPACE: the template for target T1

- **Goldberg, Papadimitriou, Savani (FOCS 2011)**, "The Complexity of the Homotopy Method,
  Equilibrium Selection, and Lemke-Howson Solutions", arXiv 1006.5352. Computing the
  specific equilibrium found by Lemke–Howson is PSPACE-complete; the homotopy method's
  output is PSPACE-complete. Reduction from OEOTL (other end of this line). This is the
  closest precedent for proving LOLLIPOP-OUTPUT hard.
- **Savani, von Stengel (2006)**: exponentially long Lemke–Howson paths (the "exponential
  examples" that preceded the PSPACE result, analogous to Krawczyk/Briański–Szady here).
  **[verify exact reference]**
- **Bennett (1984); Lange, McKenzie, Tapp (2000)**: reversible space equals deterministic
  space; underlies FP^PSPACE-completeness of connected-leaf problems.
- **Demaine, Hearn, Hendrickson, Lynch (2022)**, "PSPACE-Completeness of Reversible
  Deterministic Systems", arXiv 2207.07229. Any system implementing three basic gadgets is
  PSPACE-complete; zero-player motion planning with any reversible deterministic interacting
  k-tunnel gadget plus "rotate clockwise" is PSPACE-complete; the 3-spinner alone suffices.
  Template for route R of T1. **[read full text: gadget definitions, wiring model]**
- **Ani, Demaine, Hendrickson, Lynch**, "Trains, Games, and Complexity: 0/1/2-Player Motion
  Planning through Input/Output Gadgets", WALCOM 2022 / TCS 969 (2023), arXiv 2005.03192.
  Zero-player motion planning with branchless connections; PSPACE-completeness results.
- Simplex method precedents (Disser–Skutella 2015; Fearnley–Savani 2015): following the
  simplex path with certain pivot rules is PSPACE-complete. **[verify details]**

## 5. Related structural results

- **Goedgebeur, Meersman, Zamfirescu (2018/19)**, "Graphs with few Hamiltonian Cycles",
  arXiv 1812.05650. Infinitely many cubic graphs with exactly three Hamiltonian cycles;
  open small cases for girth 4. **[verify authorship]**
- Infinite cubic graphs (arXiv 1705.07031): second Hamilton cycles in one-ended cubic
  graphs with end degree ≤ 3; uniquely Hamiltonian infinite cubic examples exist (Heuer).
