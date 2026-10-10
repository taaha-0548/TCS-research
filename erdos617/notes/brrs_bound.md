# N(r) ≤ r² + r − 2, conditional on the local Fajtlowicz bound

**Dependency, stated first.** Everything here rests on the local Fajtlowicz bound

  (LF)  α(G) ≥ Σ_u 2 / (d(u) + ω(u) + 1),   where ω(u) is the largest clique containing u.

- Brause, Randerath, Rautenbach and Schiermeyer conjectured (LF) (Discrete Appl. Math. 209 (2016) 59–67)
  and proved it for perfect graphs and for maximum degree ≤ 4.
- A 2026 arXiv preprint, Abiad, Kumar and Pragada, "Localization of the Caro–Wei bound and its
  applications to bipartiteness", arXiv:2609.00210 (submitted 31 Aug 2026), reports a proof via a
  Motzkin–Straus-type inequality (its Theorem 2.2). It is unrefereed.
  - A reviewer confirmed that its abstract and statement match (LF) exactly.
  - Before this preprint, (LF) was known only for subquartic and perfect graphs.
  - Not yet done: reading its Theorem 2.2 and Section 3 for hidden hypotheses. One snippet mentions
    connectedness, but only inside the equality case.
- We use only the weaker global-ω form, α(G) ≥ Σ_u 2/(d(u) + ω(G) + 1), which is implied by (LF). We
  have not found an earlier refereed proof of this weaker form. Kelly–Postle (JCTB 169 (2024)) is the
  remaining candidate to check, and would be a safer citation if it covers this form.
- Sanity check, not evidence of truth: `scripts/local_fajtlowicz_check.py` checks (LF) exhaustively on
  all 1,252 graphs with 1–7 vertices (tight on 48) and on 4,000 random graphs with 8–13 vertices. It
  finds no counterexample.

**Theorem D (conditional on (LF)).** N(2) ≤ 5, and N(r) ≤ r² + r − 2 for r ≥ 3.

For r = 2 this is sharp, since N(2) = 5 (the pentagon). The conjecture is N(r) ≤ r² for r ≥ 3, so the gap
is r − 2.

## Proof
1. **Setup.** Take an r-colouring of K_n in which every (r+1)-set sees all r colours. Let G be the colour
   class with the fewest edges, so 2e(G) ≤ D := 2⌊C(n,2)/r⌋.
2. **Cliques are small.** A monochromatic K_{r+1} would miss the other r−1 ≥ 1 colours, so ω(G) ≤ r.
3. **Apply (LF).** This gives α(G) ≥ Σ_u 2/(d(u) + r + 1).
4. **Minimise the right-hand side over degree sequences.** f(d) = 2/(d + r + 1) is convex and decreasing.
   So over integer sequences with Σ d(u) ≤ D, the sum is smallest when the whole budget D is spread as
   evenly as possible, with every degree equal to ⌊D/n⌋ or ⌈D/n⌉.
5. **Conclude.** If that minimum exceeds r, then α(G) ≥ r+1. Some r+1 vertices then span no edge of G,
   so they miss G's colour, which contradicts the assumption.
6. **The exact margin.** Take n = r² + r − 1 and r ≥ 3.
   - Then n(n−1)/r = n(r+1) − (2r + 2 − 2/r), so D ≤ n(r+1) − (2r+2).
   - The most balanced sequence therefore has at least 2r+2 vertices of degree r, and the rest have
     degree r+1.
   - The sum is at least n/(r+1) + (2r+2)/((2r+1)(r+1)) = r − 1/(r+1) + 2/(2r+1) = r + 1/((r+1)(2r+1)).
   - This is strictly above r, so α ≥ r+1.

   **Fragility.** The margin is only 1/((r+1)(2r+1)), so r² + r − 2 needs (LF) exactly as stated. Any
   lossy constant in the published version would leave only the real-valued bound r² + r − 1 (Remark).
7. **Larger n.** For every larger n the sum stays above r. `scripts/brrs_bound.py` checks this exactly,
   in rational arithmetic, for r ≤ 20. It reports exactly r² + r − 2 for every r from 3 to 20. ∎

**Remark on the integer step.** Without it, convexity alone gives N(r) ≤ r² + r − 1 for all r ≥ 2.

## Sanity checks
- At n = r² the affine-plane colouring meets (LF) with equality: r disjoint K_r give 2r²/(2r) = r.
- r = 3 gives 10, consistent with the known N(3) = 9.
- At r = 2 the integer step does not apply, since 2/r = 1. The separate statement N(2) ≤ 5 is sharp.

## What this means
- If (LF) holds, Theorem D supersedes every asymptotic bound we know of. That includes the
  Alon–Erdős–Gunderson–Molloy (1+o(1))r² bound (J. Graph Theory 40 (2002) 120–129), whose rate the
  reviewer reads as roughly r² + O(r^{5/3}), and our own Füredi-based r² + O(r^{3/2})
  (`notes/asymptotic.md`).
- The argument is a one-line corollary of (LF), so its novelty is only as an observation. Its weight
  rests entirely on (LF) being correct.
- **(LF) alone cannot reach r².** The F2 example (README) is tight for (LF) at r = 7:
  - each K_7 vertex contributes 2/(6+7+1) = 1/7, and the 35 of them sum to 5;
  - each of the 15 vertices of B has degree 8 and local clique number 6, contributing 2/15, which sums
    to 2;
  - the total is 7 = α.

  So the minority colour together with (LF) is exactly balanced there.
- **Research direction: a stability version of (LF).** At n = r² + 1 the minority colour falls short of
  the (LF) bound by only about 1.5. If near-equality in (LF) forces structure (near-disjoint cliques,
  plus pieces like the C₅-blow-up complement), the coloured constraints may close the remaining gap.
  The (r+1)-set cap and the other colours' Turán bounds are the extra information.

## To verify
- Read Pragada, arXiv:2609.00210, in full. Check that the theorem proved is (LF), or at least the
  global-ω form, with no extra hypotheses.
- Check whether the Bertram–Horák global-ω form was proved earlier. Kelly–Postle,
  "Fractional coloring with local demands …" (JCTB 169 (2024)), is a candidate; we have not seen its
  theorem statements.
