# Rigidity of the balanced Füredi frame at n = r² + 1

Status: a lemma for one special configuration, not a result about the conjecture. It is a research
direction until the unbalanced case is handled, or shown to reduce to the balanced one.

## Setting
Fix a balanced r-colouring of K_{r²+1}. Let G be the minority colour and H its complement.
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
6. **Count against the budget.** |E⁺| ≥ C(r−1,2)(r−2) + 2(r−1). This exceeds r(r−1) for every r ≥ 5
   (r = 5: 26 > 20; the left side grows like r³/2). ∎

At r = 4 the bound is 6 + 6 = 12 against a budget of 12, so the lemma just fails there.

## Why this matters
At n = r² + 1, with near-balanced parts, blocking all independent sets needs about r³/2 cross edges,
while the budget is r². The affine-plane colouring of K_{r²} sits exactly on the boundary: its merged
colour is r row-cliques joined by perfect matchings (the columns). The one extra vertex is what forces
the cubic cost.

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
