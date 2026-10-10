# Lollipop: a Lean 4 formalization of the lollipop walk

Core Lean 4 only (no Mathlib), toolchain Lean 4.24.0. Build with `lake build`.

Toolchain setup used here: the Lean release server was blocked, so the official
`lean-4.24.0-linux.tar.zst` from the GitHub release was unpacked and linked with
`elan toolchain link lean-4.24.0 <dir>`. That is why `lean-toolchain` reads `lean-4.24.0`; on a
normal machine replace it with `leanprover/lean4:v4.24.0`.

## Status (all statements proved; no `sorry`)

| File | Content |
|---|---|
| `Rotation.lean` | `rot P i = P[0..i] ++ reverse P[i+1..]`. Proves: it permutes the vertices (so it keeps Hamiltonicity), keeps the prefix up to `w`, `rot (rot P i) i = P` (the state graph is undirected), and the new endpoint is `P[i+1]`. |
| `Path.lean` | `Chain` (walk in a graph), append and reverse lemmas; **`rot_chain`**: with a symmetric adjacency, if `z w` is an edge then the rotated sequence is again a path. |
| `Contract.lean` | Contraction of the 3-pole `X` to one vertex (`collapse`: each block of consecutive `X`-vertices becomes `none`). Proves that it splits over concatenation (merging at an `X`–`X` junction) and **commutes with reversal**; and **`collapse_rot`**: if the deleted edge `w s` and the added edge `z w` are not inside `X`, contracting after the rotation equals rotating after contracting, at the image of `w`. This is the principle behind every case of the Mirror Lemma. |
| `Walk.lean` | **`NBWalk.injective`**: a non-backtracking walk in a loopless symmetric graph of maximum degree 2, starting from a vertex of degree ≤ 1, never revisits a vertex. This is the reversibility fact behind Thomason's algorithm and Lemma 4 of the paper. |

Axiom check (`#print axioms`): only `propext`, `Quot.sound`, `Classical.choice`.

## Plan

1. Instantiate `Walk` for the lollipop state graph of a cubic graph. That gives a Lean proof that
   Thomason's algorithm terminates at a second Hamiltonian cycle, i.e. Smith's theorem.
2. **Mirror Lemma**: the core (`collapse_rot`) is done; remaining: the projection `π` (dropping the
   trailing block of a B3 state) and the case analysis A/B1/B3, which together show that `π` maps
   each rotation to a rotation or to a stay.
3. Transducer Theorem and composition with memory (the line–mirror reduction). In the research
   these are empirical for non-simple poles; a proof here would make them theorems.
4. Precise Lean statements of the Eppstein-question hypotheses (single-turn towers are
   predictable / multi-reflection towers are universal).
