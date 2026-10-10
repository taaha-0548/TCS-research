# Rigidity of the balanced Füredi frame at n = r² + 1

Status: a lemma for one special configuration, not a result about the conjecture. It is a research
direction until the unbalanced case is handled, or shown to reduce to the balanced one.

## Setting
Fix an r-colouring of K_{r²+1} in which every (r+1)-set sees all r colours (balanced, in Erdős–Gyárfás's
sense). Let G be the minority colour and H its complement.
- Since e(G) ≤ C(n,2)/r and p_r(r²+1) = r·C(r,2) + r, the budget is t := e(G) − p_r(n) ≤ C(r,2).
- Füredi gives an r-partition V_1, …, V_r with m := Σ_j e(H[V_j]) ≤ t.
- Write M for the non-edges of G inside parts (so |M| = m), and E⁺ for the G-edges between parts.
- Then e(G) = Σ_j C(|V_j|,2) − |M| + |E⁺|. With I := Σ_j C(|V_j|,2) − p_r(n) ≥ 0 this gives

  I + |E⁺| = t + |M| ≤ 2t ≤ r(r−1).        (budget)

## Lemma (balanced frame)
Let r ≥ 5. The Füredi partition cannot be |V_1| = r+1, |V_2| = … = |V_r| = r with V_2, …, V_r cliques of G.
Nothing is assumed about the inside of V_1.

## Proof
1. **The big part has a missing edge.** By (C), the (r+1)-set V_1 spans at least r−1 edges of H. So V_1
   contains a pair uv that is not an edge of G.
2. **Cross edges are matchings.** If x lies outside an r-clique Q of G, then Q ∪ {x} has
   C(r,2) + d_Q(x) ≤ C(r,2) + 1 edges, so d_Q(x) ≤ 1. Hence G between two of V_2, …, V_r is a matching,
   and u, v each have at most one neighbour in each V_k.
3. **What an independent set looks like.** An independent (r+1)-set may consist of u, v and one vertex
   from each of V_2, …, V_r. Put R_k = V_k \ (N(u) ∪ N(v)), so |R_k| ≥ r−2. We need an independent
   transversal of R_2, …, R_r in a graph where every vertex has at most one neighbour in every other part.
4. **Greedy succeeds unless every R_k has size exactly r−2.** Order the parts by increasing size and pick
   greedily. At step i at most i−1 vertices are forbidden, so we succeed unless |R_(i)| ≤ i−1 for some i.
   With all |R_k| ≥ r−2 and r−1 parts, that can happen only at the last step with every |R_k| = r−2.
   So u and v have distinct neighbours in every V_k, giving 2(r−1) edges of E⁺ at u, v.
5. **Then the matchings are perfect.** Take x ∈ R_j. Deleting N(x) removes at most one vertex from each
   other R_l. If some R_l loses none, put it last; greedy then completes an independent transversal
   through x. So x has exactly one neighbour in every other R_l, and every pair R_j, R_l is joined by a
   perfect matching. That is C(r−1,2)·(r−2) more edges of E⁺.
6. **Count against the budget.** |E⁺| ≥ C(r−1,2)(r−2) + 2(r−1). This exceeds r(r−1) exactly when
   (r−1)(r−2)(r−4) > 0, i.e. for every r ≥ 5 (r = 5: 26 > 20; the left side grows like r³/2). ∎

At r = 4 the bound is 6 + 6 = 12 against a budget of 12, so the lemma just fails there.

## Why this matters
At n = r² + 1, with near-balanced parts, blocking all independent sets needs about r³/2 cross edges,
while the budget is r². Compare the affine-plane colouring of K_{r²}. There the minority colour is a
single parallel class: r disjoint r-cliques, with t = 0 and no cross edges at all, and nothing needs
blocking because no part has a missing edge. Adding one vertex forces a part of size r+1 and hence a
missing edge uv. Blocking all the independent sets through uv then costs about r³/2 cross edges.
(The merged colour of the affine construction, rows joined by column matchings, is the largest class,
not the minority one, so it is not the relevant picture here.)

## Proof strategy for all large r
The lemma needs a robust version that allows:
- (a) parts with sizes r + x_j, where Σ x_j = 1 and Σ x_j(x_j−1)/2 = I ≤ r²;
- (b) M-edges inside parts other than V_1, with |M| ≤ C(r,2) in total;
- (c) parts that are not cliques.

The degree bound in step 2 generalises to d_A(x) ≤ 1 + e(H[A]) for any r-set A in a part of size at
least r. The difficulty is deficient parts (size r − y), which an outside vertex may dominate
completely. Such a part costs y(y+1)/2 of the imbalance budget, and its missing vertices must be
absorbed by oversized parts, each costing at least r−1 of |M| ≤ C(r,2).

Tools that should handle this:
- greedy or independent-transversal arguments with local degree bounds (Haxell; Loh–Sudakov;
  DP-colouring degeneracy);
- a potential function that charges deficient parts.

Because the slack is r³ against r², this looks feasible for r ≥ r₀. `scripts/frame_min.py` tests
generalised frames exactly for small r.

## Working notes: deficient parts (in progress)

All of this is at n = r² + 1, using the notation above.

**D1. Budgets.** m ≤ t ≤ C(r,2). Also I + |E⁺| = t + m ≤ r(r−1), where I = Σ_j x_j(x_j−1)/2. (This
uses p_r(r²+1) ↔ x = (1,0,…,0).) Moreover P ≤ r/2 and Σ_j x_j = 1.

**D2. Degree bound into a deficient clique.** Let K be a G-clique part of size r − y, and Z a set of y+1
vertices outside K. Then K ∪ Z is an (r+1)-set, so

  Σ_{z∈Z} d_K(z) + e_G(Z) ≤ C(r,2) + 1 − C(r−y,2) = y(2r−y−1)/2 + 1.

For y = 1 this is d_K(a) + d_K(b) + [ab ∈ G] ≤ r for all a, b outside K. The bound d ≤ 1 is lost: many
outside vertices can have about r/2 neighbours each in K. At most one can have more than r/2.

**D3. Local optimality.** Take the Füredi partition that minimises m; this still has m ≤ t. Moving a
vertex u from V_j to V_k changes m by d_H(u,V_k) − d_H(u,V_j) ≥ 0. Therefore

  d_G(u, V_k) ≤ |V_k| − d_H(u, V_j)   for all u ∈ V_j and k ≠ j.

In particular, an endpoint of an H-edge never dominates another part on its own.

**D4. Spread surplus (P ≥ 2).**
- Each oversized part supplies an independent pair (an H-edge). So an independent (r+1)-set can use two
  pairs and skip one part, in particular a deficient one.
- More generally, with P oversized parts up to P−1 parts can be skipped. The remaining parts are then
  back in the near-balanced regime of the lemma, where blocking costs about r³/2.
- Not yet written carefully: the doubled parts take 4 vertices' neighbourhoods out of the others, so the
  reduced sizes are ≥ r−4 on r−3 parts. The same greedy then forces near-perfect matchings.

**D5. Concentrated surplus (P = 1). This is the dangerous case.**
- Here one part has size r + x and absorbs all deficiency. If H[V_1] is triangle-free, V_1 offers only
  pairs, so every part must be used and no deficient part can be skipped.
- Blocking an H-edge uv can then be cheap: it suffices that N(u) ∪ N(v) ⊇ K for some deficient K. By D2
  that costs only about r/2 edges per vertex.
- **Budget-tight candidate** (one specific attempt, not the general case). Sizes (r+2, r−1, r, …, r).
  V_1 has H[V_1] = C_{r+2}, so G[V_1] is the complement of the cycle. K is the (r−1)-part. Every cycle
  edge uv is blocked by covering, N(u) ∪ N(v) ⊇ K; no other blocking is used.
  - Covering forces d(u) + d(v) ≥ r−1 on every cycle edge. Summing over the r+2 edges, the edges from
    V_1 to K number Σd ≥ (r+2)(r−1)/2.
  - With I = 2 and m = r+2, the budget t = I + |E⁺| − m ≤ C(r,2) allows |E⁺| ≤ (r² + r)/2. That is one
    edge more than (r+2)(r−1)/2.
  - So all but at most two units of slack are tight: d(u) + d(v) = r−1 on all cycle edges but at most
    two. (By D2, d(u) + d(v) ≤ r on an H-edge, so no single edge can absorb more.)
  - On a tight edge, |N(u)| + |N(v)| = |K| and the union is K, so N(v) = K \ N(u).
  - **r odd.** C_{r+2} is an odd cycle. If every edge is tight, going round the cycle gives
    N(w) = K \ N(w) for a vertex w, which is impossible. With one or two slack edges the alternation
    breaks there, so this case still needs a short extra argument.
  - **r even.** If every edge is tight, the alternation gives the two colour classes A and B of the even
    cycle common neighbourhoods K_A and K_B = K \ K_A. Vertices on the same side are non-adjacent in H,
    so they are adjacent in G. Hence A ∪ K_A and B ∪ K_B are G-cliques with total size
    (r+2) + (r−1) = 2r+1, so one has at least r+1 vertices. That violates (C). The one or two slack edges
    again need a short extra argument.
  - **Status.** The configuration looks impossible, but the slack-edge cases are not written out. It is
    budget-tight to within one edge, which is why it is the one to check.
- Open: whether unequal degrees, or another H[V_1] with more edges, escapes this. That needs the pair
  sums of D2 together with the clique cap on Q ∪ K′ for G-cliques Q ⊆ V_1.
- Exact check prepared but stopped: `DECIDE_CAP=65 python3 scripts/frame_min.py 5 custom 7,4,5,5,5 0`, and
  `8,5,6,6,6,6` for r = 6. r = 5 and 6 are claimed solved, so these would only probe the lemma.

**Proposed lemma to aim for.** In the m-minimal Füredi partition at n = r²+1, suppose an H-edge uv lies in
V_j. Then blocking all independent (r+1)-sets through uv costs more than the budget allows, once each
deficient part's cost y(y+1)/2 and each oversized part's cost are charged against r(r−1).
