# Research directions after Theorem E (reviewer's ranking, round 6)

1. Robust rigidity lemma, first aiming at r² + O(√r) or r² + o(r).
2. A robust Singleton/Plotkin bound across all colours: each colour's Füredi partition gives an
   approximate code.
3. Computational supersaturation experiments to guide 1 and 2. **Started first.**

Also: map which parts of Sneiderman's r = 5–9 machinery are uniform in r.

## Direction 3: supersaturation at n = r² + 1 (`scripts/supersat.py`, `scripts/analyze_extremal.py`)
bad(χ) is the number of (r+1)-sets that miss a colour. The conjecture says bad ≥ 1.

### r = 3, n = 10
- **The minimum is exactly 2.** CP-SAT proves bad ≤ 1 is infeasible, and annealing finds bad = 2.
- **The exact best one-vertex extension of the merged AG(2,3) has bad = 5** (CP-SAT, optimal).
- In all three optimal colourings examined, the two bad sets share a vertex. Deleting it leaves a balanced
  3-colouring of K_9 that is **not isomorphic to the merged affine plane**, under vertex and colour
  permutations.
  - Its colour-class sizes are 13/13/10, 9/12/15 or 10/14/12; the affine colouring has 9/9/18.
  - The isomorphism test was validated on a relabelled, colour-permuted affine copy.
- So non-affine balanced K_9 colourings exist, and they extend better than the affine one (2 against 5).
  A stability target of the form "balanced K_{r²} = affine, plus one vertex" is false at r = 3. Candidate
  targets: the bad-set count, or deletion distance to a balanced K_{r²} of any kind.
- Random balanced K_9 colourings found by search extend with bad = 3, 4, 3.

### r = 4, n = 17 (upper bounds only: annealing is noisy)
- The best found is bad = 43 (four 2M-step runs gave 43, 44, 44, 43). Earlier 200k-step runs gave 48–90.
- In the bad = 43 colouring the bad sets do not share a vertex: the top vertex lies in 38 of the 43.
- Random balanced K_16 colourings found by search extend with bad = 61, 62, 70.
- The exact extension of the merged AG(2,4) (built over GF(4)) and full profiles are running in
  `analyze_extremal.py`.

### r = 5 (upper bounds only)
- Annealing over the full colouring reaches only 5379, so it is unreliable at this size.
- The annealed one-vertex extension of the merged AG(2,5) gives 1075, the best known upper bound here.

### Recorded per colouring (reviewer's list)
Colour-class sizes; for the least colour, t, the (heuristic) min-m Füredi partition sizes, m and S⁺;
whether all bad sets share a vertex; and the exact minimum deletion set. Profiles are in the
`analyze_extremal.py` output.

## Sneiderman's machinery: uniform versus per-r
From the consolidated draft, §3; recursion replayed with Girambona's independent `ladder.py`.

**Uniform in r.**
- Full-colour density (Lemma 3.4); this is our (S6).
- The terminal core (Thm 3.5, r ≥ 6).
- The ladder (Thm 3.6): T_3 = 1 and T_4 = 2 for all r ≥ 6.
- Representative selection (Lemma 3.7) and block exclusion (Prop 3.8).

**Per r.** The margin recursion (20), which raises the least colour's minimum degree δ(G) to r − 1 before
a finite endgame.

Caveat: this is Girambona's `ladder.py`, transcribed from the draft's text and documented only for
r ≤ 9. So the table shows that **the recursion as transcribed** fails to exclude these degrees. It does
not show that Sneiderman's method fails: his r = 9 proof adds bridges the script omits, and the r = 9 row
already differs from a complete proof. Read the widening band as a suggestion, not a finding. Reading
his r = 9 bridges directly would settle it. Degrees d left unexcluded by the transcribed recursion:

| r | unexcluded d |
|---|---|
| 7 | 6 |
| 8 | 7 |
| 9 | 7, 8 |
| 10 | 7, 8, 9 |
| 11 | 8, 9, 10 |
| 12 | 8–11 |
| 13 | 8–12 |

So the recursion excludes only d ≲ 8, and the open band widens towards (r/2, r−1). This is consistent
with Sneiderman needing extra bridges at r = 9 and stopping there.

**Where our structure could enter.** Both statements below are unverified leads, not arguments. In the
Füredi partition of the least colour, a vertex v of G-degree d in
part V_j has d_H(v, V_j) ≥ |V_j| − 1 − d. So a vertex with d ≈ r/2 costs about r/2 missing edges. With
m ≤ C(r,2), about r such vertices are affordable, so this alone does not close the band. It might,
combined with block exclusion (Prop 3.8): about r − 4 untouched exact r-cliques in the non-neighbourhood
of v are forbidden.
