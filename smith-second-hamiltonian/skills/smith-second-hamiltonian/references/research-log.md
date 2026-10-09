# Research log

Newest session first. Each experiment: hypothesis, method, numbers, verdict, next step.
Result files are in `scripts/` with the same E-number.

---

## Session 2 (October 2026): T2 mechanism, then pivot to T1 gadget theory

### E6: attach position and chord freshness (`exp_t2_mechanism.py`)
- Hypothesis (mechanism behind C2): the walk's attachment point is near-uniform along the
  path, so each step closes the cycle with probability ~2/n.
- Method: n = 1000, 300 random instances; record attach position i/n per step and whether
  the added edge was already added earlier in the walk.
- Attach-position deciles: 0.098–0.101 in every decile (uniform), with no burn-in effect
  (identical after skipping the first 20 steps).
- Fresh edges: 82.8% of steps add an edge never added before; **17.2% reuse an edge**.
- Mean steps/(n/2) = 0.99 (consistent with E2, E5).
- Verdict: **mechanism supported** (uniform attachment from step 1). The reuse rate is not
  negligible: a deferred-decisions proof must handle a constant fraction of revisited
  edges, not a vanishing one.
- Next step: classify reused edges (cycle edges vs chords; immediate back-and-forth vs
  long-range) and test whether conditioning on the history keeps the attach position
  uniform on reuse steps too. Then write the proof sketch with gaps marked.

### E7: what the walk re-adds (`exp_t2_reuse.py`, `e7_reuse_n*.json`)
- Reuse fraction 16.7% (n = 1000), 18.6% (n = 200). Chords make up ~60% of added edges, both
  among fresh and among reused edges (no bias).
- Reuse is never short-range: > 99.8% of reuses come ≥ 10 steps after the previous addition.
- Attach position is uniform on reuse steps too (deciles 0.094–0.104).

### E8: stopping hazard over time (`exp_t2_hazard.py`, `e8_hazard_n*.json`)
- hazard × (n/2) stays ≈ 1 (0.87–1.18, noise) for t = step/(n/2) from 0 to 2, n = 400 and
  1500, while P(reuse) climbs roughly linearly in t (0.004 → 0.39).
- Verdict: **memoryless stopping supported** despite growing reuse. C2's Exp(1) law is
  consistent with a constant-hazard mechanism; reuse does not bias the stopping chance.
- Novelty risk: a 2018 Liverpool seminar abstract reportedly mentions polynomial-time results
  for SMITH on random cubic graphs. Page unreachable from here (DNS). **Find it before
  writing T2 up.**

### Pivot to T1 (user decision): gadget theory for 3-edge cuts

### E9–E11: are 3-poles transparent? (`general.py`, `exp_3pole_transparency.py`,
`exp_3pole_state.py`, `exp_3pole_classify.py`, `e9_3pole.json`)
- Setup: host H (random cubic Hamiltonian graph, n = 10–30); replace a vertex x (away from
  v0) by a 3-pole X = (small cubic graph minus a vertex); extend C0 through X in every possible
  way; compare the walk on G, projected back to H, with the walk on H.
- Smith parity check: h_ab ≡ h_ac ≡ h_bc (mod 2) for every pole, where h = number of Ham
  paths of X between a port pair.
- Transparent (always agree): triangle, prism−v (h = 1,1,1), K33−v, two random even poles.
- Not transparent: cube−v and 4 random poles. For odd poles with some h = 3 the outcome
  depends on X's internal path (state-dependent).
- **Every** projected output is either H's lollipop output or exactly C0 (a "local swap": a
  cycle differing from C0 only inside X). No other Ham cycle of H ever appears (E11).

### E12: the mirror mechanism (`exp_mirror.py`)
- Index H's walk states S_0..S_L. Project each G-state whose endpoint is outside X.
- 0 violations across ~2,700 runs: outside X the projected walk moves exactly ±1 along H's
  line; direction reverses **only** during an excursion into X; one excursion moves the
  projection by 0, 1 or 2.
- Transparent poles never reflect. Non-transparent ones reflect, some several times in one run
  (up to 8), so X's internal state persists between visits and changes behaviour.
- Verdict: **Mirror Lemma (conjecture L3) strongly supported.** See open-problems.md T1, route R.

---

## Session 1 (October 2026): literature map, simulator, first experiments

### Literature outcome
- SMITH: in PPA; neither P nor PPA-completeness known.
- LOLLIPOP-OUTPUT: in FP^PSPACE (Eppstein); FP^PSPACE-completeness open. Chosen as
  primary target T1, using the Goldberg–Papadimitriou–Savani Lemke–Howson theorem as the
  template.
- Thomassen's cyclically 4-edge-connected route is closed by Zhong (2018).

### Simulator (`lollipop.py`)
Self-test passes: for n = 6..40 and 200 random instances each, with two start vertices and
both orientations, the output is a Hamiltonian cycle, differs from the input cycle, and
contains the fixed edge. Brute-force counts confirm Smith's parity theorem on 50 random
instances (n = 8–12, every edge).

### E1: exact worst case for small n (`exp_worst_small.py`, `e1_worst_small.json`)
- Method: all labelled chord matchings (11.6 million at n = 18), start (v0 = 0, +1),
  which covers every configuration.
- Worst-case steps W(n), n = 6..18: **3, 6, 11, 18, 29, 47, 74**.
- Mean steps: 2.00, 2.94, 3.88, 4.83, 5.77, 6.71, 7.66 (slope ≈ 0.475 per vertex).
- Verdict: exponential-looking growth with ratio ≈ 1.57 per two vertices at the top end.
  Note: 11, 18, 29, 47 are Lucas numbers, but 74 ≠ 76, so this is likely a coincidence.

### E2: random instances (`exp_random.py`, `e2_random.json`)
- Mean/n: 0.434 (n=20), 0.449 (50), 0.491 (100), 0.496 (200), 0.499 (500), 0.491 (1000),
  0.524 (2000), 0.473 (5000; 100 trials). Median ≈ 0.34–0.38 n.
- Verdict: **supports E[steps] ≈ n/2.** Exponential worst cases are rare on random
  instances.

### E3: structure of the worst cases (`exp_worst_structure.py`)
- Every worst instance for n = 6..18 has cyclic edge-connectivity 3 (triangles present)
  and only 3–7 Hamiltonian cycles. The worst instances share the chords (0, n−2), (1, 4),
  (2, n−1).
- Verdict: consistent with the Krawczyk-type mechanism; motivates the 3-edge-cut
  composition hypothesis (T1, M2).

### E4: annealing for long walks (`exp_search_long.py`, `e4_search.json`)
- Recovers the exact optima at n = 14 (29) and n = 18 (74), which validates the search.
- Best found: 162 (n=22), 242 (26), 400 (30), 751 (34).
- Verdict: **inconclusive** for the worst-case base; search quality drops with n.

### E5: distribution law (`exp_exponential_law.py`, `e5_exponential_law.json`)
- Hypothesis: steps/(n/2) → Exp(1).
- n = 1000, 1500 trials: KS distance 0.025 (5% critical value 0.035); quantiles match
  Exp(1) within sampling error (median 0.67 vs 0.69, 90% 2.42 vs 2.30).
- n = 200, 4000 trials: KS 0.036 exceeds the critical value 0.022; mild finite-size
  deviation (median 0.64).
- Verdict: **supported asymptotically.** Recorded as Conjecture C2.

### Next steps (in order)
1. T2: test the mechanism behind C2 (endpoint near-uniformity), then attempt a
   deferred-decisions proof sketch. Search for prior average-case results first.
2. T1 M1: reconstruct the Briański–Szady or Zhong family in code and reproduce its counts.
3. T1 M2: test the 3-edge-cut composition hypothesis computationally.
