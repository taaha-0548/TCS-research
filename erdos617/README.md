# Erdős Problem #617 (Erdős–Gyárfás balanced colourings)

## Statement

For r ≥ 3, every r-colouring of the edges of K_{r²+1} has r+1 vertices whose induced K_{r+1} misses at
least one colour.

Equivalent forms:
- A colouring is *balanced* if every (r+1)-set sees all r colours. The conjecture says K_{r²+1} has no
  balanced r-colouring.
- Every colour class G_i has α(G_i) ≤ r. Equivalently, H_i = complement(G_i) is K_{r+1}-free, and every
  edge of K_n lies in exactly r−1 of the H_i.
- Write N(r) for the largest n with a balanced r-colouring of K_n. The conjecture is N(r) ≤ r².
- In set-colouring Ramsey language the conjecture is R(r+1; r, r−1) ≤ r²+1.

Basic constraints on each colour class G of a balanced colouring:
- (A) α(G) ≤ r.
- (C) Every (r+1)-set spans at most C(r,2)+1 edges of G, because the other r−1 colours need an edge
  each. In particular ω(G) ≤ r.
- (D) The coloured density cap (Sneiderman): e(G[W]) ≤ D_r(|W|) := C(|W|,2) − (r−1)·p_r(|W|) for every W.
  Here p_r(m) is the Turán minimum number of edges for α ≤ r. This uses the other r−1 colours.

## Status (October 2026; nothing below has been refereed)

| r | status | source |
|---|---|---|
| 2 | false (pentagon) | ErGy99 |
| 3, 4 | proved | Erdős–Gyárfás, Discrete Math. 200 (1999) 79–86 |
| 5 | several independent machine-checked proofs (Lean 4 + LRAT) | Sneiderman preprint; nwinter/erdos-617-r5; RamazanKara/erdos-617-r5-formal-verification |
| 6 | claimed human proof (Sneiderman); separate Lean proof (nwinter) | Robby955/erdos-617-fixed-cases |
| 7, 8, 9 | claimed, computer-assisted (enumeration, LRAT) | same; r = 6, 7 audited by Girambona/erdos-617-audit-r6-r7 |
| ≥ 10, general r | **open** | — |

- Lower-bound side: affine planes give N(r) ≥ r² whenever an affine plane of order r exists. Use r−1
  parallel classes as colours, and merge the remaining two classes into one colour.
- Known obstruction: the AG(2,r) colourings of K_{r²} do not extend to r²+1 vertices
  (nwinter, review_queue/ag-nonextension.md). So a counterexample would need a non-affine balanced K_{r²}.
- Every existing proof works for one fixed r, and its case analysis or SAT work grows quickly with r.
  Sneiderman's general-r machinery (the coloured core ladder T_s(r) and the recursion B_r(a,m)) is
  explicitly stated not to extend to r = 10 or to general r.

## New findings in this workspace

**F1. Exact single-colour minimum for small r** (`scripts/single_colour_min.py`).
Define q(r) as the minimum e(G) over graphs on r²+1 vertices satisfying (A) and (C). The minority colour
has at most M_r := C(r²+1,2)/r edges, so q(r) > M_r would prove case r.

| r | q(r) | M_r | result |
|---|---|---|---|
| 2 | 5 | 5 | no gap (consistent with r = 2 being false) |
| 3 | 18 | 15 | gap 3 |
| 4 | not yet determined (CP-SAT run pending) | 34 | — |

**F2. The single-colour approach fails for large r** (`scripts/c5_blowup_single_colour.py`,
`scripts/verify_r7_example.py`).
Take G = complement(C₅ blow-up on 2r+1 vertices) plus r−2 disjoint copies of K_r.
- It has r²+1 vertices, α(G) = r, and satisfies the cap (C).
- It has fewer than M_r edges for r = 7, 9 and 11–19 (all values checked). For r = 7: e = 165 < 175,
  checked by brute force.
- This family gives nothing at r = 8 or 10. The edge margin grows like 0.3r², so all large r are expected.

So no proof can use the minority colour alone with (A) and (C). Information about the other colours,
for example (D), is needed. (D) does kill this example: on the 2r+1 block, the other r−1 colours need at
least (r−1)(r+2) ≈ r² edges, but only ≈ 0.8r² are available.

**F3. A short asymptotic bound: N(r) < 2r³/(r+1) < 2r²** (proof sketch, uses only Füredi 2015).
1. Let G be the minority colour on n vertices, and set t = e(G) − p_r(n). Then t ≤ C(n,2)/r − p_r(n) < n/2.
2. H = complement(G) is K_{r+1}-free with t_r(n) − t edges. By Füredi (JCTB 115, 2015), deleting at
   most t edges makes H r-partite. So some r-partition V_1, …, V_r has at most t H-edges inside parts.
3. G has no K_{r+1}, so α(H[V_j]) ≤ r. Hence e(H[V_j]) ≥ p_r(|V_j|) ≥ |V_j| − r.
4. Summing over parts: n − r² ≤ t < n(r−1)/(2r). This gives the bound.

Adding cap (C) inside parts, a part of size s ≥ r+1 needs at least (r−1)·C(s,2)/C(r+1,2) H-edges. The
resulting optimisation gives N(r) ≤ (8/7 + o(1))·r² (`scripts/asymptotic_bound.py`). For example
N(3) ≤ 10, N(10) ≤ 116, N(20) ≤ 461.

**F4. N(r) ≤ r² + 2√2·r^{3/2} + 16r for r ≥ 10** (an asymptotic statement: it improves on F3 only from r = 35; constant √2 + o(1) as a weaker-claimed corollary), so N(r) = (1 + o(1))·r². Full proof with explicit constants in
`notes/asymptotic.md`. It adds the imbalance cost Σ C(s_j,2) − p_r(n) ≤ 2t to F3, observes that only
about r/2 parts can be oversized, and finishes with Cauchy–Schwarz. The exact optimisation version is
`scripts/asymptotic_bound2.py`.

The only general bound found in the literature is Erdős–Szemerédi (1972), which gives N(r) ≤ r^{O(1)}.
I did not find an O(r²) upper bound in the sources read: ErGy99, the 2026 repos, and the
set-colouring Ramsey abstracts. The literature still needs checking before calling this new.

**F4 status (revised).** The qualitative (1+o(1))r² is already known: Alon–Erdős–Gunderson–Molloy,
J. Graph Theory 40 (2002). F3 and F4 are an independent, explicit-constant route, and at most a modest
quantitative sharpening.

**F6. N(r) ≤ r² + r − 2 for r ≥ 3, conditional on the local Fajtlowicz bound**
α(G) ≥ Σ_u 2/(d(u)+ω(u)+1). This is the Brause–Randerath–Rautenbach–Schiermeyer conjecture (2016),
and a 2026 preprint (Abiad, Kumar and Pragada, arXiv:2609.00210, unrefereed) claims a proof.
- Apply it to the minority colour: ω ≤ r and average degree ≤ (n−1)/r, then use convexity and integer
  degrees. Details in `notes/brrs_bound.md`; exact check in `scripts/brrs_bound.py`.
- For r = 2 it gives N(2) ≤ 5, which is sharp.
- The integer step's margin is only 1/((r+1)(2r+1)); r² + r − 1 needs only the real-valued bound.
- It needs verification of the preprint. If that holds, it supersedes F3 and F4. The F2 example is
  tight for the bound, so it alone cannot reach r².

**F7. N(r) ≤ r² + ⌊r/2⌋ for every r ≥ 2, unconditional** (`notes/colour_density_bound.md`).
- Inside each Füredi part of the minority colour, each of the other r−1 colours has α ≤ r. So it needs
  at least p_r(|V_j|) edges there, all of them non-G edges.
- Hence m ≥ (r−1)(n − r²), while m ≤ t ≤ n(r−1)/(2r).
- This is a three-line proof, sharp at r = 2, checked exactly for r ≤ 15 (`scripts/colour_density_bound.py`).
- It supersedes F3, F4 and AEGM's rate, and beats the conditional F6 for r ≥ 5. Novelty is unchecked.

**F5. Rigidity of the balanced frame at n = r²+1** (`notes/frame_rigidity.md`).
- Setting: in the minority colour, a Füredi partition with sizes (r+1, r, …, r) whose r-sized parts
  are cliques.
- (C) makes the cross edges matchings, and a greedy independent-transversal argument then forces
  perfect matchings between all parts.
- That costs at least C(r−1,2)(r−2) + 2(r−1) ≈ r³/2 cross edges, against a budget of r(r−1). So this
  frame is impossible for every r ≥ 5.
- The cubic-versus-quadratic slack is the main reason to expect a proof for all large r. What remains
  is a robust version allowing unbalanced parts and missing edges inside parts.

## Current plan
1. Make F5 robust. The hard case is deficient parts (size r − y), which an outside vertex can dominate.
   They cost imbalance y(y+1)/2, and their deficit must be absorbed by oversized parts. Each oversized
   part costs at least r−1 missing edges, but also supplies an extra independent pair.
2. Test the shapes exactly for small r in decision mode:
   - `DECIDE_CAP=M_r python3 scripts/frame_min.py r furedi` (the F5 shape with a free big part);
   - `DECIDE_CAP=M_r python3 scripts/blocking_lemma.py r` (covers by r+1 cliques).
3. Literature check of F4 by a human. arXiv and most journals are blocked from this sandbox.

## Approaches (ranked)

1. **Asymptotic conjecture: N(r) ≤ (1+o(1))r², then r² + O(r).** Start from F3.
   - Step 2 throws away α(G) ≤ r across parts. Independent sets that take two vertices from an
     oversized part and one from each other part must be blocked by cross edges E⁺.
   - E⁺ is paid for from the same budget t, and (C) makes E⁺ between near-cliques almost a matching.
   - Tools: independent transversals (Haxell; Szabó–Tardos; Loh–Sudakov local-degree versions) and
     coloured density (D) for the other colours.
   - This is the most tractable target and would be a real result if it is new.
2. **Stability method for r ≥ r₀.** Show that every balanced colouring with n ≈ r² is close to the
   affine-plane shape: r−1 near-clique partitions, pairwise near-orthogonal, plus one "double" colour.
   - The F3 machinery already gives each low-excess colour an r-partition into near-cliques.
   - The total excess Σ_i (e(G_i) − p_r(n)) is exactly C(n,2) − r·p_r(n) = r·C(r,2).
   - Then prove an exact extension lemma near that structure. The AG non-extension argument is the
     model: monochromatic lines force each new vertex's colour classes to be lines of an exempt direction.
   - This would settle the conjecture for all r ≥ r₀ (r₀ ineffective or large). Closing the gap
     10 ≤ r < r₀ is a separate problem.
3. **The key subproblem: a blocking lemma.** Consider r+1 near-cliques of size about r−1, with (C)
   limiting each vertex to about r/2 neighbours in any other block. How many cross edges kill every
   independent transversal?
   - The union bound gives (r−1)², but it is attained only by complete bipartite pieces, which (C)
     forbids.
   - Any constant > 1 in front of r² closes the minority budget, which is about r² − r + 1.
   - This is a clean extremal question that can be tested numerically for small r.
4. **Uniform-in-r counting certificates.** Solve LP or SDP relaxations (local colour-degree profiles,
   triangle and (r+1)-set counts) for r = 3…7. Look for a dual certificate with a parametric pattern in r,
   in the spirit of flag algebras.
5. **Computation and counterexamples.** Erdős–Gyárfás themselves doubted the conjecture.
   - Search for non-affine balanced colourings of K_{r²} at r = 4, 5, 7. These are needed both for a
     counterexample and to calibrate approach 2.
   - Bound N(r) at non-prime-power r (6, 10). There is no plane of order 10, so N(10) < 100 is
     possible, which would make r = 10 easier.
   - Extending Sneiderman's pipeline to r = 10 is possible but low-novelty and compute-heavy.

## Files
- `balanced_sat.py`: SAT model of balanced colourings (optional cyclic symmetry).
- `scripts/single_colour_min.py`: exact q(r) via CP-SAT with lazy constraints (F1).
- `scripts/c5_blowup_single_colour.py`, `scripts/verify_r7_example.py`: single-colour counterexamples (F2).
- `scripts/asymptotic_bound.py`: the F3 bound with the cap refinement.
