# Candidate result: Thomason chains of length Ω(1.1974^n) on 3-connected planar cubic graphs

Status (session 2): **exact recursion found and verified computationally; proof reduced to one
lemma (marked GAP below) plus routine checks.** Not yet a theorem. Novelty: Briański–Szady
(Discrete Math. 2022, arXiv 1903.02515) give Ω(1.1812^n) for 3-connected planar cubic graphs and
are still cited as the best bound in 2023–2024 (Björklund–Kaski–Nederlof, ICALP 2024). No newer
improvement turned up in searches up to October 2026, but full texts could not be read from this
environment.

## The family

- K = the 8-vertex cubic graph given by the cycle 0-1-…-7-0 plus chords
  chord = [4, 3, 6, 1, 0, 7, 2, 5], i.e. {0,4}, {1,3}, {2,6}, {5,7}. Hamiltonian cycle C = 0..7.
- x = 5 (the vertex to be replaced), r = 2 (the vertex removed to make the pole), and wiring
  perm = (2, 0, 1): the k-th neighbour of x in K (adjacency order [4, 6, 7]) is joined to port
  perm[k] of the pole (ports in the adjacency order of r).
- G_0 = K; G_{k+1} = K[x ← P_k] with P_k = G_k − r_k, where r_k is the outer copy of r.
  So |G_k| = 8 + 6k. Code: `scripts/nested_fast.py` (`next_level`).

## Facts verified by computation

| Property | Checked for | Script |
|---|---|---|
| simple cubic, C_k Hamiltonian | k ≤ 13 (n ≤ 86) | `nested_fast.py` asserts |
| 3-connected, planar, not bipartite, has triangles | k ≤ 12 (n ≤ 80) | `graph_props.py` |
| exactly 3 Hamiltonian cycles | k ≤ 4 (n ≤ 32) by full enumeration; 3 found by walks for k ≤ 11 | `count_ham.py`, `level_tables.py` |
| pole outcome table: all 12 visits TRANSMIT, same successor states, at every level | k ≤ 11 | `level_tables.py` (E19) |
| sub-visit matrix M and offset b level-independent | k = 1..6 | `m_matrix.py` (E20) |
| c_{k+1} = M c_k + b exact | all transitions k = 0..10 (levels 7–11 are out of sample) | E20 check |
| max lollipop steps on G_k (over all starts of C_k) | 6, 27, 97, 249, 886, 2187, 7747, 19025, 67358, 165331, 585321, 1436585, 5085902, 12482515 for k = 0..13 | `nested_fast.py` (E18) |

## The recursion

c_k ∈ ℕ^12 is the cost vector of the pole P_k: the number of walk steps spent in each of its 12
visits (6 oriented states × {B1, B3}). Then

  c_{k+1} = M c_k + b,   b = c_0 = (3, 10, 5, 10, 3, 10, 5, 10, 3, 6, 3, 6),

with the 0/1 matrix M in `scripts/e20_M.json`. Its characteristic polynomial is

  λ^12 − 2λ^11 − 3λ^10 + 4λ^7 + 4λ^6 − λ^4 − 2λ^3 − λ^2,

and its spectral radius is ρ = 2.947711586844…, the largest root of λ^4 − 2λ^3 − 2λ^2 − 2λ − 1.
Every growing cost entry satisfies a_k = 2a_{k−1} + 2a_{k−2} + 2a_{k−3} + a_{k−4} + const.
Since n grows by 6 per level, the walk length is Θ(ρ^{n/6}) = Θ(1.19742^n).

## Proof plan

1. **Exactly 3 Hamiltonian cycles (easy induction).** Hamiltonian cycles of K[x ← P] correspond to
   pairs (Hamiltonian cycle of K using the edge pair {i, j} at x, Hamiltonian path of P between
   ports i, j). If K and G_k each have exactly 3 Hamiltonian cycles, Smith's theorem forces each
   edge pair at a vertex to be used exactly once, so h_ij = 1 for every pair and G_{k+1} has
   1·1 + 1·1 + 1·1 = 3. K itself has 3 (check).
2. **Planarity and 3-connectivity (routine).** Substituting a planar 3-pole into a vertex keeps
   planarity when the cyclic order of the ports matches the rotation at x; 3-connectivity is
   preserved by substituting a 3-connected 3-pole. Verify that perm respects the rotation of the
   embedding (it must, since planarity holds through n = 80; write the argument).
3. **GAP: Nested Transducer Lemma.** During a visit to P_{k+1}, the internal walk enters the
   nested pole P_k as a sequence of sub-visits, and depends on P_k only through P_k's outcome
   table (which visit transmits, and the successor state). This is the Transducer Theorem applied
   to the visit walk instead of the full lollipop walk. Two things need care:
   (a) the visit walk is a walk on a pole with boundary, not a lollipop walk on a closed graph.
   Either restate the Mirror Lemma for such walks, or use the identification of a visit with a
   full lollipop walk on G_{k+1} (B1: rooted at r; B3: rooted at a port, with r inside the path);
   (b) hypothesis (ii) of the Mirror Lemma (v0 ∉ X ∪ N(X)) may fail for B3 visits rooted at the port
   adjacent to x (vertex 6 is adjacent to x = 5). The exact computation suggests the conclusion
   still holds; the lemma needs a version without (ii), or a check that the failing case does
   not occur.
4. **Induction.** Given the lemma, the outcome table of P_{k+1} and the sub-visit counts are a
   function of K, x, r, perm and P_k's outcome table alone. The finite computation (E19/E20)
   shows the table is a fixed point and yields M and b, so c_{k+1} = M c_k + b for all k.
5. **Lower bound.** One visit to P_{k−1} occurs inside the walk on G_k from a suitable start, so
   steps(G_k) ≥ c_{k−1}[e] for an entry e with the dominant growth, which is ≥ C·ρ^k. Hence
   Ω(ρ^{n/6}) = Ω(1.1974^n).

## What would make this a paper

- Close the GAP (step 3) and write steps 1, 2 and 5 properly.
- Explain the construction in words (which visits feed which), not only through the matrix.
- Search over more (K, x, r, perm) with |K| = 10, 12, and over multi-vertex substitution, for
  larger bases; the transfer-matrix method gives each family's exact base by a finite
  computation, which is itself a contribution.
- Read Briański–Szady in full (blocked here) to confirm the counting convention (steps vs states)
  and that no stronger result exists.
