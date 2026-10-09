"""Step 5: exact rational growth certificate.
Find u >= 0 (rational) with (M u)_i >= lam * u_i for all i, lam rational < rho(M).
Then c_k >= c_0 + M c_{k-1} >= ... gives c_k >= eps * lam^k * u with eps = min_{u_i>0} c_0[i]/u_i.
Lower bound for the walk: steps(G_k; start) >= N(start) . c_{k-1} >= eps * lam^(k-1) * (N . u)."""
import json
from fractions import Fraction as F
import numpy as np
d = json.load(open("e20_M.json")); M = d["M"]; c0 = d["b"]; keys = d["keys"]; n = len(M)
A = np.array(M, float); w, V = np.linalg.eig(A)
i = int(np.argmax(w.real)); rho = w[i].real; v = np.abs(V[:, i].real)
print("rho =", rho)
# rational u: round the Perron vector (scaled), zero tiny entries
u = [F(round(x / v.max() * 10**6)) for x in v]
for lam in [F(29477, 10000), F(2947, 1000), F(2945, 1000), F(294, 100)]:
    Mu = [sum(F(M[r][j]) * u[j] for j in range(n)) for r in range(n)]
    ok = all(Mu[r] >= lam * u[r] for r in range(n))
    print(f"lam = {lam} ({float(lam):.4f}): M u >= lam u componentwise: {ok};  support of u: {sum(1 for x in u if x > 0)}/{n}")
    if ok: best = lam; break
eps = min(F(c0[j]) / u[j] for j in range(n) if u[j] > 0)
print("eps = min c0/u =", float(eps))
print("per-vertex base certified: lam^(1/6) =", float(best) ** (1/6))
json.dump(dict(u=[str(x) for x in u], lam=str(best), eps=str(eps)), open("certificate.json", "w"))
