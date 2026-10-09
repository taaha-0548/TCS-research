"""A4: exact characteristic polynomial, factorisation, Perron root.
A8: the recursion is only proved for visit kinds that actually occur.  Restrict to the set R of
entries reachable from ca/B3 (the single passage of start (0,+1)) along M, and re-check the growth
certificate on R alone, in exact rational arithmetic."""
import json, sympy as sp
from fractions import Fraction as F
d = json.load(open("../e20_M.json")); keys = d["keys"]; M = d["M"]; c0 = d["b"]
lam = sp.symbols("lam"); Ms = sp.Matrix(M)
cp = sp.factor(Ms.charpoly(lam).as_expr()); print("charpoly =", cp)
q = lam**4 - 2*lam**3 - 2*lam**2 - 2*lam - 1
print("quartic irreducible over Q:", sp.Poly(q, lam).is_irreducible)
roots = sp.Poly(q, lam).nroots(n=30); rho = max(r for r in roots if r.is_real); print("rho =", rho)
eig = {complex(k).__abs__(): v for k, v in Ms.eigenvals().items()}
print("max |eigenvalue| of M =", sp.N(max(abs(sp.N(e)) for e in Ms.eigenvals()), 20))
# A8: reachable set from ca/B3
start = keys.index("ca/B3"); Rset = {start}; stack = [start]
while stack:
    i = stack.pop()
    for j in range(12):
        if M[i][j] and j not in Rset: Rset.add(j); stack.append(j)
Rl = sorted(Rset); print("reachable entries R:", [keys[i] for i in Rl], f"({len(Rl)}/12)")
MR = sp.Matrix([[M[i][j] for j in Rl] for i in Rl])
print("rho(M restricted to R) =", sp.N(max(abs(sp.N(e)) for e in MR.eigenvals()), 20))
# certificate on R: Perron vector of MR, rationalised, check MR u >= lam u exactly
import numpy as np
w, V = np.linalg.eig(np.array(MR.tolist(), dtype=float)); i = int(np.argmax(w.real))
v = np.abs(V[:, i].real); u = [F(round(x / v.max() * 10**8)) for x in v]
L = F(29477, 10000)
ok = all(sum(F(MR[a, b]) * u[b] for b in range(len(Rl))) >= L * u[a] for a in range(len(Rl)))
pos = all(x > 0 for x in u)
print(f"certificate on R: MR u >= {L} u exactly: {ok}; u > 0 on all of R: {pos}")
eps = min(F(c0[Rl[a]]) / u[a] for a in range(len(Rl)))
print("u[ca/B3] =", float(u[Rl.index(start)]), " eps =", float(eps))
print("certified per-vertex base:", float(L) ** (1/6))
