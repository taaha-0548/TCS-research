"""Cycle 3 (addressability): at depth 3, a word g that fixes level 1, and changes level 3 for some
level-2 values but not others, possibly also changing level 2 (level 2 controls level 3).
Strict variant: level 2 also fixed (pure controlled action on level 3)."""
import sys, random, json, time
from collections import Counter, deque
sys.path.insert(0, "../phase3"); sys.path.insert(0, "../phase1"); sys.path.insert(0, ".."); sys.path.insert(0, "../../../../../paper")
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import selfsimilar2 as S2
from dynamics_group import involutions
import verify as V
from tower import from_pole
from lollipop import random_instance
def levels(s, d):
    out = []
    for _ in range(d): key, s = s; out.append(key)
    return out, s
def search(A, d, budget=400000, maxlen=14):
    n = len(A["states"]); gens, _, _ = involutions(A); G = [[g(i) for i in range(n)] for g in gens]
    lv = [levels(s, d) for s in A["states"]]
    start = tuple(range(n)); seen = {start: 0}; q = deque([start]); found = {}
    while q and len(seen) < budget:
        p = q.popleft(); L = seen[p]
        if L >= maxlen: continue
        for g in G:
            r = tuple(g[x] for x in p)
            if r in seen: continue
            seen[r] = L + 1; q.append(r)
            if not all(lv[r[i]][0][0] == lv[i][0][0] for i in range(n)): continue        # level 1 fixed
            fix2 = all(lv[r[i]][0][1] == lv[i][0][1] for i in range(n))
            ch = Counter(); tot = Counter()
            for i in range(n):
                q2 = lv[i][0][1]; tot[q2] += 1
                if (lv[r[i]][0][2:], lv[r[i]][1]) != (lv[i][0][2:], lv[i][1]): ch[q2] += 1
            if any(ch[a] > 0 for a in tot) and any(ch[a] == 0 for a in tot):
                found.setdefault("level2 controls level3" + (" (level2 fixed)" if fix2 else ""), L + 1)
                if fix2: return found, len(seen)
    return found, len(seen)
rich = json.load(open("../phase3/p31_rich.json")); rng = random.Random(5)
for _ in range(200):
    G0 = [[(v - 1) % 8, (v + 1) % 8, c] for v, c in enumerate(random_instance(8, rng))]
    P, ports, _ = V.pole(G0, rng.randrange(8)); A0 = from_pole(P, ports)
    if len(A0["states"]) >= 5: break
for gi in (21, 9, 0, 6):
    g = rich[gi]; P1, ports1, _ = V.pole(g["K"], g["r"]); t0 = time.time()
    A = S2.build_tower_automaton(P1, ports1, g["x"], tuple(g["perm"]), A0, 3)
    found, explored = search(A, 3)
    print(f"P'#{gi} depth 3 ({len(A['states'])} states): {found or 'none'} (explored {explored}, {time.time()-t0:.0f}s)", flush=True)
