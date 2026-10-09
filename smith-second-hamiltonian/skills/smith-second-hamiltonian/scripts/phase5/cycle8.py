"""Cycle 7 (G1'): realisable pair-respecting controlled gates.  For a tower (depth d) and a port-pair class
p with >= 2 distinct level-1 values, enumerate lines of sites (types chained consistently from p) up to
length L; run the exact dynamics from every state of class p; a GATE fixes level 1 and changes deeper
levels for some level-1 values but not others.  Prefer pass-through gates (all states exit far)."""
import io, contextlib, json, random, itertools, time
from collections import Counter
with contextlib.redirect_stdout(io.StringIO()):
    import cycle6 as C6
import verify as V
from tower import from_pole
from lollipop import random_instance
third = C6.third
def after(pr, kd): return frozenset((pr[1], third(pr)) if kd == "B1" else (pr[0], third(pr)))
def lines_from(p, L):
    """All site-type sequences of length L whose transmit-chain of pairs is consistent, starting at class p."""
    def rec(pair, k):
        if k == 0: yield []; return
        for a, b in (tuple(sorted(pair)), tuple(sorted(pair))[::-1]):
            for kd in ("B1", "B3"):
                for rest in rec(after((a, b), kd), k - 1): yield [C6.TYPES.index(((a, b), kd))] + rest
    yield from rec(p, L)
def levels(s, d):
    out = []
    for _ in range(d): key, s = s; out.append(key)
    return out, s
rich = json.load(open("../phase3/p31_rich.json")); rng = random.Random(5)
for _ in range(200):
    G0 = [[(v - 1) % 8, (v + 1) % 8, c] for v, c in enumerate(random_instance(8, rng))]
    P, ports, _ = V.pole(G0, rng.randrange(8)); A0 = from_pole(P, ports)
    if len(A0["states"]) >= 5: break
for gi in (21, 9, 0, 6, 15):
    g = rich[gi]; P1, ports1, _ = V.pole(g["K"], g["r"])
    for d in (2, 3):
        A = C6.S2.build_tower_automaton(P1, ports1, g["x"], tuple(g["perm"]), A0, d)
        classes = {}
        for s in A["states"]: classes.setdefault(A["pair"][s], []).append(s)
        best = None; t0 = time.time()
        for p, S in classes.items():
            if len({levels(s, d)[0][0] for s in S}) < 2: continue
            for L in range(1, 8):
                for line in lines_from(p, L):
                    res = [C6.run_line(A, line, s)[0] for s in S]
                    if any(r is None for r in res): continue
                    lv0 = [levels(s, d) for s in S]; lv1 = [levels(r[0], d) for r in res]
                    if any(a[0][0] != b[0][0] for a, b in zip(lv0, lv1)): continue
                    ch = Counter(); tot = Counter()
                    for a, b in zip(lv0, lv1):
                        tot[a[0][0]] += 1
                        if (a[0][1:], a[1]) != (b[0][1:], b[1]): ch[a[0][0]] += 1
                    if any(ch[q] for q in tot) and any(ch[q] == 0 for q in tot) and all(r[1] == "far" for r in res):
                        passthru = all(r[1] == "far" for r in res)
                        cand = (L, not passthru)
                        if best is None or cand < best[0]: best = (cand, [C6.TYPES[w] for w in line], passthru)
                        break
                if best and best[0][0] <= L: break
                if time.time() - t0 > 40: break
        print(f"P'#{gi} depth {d} ({len(A['states'])} states): " + (f"realisable controlled gate, length {best[0][0]}, pass-through {best[2]}: {best[1]}" if best else "NO pass-through controlled gate up to length 7"), flush=True)
