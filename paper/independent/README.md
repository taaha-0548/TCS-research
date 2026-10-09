# Independent reimplementation (verification round 1)

Written from the definitions in `paper.tex` alone, without reading or importing `verify.py` or any
research code. It uses networkx and sympy.

| Script | Checks | Result |
|---|---|---|
| `run_steps.py K` | builds G_k, runs the lollipop walk (two implementations), compares with Table 1 | k ≤ 12 match; k = 13 gives 3,573,892 (= recursion) |
| `structure.py H S` | K has 3 Hamiltonian cycles and is the only connected cubic 8-vertex graph with 3; P_0 simple; G_k simple, cubic, 3-connected, planar for k ≤ S; exactly 3 Hamiltonian cycles for k ≤ H | all pass with H = 8 (n ≤ 56), S = 12 (n ≤ 80) |
| `appB.py` | Appendix B trace on G_1, path by path | identical |
| `linalg.py` | M and c_0 vs Table 2, characteristic polynomial, irreducibility, ρ, R, Table 3 certificate, Perron certificate | all pass |
| `instrument.py` | re-derives Table 2 and Appendix A from visits observed in G_k (k ≤ 8) and in 109,632 runs on 21 hosts H[y ← P_0] | all 12 visit types host-independent, transmit, and match the paper exactly |
