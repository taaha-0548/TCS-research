"""Cycle 9 (Hypothesis O, pass-through rigidity).  For every pass-through line (all states of a pair class
exit far) up to length 6, test decoupling:
  (i)  the change of deeper levels is independent of level 1   (per deep configuration)
  (ii) the new level-1 value is independent of deeper levels   (per level-1 value)
Count lines satisfying both, each, or neither."""
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
rich = json.load(open("../phase3/p31_rich.json")); rng = random.Random(5)
for _ in range(200):
    G0 = [[(v - 1) % 8, (v + 1) % 8, c] for v, c in enumerate(random_instance(8, rng))]
    P, ports, _ = V.pole(G0, rng.randrange(8)); A0 = from_pole(P, ports)
    if len(A0["states"]) >= 5: break
for gi in (21, 9, 0, 6, 15):
    g = rich[gi]; P1, ports1, _ = V.pole(g["K"], g["r"]); d = 2
    A = C6.S2.build_tower_automaton(P1, ports1, g["x"], tuple(g["perm"]), A0, d)
    classes = defaultdict(list)
    for s in A["states"]: classes[A["pair"][s]].append(s)
    C = Counter(); t0 = time.time()
    for p, S in classes.items():
        if len({levels(s, d)[0][0] for s in S}) < 2: continue
        for L in range(1, 7):
            for line in lines_from(p, L):
                res = [C6.run_line(A, line, s)[0] for s in S]
                if any(r is None for r in res) or not all(r[1] == "far" for r in res): continue
                lv0 = [levels(s, d) for s in S]; lv1 = [levels(r[0], d) for r in res]
                deep_change = defaultdict(set); top_map = defaultdict(set)
                for a, b in zip(lv0, lv1):
                    deep0 = freeze((a[0][1:], a[1])); deep1 = freeze((b[0][1:], b[1]))
                    deep_change[deep0].add((deep1,))              # (i): same deep input -> same deep output for all level-1 values?
                    top_map[freeze(a[0][0])].add(freeze(b[0][0]))                 # (ii): same level-1 input -> same level-1 output for all deep values?
                i_ok = all(len(v) == 1 for v in deep_change.values())
                ii_ok = all(len(v) == 1 for v in top_map.values())
                C[("decoupled (i)" if i_ok else "deep depends on level 1", "decoupled (ii)" if ii_ok else "level 1 depends on deep")] += 1
            if time.time() - t0 > 40: break
    print(f"P'#{gi} depth 2: pass-through lines classified: {dict(C)}", flush=True)
