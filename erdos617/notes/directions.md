# Research directions after Theorem E (reviewer's ranking, round 6)

1. Robust rigidity lemma, first aiming at r² + O(√r) or r² + o(r).
2. A robust Singleton/Plotkin bound across all colours: each colour's Füredi partition gives an
   approximate code.
3. Computational supersaturation experiments to guide 1 and 2. **Started first.**

Also: map which parts of Sneiderman's r = 5–9 machinery are uniform in r.

## Direction 3: supersaturation at n = r² + 1 (`scripts/supersat.py`)
bad(χ) is the number of (r+1)-sets that miss a colour. The conjecture says bad ≥ 1.

- **r = 3, n = 10: min bad = 2, exactly.**
  - CP-SAT proves bad ≤ 1 is infeasible; annealing finds bad = 2.
  - In the best colouring found, one 4-set misses two colours.
  - The best one-vertex extension of the AG(2,3) colouring is worse (bad = 5). So the extremal colourings
    need not be affine-plus-one.
- **r = 4, n = 17: best found bad = 48** (annealing, 200k steps; results vary 48–90 across seeds).
  - In the best colouring one vertex lies in all 48 bad sets. So it is a balanced K_16 plus one vertex.
  - Longer runs and the best extension of a balanced K_16 (`extend` mode) are in progress.
- **r = 5:** runs queued.

Early reading: the minimum is small at r = 3 (2), larger at r = 4 (≤ 48), and the r = 4 extremum
concentrates on one vertex. If "near-extremal = balanced K_{r²} + one vertex" persists, a stability
statement of that form is the natural strengthened target for direction 1.

## Sneiderman's machinery: uniform versus per-r
From the consolidated draft, §3; recursion replayed with Girambona's independent `ladder.py`.

**Uniform in r.**
- Full-colour density (Lemma 3.4); this is our (S6).
- The terminal core (Thm 3.5, r ≥ 6).
- The ladder (Thm 3.6): T_3 = 1 and T_4 = 2 for all r ≥ 6.
- Representative selection (Lemma 3.7) and block exclusion (Prop 3.8).

**Per r.** The margin recursion (20), which raises the least colour's minimum degree δ(G) to r − 1 before
a finite endgame. Our scan shows it does **not** do this for larger r. The degrees d left unexcluded are:

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

**Where our structure could enter.** In the Füredi partition of the least colour, a vertex v of G-degree d in
part V_j has d_H(v, V_j) ≥ |V_j| − 1 − d. So a vertex with d ≈ r/2 costs about r/2 missing edges. With
m ≤ C(r,2), about r such vertices are affordable, so this alone does not close the band. It might,
combined with block exclusion (Prop 3.8): about r − 4 untouched exact r-cliques in the non-neighbourhood
of v are forbidden.
