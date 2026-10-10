# Upper bounds on N(r)

N(r) is the largest n for which K_n has an r-colouring where every (r+1)-set sees all r colours.
Affine planes give N(r) ≥ r² for prime powers r. Erdős–Gyárfás (Problem #617) conjecture N(r) ≤ r².

Status: elementary arguments whose only external input is Füredi's stability theorem.
- Not refereed.
- Novelty is unverified. The relevant papers were seen only as search summaries: Erdős–Szemerédi 1972;
  Conlon–Fox–He–Mubayi–Suk–Verstraëte; Aragão–Collares–Marciano–Martins–Morris.
- The best general bound we know of is Erdős–Szemerédi: R(k; r, r−1) ≤ r^{O(k/r)}, which gives
  N(r) ≤ r^{O(1)}.

**Theorem A (headline).** N(r) < 2r³/(r+1) < 2r² for all r ≥ 2.

**Theorem B.** For r ≥ 10, N(r) ≤ r² + 2√2·r^{3/2} + 16r.
The proof is valid from r = 10, but B only improves on A from r = 35 on (r = 34: A ≈ 2246, B ≈ 2261;
r = 35: A ≈ 2382, B ≈ 2371). So B is an asymptotic statement. For actual finite-r values, use the
script optimisation (see Remarks), which beats both theorems at every r computed.

**Corollary C** (more fragile; the constant needs its own check). N(r) ≤ r² + (√2 + o(1))·r^{3/2}.

## Tools
- **Turán.** p_r(n) is the minimum number of edges of an n-vertex graph with α ≤ r. It is attained by
  r cliques of near-equal sizes, and by convexity p_r(n) ≥ n²/(2r) − n/2.
- **Füredi** (JCTB 115 (2015) 66–71, Thm 1). If H is K_{r+1}-free with e(H) = t_r(n) − t, where t ≥ 0,
  then H has an r-partite subgraph with at least e(H) − t edges. Equivalently, deleting at most t edges
  makes H r-partite.

## Common setup
Fix an r-colouring of K_n, r ≥ 2, in which every (r+1)-set of vertices sees all r colours. Erdős–Gyárfás
call such a colouring "balanced"; this is a condition on (r+1)-sets, not on class sizes. Let G be a colour class with the fewest edges, so
e(G) ≤ C(n,2)/r, and let H be the complement of G.

- **(S1)** α(G) ≤ r, so H is K_{r+1}-free.
- **(S2)** Every (r+1)-set spans at least r−1 edges of H, one for each of the other r−1 colours.
- **(S3)** Put t := e(G) − p_r(n). Turán gives t ≥ 0, and
  t ≤ n(n−1)/(2r) − (n²/(2r) − n/2) = n(r−1)/(2r).
- **(S4)** Since e(H) = C(n,2) − e(G) = t_r(n) − t, Füredi gives an r-partition V_1, …, V_r with
  m := Σ_j e(H[V_j]) ≤ t.
- **(S5)** e(G) ≥ Σ_j e(G[V_j]) = Σ_j (C(|V_j|,2) − e(H[V_j])). So
  p_r(n) + t = e(G) ≥ Σ_j C(|V_j|,2) − m ≥ Σ_j C(|V_j|,2) − t, that is,

  Σ_j C(|V_j|,2) ≤ p_r(n) + 2t.

## Proof of Theorem A
G has no K_{r+1}, because a monochromatic K_{r+1} misses the other colours. So for each j,
α(H[V_j]) ≤ r. A graph with s vertices and e edges has α ≥ s − e (delete one endpoint of each edge), so
e(H[V_j]) ≥ |V_j| − r. Summing over j gives n − r² ≤ m ≤ t ≤ n(r−1)/(2r). Hence n·(r+1)/(2r) ≤ r², that
is, n ≤ 2r³/(r+1). ∎

## Proof of Theorem B
Put n = r² + K with K ≥ 1, write |V_j| = r + x_j (so Σ_j x_j = K), and let
P = #{j : x_j ≥ 1} and S⁺ = Σ_{x_j ≥ 1} x_j. Note S⁺ ≥ K.

**(B1) Imbalance.** For every integer x, C(r+x, 2) = C(r,2) + rx + x(x−1)/2. The balanced parts that
achieve p_r(n) have x ∈ {⌊K/r⌋, ⌈K/r⌉}, so each contributes x(x−1)/2 ≤ (K/r)(K/r + 1)/2. Then (S5) gives

  Σ_j x_j(x_j−1) ≤ K²/r + K + 4t.

**(B2) Oversized parts.** If x_j ≥ 1, any (r+1)-subset of V_j spans at least r−1 H-edges by (S2), so
e(H[V_j]) ≥ r−1. Hence P(r−1) ≤ m ≤ t ≤ n(r−1)/(2r), which gives

  P ≤ n/(2r).

The averaging form is also used: e(H[V_j]) ≥ (r−1)·C(|V_j|,2)/C(r+1,2) ≥ (r−1)·(1 + 2(x_j−1)/(r+1)).
The last step uses (r+x)(r+x−1) = r(r+1) + 2(x−1)r + x(x−1) ≥ r(r+1) + 2(x−1)r for x ≥ 1.

**(B3) Cauchy–Schwarz.**
- Since x(x−1) ≥ 0 for every integer x, Σ_{x_j≥1} x_j² ≤ Σ_j x_j(x_j−1) + S⁺ ≤ K²/r + K + 4t + S⁺.
- By (S3), 4t < 2n = 2r² + 2K. Using K ≤ S⁺, this gives Σ_{x_j≥1} x_j² ≤ S⁺²/r + 4S⁺ + 2r².
- Then S⁺² ≤ P·Σ_{x_j≥1} x_j², so

  (★)  S⁺²·(1 − P/r) ≤ P·(4S⁺ + 2r²).

**(B4) A first bound on S⁺, for r ≥ 10.**
- Summing the averaging bound in (B2) over oversized parts and dropping the P term gives
  2(r−1)S⁺/(r+1) ≤ m ≤ t < n/2 ≤ (r² + S⁺)/2.
- So S⁺·(2(r−1)/(r+1) − 1/2) < r²/2. At r = 10 the coefficient is 18/11 − 1/2 > 1.13, and it increases
  with r, so S⁺ < 0.45r².
- Hence n < 1.45r², and (B2) gives P ≤ n/(2r) < 0.73r, so 1 − P/r > 0.27.

**(B5) Conclusion.**
- Put the bounds from (B4) into (★): 0.27·S⁺² ≤ 0.73r·(4S⁺ + 2r²).
- Hence S⁺² ≤ 11r·S⁺ + 5.5r³, so S⁺ ≤ 11r + √(5.5)·r^{3/2}.
- This is at most 16r + 2√2·r^{3/2}, since √5.5 < 2.35 < 2√2. And K ≤ S⁺. ∎

## Proof of Corollary C
Theorem B gives S⁺ = O(r^{3/2}). So n = r² + O(r^{3/2}) and P ≤ n/(2r) = r/2 + O(r^{1/2}). Feed this
into (★): (1/2 − O(r^{−1/2}))·S⁺² ≤ (r/2 + O(r^{1/2}))·(2r² + O(r^{3/2})) = r³ + O(r^{5/2}). Hence
S⁺ ≤ (√2 + O(r^{−1/2}))·r^{3/2}. ∎

## Remarks
- Only the minority colour and (S2) are used. The F2 construction in the README shows that, for large r,
  these two constraints alone cannot give N(r) ≤ r². So any further progress must use α(G) ≤ r across
  parts (cross-edge blocking), or the other colours.
- `scripts/asymptotic_bound.py` and `scripts/asymptotic_bound2.py` solve the exact optimisation behind
  these arguments. They give N(r) ≤ 10, 18, 30, 42, 57, 74, 116, 259, 460 for
  r = 3, 4, 5, 6, 7, 8, 10, 15, 20. These beat both Theorem A and Theorem B at every r listed; the
  theorems describe the asymptotic shape, and the scripts give the finite-r data.
