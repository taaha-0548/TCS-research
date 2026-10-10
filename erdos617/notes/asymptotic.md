# N(r) = r² + O(r^{3/2})

N(r) is the largest n for which K_n has an r-colouring where every (r+1)-set sees all r colours.
Affine planes give N(r) ≥ r² for prime powers r. Erdős–Gyárfás conjecture N(r) ≤ r².

**Theorem.** N(r) ≤ r² + (√2 + o(1))·r^{3/2}. In particular N(r) ≤ (1 + o(1))·r², which is the
asymptotic form of Erdős Problem #617.

Status: an elementary proof whose only external input is Füredi's stability theorem.
- Not refereed.
- Not found in the sources we could read: ErGy99, the 2026 fixed-r repositories, and abstracts of the
  set-colouring Ramsey literature. The relevant papers themselves were blocked by the sandbox network.
- The best general bound we know of in the literature is Erdős–Szemerédi (1972):
  R(k; r, r−1) ≤ r^{O(k/r)}. At k = r+1 this gives only N(r) ≤ r^{O(1)}.
- A literature check by a human is still needed.

## Tools

- **Turán's theorem.** p_r(n) is the minimum number of edges in an n-vertex graph with α ≤ r. It is
  attained by r near-equal cliques, so p_r(n) = Σ_j C(s_j, 2) with the s_j balanced.
- **Füredi's stability theorem** (JCTB 115 (2015) 66–71). If a graph is K_{r+1}-free with
  t_r(n) − t edges, then deleting at most t edges makes it r-partite.

## Proof

Fix a balanced r-colouring of K_n with r ≥ 2, and put K = n − r² ≥ 1. Let G be a colour class with the
fewest edges, so e(G) ≤ C(n,2)/r, and let H be the complement of G.

1. **The two basic constraints.** α(G) ≤ r, so H is K_{r+1}-free. Every (r+1)-set contains an edge of
   each of the other r−1 colours, so it spans at least r−1 edges of H.

2. **The budget t is less than n/2.** By Turán, e(G) ≥ p_r(n). Put t := e(G) − p_r(n) ≥ 0. By
   convexity p_r(n) ≥ n²/(2r) − n/2, so
   t ≤ n(n−1)/(2r) − n²/(2r) + n/2 = n(r−1)/(2r) < n/2.

3. **Füredi partition.** We have e(H) = t_r(n) − t. By Füredi, some partition V_1, …, V_r satisfies
   m := Σ_j e(H[V_j]) ≤ t. Write s_j = |V_j| = r + x_j, so Σ_j x_j = K.

4. **Imbalance is cheap only up to 2t.**
   - First, e(G) ≥ Σ_j (C(s_j,2) − e(H[V_j])) ≥ Σ_j C(s_j,2) − t. Since e(G) = p_r(n) + t, this gives
     Σ_j C(s_j,2) ≤ p_r(n) + 2t.
   - The identity C(r+x, 2) = C(r,2) + rx + x(x−1)/2 holds for every integer x.
   - The balanced parts defining p_r(n) have x ∈ {⌊K/r⌋, ⌈K/r⌉}, so they contribute at most K²/(2r) + K/2.
   - Putting these together:

     (1)  Σ_j x_j(x_j − 1)/2 ≤ K²/(2r) + K/2 + 2t < K²/(2r) + K/2 + n.

5. **Oversized parts cost r−1 each.** Suppose x_j ≥ 1. Any (r+1) vertices of V_j span at least r−1
   edges of H, all inside V_j, so e(H[V_j]) ≥ r−1. Let P = #{j : x_j ≥ 1}. Then

   (2)  P(r−1) ≤ m ≤ t < n/2.

   The sharper bound e(H[V_j]) ≥ (r−1)·C(s_j,2)/C(r+1,2), from averaging over (r+1)-subsets, is
   used only in the bootstrap step 7.

6. **Cauchy–Schwarz.**
   - Let S⁺ = Σ_{x_j ≥ 1} x_j ≥ K.
   - Since x(x−1) ≥ 0 for every integer x, we have Σ_{x_j≥1} x_j² ≤ Σ_j x_j(x_j−1) + S⁺.
   - So (1) gives Σ_{x_j≥1} x_j² ≤ K²/r + K + 2n + S⁺.
   - Then S⁺² ≤ P · Σ_{x_j≥1} x_j² ≤ P·(S⁺²/r + 2S⁺ + 2n), using K ≤ S⁺. That is,

   (3)  S⁺²·(1 − P/r) ≤ 2P·(S⁺ + n).

7. **Bootstrap.** We first need P/r bounded away from 1.
   - Using the averaging bound, Σ_j e(H[V_j]) ≥ (r−1)·Σ_{x_j≥1} (1 + (x_j−1)/r)², and this is at least
     (r−1)·(P(1 − 2/r) + 2S⁺/r).
   - Comparing with m < n/2 ≤ (r² + S⁺)/2 gives S⁺ ≤ (1/3 + o(1))·r².
   - Hence n ≤ (4/3 + o(1))·r², and (2) gives P ≤ (2/3 + o(1))·r.
   - Now (3) gives S⁺ = O(r^{3/2}). So n = r² + O(r^{3/2}), and (2) improves to P ≤ (1/2 + o(1))·r.
   - Feeding this back into (3): S⁺²·(1/2 − o(1)) ≤ (1 + o(1))·r³. So K ≤ S⁺ ≤ (√2 + o(1))·r^{3/2}. ∎

## Remarks

- The proof uses only the minority colour plus constraint (C): every (r+1)-set has at least r−1
  edges outside the colour. Example F2 in the README shows these alone cannot give N(r) ≤ r² for
  large r, so going beyond r² + O(r^{3/2}) has to use more information.
- **What is left on the table:** α(G) ≤ r across parts. Consider an H-edge uv inside an oversized part,
  plus one vertex from each other part. Such an independent (r+1)-set must be blocked by G-edges
  between parts (E⁺). Those edges come out of the same budget, since I + |E⁺| = t + m ≤ 2t, where
  I = Σ_j C(s_j,2) − p_r(n).
- **What a blocking lemma would give.** Suppose blocking needs |E⁺| ≥ (1+c)·r² whenever some part
  is oversized and the parts are near-balanced. Then this line would close to N(r) ≤ r² + O(r), and
  possibly to exactly r². That is approach 3 in the README; `scripts/blocking_lemma.py` measures the
  constant.
- **Numerics.** `scripts/asymptotic_bound2.py` runs the exact optimisation version of steps 3–6
  (balanced Turán p_r and the best per-part bound φ). It gives N(r) ≤ 30, 42, 57, 74, 116 for
  r = 5, 6, 7, 8, 10; the excess is about 0.4–0.5·r^{3/2}.
