"""Cycle 10 (Hypothesis O', triangularity).  Write a tower state as components (level 1, ..., level d, base).
On a line, component j's new value is 'triangular' if it is a function of components 0..j of the old state.
O': on pass-through lines every component is triangular (information flows only downward).
Control: on reflecting lines (some states exit 'start'), count which components (and the exit side) fail
triangularity, i.e. where information flows upward."""
import io, contextlib, json, random, time
from collections import Counter, defaultdict
with contextlib.redirect_stdout(io.StringIO()):
    import cycle6 as C6
    from cycle7 import lines_from, levels
import verify as V
from tower import from_pole
from lollipop import random_instance
def freeze(x):
    return tuple(freeze(y) for y in x) if isinstance(x, (list, tuple)) else x
def comps(s, d):
    ks, rest = levels(s, d); return [freeze(k) for k in ks] + [freeze(rest)]
def is_fn(pairs):
    m = {}
    for a, b in pairs:
        if m.setdefault(a, b) != b: return False
    return True
rich = json.load(open("../phase3/p31_rich.json")); rng = random.Random(5)
for _ in range(200):
    G0 = [[(v - 1) % 8, (v + 1) % 8, c] for v, c in enumerate(random_instance(8, rng))]
    P, ports, _ = V.pole(G0, rng.randrange(8)); A0 = from_pole(P, ports)
    if len(A0["states"]) >= 5: break
d = 3
for gi in (21, 6, 15, 9, 0):
    g = rich[gi]; P1, ports1, _ = V.pole(g["K"], g["r"])
    A = C6.S2.build_tower_automaton(P1, ports1, g["x"], tuple(g["perm"]), A0, d)
    classes = defaultdict(list)
    for s in A["states"]: classes[A["pair"][s]].append(s)
    Cp, Cr = Counter(), Counter(); np_, nr = 0, 0; t0 = time.time()
    for p, S in classes.items():
        if len(S) < 2: continue
        for L in range(1, 6):
            for line in lines_from(p, L):
                res = [C6.run_line(A, line, s)[0] for s in S]
                if any(r is None for r in res): continue
                old = [comps(s, d) for s in S]; new = [comps(r[0], d) for r in res]
                bad = tuple(j for j in range(d + 1) if not is_fn((tuple(o[:j + 1]), n[j]) for o, n in zip(old, new)))
                if all(r[1] == "far" for r in res):
                    np_ += 1; Cp[bad] += 1
                else:
                    nr += 1
                    side_up = not is_fn((o[0], r[1]) for o, r in zip(old, res))   # exit side needs more than level 1
                    Cr[(bad, "side needs deep" if side_up else "side from level 1")] += 1
            if time.time() - t0 > 45: break
    print(f"P'#{gi} d={d}: pass-through {np_} lines, non-triangular components -> {dict(Cp)}", flush=True)
    print(f"        reflecting {nr} lines -> {dict(Cr.most_common(6))}", flush=True)
