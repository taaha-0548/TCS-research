# N(r) ≤ r² + ⌊r/2⌋ (unconditional)

**Theorem E.** For every r ≥ 2, N(r) ≤ 2r³/(2r−1). Equivalently, N(r) ≤ r² + ⌊r/2⌋.

For r = 2 this gives 5 = N(2), so it is sharp there. The conjecture (Erdős #617) is N(r) ≤ r² for r ≥ 3, so
the gap is ⌊r/2⌋.

Inputs: Turán's theorem and Füredi's stability theorem (JCTB 115 (2015) 66–71), nothing else. It does not
depend on the local Fajtlowicz preprint (`notes/brrs_bound.md`), and for r ≥ 5 it beats the bound
r² + r − 2 that would follow from it.

Status: unrefereed. Novelty unchecked, though it is not in ErGy99, AEGM (as reported to us), or the 2026
fixed-r manuscripts and repositories. The key inequality (S6) is the coloured-density bound that
Sneiderman's fixed-r proofs use on other sets; here it is applied inside the parts of a Füredi partition.

## Proof
Fix an r-colouring of K_n in which every (r+1)-set sees all r colours, with r ≥ 2. Let G be the colour
class with the fewest edges, and H its complement.

- **(S1)** α(G) ≤ r, so H is K_{r+1}-free.
- **(S3)** Put t := e(G) − p_r(n) ≥ 0. Since e(G) ≤ C(n,2)/r and p_r(n) ≥ n²/(2r) − n/2, we get
  t ≤ n(r−1)/(2r).
- **(S4)** Since e(H) = t_r(n) − t, Füredi gives an r-partition V_1, …, V_r with m := Σ_j e(H[V_j]) ≤ t.
- **(S6) Coloured density inside parts.** Fix a part V_j and another colour c. Its colour class G_c has
  α(G_c) ≤ r, so α(G_c[V_j]) ≤ r. By Turán, e(G_c[V_j]) ≥ p_r(|V_j|) ≥ |V_j| − r (a graph with s vertices
  and e edges has α ≥ s − e). The r−1 other colour classes are edge-disjoint, and each of their edges
  inside V_j is an H-edge. So

  e(H[V_j]) ≥ (r−1)·max(0, |V_j| − r).

Summing over j gives (r−1)(n − r²) ≤ m ≤ t ≤ n(r−1)/(2r). Dividing by r−1: n − r² ≤ n/(2r), so
n ≤ 2r³/(2r−1) = r² + r/2 + 1/4 + 1/(4(2r−1)). Taking the floor gives n ≤ r² + ⌊r/2⌋:
- for r even, r/2 + 1/4 + 1/(4(2r−1)) < r/2 + 1;
- for r odd, (r−1)/2 + 3/4 + 1/(4(2r−1)) < (r−1)/2 + 1. ∎

**Exact check.** `scripts/colour_density_bound.py` uses exact p_r, the exact budget
⌊C(n,2)/r⌋ − p_r(n), and the exact minimum of Σ_j p_r(|V_j|) over all r-partitions. For every r from 2
to 15 it returns exactly r² + ⌊r/2⌋, and it confirms that no larger n up to 2r² passes.

## Comparison with the other bounds
| bound | source | r = 5 | r = 10 | r = 20 |
|---|---|---|---|---|
| (1+o(1))r², rate about r² + O(r^{5/3}) as read | AEGM 2002 | — | — | — |
| r² + O(r^{3/2}) | Theorems B, C (`asymptotic.md`) | — | — | — |
| r² + r − 2, conditional on (LF) | Theorem D (`brrs_bound.md`) | 28 | 108 | 418 |
| **r² + ⌊r/2⌋** | **Theorem E** | **27** | **105** | **410** |
| r² (conjectured) | ErGy99 | 25 | 100 | 400 |

## Consequences for the exact problem at n = r² + 1
Apply (S6) to the minority colour's Füredi partition, with m ≤ t ≤ C(r,2):
- The total surplus satisfies S⁺ = Σ_j max(0, |V_j| − r) ≤ C(r,2)/(r−1) = r/2. So at most r/2 vertices
  sit in oversized parts, and since Σ_j(|V_j| − r) = 1, the total deficit is at most r/2 − 1.
- Every oversized part carries at least (r−1)·(its surplus) missing edges, not just the r−1 from (C).
- This shrinks the case space for the rigidity programme (`frame_rigidity.md`). It also kills the
  single-colour obstructions: both the F2 example and the r = 7 covering-frame witness violate (S6).

## Checks recorded
- **Reviewer's hand check (round 3).** (S6) is sound. H is exactly the union of the other r−1 colour
  classes, so there is no double-counting. The pentagon meets the bound with equality at r = 2: G = C_5,
  t = 1, parts of sizes 3 and 2, m = 1 = (r−1)(n−r²). Tightening the budget to the exact
  t ≤ C(r,2) + k(k−1)/(2r) does not move the threshold.
- **Füredi wording.** We use Theorem 1 of the arXiv version: a K_{p+1}-free graph with e = e(T_{n,p}) − t has
  an at-most-p-chromatic subgraph with at least e − t edges. This gives an r-partition (possibly with
  empty parts) with at most t edges inside parts. The published JCTB abstract words it as "≥ e(T_{n,p}) − 2t
  edges", which is consistent; the journal text is still to be confirmed.

## Next lead: (S6) on unions of two parts
For W = V_j ∪ V_k, every pair inside W is either a G-edge or an H-edge, so

  e_G(V_j, V_k) ≤ |V_j||V_k| + m_j + m_k − (r−1)·p_r(|V_j| + |V_k|).

- For two r-parts, p_r(2r) = r, so e_G ≤ r + m_j + m_k. The cross G-edges are nearly a matching, by
  colour density alone and without needing exact cliques.
- For an (r+1)-part and an r-part, p_r(2r+1) = r + 2, so e_G ≤ 2 + m_j + m_k.
- Plan: combine these pair bounds with the greedy blocking argument (`frame_rigidity.md`) and the
  budget I + |E⁺| = t + m ≤ 2t at n = r² + 1.

## Limits
At n = r² + 1, (S6) gives only m ≥ r−1 against m ≤ C(r,2), so the gap of about r/2 remains. Closing it
needs an extra cost of roughly C(r,2) once a part is oversized. The natural candidates are the blocking
cost E⁺ (with I + |E⁺| = t + m ≤ 2t) and (S6) applied to sets other than single parts.
