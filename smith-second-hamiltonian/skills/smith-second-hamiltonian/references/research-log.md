# Research log

Newest session first. Each experiment: hypothesis, method, numbers, verdict, next step.
Result files are in `scripts/` with the same E-number.

---

## Session 6d (October 2026): Phase 3: towers as Turing machines (`scripts/phase3/`, `t1-roadmap.md`)

- Reframing: a tower of a fixed gadget P' is a Turing machine (levels = cells, calls = right moves,
  returns = left moves); the initial cycle is the input tape and the returned cycle is the output
  tape. Full write-up: `references/t1-roadmap.md`.
- Cell procedures (`procedure.py`, `survey_procedures.py`): most P' are answer-sensitive and
  branching. (A first metric was wrong: it grouped by the full answer prefix, which is trivially
  deterministic; fixed.)
- Minimal-machine growth (`tower.py`): bounded / polynomial / exponential-incompressible regimes
  (12 → 48 → 192 → 768 → 3072).
- Clock × tower (`clock_tower.py`): trivial for the tried towers (they reflect the first visit).
  Single-gadget hosts can reflect several times (real hosts: 1,338 with 2 reflections, 151 with
  ≥ 4; none with exactly 3, an unexplained parity pattern).
- Calls per visit (`calls_per_visit.py`): grows with depth for some P' (3, 4, 5, 7, 10), so
  shuttling is possible.
- Next: S1 (recursive bounce machine universality, abstract), then S2 (gadget compiler).

---

## Session 6c (October 2026): Phase 2 (a) clock and (b) power of line–mirror systems

### (a) Clock Theorem (`phase2/clock.py`, `clock_check.py`): exact
- Morphism σ on the 12 visit types of P_0 (σ(e) = ordered passages through x; lengths 1–5),
  start word w0 = (ca/B3). The site sequence of any vertex u at depth d of G_k equals
  concat over f ∈ σ^{d−1}(w0) of pattern_u(f), with pattern_u(f) = u's sites during a P_0-visit of
  type f. Exact for every vertex at every depth, k = 3..7 (19/19 … 43/43). The innermost depth
  sees 21, 61, 180, 531, 1565 visits. **The nested host is a morphic-word clock.**

### (b) Site rule and the Retrace Lemma
- Site rule (`site_rule.py`): forward (in,out)/B1 ↦ backward (c,out)/B1; forward (in,out)/B3 ↦
  backward (in,c)/B3 (c = third port). Deterministic, from 3,000 hosts.
- **Retrace Lemma** (proof sketch). If a gadget transmits at a site and the particle later returns
  through that site from the other side with the gadget's state unchanged, the gadget transmits
  back and restores its earlier state. Reason: the state graph has degree ≤ 2 and the walk never
  backtracks, so the walk exactly undoes the visit; the visit moves are host-independent.
- **Corollary (obstruction):** gadgets with a single site are computationally trivial: at most one
  reflection, after which the particle retraces to the start. Tests (`cells.py`,
  `retrace_test.py`): the longest run with N single-site cells is exactly 2N − 1 (N = 1..10);
  20,000 random lines (N < 40) never reflect twice; 6,485 retrace events in real multi-site hosts,
  all as predicted.
- Interaction can only come from multiple sites of the same gadget: a reflection changes the
  gadget, and the retrace breaks exactly at that gadget's other sites. Passing straight through
  (no reflections) is easy (each gadget reads its own sites independently).
- Random multi-site interleavings (`multisite.py`): longest runs 7, 34, 83, 161, 237, 344, …, 449 for
  m = 1..8 gadgets with 3 sites each. Roughly quadratic; random designs don't reach exponential.
- The known exponential behaviour comes from **hierarchy** (gadget-internal cost of nested gadgets),
  not from bouncing on a flat line. Next model to study: hierarchical composition with memory
  gadgets; the automaton of P_k = Φ(automaton of P_{k−1}), with a state space that may grow
  exponentially with depth. That is the natural home for a PSPACE-hardness construction.

---

## Session 6b (October 2026): T1 Phase 2, step 1: the line–mirror system (`scripts/phase2/`)

- **Line–Mirror Reduction (empirical theorem).** For gadgets at host vertices pairwise at distance
  ≥ 3 and away from v0, the lollipop walk on G = H[x ← X_x] equals the abstract system: a particle
  on H's line S_0..S_L; sites at passages through gadget vertices (B1: a state with endpoint x;
  B3: a step attaching to x); a site traversed in either direction presents a visit type to its
  gadget, whose automaton (state shared by all its sites) answers TRANSMIT (continue) or REFLECT
  (reverse). `linemirror.py`, `test_linemirror.py`: ~182,000 random hosts with 1–3 gadgets (memory
  allowed), all exact (end and step count). Coverage: 16,440 with 1 reflection, 1,965 with ≥ 2,
  138 with reflections at ≥ 2 different gadgets.
- Eppstein's question now splits into Q1 (can line–mirror systems with realisable automata
  simulate reversible computation?) and Q2 (which site sequences can hosts produce?).
- Q2 survey (`sites_survey.py`): random hosts give ≤ ~6 sites per vertex (n = 800). The nested
  family G_k gives single vertices 61 (n = 32) and 531 (n = 44) sites, in a recursive pattern.
  **Idea: use G_k as an exponential "clock" host and substitute memory gadgets at chosen
  vertices, so the clock drives exponentially many reads and writes; iterating a reversible
  circuit is the FP^PSPACE-complete source problem.**
- Next: (a) characterise the site sequence of the nested host recursively, via the composition
  structure; (b) Q1 for the abstract model, i.e. a construction or an obstruction (e.g. whether
  bouncing particles on a line with toggles are polynomially predictable).

---

## Session 6 (October 2026): T1 Phase 1, gadgets with memory (`scripts/phase1/`)

Target: Eppstein's question (LOLLIPOP-OUTPUT FP^PSPACE-complete?). Phase 1 = gadget algebra + go/no-go.

### P1.1 General Composition Theorem (`compose.py`, `test_compose.py`)
- Algorithm: the transducer of P = P'[x ← X] is computed from P' plus X's table. Simulate the P'
  visit and hand each passage through x to X. B1 passage: X picks the exit port; exit = entry port
  means REFLECT, and the rotation undoes the previous one. B3 passage: rotate iff TRANSMIT; the
  previous attachment becomes x. X's internal path is carried as state.
- Test vs direct computation on P: 19,411 pairs with X having memory (804,160 visits) and 27,902
  with X simple (607,160 visits). **All exact.** (Proof idea: Transducer Theorem items 2–3 applied
  inside the host; no simplicity needed.)

### P1.2 Expressiveness (`expressive.py`, `p12_examples.json`)
- Pole = Mealy machine (states = internal paths; inputs = visit types; outputs = T/R). Nerode
  minimisation; "toggle" = same input, two mutually reachable states, different outputs;
  "interacting" = a different input moves the walk between those states.
- Interacting toggle memory: 0% of 5-vertex poles, 16% at 7, 31% at 9, 44% at 11, 59% at 13.
- Smallest example (7 vertices): the cubic graph [[7,1,4],[0,2,5],[1,3,7],[2,4,6],[3,5,0],
  [4,6,1],[5,7,3],[6,0,2]] minus vertex 0. Pair {a,c} has 3 states. Entry via ab/B3 → ac1,
  cb/B3 → ac2, B1 entries → ac0. ac/B1 passes iff ac0, and otherwise reflects while swapping
  ac1 ↔ ac2. ca/B3 passes iff ac2.
- **Go/no-go: GO.** Memory that one traversal writes and another reads exists at the smallest
  possible size.

### Next (Phase 2)
- Formalise the "particle on a line with stateful mirrors" model induced by a host line, and decide
  whether it can simulate reversible computation. Use the deep-research report on the DHHL gadget
  framework (which gadgets suffice, and whether a linear track is enough).
- Wiring: which visit sequences can a host produce at one pole, and can several poles in one host be
  coupled?

---

## Session 5 (October 2026): can we do better? (`search_base.py`, `mix_search.py`, `memory_screen.py`)

- E21 exhaustive single-gadget search (exact method, all x, r ∉ N[x], wirings, starts), base graphs
  with exactly 3 Hamiltonian cycles. |K| = 8: 1 graph, best base 1.197423 (ours, the only one).
  |K| = 10: 3 graphs, 1.184113. |K| = 12: 7 graphs, 1.191341. |K| = 14: 24 graphs, 1.197423
  (ρ = 8.689 = 2.9477², i.e. two levels of our family). Dedup by adjacency spectrum (WL hashing
  cannot separate regular graphs; first attempt was wrong for that reason).
- E22 mixed periodic families: 1,392 distinct gadget matrices (|K| ≤ 12), periods 1–8 (beam
  search): best 1.197423, no improvement.
- E23 non-simple (memory) nested families by direct simulation, |K| = 10, 12: best ≈ 1.189.
- Verdict: 1.19742 is optimal within the simple-nesting design space at these sizes. Larger bases
  need a new idea: non-simple poles with an exact theory, larger K (|K| ≥ 16), or cuts other than
  3-edge cuts. Added a paragraph on this to the paper's discussion.

---

## Session 4 (October 2026): reviewer-ready package (`/paper`)

- Manuscript `paper/paper.tex`: Theorem 1 (Θ(1.19742^n)), Mirror Lemma, Transducer Theorem,
  Lemma S, Composition Lemma, construction, recursion and certificate, graph-class proofs,
  verification, discussion. Appendix: every move of the 12 base visits (generated).
- `paper/verify.py`: standalone and standard library only; checks every computational claim; ALL
  CHECKS PASSED (k ≤ 10).
- While re-checking the Mirror Lemma cases for the paper, made explicit that outside visits the
  projected walk follows H's own walk (the admissible edge and the forbidden vertex map
  identically). Now Transducer Theorem item 1.
- Literature (search only, full texts blocked): Briański–Szady ask whether faster-growing families
  exist; no 2025–2026 improvement found. Author checklist in `paper/README.md`.

---

## Session 3b (October 2026): comprehensive audit (`scripts/audit/`)

- A1/A2 simulator = Thomason: production = independent edge-set walk = brute-force state graph
  (300 random graphs; every start of family levels 0–2). **Pass.**
- A3 independent rebuild of the family (tuple labels, Hamiltonian cycles by recursion, independent
  walk): steps(G_k; 0, +1) = 10, 25, 73, 214, 628, 1849, 5449, 16060, 47338, 139537 for k = 1..10,
  all equal to the prediction 4 + c_{k−1}[ca/B3]. **Pass.**
- A4 exact algebra: charpoly(M) = λ²(λ−1)²(λ+1)²(λ²+1)(λ⁴−2λ³−2λ²−2λ−1); quartic irreducible;
  ρ = 2.947711586844637235. **Pass.**
- A5 Lemma C in general: 71,484 random (P', X) pairs with X simple, all exact. Control (X not
  simple): h differs 98%, outcomes differ 56%. **Pass; hypothesis essential.**
- A6 Lemma S: 7,233 random simple poles of size 9–21, all transparent. **Pass.**
- A7 graph class (independent build): cubic and planar n ≤ 80, 3-connected n ≤ 68, exactly 3
  Hamiltonian cycles by exhaustive search n ≤ 50. **Pass.**
- A8 **gap found and closed**: the recursion is proved only for visit kinds that occur. The
  certificate is restricted to the 10 entries reachable from ca/B3; same ρ, exact inequality, u > 0.
- Written in full: Transducer Theorem (§0.5), 3-connectivity (edge-count argument), planarity (any
  3-pole substitution is planar, since every bijection of 3 elements preserves or reverses cyclic
  order).
- Verdict: complete proof by the authors; pending (i) independent human reading, (ii) full-text
  literature check.

---

## Session 3 (October 2026): testing and proving the Composition Lemma

### Reasoning
- The old GAP (visit walks as walks on a pole with open edges; hypothesis (ii) failing at port 6)
  disappears. Apply the Transducer Theorem to the inner pole X = P_{k−1} inside the full graph.
  There v0 lies in the host and N(X) ⊆ P, so (ii) holds. Contracting X turns P_k into P_0 = K − r.
- **Lemma S (new): a simple pole (one Ham path per port pair) is transparent.** A reflection would
  return the walk to the unique lift of an A-state, i.e. a revisit, impossible on a path.
- **Lemma C (composition):** with X simple and N(X) ⊆ P: h(P) = h(P/X), same outcome table, and
  c_P = c_{P/X} + M c_X, where M counts the passages through x in visits to P/X.

### Tests
- **T1** (`exp_composition_T1.py`): M computed from the 7-vertex P_0 alone equals the M measured
  on the real nested graphs (E20); c_0 = b; T_0 = all transmit; P_0 simple. **Pass.**
- **T2** (`exp_composition_T2.py`): closed-form walk length on G_k from K's walk: 64 / 64
  eligible starts (v0 ∉ N[x]) exact for k = 1..8. Control: 16 of 48 starts with v0 ∈ N(x)
  fail, so the hypothesis is needed. **Pass.**
- **T3** (`exp_composition_T3.py`, `t3_composition.json`): 2,223 random nested families
  satisfying the hypotheses (|K| ∈ {6, 8, 10}, k ≤ 3): prediction from P_0 exact at every level,
  **0 failures**. Excluded because the prediction is undefined: 6,770 with P_0 not simple,
  2,143 with r ∈ N(x). All simple poles met were transparent (supports Lemma S).
- **Certificate** (`certificate.py`, `certificate_N.py`): rational u ≥ 0 with M u ≥ (29477/10000) u
  exactly; start (0, +1) has the single passage ca/B3 with u > 0, so
  steps(G_k) = 4 + c_{k−1}[ca/B3] ≥ ε · 2.9477^{k−1}. Ω(1.19742^n).

### Verdict
- Proof complete in structure; audit table in `composition-proof.md` §7. Remaining before a
  public claim: human check of the Mirror Lemma and a full write-up of the Transducer Theorem;
  write out the 3-connectivity and planarity arguments; full-text literature check (blocked here).

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

### E13 + proof: Mirror Lemma is now a theorem (`exp_projection_lemma.py`, `e13_projection.json`,
`references/mirror-lemma.md`)
- Total projection π: type A (Y1·X·Y2) ↦ Y1·x·Y2; B1 (Y1·X) ↦ Y1·x; B3 (Y1·X1·Y2·X2) ↦ Y1·x·Y2.
- E13: every G-step maps to an H-step or stays: 0 violations in ~85,000 steps, 22 poles
  (sizes 3–15). B1 → B3 moves never occur.
- Hand proof by case analysis (A: 3 cases, B1: 2, B3: 3), in `mirror-lemma.md`. Hypotheses:
  cut edges form a matching, v0 ∉ X ∪ N(X).
- Verdict: **theorem (needs an independent check).** C1(G)/X ∈ {C0/X, C1(H)}.
- Novelty: not found in literature searches; compare against the proof of Thomassen's 3-cut
  reduction and against Cameron 2001 before claiming it.

### E14: Transducer Theorem (`transducer.py`, `exp_transducer_check.py`, `show_transducer.py`)
- A pole's visits are host-independent (from cases 2a, 3a, 3b of the proof). Each visit is a
  B1 or B3 visit, and returns (TRANSMIT/REFLECT, new internal path, steps).
- Host walk plus transducer reproduces G's walk exactly, with the same final cycle and step
  count: 4,691 / 4,691 runs.
- It also predicts E11 without fitting: the transducer reflects for exactly the poles that
  were non-transparent.

### E15: survey of pole classes (`exp_pole_survey.py`, `e15_pole_survey.json`)
- Active-memory poles (transmit or reflect depends on the internal path): 12% at |X| = 7,
  rising to ~70–77% at |X| = 13–15. Memory gadgets are plentiful.
- Verdict: R2 done. The raw material for R3 exists; the open question is wiring (R4).

### Next steps (session 3)
1. Formalise the **line–mirror model**: a particle on the host line S_0..S_L moving ±1, with
   sites where poles act (transmit/reflect plus a state update, shared among all sites of the
   same pole). Ask whether predicting the exit end is PSPACE-hard for arbitrary reversible
   mirror automata. If not even that holds, route R fails at R4.
2. Read arXiv 2207.07229 in full: gadget definitions, and whether a linear "track" with
   interleaved tunnels of interacting gadgets suffices for their hardness.
3. Find out which visit sequences a host H can produce (which sites, in what order and
   orientation). Start with small hosts and 2 poles.
4. Independent check of the Mirror Lemma proof; novelty check against Thomassen's 3-cut
   reduction and Cameron 2001.

### Novelty check: blocked
- The environment's network policy blocks arxiv.org, ar5iv, cambridge.org, researchgate,
  sciencedirect, semanticscholar and dagstuhl. Only search snippets are available.
- From snippets: Thomassen's observation is cited as a private communication, with no proof
  given; Cameron 2001 and Briański–Szady 2022 analyses are not visible. **Novelty of the Mirror
  Lemma and the Transducer Theorem remains unverified.**
- Briański–Szady family (from snippets): cap K3, n two-vertex gadgets, pac; 2n + 6 vertices;
  exactly 3 Hamiltonian cycles; 3-connected planar. Rebuilding it (M1) needs the paper.

### E16–E17: nested 3-pole families (`chains.py`, `nested*.py`, `e16*.json`, `e17*.json`)
- `chains.py`: chains of 2-vertex gadgets between K3 caps with every wiring, period ≤ 2.
  All grow linearly (4 steps per gadget). Not the Briański–Szady construction.
- Nested families G_k = K[x ← G_{k−1} − r] (fixed K, x, r and wiring). K = 6: growth per level
  tends to ≈ 1.84, i.e. ≈ 1.165 per vertex (below 1.1812).
- **K = 8 candidate** (chord [4,3,6,1,0,7,2,5], x = 5, r = 2, perm (2,0,1); same numbers for
  chord [2,5,0,7,6,1,4,3], x = 4, r = 1, perm (2,0,1)): max steps over all starts of one C0:
  6, 27, 97, 249, 886, 2187, 7747, 19025 at n = 8..50. Two-level factors (12 vertices) 9.22,
  9.13, 8.78, 8.74, 8.70, i.e. ≈ 1.1975 per vertex, still drifting down. Beating 1.1812 needs
  the two-level factor to stay above 7.36.
- Verdict: **inconclusive, promising.** Caveats: few terms, no proof; probably not planar
  (Briański–Szady is planar 3-connected); whether 1.1812 is also the record for general cubic
  graphs is unverified.
- `nested_extend.py` (top-5 starts only) underestimates, e.g. level 7 gave 15219 vs 19025:
  always evaluate all starts. DFS for Hamiltonian paths times out at level 9.
- `nested_fast.py` (Hamiltonian cycles generated by lollipop walks instead of DFS) is written
  but **not yet run**.
- Next: run `python3 nested_fast.py "[4, 3, 6, 1, 0, 7, 2, 5]" 5 2 "(2, 0, 1)" 14 450` (about 10
  minutes) to see where the growth rate settles; if it stays above 1.1812, derive the exact
  recurrence from the transducer composition and prove the lower bound.

### E18–E20: exact recursion for the K=8 nested family (`nested_fast.py`, `level_tables.py`,
`m_matrix.py`, `graph_props.py`, `count_ham.py`, `e19*`, `e20_M.json`)
- Deep run (E18): max steps 6, 27, 97, 249, 886, 2187, 7747, 19025, 67358, 165331, 585321,
  1436585, 5085902, 12482515 for n = 8..86. Two-level factor converges to 8.689.
- Every level is 3-connected and planar (n ≤ 80) with exactly 3 Hamiltonian cycles (n ≤ 32 by
  enumeration), the same class as Briański–Szady.
- Pole table (E19): all 12 visits transmit, with an identical pattern at every level k ≤ 11.
  The growth comes from visit costs, not reflections.
- Sub-visit matrix (E20): M and b are level-independent; c_{k+1} = M c_k + b holds exactly
  for k = 0..10 (levels 7–11 out of sample). ρ(M) = 2.947711586844 = largest root of
  λ^4 − 2λ^3 − 2λ^2 − 2λ − 1, giving **Θ(1.19742^n) vs Briański–Szady's 1.1812^n**.
- First extraction missed sub-visits that start at the visit's first state (spectral radius
  2.833). Fixed by including the pre-visit state.
- Verdict: **candidate improved lower bound**; proof plan with one GAP (Nested Transducer
  Lemma) in `references/improved-lower-bound.md`.

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
