# The Mirror Lemma (3-edge-cut projection theorem)

Status: **theorem, proof written in session 2 by case analysis; needs an independent
line-by-line check before it is used in a paper.** Computational check: E13
(`scripts/exp_projection_lemma.py`), 0 violations in ~85,000 walk steps over 22 different
3-poles. Novelty: **[verify]** against Krawczyk 1999, Cameron 2001 and the proof of
Thomassen's 3-cut reduction (cited by Zhong 2018); none of the abstracts or summaries found so
far state it.

## Setting

- G cubic, C0 a Hamiltonian cycle, v0 the fixed vertex and v0v1 the fixed first edge.
- **State graph 𝒢(G).** Vertices: Hamiltonian paths of G that start with v0v1. For a path P
  with endpoint z and a non-path edge zw with w ≠ v0, let s be the successor of w on P. The
  *rotation* is P' = P[v0..w] · reverse(P[s..z]) (delete ws, add zw). Every vertex has degree
  ≤ 2. A path is a *leaf* when z is adjacent to v0; it closes to a Hamiltonian cycle. The
  lollipop walk follows the component of 𝒢 from S0(G) = C0 minus its last edge at v0, and
  stops at the other leaf of that component.
- **3-pole.** X ⊂ V(G) with cut δ(X) = {e1, e2, e3}, ei = pi qi, pi ∈ X (ports), qi ∈ Y = V − X.
  Assume (i) the cut edges form a matching (p's distinct, q's distinct) and (ii) v0 ∉ X ∪ N(X).
  H = G/X: contract X to a single vertex x (H is a simple cubic graph by (i)). C0 crosses the
  cut exactly twice, so C0/X is a Hamiltonian cycle of H.

## Theorem (Mirror Lemma)

There is a map π : V(𝒢(G)) → V(𝒢(H)) such that every edge of 𝒢(G) is mapped either to an
edge of 𝒢(H) or to a single vertex. Consequently, writing C1(G) and C1(H) for the lollipop
outputs,

  C1(G)/X ∈ { C0/X, C1(H) }.

In the first case, C1(G) and C0 agree outside X: the walk returns a "local swap" inside X.

## The projection π

A Hamiltonian path from v0 ∈ Y alternates between Y-segments and X-segments, starting in Y,
and uses at most 3 cut edges. So it has exactly one of three shapes:

| type | shape | cut edges used | π(P) |
|---|---|---|---|
| A | Y1 · X · Y2 (endpoint in Y2) | 2 | Y1 · x · Y2 |
| B1 | Y1 · X (endpoint in X) | 1 | Y1 · x |
| B3 | Y1 · X1 · Y2 · X2 (endpoint in X2) | 3 | Y1 · x · Y2 (drop X2) |

Each π(P) is a Hamiltonian path of H starting with v0v1, since v0, v1 ∈ Y1 by (ii).

## Proof that π is a homomorphism (reflexive)

Let P → P' be a rotation at endpoint z with new edge zw and deleted edge ws. Contracting a
contiguous block commutes with suffix reversal, provided the cut point ws is not inside the
block. Most cases below reduce to that remark.

**Type A** (z ∈ Y2).
- *w, s ∈ Y.* The X-block is untouched or reversed whole; P' is of type A and
  π(P') = rotation of π(P) along zw. → 𝒢(H)-edge.
- *w ∈ Y, s ∈ X.* Then ws is the entry cut edge: w = q_in is the last vertex of Y1 and
  s = p_in. P' = Y1 · rev(Y2) · rev(X) has type B1 and π(P') = Y1 · rev(Y2) · x. This is
  the rotation of π(P) = Y1 · x · Y2 along zw, which deletes w x. → edge.
- *w ∈ X.* Then zw = ej is the unused cut edge (z = qj, w = pj), and pj is an interior
  vertex of the X-block, so s ∈ X. Write X = Xa · Xb with Xa ending at w. Then
  P' = Y1 · Xa · rev(Y2) · rev(Xb) has type B3 and π(P') = Y1 · x · rev(Y2). In H, z = qj
  has the non-path edge qj x; rotating along it deletes x·first(Y2) and gives exactly
  Y1 · x · rev(Y2). → edge.

**Type B1** (z ∈ X, entered once through port p_in).
- *w ∈ X.* Then s ∈ X; P' is B1 with the same Y-part, so π(P') = π(P). → same vertex.
- *w ∈ Y.* Then z = pj and w = qj with j ≠ in (e_in is a path edge, and the q's are distinct
  by (i)). So w is not the last vertex of Y1 and s ∈ Y1. Write Y1 = Ya · Yb with Ya ending
  at w. P' = Ya · rev(X) · rev(Yb) has type A and π(P') = Ya · x · rev(Yb). This is the
  rotation of π(P) = Y1 · x along x qj, a non-path edge of H at the endpoint x, and qj ≠ v0
  by (ii). → edge.

**Type B3** (z ∈ X2). All three cut edges are path edges, so w ∈ X.
- *w ∈ X2.* Then s ∈ X2; P' is B3 with the same Y1 and Y2. → same vertex.
- *w ∈ X1, w ≠ p_b* (p_b = exit port of X1). Then s ∈ X1. Write X1 = X1a · X1b with X1a
  ending at w. P' = Y1 · (X1a · rev(X2)) · rev(Y2) · rev(X1b) has type B3, and
  π(P') = Y1 · x · rev(Y2).
- *w = p_b.* Then s = q_b ∈ Y2 and P' = Y1 · (X1 · rev(X2)) · rev(Y2) has type A, with
  π(P') = Y1 · x · rev(Y2).
- In both of the last two cases, π(P) = Y1 · x · Y2 ends at q_c, and q_c x is a non-path
  edge of π(P) (π dropped e_c). The rotation along it deletes x q_b and gives
  Y1 · x · rev(Y2). → edge.

No other case can occur: a non-path edge at an endpoint in Y leads into X only through an
unused cut edge, and at an endpoint in X it leads into Y only through an unused cut edge.
Moves of type B1 → B3 never happen, which matches E13. ∎

## Proof of the consequence

The walk on G runs along the component K of 𝒢(G) from the leaf S0(G) to its other leaf T.
Since π(S0(G)) = S0(H), π maps K into the component L of 𝒢(H) containing S0(H). L is the
path S0(H) = S_0, …, S_L, and its leaves close to C0/X and C1(H). The leaf T has its endpoint
adjacent to v0, so by (ii) the endpoint lies in Y, T has type A, and the closing edge is a
Y-edge. Hence π(T) is a leaf of 𝒢(H) lying in L, so π(T) ∈ {S_0, S_L}, and the cycle T
closes to projects to C0/X or C1(H). ∎

## What it says about the dynamics

- The projected walk is a lazy walk on the line S_0..S_L. Stays come from rotations inside
  X (B1 and B3 runs). A B3 run alternates between two adjacent states of the line
  (Y1·x·Y2 ↔ Y1·x·rev(Y2)), which is where reversals happen.
- The walk ends at the far end of the line (C1(H)) or back at the start (a local swap). The
  pole's internal state, meaning which Hamiltonian path of X is currently in use, decides
  each time whether the walk passes through or turns back, and it persists between visits.
  So **a 3-pole is a stateful reversible mirror**, and the lollipop walk on a graph with
  many disjoint 3-poles is a zero-player reversible motion-planning system (route R of T1).

## Immediate corollaries (to check)

1. **Recursion.** For disjoint 3-poles X1..Xk (each satisfying (i), (ii)), the output projects
   onto each contraction as C0 or the contracted graph's output. Applying the theorem
   repeatedly, C1(G) projects to C0/{X1..Xk} or to the output on G/{X1..Xk}.
2. **SMITH side remark.** If the walk returns a local swap, the second cycle was "trivial":
   it changes only inside X. Hard instances for any SMITH algorithm can be assumed to have
   no 3-pole with two Hamiltonian paths between the same pair of ports (this is close to
   Thomassen's reduction; compare).
3. **Lower bounds.** The step count of G equals the steps spent along the line plus the
   steps spent inside each excursion. A family whose poles reflect many times gives long
   walks. Check whether the Krawczyk/Cameron analyses are an instance of this.

## Transducer Theorem (session 2)

Status: **follows from the case analysis above (sketch below); checked exactly by E14.**

The cases where the endpoint lies inside X (B1 runs: case 2a; B3 runs: cases 3a and 3b) only
use edges inside X and the three port labels. So what happens during a visit to X is decided
by X alone and by its internal state, never by the host. That state is the Hamiltonian path Q
of X that the current path uses, oriented from the port nearer v0.

- **B1 visit** (the host walk deletes x's entry edge, case 1b): X is re-rooted at p_out and the
  endpoint wanders inside X (case 2a). It leaves through a cut edge (case 2b): through p_in =
  REFLECT, through the third port = TRANSMIT.
- **B3 visit** (the host walk adds the unused cut edge at the third port, case 1c): X splits
  into X1 and X2, and the walk ping-pongs between the two host states Y1·x·Y2 and Y1·x·rev(Y2)
  (case 3b-i) until it exits (case 3b-ii). TRANSMIT iff the number of 3b-i moves is odd.
- Every visit returns (TRANSMIT or REFLECT, new path Q', number of steps). `scripts/transducer.py`
  computes the table; `scripts/show_transducer.py` prints it.
- **Exactness (E14):** simulating the host walk on H and consulting the table at each visit
  reproduces the walk on G exactly, with the same final cycle and the same step count, in 4,691
  of 4,691 runs (20 poles, hosts up to n = 50).

So **the lollipop walk on G equals the walk on G/X plus a finite reversible automaton for X**.
Disjoint 3-poles compose: one automaton each.

## Pole classes (E15)

- *transparent*: never reflects (triangle, prism−v, K33−v, …).
- *fixed mirror*: reflects, but transmit or reflect never depends on Q (cube−v: every B1 visit
  transmits, every B3 visit reflects).
- *active memory*: transmit or reflect depends on Q. Example rand10−v#0 (h = 3, 3, 1): for
  pair {a,b} oriented a→b, a B1 visit transmits from path 0 but reflects from paths 1 and 2,
  and the reflection swaps 1 ↔ 2.
- Share of random poles with active memory: 12% (|X| = 7), 35% (9), 55% (11), 77% (13),
  70% (15).
