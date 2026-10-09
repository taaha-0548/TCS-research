# Proof of the Ω(1.1974^n) lower bound: Composition Lemma, full argument and audit

Session 3. This replaces the "GAP" in `improved-lower-bound.md`. Status at the end (audit table).

## 0. Conventions

- Lollipop walk exactly as in Thomason 1978 / `lollipop.py`: fixed start vertex v0 and fixed first
  edge v0 v1; states are Hamiltonian paths starting with v0 v1; a step rotates at the endpoint z
  along the non-path edge zw with w ≠ previous attachment ("forbidden"), w ≠ v0; it stops when the
  endpoint's admissible edge goes to v0. **Steps = number of rotations.**
- A 3-pole X has ports p1, p2, p3 and cut edges ei = pi qi forming a matching. h_ij(X) = number of
  Hamiltonian paths of X between p_i and p_j. "Simple" means h_ij = 1 for all pairs.
- Visits and the transducer table (B1, B3 visits, outcome TRANSMIT/REFLECT, successor state, cost)
  as in `mirror-lemma.md` (Transducer Theorem). Cost convention: a B1 visit takes 2 + cost moves
  (entry, exit, cost internal moves); a B3 visit takes 1 + cost moves (entry, then cost moves
  including the exit move). Contracting X to a vertex x, the same passage takes 2 moves (B1) or
  1 move (B3) in the contracted graph. So **cost = extra moves caused by X**.
- Standing hypothesis (ii): v0 ∉ X ∪ N(X).

## 1. Lemma S (simple ⇒ transparent)

*If X is simple, every visit to X transmits, in every host satisfying (ii).*

Proof. Let H = G/X. By the Mirror Lemma, π maps the walk on G into H's line S_0, …, S_L. A host state
whose endpoint is outside X and which passes through x (type A) has exactly one lift: its Y-part is
fixed, and the X-part is the unique Hamiltonian path of X between the two ports it uses, oriented
by the path. Suppose a visit reflects.
- B1 visit: it is entered by the move S_{i−1} → S_i (endpoint becomes x). On reflection the walk
  exits to S_{i−1}, which has type A, so the walk is back at the unique lift of S_{i−1}: the
  G-state just before the visit.
- B3 visit: it is entered from an A-state S by the move adding the edge into x. On reflection it
  lands back at S (case 3b-ii), again the unique lift: the G-state just before the visit.
Either way the walk revisits a state. That is impossible: the state graph has maximum degree 2,
and the walk starts at a leaf, so it is a simple path. ∎

Evidence: E15/T3 — 2,223 / 2,223 random simple poles were transparent.

## 2. Lemma C (Composition)

Let P be a 3-pole and X ⊂ P a 3-pole with **(H2) δ(X) ⊆ E(P)**, i.e. N(X) ⊆ P. Let P' = P/X (X
contracted to a vertex x). If X is simple, then:
(a) P is simple iff P' is simple; more precisely h_ij(P) = h_ij(P');
(b) P and P' have the same outcome table (outcome and successor state for every visit);
(c) c_P[e] = c_{P'}[e] + Σ_f M[e][f] · c_X[f], where M[e][f] is the number of passages of kind f
    through x during a visit of kind e to P' (kind of a passage: B1 if the move makes x the endpoint
    by deleting x's entry edge, B3 if the move attaches to x; plus the oriented pair of X-ports used).
    M depends only on P' and the port naming of X.

Proof. Fix any host H with vertex y and v0 ∉ N_H[y]; let G = H[y ← P] and G' = G/X = H[y ← P'].
Since N(X) ⊆ P and v0 ∉ P ∪ N(P), hypothesis (ii) holds for X in G, and for P in G and P' in G'.

(a) A Hamiltonian path of P between two ports crosses δ(X) exactly twice (3-edge cut, even number
of crossings, at least 2). So it is a Hamiltonian path of P' together with a Hamiltonian path of X
between the matching X-ports. Since X is simple, this is a bijection.

(b), (c). By Lemma S, every visit to X transmits. By the Transducer Theorem, the walk on G is
the walk on G' in which each passage through x, i.e. each move of the form 1b (deleting x's entry
edge) or 1c (attaching to x), is replaced by a visit to X. That visit:
- starts in a state determined by the G'-state (X's internal path is unique by simplicity);
- transmits, so it ends in the G-state lifting the G'-state that follows the passage, with the
  same forbidden vertex (B1: the exit attachment q_c; B3: x, represented by the port p_b);
- takes c_X[f] extra moves.

So the G-walk is the G'-walk with these insertions. In particular the final cycles correspond, and
steps(G) = steps(G') + Σ over passages of c_X[f].

*Locality of the inserted moves.* Every passage through x happens inside a visit to P', possibly
sharing that visit's entry or exit move. The proof:
- A 1c move at x has its endpoint z ∈ N(x) ⊆ P' (by H2) before the move, so it occurs while a
  P'-visit is in progress. Its new endpoint lies in N(x) ⊆ P', so it is neither that visit's entry
  nor its exit.
- A 1b move at x makes x the endpoint, so it is the P'-visit's entry move or occurs inside the
  visit. It is the entry move exactly when the P'-entry deletes the edge from a port to x (B3 entry
  of P' with x right after the port).
- The passage's last move, the rotation at x, may be the P'-visit's exit move (case 3b-ii of P'
  with x as endpoint and the attachment a port of P').
In every case the extra moves of the X-visit lie strictly after the passage's entry move and up to
its exit move, which is the P-visit's exit move only if it is also the P'-visit's exit move. Hence
they are inside the window of the corresponding P-visit. Visits to P in G and visits to P' in G'
therefore correspond one-to-one, with the same kind, state, outcome and successor (this gives (b)),
and costs differing by the inserted X-costs (this gives (c)). The passages, their kinds and states
during a P'-visit depend only on P' and the visit (Transducer Theorem, host independence), so M is
well defined. ∎

## 3. The family and the induction

K, x = 5, r = 2, perm = (2,0,1) as in `improved-lower-bound.md`. P_0 = K − r, and
P_k = G_k − r = (K − r)[x ← P_{k−1}] = P_0[x ← P_{k−1}], because r ≠ x and r ∉ N_K(x)
(N_K(5) = {4, 6, 7}). Hence H2 holds with X = P_{k−1} inside P = P_k, and P' = P_k / P_{k−1} = P_0.

- Base (finite check, T1): P_0 is simple; table T_0 = all 12 visits transmit; c_0 =
  (3,10,5,10,3,10,5,10,3,6,3,6); M from the passages through x in the 12 visits of the 7-vertex P_0.
- Step: if P_{k−1} is simple, Lemma C(a) gives P_k simple (P_0 is simple). Lemma C(b) gives
  table(P_k) = T_0, and Lemma C(c) gives c_k = c_0 + M c_{k−1}.
- Hence c_k = Σ_{j=0}^{k} M^j c_0 for all k.

## 4. Walk length on G_k

G_k = K[x ← P_{k−1}]. For a start (v0, d) of K's cycle with v0 ∉ N_K[x], the Transducer Theorem and
Lemma S (P_{k−1} is simple) give

  steps(G_k; v0, d) = steps(K; v0, d) + Σ_f N_f(v0, d) · c_{k−1}[f],

where N_f counts passages of kind f through x in K's own walk. For (v0, d) = (0, +1): steps(K) = 4,
and there is a single passage, of kind ca/B3. So **steps(G_k; 0, +1) = 4 + c_{k−1}[ca/B3].**

## 5. Growth certificate (exact rational arithmetic, `certificate.py`)

There is a rational vector u ≥ 0 (support 10 of 12 entries) with M u ≥ λ u componentwise, for
λ = 29477/10000. Since c_0 > 0, ε := min_{u_i > 0} c_0[i]/u_i > 0, so c_0 ≥ ε u. By induction,
c_k ≥ M c_{k−1} ≥ ε λ^k u, using M ≥ 0. u[ca/B3] > 0, so

  steps(G_k; 0, +1) ≥ ε λ^{k−1} u[ca/B3] = Ω(λ^k).

With n = 8 + 6k this gives **Ω(λ^{n/6}) = Ω(1.19742^n)**. The spectral radius of M is
ρ = 2.947711586844… (largest root of λ^4 − 2λ^3 − 2λ^2 − 2λ − 1), so the bound is tight:
c_k = Θ(ρ^k).

## 6. Graph class

- **Exactly 3 Hamiltonian cycles.** Every Hamiltonian cycle of K[x ← P] crosses the cut twice, so
  the Hamiltonian cycles are pairs (Hamiltonian cycle of K through an edge pair at x, Hamiltonian
  path of P between the matching ports). K has exactly 3 Hamiltonian cycles. By Smith's theorem
  every edge lies in an even number of them, hence exactly 2, so each edge pair at x is used by
  exactly one. With P_{k−1} simple, G_k has exactly 3.
- **3-connected.** For cubic graphs this is equivalent to 3-edge-connected. Substituting a
  3-edge-connected 3-pole (G − r with G 3-edge-connected) into a vertex of a 3-edge-connected cubic
  graph keeps it 3-edge-connected: an edge cut of size ≤ 2 would induce one of size ≤ 2 in K or in
  G_{k−1}. **[write out]**
- **Planar.** K and every G_k are 3-connected, so by Whitney each has a unique embedding up to
  mirror image. The rotation at r is the same at every level, since r's edges are never touched.
  G_{k+1} is planar iff the cyclic order of K's rotation at x matches, under perm, the cyclic
  order of r's rotation in G_k up to reversal. That condition involves only K, x, r and perm, and
  the same holds at every level. G_1 is planar (computation), so the condition holds and every G_k
  is planar. **[write out the face argument]**
- Verified directly for n ≤ 80 (`graph_props.py`).

## 7. Audit: can this be counted as a proof?

| # | Claim | Status | Evidence |
|---|---|---|---|
| 1 | Mirror Lemma (π is a reflexive homomorphism) | proof written, 8 cases | E12, E13 (0 / 85k violations) |
| 2 | Transducer Theorem (host independence, exit states, costs) | proof sketched from the cases of 1 | E14 exact 4,691 / 4,691 |
| 3 | Lemma S (simple ⇒ transparent) | proof written (short) | 2,223 / 2,223 simple poles transparent (T3) |
| 4 | Lemma C (composition) | proof written | T1 (M from P_0 = M measured), T3 (2,223 random families exact), E20 |
| 5 | Induction and recursion c_k = c_0 + M c_{k−1} | follows from 3, 4 and the finite base | exact for k = 0..11 (E19/E20) |
| 6 | Walk formula on G_k | follows from 2, 3 | T2: 64 / 64 eligible starts exact, k ≤ 8; 16 / 48 ineligible fail (hypothesis needed) |
| 7 | Growth certificate | exact rational check | `certificate.py` |
| 8 | Exactly 3 Hamiltonian cycles | proof written | enumeration n ≤ 32 |
| 9 | 3-connected, planar | proof outlined | computation n ≤ 80 |
| 10 | Better than all known bounds | **unverified** | full-text access blocked; snippets show B–S 1.1812 as best through 2024 |

**Verdict.** The argument is complete in structure. Every step is either proved in writing or is a
finite exact computation, and each was cross-checked by an independent experiment. It reaches the
standard of a careful paper draft, **not yet a refereed proof**. Before claiming it publicly:
1. A human should check the Mirror Lemma case analysis (1) and write the Transducer Theorem (2) in
   full. Item 2 is the most compressed part of the chain.
2. Write out the 3-connectivity and planarity arguments (9).
3. Read Briański–Szady and later citing papers in full (10), and confirm the step-counting
   convention matches theirs. A difference of a constant number of steps does not change the base.
