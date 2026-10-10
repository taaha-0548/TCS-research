# Draft forum post for Erdős Problem #617 (to be posted by a human; not yet posted)

Before posting, check that someone can actually post on this problem: an issue thread reported that
comments on the page were closed.

**Title:** A short general bound: N(r) ≤ r² + ⌊r/2⌋

Let N(r) be the largest n such that K_n has an r-colouring in which every r+1 vertices see all r colours.
The conjecture is N(r) ≤ r² for r ≥ 3. Affine planes give N(r) ≥ r² for prime powers r.

**Claim.** For every r ≥ 2, N(r) ≤ 2r³/(2r−1), i.e. N(r) ≤ r² + ⌊r/2⌋.

**Proof.**
1. Take such a colouring of K_n. Let G be a colour class with the fewest edges, and let H be its
   complement, which is the union of the other r−1 classes.
2. Every colour class has independence number at most r, so H is K_{r+1}-free.
3. Let p_r(n) be the Turán minimum number of edges in an n-vertex graph with α ≤ r, and put
   t = e(G) − p_r(n). Then 0 ≤ t ≤ C(n,2)/r − p_r(n) ≤ n(r−1)/(2r).
4. Since e(H) = t_r(n) − t, Füredi's stability theorem (JCTB 115 (2015)) gives an r-partition V_1, …, V_r
   with at most t edges of H inside the parts.
5. Each other colour c has α ≤ r inside every V_j, so it has at least p_r(|V_j|) ≥ |V_j| − r edges inside
   V_j. These are edges of H, and different colours give disjoint edges.
6. Hence (r−1)·Σ_j max(0, |V_j| − r) ≤ t. The left side is at least (r−1)(n − r²).
7. So (r−1)(n − r²) ≤ n(r−1)/(2r), which gives n ≤ 2r³/(2r−1). ∎

**Remarks.**
- The bound is sharp at r = 2: it gives 5, and the pentagon colouring attains equality.
- An exact computation (exact Turán numbers and budget, optimised over all part sizes) gives exactly
  r² + ⌊r/2⌋ for 2 ≤ r ≤ 15.
- The inequality in step 5 is the coloured-density bound used in Sneiderman's fixed-r proofs. Here it is
  applied inside the parts of a Füredi partition.
- Alon, Erdős, Gunderson and Molloy (J. Graph Theory 40 (2002)) give N(r) ≤ (1+o(1))r², with an
  unquantified error term. This bound makes the error term explicit and linear.
- It does not settle the problem: at n = r²+1 the argument only forces t ≥ r−1, while t may be as large as
  C(r,2).

**Status.** We do not claim this is new. We could not access this forum's existing discussion. We found no
bound of this form in ErGy99, AEGM, the set-colouring Ramsey papers, or the 2026 fixed-r manuscripts, but
that search was incomplete. If an N(r) ≤ r² + O(r) bound is already known, we would be grateful for the
reference.

AI-assistance disclosure: found and checked with the help of an AI assistant (Claude); the proof was also
independently re-checked line by line by a second reviewer. Not refereed.
