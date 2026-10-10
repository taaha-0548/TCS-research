"""Cycle 19b: correct metric.  T-down is violated only by a TRANSMIT visit that made a REFLECT call
("T after R" in cycle 15's census; ">=2 R-calls" with outcome R is not a violation).
Compare three local conditions on P' with observed T-down over 4 bases x 3 levels:
  strong  = RForcesR over ALL answer sequences (cap 14 calls; 'unknown' if truncated)  -> Lean tower_TDown
  fresh   = RForcesR over sequences realizable by a reversible child with fresh states (cycle 19)"""
import random, time, io, contextlib
from collections import Counter
with contextlib.redirect_stdout(io.StringIO()):
    import cycle18 as C18, cycle19 as C19
    from cycle15 import level, bases
    from selfsimilar2 import chord_adj, paths_of
import verify as V
from lollipop import random_instance
def strong(P1, ports1, x, perm):
    port_of = {u: "abc"[perm[j]] for j, u in enumerate(P1[x])}; trunc = False
    for key, Q in paths_of(P1, ports1).items():
        for Qo in key:
            for kd in ("B1", "B3"):
                leaves, t = C18.tree(P1, ports1, x, port_of, Qo, kd, cap=14); trunc |= t
                if any("REFLECT" in a and o == "TRANSMIT" for a, o in leaves): return "fails"
    return "unknown (truncated)" if trunc else "holds"
rng = random.Random(191); tab = Counter(); t0 = time.time()
while time.time() - t0 < 220:
    n = rng.choice([8, 10, 12]); K = chord_adj(n, random_instance(n, rng))
    try: P1, ports1, _ = V.pole(K, rng.randrange(n))
    except Exception: continue
    xs = [v for v in range(len(P1)) if P1[v] and v not in ports1]
    if not xs: continue
    x = rng.choice(xs); perm = list(range(3)); rng.shuffle(perm)
    try:
        st = strong(P1, ports1, x, perm); fr = "holds" if C19.check(P1, ports1, x, perm)[0] == 0 else "fails"
    except Exception: continue
    viol = False; seen = False
    for A in rng.sample(bases, 4):
        try:
            for lev in range(3):
                A, c = level(P1, ports1, x, perm, A)
                if not A["states"] or len(A["states"]) > 1500: break
                seen = True; viol |= c["T after R"] > 0
        except Exception: pass
    if seen: tab[(f"strong {st}", f"fresh {fr}", "T-down VIOLATED" if viol else "T-down holds")] += 1
for k, v in sorted(tab.items()): print(k, v)
