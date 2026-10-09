# Targets, hypotheses, and strategies

Ranked by (importance × feasibility). Each target lists its current hypothesis, the next
concrete step, and what would refute it. Update the "Current state" lines after every
session.

## T1 (primary): LOLLIPOP-OUTPUT is FP^PSPACE-complete

**Why it matters.** Eppstein lists it as open. It would be the Smith analogue of the
celebrated Goldberg–Papadimitriou–Savani theorem that Lemke–Howson solutions are
PSPACE-complete to compute, and would explain *why* every known exponential family exists:
no shortcut to the lollipop's answer is possible unless P = PSPACE. Membership in
FP^PSPACE is already known, so hardness is the whole result.

**Strategy (GPS template).**
1. Reduce from iterating a reversible circuit (Eppstein, Observation 9), which is
   FP^PSPACE-complete. Build a cubic graph whose lollipop walk passes through
   "macro-states" encoding the circuit's successive states, so the final Hamiltonian cycle
   reveals the output bit.
2. Memory lives in the shape of the current Hamiltonian path: a gadget that the path can
   traverse in two different ways stores one bit. The known exponential families already
   do this; they behave like binary counters.

**Route R (new, Session 2): the walk as zero-player reversible motion planning.**

*Theorem L3 (Mirror Lemma; proved in session 2, see `mirror-lemma.md`; needs an independent check).* Let X be the side of a 3-edge cut of G with v0, its
neighbours and C0's last vertex outside X, and let H = G/X (X contracted to x). Project every
G-state whose endpoint is outside X to an H-state. Then the projected walk moves one step at a
time along H's lollipop line S_0..S_L, and changes direction only during excursions of the
endpoint into X. Consequently the lollipop output of G projects to either H's output (even
number of reflections) or to C0/X (odd number), and in the second case it differs from C0
only inside X.

*Original proof sketch (superseded by the full proof in `mirror-lemma.md`).*
1. A state with endpoint outside X uses exactly two cut edges, so X is covered by one subpath
   between two ports and the projection is a Ham path of H from v0 with the same first edge.
2. A step with endpoint and attachment both outside X commutes with projection (the X-subpath
   is contiguous and only gets reversed). The "forbidden vertex" rule maps across (port ↦ x).
   Since H's state graph has degree ≤ 2 and the rule forbids undoing the previous rotation, the
   projection keeps its direction.
3. **[gap]** An excursion (endpoint inside X) starting at projected state S_i ends at S_j with
   |i − j| ≤ 2. Needs a case analysis of states using all three cut edges (path = Y1 X1 Y2 X2).
   E12 observed j − i ∈ {−2,…,2} always.
4. Termination happens at a Ham cycle whose projection is a Ham cycle of H, i.e. a leaf of H's
   line: S_0 (local swap) or S_L (H's answer).

*Why it matters for T1.* A 3-pole is a stateful reversible mirror: each visit transmits or
reflects the walk and updates X's internal state (which Ham path of X is in use). The walk on
G is then a deterministic, reversible particle moving through stateful gadgets. That is
exactly the setting of Demaine–Hearn–Hendrickson–Lynch, "PSPACE-Completeness of Reversible
Deterministic Systems" (arXiv 2207.07229): zero-player motion planning with reversible
deterministic gadgets is PSPACE-complete (for example with the 3-spinner alone, or any
interacting k-tunnel gadget plus "rotate clockwise").

*Plan.*
- R1. ~~Prove L3.~~ **Done (session 2).** Remaining: independent check, novelty check.
- R2. Compute the full **transducer** of each small 3-pole: for each (entry site type, travel
  direction, internal state) the response (transmit/reflect, new internal state). Enumerate
  all 3-poles up to 12–14 vertices. *Refuted if* every 3-pole's transducer is trivial
  (a pure function of the visit count, e.g. a fixed toggle with no interaction).
- R3. Find a 3-pole (or a small 4-pole) whose transducer simulates a gadget known to be
  PSPACE-complete in the zero-player reversible framework (3-spinner, toggle/locking
  2-tunnel, interacting k-tunnel). Note that a single 3-pole touches many sites of H's line
  (every H-step involving x), which gives the non-local coupling those gadgets need.
- R4. Wiring: build the host H whose lollipop line visits the gadgets in a prescribed order
  (H's own walk can be short; all the complexity should come from reflections). Readout:
  "is the output a local swap inside X1?", i.e. the parity of reflections at X1.
- *Main risk.* The track is the single line S_0..S_L, and sites of a gadget are fixed by H's
  walk. It is unclear whether the framework's wiring freedom can be realised; R4 is where
  this can fail. Also verify L3's novelty: Krawczyk/Cameron/Zhong analyses may use an
  equivalent reflection argument informally.

**Milestones (original GPS route).**
- M1. Reconstruct one known exponential family in code (Briański–Szady or Zhong) and
  reproduce its exact step counts. This validates our understanding of how the families
  store and carry bits. *Refuted if* we cannot reproduce the published counts.
- M2. **3-edge-cut composition hypothesis (H1.1).** If G is obtained by joining G1 and G2
  across a 3-edge cut, the walk on G decomposes into walks on the sides, with an
  interface describable by a finite transducer (which of the 3 cut edges the path uses,
  in which direction). *Test:* build random joins, record the interface sequence, and
  check whether the step count and output on G are determined by small per-side tables.
  All worst cases found so far (E3) have 3-edge cuts, which supports looking here.
- M3. A controlled-toggle gadget: its traversal mode flips if and only if a designated
  control gadget is in mode 1 when the walk passes. Together with M2, this gives
  reversible logic.
- M4. Readout: arrange that the final cycle's use of one designated edge equals the output
  bit.

**Main risk.** The walk's state is a whole Hamiltonian path, so gadgets interact
globally. 3-edge cuts are the natural tool for enforcing modularity, which is why M2
comes before M3.

**Current state.** Session 2: Mirror Lemma L3 strongly supported (E9–E12); route R opened
and ranked above M1. R1 done (theorem). Next: R2 (transducer enumeration).

## T2 (quick win, publishable note): average-case behaviour of the lollipop walk

**Conjecture C2.** On a uniformly random instance (cycle + uniformly random chord
matching, n vertices), the number of lollipop steps divided by n/2 converges in
distribution to Exp(1). In particular E[steps] = (1 + o(1)) n/2.

**Heuristic reason.** If each step's new endpoint behaves like a near-uniform vertex, the
walk stops exactly when the endpoint is one of v0's two eligible neighbours and the
forced edge goes to v0, which happens with probability about 2/n per step: a geometric
waiting time with mean n/2.

**Evidence.** E2 (mean/n between 0.47 and 0.52 for n from 100 to 5000), E5 (KS test
consistent with Exp(1) at n = 1000; finite-size deviation at n = 200).

**Next steps.**
- Measure the endpoint's position distribution along the path during the walk; the
  heuristic predicts near-uniformity after O(1) steps. *Refuted if* positions are strongly
  non-uniform yet the law still holds (then the mechanism is different).
- Proof route: a coupling showing the chords not yet "explored" by the walk are uniformly
  random given the history (principle of deferred decisions), so each step reveals a
  fresh random chord. The difficulty is that the walk revisits chords; control how often.
- Check the model caveat: transfer to random cubic graphs with a random Hamiltonian cycle
  via Robinson–Wormald contiguity.

**Why it is worth doing.** No paper we found studies the lollipop walk's average case.
It contrasts sharply with the exponential worst case: exponential examples are
vanishingly rare. Session 2 adds E7 (reuse is long-range only) and E8 (constant hazard).
Novelty risk: a 2018 Liverpool seminar abstract on random cubic graphs, still to be found. **[verify novelty with a targeted search before writing]**

## T3 (modest): better worst-case base for the lollipop walk

Exact worst cases for n = 6..18: 3, 6, 11, 18, 29, 47, 74 (E1). The consecutive ratios
(about 1.57 per two vertices, i.e. about 1.25 per vertex) exceed the best published base
1.1812 (Briański–Szady). Small-n ratios may not persist, and annealing at n ≤ 34 (E4)
degrades with n and is inconclusive.

**Next step.** Extract the recursive pattern from the exact optima (they share the chords
(0, n−2), (1, 4), (2, n−1) and 3-edge cuts) and test a family built from it at n = 50–200.
*Refuted if* the family's growth rate falls to ≤ 1.1812.

## T4 (long shot): SMITH is PPA-complete, or SMITH ∈ P

Both are major open problems. Do not attempt directly. Watch for: progress on
PPA-completeness of other parity problems (e.g. Sperner variants, necklace splitting,
which became PPA-complete) whose techniques might transfer.

## Ideas parking lot (untested)

- Does the lollipop walk's length relate to the number of Hamiltonian cycles? The worst
  small cases have very few (3–7), while Zhong's family has exponentially many.
- Is the walk length polynomial on cyclically 5-edge-connected cubic graphs? Zhong's
  examples are only 4-connected; this would be a new version of Thomassen's question.
- Restricting to planar triangle-free (or girth ≥ 5) graphs: is the walk still
  exponential?
