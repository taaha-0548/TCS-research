# Eppstein's question: hypotheses, their Lean status, and evidence

**Question (Eppstein 2023):** is computing the cycle returned by Thomason's lollipop algorithm
FP^PSPACE-complete?

**Research model.** Towers of 3-pole gadgets, `P_j = P'[x ← P_{j+1}]`. By the Transducer Theorem
each level is a recursive bounce machine (`Machine.lean`): a visit makes calls to the level below,
each answered transmit or reflect.

| Id | Statement | Status |
|---|---|---|
| L1 | If every local procedure of P′ satisfies `RForcesR` (after a reflecting answer, every reachable return reflects), every tower over a T↓ base has T↓: a transmitting visit makes only transmitting calls, at every depth. | **Proved** (`RBM.tower_TDown`) |
| L2 | In an all-transmit visit, the outcome and new local state depend only on (local state, entry type), and the child is acted on by the fixed call word of the all-transmit branch. So transmitting dynamics is a functionally recursive self-similar action `g_e(s, c) = (s', w_{s,e}·c)`. | **Proved** (`RBM.run_of_ok`, `RBM.run_child_of_ok`, `RBM.tower_transmit_selfsimilar`) |
| L1′ | As L1, but `RForcesR` is required only on answer sequences that a reversible child can produce (Site Normal Form axioms: retrace, and reflection is an involution). | **Empirical:** over 1,385 random gadgets × 4 bases × 3 levels, L1′ ⇒ T↓ in 362/362 (`phase5/cycle19b.py`). When L1′ fails, T↓ breaks in 840/1,023. Lean statement pending: it needs the reversible-gadget axioms in `Machine.lean` and their closure under composition. |
| L3 | Closure: if the child satisfies the Site Normal Form axioms, so does `P'[x ← child]`. | Empirical (Site Normal Form on all tested poles). Next to formalize; together with L1′ it would make T↓ a theorem for the L1′ class. |
| H-cascade | For L1′ towers, a top visit is a self-similar action plus at most one reflecting spine, so predicting the output reduces to **evaluating a functionally recursive action** on a depth-d point. | Follows from L1′+L2 (to formalize). Complexity of that evaluation is open (H4: realisable transparent libraries with a hard point-evaluation?). |
| H-hard | Hardness, if any, among single-slot towers lives in towers where L1′ fails (multi-reflection: upward information flow). 256/8,172 random towers are both exponentially growing and multi-reflecting (cycle 16). | Hypothesis. Next test: reflections per top visit by depth in these candidates (`cycle17.py`, written, not run). |

Refuted along the way:
- **L1 with all answer sequences, as the explanation of T↓ in real towers.** Rich tower #21 has T↓ empirically but fails strong `RForcesR`. The failing branches need a non-reversible child, e.g. repeated `bc/B1` reflections, which by the involution axiom would loop forever (cycle 18).
