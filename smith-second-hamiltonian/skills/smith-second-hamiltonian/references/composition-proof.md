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

## 0.5 Transducer Theorem: full proof (session 3 audit)

Setting of the Mirror Lemma (cut edges a matching, v0 ∉ X ∪ N(X), H = G/X simple).

**(T-i) Host independence.** While the endpoint is in X, a move is decided by the endpoint z, its
neighbours, its path predecessor and the forbidden vertex (the last attachment). Where the cut
edges at z are already path edges, z's admissible edges all lie inside X.
- In a B1 state Y1·X, an attachment w ∈ X has its successor in X, so only the X-segment is
  rearranged and Y1 is untouched.
- In a B3 state Y1·X1·Y2·X2, the moves are 3a (inside X2), 3b-i (Y2 reversed as one opaque block,
  X-pieces re-split) and 3b-ii (exit).
Hence the sequence of X-pieces with their order and orientation evolves as a function of the
entry configuration alone. The forbidden vertex is in X after the first internal move. At the
first move of a B1 visit it is q_in, so the cut edge at p_in is excluded: the visit cannot leave
immediately. That matches `visit_B1`.

**(T-ii) Exit states.**
- *B1.* The visit is entered by the host move S_{i−1} → S_i that deletes q_in x, with forbidden
  q_in. It exits from a port p_j by adding e_j, which projects to the host rotation at x along
  x q_j, with forbidden q_j in both graphs. The host walk at S_i takes the non-forbidden edge
  x q_c (c = third port), so exiting through p_c is the host's own next move (TRANSMIT). Exiting
  through p_in is the rotation along x q_in, which undoes the entry move (REFLECT, back to S_{i−1}).
- *B3.* The visit is entered by the host move S → S* attaching q_j to x, with forbidden x. It exits
  by case 3b-ii at Y1·x·rev(Y2) with forbidden p_b ↦ x. The run alternates S*, S, S*, …, so the
  exit lands at S* (TRANSMIT: the host continues from S* with forbidden x) or at S. In the second
  case, S's endpoint q_j has non-path edges x (forbidden) and one other, so the host walk moves
  backwards (REFLECT).

**(T-iii) Costs.** The number of moves between entry and exit is fixed by (T-i), so it is
host-independent. ∎ Exact check: E14 (4,691 / 4,691 runs, same final cycle and step count).

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

## 5. Growth certificate (exact rational arithmetic, `certificate.py`, refined by audit A8)

**A8 refinement.** The recursion is proved only for visit kinds that actually occur. Let R be the
set of entries reachable from ca/B3 along M. Every entry of R occurs (induction from the realized
passage of start (0, +1)), and rows of R reference only columns in R. R has 10 of the 12 entries;
ρ(M_R) = ρ(M). `audit/a4_a8_algebra.py` checks M_R u ≥ (29477/10000) u exactly, with u > 0 on all of
R. The argument below is applied to R only.


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
- **3-connected (proof).** For cubic graphs 3-connected ⇔ 3-edge-connected. Let K, G be
  3-edge-connected and cubic, P = G − r, K' = K[x ← P] with any wiring. Suppose F is an edge cut
  of K' with |F| ≤ 2 and sides A, B. If V(P) lies on one side, contracting V(P) to x gives a cut
  of K with the same edges: contradiction. Otherwise let F_P = F ∩ E(P). In G, put r on side A:
  the crossing edges are F_P plus r's edges to ports in B. Putting r on side B instead gives F_P
  plus r's edges to ports in A. Both partitions are nontrivial, so |F_P| + #ports(B) ≥ 3 and
  |F_P| + #ports(A) ≥ 3. Adding, 2|F_P| ≥ 3, hence |F_P| = 2 = |F|. So F avoids the edges at the
  ports, each port is on the same side as its K-neighbour u_i, and V(K) − x meets both sides. In
  K, put x on side A: the crossing edges are x's edges to u_i ∈ B, so #ports(B) ≥ 3. Likewise
  #ports(A) ≥ 3. That gives 6 ≤ 3, a contradiction. ∎
- **Planar (proof).** Embed G_k in the plane. Deleting r merges its faces into one face whose
  boundary meets the three ports in r's rotation order. Embed K; deleting x leaves a face meeting
  u_1, u_2, u_3 in x's rotation order. Place P = G_k − r inside that face and join u_i to its
  port. This is crossing-free iff the wiring maps one cyclic order to the other or to its
  reverse. Every bijection of 3-element sets does one of the two, and the reverse case is handled
  by mirroring P's embedding. So **any** substitution of a planar 3-pole into a vertex of a planar
  cubic graph is planar, and by induction every G_k is planar (K is planar). ∎
- Verified directly: cubic and planar for n ≤ 80, 3-connected for n ≤ 68, exactly 3 Hamiltonian
  cycles by exhaustive search for n ≤ 50 (audit A7, independent construction).

## 7. Audit (session 3, second pass): can this be counted as a proof?

All `audit/` scripts are independent of the production code unless noted.

| # | Claim | Proof status | Independent verification |
|---|---|---|---|
| 0 | Simulator = Thomason's algorithm | definition | A1/A2: production = edge-set reimplementation = brute-force state graph, 300 random graphs + all starts of levels 0–2 |
| 1 | Mirror Lemma | written, 8 cases | E12, E13 (0 / 85k violations) |
| 2 | Transducer Theorem | written in full (§0.5) | E14 exact 4,691 / 4,691 |
| 3 | Lemma S (simple ⇒ transparent) | written | A6: 7,233 / 7,233 simple poles (sizes 9–21) transparent; T3 |
| 4 | Lemma C (composition) | written | A5: 71,484 random (P', X) pairs, all of (a), (b), (c) exact; control with X not simple: h differs 98%, outcomes differ 56% |
| 5 | Recursion c_k = c_0 + M c_{k−1} (on R) | from 3, 4 and the base | T1; E19/E20 exact k ≤ 11 |
| 6 | steps(G_k; 0, +1) = 4 + c_{k−1}[ca/B3] | from 2, 3 | A3: independent construction, cycles by recursion, independent walk: exact k = 1..10 (n ≤ 68) |
| 7 | Growth: Ω(2.9477^k) | exact rational certificate on R (A8) | A4: charpoly λ²(λ−1)²(λ+1)²(λ²+1)(λ⁴−2λ³−2λ²−2λ−1), quartic irreducible, ρ = 2.947711586844637… |
| 8 | Exactly 3 Hamiltonian cycles | written | A7: exhaustive n ≤ 50 |
| 9 | 3-connected; planar | written (§6) | A7: 3-connected n ≤ 68, planar n ≤ 80 |
| 10 | Better than all published bounds | **unverified** | full texts blocked; snippets show B–S 1.1812 as best through 2024 |
| — | Consistency with exhaustive data | — | n = 14: max 27 ≤ exhaustive worst case W(14) = 29 (E1); n = 8: 6 = W(8) |

**Verdict.** Every link is proved in writing and independently verified, and the audit found and
closed one gap (A8: the recursion is only proved for visit kinds that actually occur). No
counterexample was found to any claim. This meets the standard of a complete proof by the
authors; it becomes an accepted result after (i) an independent human reading of §0.5–§2 and the
Mirror Lemma, and (ii) a full-text literature check (item 10).

**Theorem (pending i–ii).** For every k ≥ 0 there is a 3-connected planar cubic graph on
n = 8 + 6k vertices with exactly three Hamiltonian cycles, a Hamiltonian cycle C and an edge e on
which Thomason's lollipop algorithm takes Θ(ρ^k) = Θ(1.19742…^n) steps, where ρ is the largest
root of λ⁴ − 2λ³ − 2λ² − 2λ − 1.
