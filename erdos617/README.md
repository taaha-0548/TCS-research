# Erdős Problem #617 (Erdős–Gyárfás balanced colourings)

**Conjecture.** For r ≥ 3, every r-colouring of the edges of K_{r²+1} contains r+1 vertices whose K_{r+1}
misses a colour (no *balanced* colouring). Proved for r = 3, 4 (Erdős–Gyárfás 1999); open from r = 5.

**Observation.** In a balanced colouring, each colour class G_k has α(G_k) ≤ r and ω(G_k) ≤ r. The union of
any r − 1 classes is K_{r+1}-free.
- The Turán bound gives e(G_k) ≥ (r³ − r² + 2r)/2, which is 55 for r = 5.
- A claimed exact bound (erdosproblemaday.com, unverified here) gives (r³ − r² + 4r − 2)/2, which is 59 for r = 5.
- So 5 classes need ≥ 295 of 325 edges. Showing that every class needs ≥ 66 edges would prove r = 5.

**Plan.**
1. Verify the claimed bound for r = 2, 3, 4 by exact computation.
2. Sanity-check the SAT model on r = 3, 4.
3. Attack the gap for r = 5 (multi-colour constraints, stability, structured SAT).

`balanced_sat.py`: SAT model of balanced colourings (optional cyclic symmetry). Written; not yet run.
