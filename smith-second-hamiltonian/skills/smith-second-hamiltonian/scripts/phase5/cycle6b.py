"""Cycle 6b: is the realised action, restricted to pair-consistent states, still a CONTROLLED gate?"""
import io, contextlib, json, random
from collections import Counter
with contextlib.redirect_stdout(io.StringIO()):
    import cycle6 as C6
import verify as V
from tower import from_pole
from lollipop import random_instance
rich = json.load(open("../phase3/p31_rich.json")); rng = random.Random(5)
for _ in range(200):
    G0 = [[(v - 1) % 8, (v + 1) % 8, c] for v, c in enumerate(random_instance(8, rng))]
    P, ports, _ = V.pole(G0, rng.randrange(8)); A0 = from_pole(P, ports)
    if len(A0["states"]) >= 5: break
for gi in (21, 9):
    g = rich[gi]; P1, ports1, _ = V.pole(g["K"], g["r"])
    A = C6.S2.build_tower_automaton(P1, ports1, g["x"], tuple(g["perm"]), A0, 2)
    word, r = C6.shortest_gate(A, 2); first = C6.TYPES[word[0]][0]
    rows = []
    for s in A["states"]:
        if A["pair"][s] != frozenset(first): continue
        res, path = C6.run_line(A, word, s)
        if res is None: continue
        (q1, rest), (q1b, restb) = s, res[0]
        rows.append((q1 == q1b, q1, rest != restb))
    by_q1 = {}
    for fixed, q1, changed in rows: by_q1.setdefault(q1, []).append((fixed, changed))
    ok_fixed = all(f for f, _, _ in rows)
    ctrl = any(any(c for _, c in v) for v in by_q1.values()) and any(not any(c for _, c in v) for v in by_q1.values())
    print(f"P'#{gi}: realised on {len(rows)} consistent states; level 1 fixed: {ok_fixed}; distinct level-1 values {len(by_q1)}; controlled (changes level 2 for some level-1 values, not others): {ctrl}")
