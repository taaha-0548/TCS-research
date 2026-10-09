# T1 roadmap: Eppstein's question (is LOLLIPOP-OUTPUT FP^PSPACE-complete?)

Status after session 6. All claims are labelled: **theorem** (proof written), **empirical**
(exact agreement in large tests, proof not yet written), **idea** (untested).

## 1. The reduction stack (what works)

1. **Mirror Lemma** (theorem): across a 3-edge cut, the walk projects to the contracted graph's
   walk, with stays and reversals.
2. **Transducer Theorem** (theorem): every 3-pole is a host-independent finite automaton;
   visit → (TRANSMIT/REFLECT, successor path, cost).
3. **General Composition** (empirical, 804k visits with memory, all exact): the automaton of
   P'[x ← X] is computable from P' and X's automaton, for any X.
4. **Line–Mirror Reduction** (empirical, ~182k hosts, all exact): walk on H[x_i ← X_i] = particle on
   H's line, with gadget automata at the sites (passages through x_i).
5. **Clock Theorem** (empirical, exact for k ≤ 7): in the nested host, each vertex's site sequence is
   a morphic word.
6. **Retrace Lemma** (proof sketch; empirical 6,485/6,485): crossing back through a site with the
   gadget unchanged undoes the earlier crossing. **Obstruction:** single-site gadgets are
   computationally trivial (≤ 1 reflection; longest run 2N − 1).

## 2. The right computational model: towers = Turing machines (idea, partly checked)

Tower: P_1 = P'[x ← P_2], …, P_k = P'[x ← P_{k+1}] (P' a fixed gadget with slot x). One visit to
level j runs P''s internal dynamics, and each passage through x is a call to level j+1.
- tape cell j = level j's internal path (persistent state);
- head moving right = call (carries a visit type: oriented port pair × kind, ≤ 12 values);
- head moving left = return (carries TRANSMIT/REFLECT);
- any head walk on a one-sided tape decomposes into nested excursions, so call/return loses
  nothing;
- input = the initial Hamiltonian cycle (chooses every level's path); **output = the returned cycle
  (contains every level's final path)**. Readout is free.

Evidence:
- minimal-machine sizes by depth (`phase3/tower.py`): three regimes. Bounded (3, 3, 3 …: finite
  state, easy); polynomial (7, 9, 10, 11 …); **exponential and incompressible** (12 → 48 → 192 →
  768 → 3072, ×4 per level, no merging). The last is a necessary condition for hardness.
- calls per visit (`phase3/calls_per_visit.py`): for some P' the number of calls a single visit
  makes grows with depth (3, 4, 5, 7, 10). The parent can shuttle against its child, so shallow
  cells are not limited to a bounded number of excursions (the feared asymmetry obstruction does
  not apply).

## 3. What does not work

- Flat designs on a host line: single-site gadgets are trivial (Retrace), and random multi-site
  interleavings grow only polynomially (`phase2/multisite.py`).
- Random combinations trivialise: e.g. towers plugged into the clock reflected at the very first
  visit for every initial state and wiring (`phase3/clock_tower.py`). Random search will not find a
  universal construction; it must be designed.
- (For the record) the clock host is not needed: a single top visit of a deep tower is already the
  whole computation.

## 4. Plan

**S1. Abstract theory (no graphs).** Define the *recursive bounce machine* (RBM): cells with finite
persistent state and a finite reversible cell procedure (entry symbol from the parent; sequence of
calls to the child with T/R answers; return T/R). Prove that RBMs simulate reversible Turing machines
with polynomial overhead. Left-moving information is only 1 bit, so the parent must recover the
head state by repeated calls (Shannon-style shuttling; reversible variants of small-state TM
constructions, e.g. by Morita, to be checked). Outcome: Eppstein's question reduces to realising a
finite list of cell procedures by gadgets.

**S2. Realisability ("gadget compiler").** Search small P' (with extra slots holding fixed memory
gadgets, each composed exactly by `phase1/compose.py`) for the cell procedures S1 needs, matching
minimal automata exactly. Constraints to respect: slot vertices not ports, gadgets at distance ≥ 3,
standing hypothesis at the top.

**S3. Assembly.** A polynomial-time map from (reversible TM, input) to (cubic graph, Hamiltonian
cycle, edge) such that the lollipop output encodes the TM's output. Membership in FP^PSPACE is known
(Eppstein), so this would give completeness.

**Possible obstruction to watch for.** An invariant of realisable cell procedures, e.g. Smith-type
parity (h_ab ≡ h_ac ≡ h_bc mod 2) or orientation constraints, that forces towers to be predictable.
If S2 keeps failing on a specific procedure, look for such an invariant: it would be a publishable
negative result (3-cut gadgets are not universal).

**Honest odds.** Full solution: 10–20%. S1 alone (RBM universality) is a clean, likely-true
statement. Combined with sections 1–2 it would make a solid paper on the structure of the lollipop
walk even without S2.
