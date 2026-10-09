---
name: smith-second-hamiltonian
description: Research workspace for Smith's theorem and the complexity of finding a second Hamiltonian cycle in cubic graphs (Thomason's lollipop algorithm, PPA, FP^PSPACE, Krawczyk/Zhong/Briański–Szady exponential families, Bazgan–Santha–Tuza, Deligkas–Mertzios–Spirakis–Zamaraev, Björklund–Kaski–Nederlof bipartite Pfaffian). Use this skill whenever the user mentions Smith's theorem, second or another Hamiltonian cycle, the lollipop method, Thomason chains, PPA-completeness of Smith, Eppstein's iterated reversible computation question, or wants to continue, test, or update hypotheses in this research program, even if they only say "the Smith problem" or "our Hamiltonian cycle research".
---

# Smith's Problem: Research Workspace

This skill holds a progressively updated research program on the complexity of finding a
second Hamiltonian cycle in cubic graphs. It has three jobs: keep the literature and the
status of every open question in one place, provide verified code for experiments, and
keep an honest log of what has been tried and what it showed.

## Start of every session

1. Read `references/research-log.md` (latest entries first) to see where the work stands.
2. Read `references/open-problems.md` for the ranked targets and the current hypothesis.
3. Before claiming anything is new, search for papers newer than the newest entry in
   `references/literature.md`. This area moves; Eppstein's question or PPA-completeness of
   Smith could be resolved at any time.

## Problems (precise statements)

- **SMITH** (total search problem, in TFNP, in PPA [Papadimitriou 1994]).
  Input: cubic graph G and Hamiltonian cycle C0. Output: a Hamiltonian cycle C1 ≠ C0.
  Status: not known to be in P, not known to be PPA-complete.
- **SMITH-THROUGH-EDGE**. Input additionally fixes an edge e of C0; output a second
  Hamiltonian cycle through e. (Smith's theorem: the number of Hamiltonian cycles through
  e is even.)
- **LOLLIPOP-OUTPUT** (functional problem, in FP^PSPACE [Eppstein]). Input: G, C0, a
  fixed edge e = (v0, v1) of C0 and its orientation. Output: the specific cycle that
  Thomason's lollipop walk reaches. Status: whether it is FP^PSPACE-complete is open
  (Eppstein, "The Complexity of Iterated Reversible Computation", TheoretiCS).
- **Lollipop running time**. Exponential in the worst case (Krawczyk 1999; Cameron 2001;
  Zhong 2018, cyclically 4-edge-connected bipartite, 2^{n/16}; Briański–Szady 2022,
  planar 3-connected, Ω(1.1812^n)). Linear on cubic bipartite Pfaffian graphs
  (Björklund–Kaski–Nederlof, ICALP 2024).

The Mirror Lemma (3-edge-cut projection theorem) and its proof are in
`references/mirror-lemma.md`.

The full annotated bibliography, with what each paper proves, is in
`references/literature.md`.

## Status map (one line each; update when something changes)

| Question | Status | Where |
|---|---|---|
| SMITH in P? | open | literature.md §1 |
| SMITH PPA-complete? | open | literature.md §1 |
| LOLLIPOP-OUTPUT FP^PSPACE-complete? | open, **primary target** | open-problems.md T1 |
| 3-edge-cut gadgets (Mirror Lemma L3) | **theorem (session 2; needs an independent check)**: C1(G)/X ∈ {C0/X, C1(G/X)}; a 3-pole is a stateful mirror | references/mirror-lemma.md, research-log E9–E13 |
| Transducer Theorem | **proved from the case analysis, exact check E14**: walk on G = walk on G/X + finite reversible automaton per 3-pole; active-memory poles common (E15) | references/mirror-lemma.md |
| Lollipop worst-case base | ≥ 1.1812 (B–S); nested K=8 family reaches ≈ 1.1975 per vertex up to n = 50, inconclusive, no proof | research-log E1, E4, E16–E17 |
| Lollipop on random instances | **our data: mean ≈ n/2, up to n = 5000; attach point uniform, 17% edge reuse (E6)**; no proof | research-log E2, E6, open-problems T2 |
| Cyclically 4-edge-connected route (Thomassen) | closed: Zhong 2018 gives exponential examples | literature.md §3 |
| Fastest exact algorithm for SMITH | O(1.23103^n) det., poly space (DMSZ, MFCS 2020) | literature.md §2 |

## Code

All code is in `scripts/`. Every experiment script writes a JSON result file next to it.

- `lollipop.py`: the verified core.
  - `lollipop(n, chord, v0, dirn)` runs Thomason's algorithm and returns `(steps, cycle)`.
  - `is_ham_cycle`, `count_ham_cycles_through` verify results independently.
  Note: run the scripts with plain `python3` from `scripts/` (not `-I`), since they import
  `lollipop` and `general` from the same folder.
  - `random_instance`, `all_instances` generate instances.
  - Run `python3 lollipop.py` for the self-test; run it after any change.
- `exp_worst_small.py N`: exact worst case over all configurations for n ≤ N (n = 18 takes
  about 2.5 minutes).
- `exp_random.py`: lollipop length on random instances.
- `exp_worst_structure.py`: connectivity and cycle counts of the worst instances.
- `general.py`: lollipop on arbitrary cubic graphs (adjacency lists), Ham-path enumeration,
  and `substitute` (replace a vertex by a 3-pole, with every extension of C0 through it).
- `exp_3pole_*.py`, `exp_mirror.py`: 3-pole transparency, state dependence, mirror test.
- `transducer.py`, `show_transducer.py`: host-independent 3-pole automata;
  `exp_transducer_check.py` (E14), `exp_pole_survey.py` (E15).
- `nested*.py`, `chains.py`: nested 3-pole families for the worst-case base (E16–E18).
- `exp_t2_*.py`: T2 mechanism tests (attach position, reuse, hazard).
- `exp_search_long.py n1 n2 ...`: simulated annealing for long walks (35 s per n). Keep
  each run under the 300 s tool limit.

**Instance representation.** Every cubic Hamiltonian graph with a marked Hamiltonian cycle
is, up to relabelling, the cycle 0-1-…-(n-1)-0 plus a perfect matching of chords. So
`chord[v]` (v's third neighbour) fully describes an instance, and enumerating chord
matchings enumerates every configuration. The uniform distribution over chord matchings
avoiding cycle edges is the "random cycle + random matching" model, which is closely
related to random cubic graphs (Robinson–Wormald contiguity). State that caveat whenever
quoting E2.

## Research workflow

Each idea moves through four stages, and the log records which stage it reached.

1. **Hypothesis.** State it precisely, in a form that could be false.
2. **Test.** Design the cheapest experiment that could refute it. Prefer exhaustive small
   cases plus random large cases. Write a new `exp_*.py` script rather than editing old ones,
   so earlier results stay reproducible.
3. **Verdict.** Supported, refuted, or inconclusive, with the numbers. An inconclusive
   result is recorded as inconclusive, not rounded up.
4. **Next step.** Either a proof attempt (write the proof sketch in the log, with every gap
   marked) or a sharper hypothesis.

## Rules that protect the work

- Keep three labels distinct in all writing: **theorem** (proved and checked),
  **conjecture** (supported by data), **idea** (untested). Never upgrade a label without
  the evidence that justifies it.
- Every claim about prior work cites an entry in `references/literature.md`. If a fact is
  not in that file, verify it from the source before using it, then add it.
- Experimental evidence never establishes a complexity result. It can refute a hypothesis
  or suggest a construction; proofs are separate.
- After each session, append a dated entry to `references/research-log.md` and update the
  status map above if anything changed.
