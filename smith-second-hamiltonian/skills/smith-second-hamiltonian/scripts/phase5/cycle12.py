"""Cycle 1 (D1): are the growing transparent-tower groups abelian?  (generator commutators)
Cycle 2 (G1): in REFLECTING towers with explicit level structure (states = (q1, (q2, (q3, ...)))),
BFS over words in the 12 site involutions for CONTROLLED GATES:
  depth 2: g fixes q1 and changes the rest for some q1-values but not others (q1 controls level 2);
  depth 3: g fixes q1 and q2 and changes level 3 depending on q1 (long-range control 1 -> 3)."""
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

rng = random.Random(11); C1 = Counter()
for (P1, ports1, A1) in S2.lib[:80]:
    inner = [v for v in range(len(P1)) if v not in ports1]
    if not inner: continue
    A0 = rng.choice(S2.lib)[2]
    try: A = S2.build_tower_automaton(P1, ports1, inner[0], (0, 1, 2), A0, 3)
    except Exception: continue
    gens, n, bad = involutions(A)
    C1["abelian" if all(g * h == h * g for g in gens for h in gens) else "NON-abelian"] += 1
print("cycle 1 (transparent towers, depth 3):", dict(C1), flush=True)

def levels(s, d):
    out = []
    for _ in range(d): key, s = s; out.append(key)
    return out, s
def gate_search(A, d, budget=150000, maxlen=10):
    states = A["states"]; n = len(states)
    gens, _, _ = involutions(A); G = [[g(i) for i in range(n)] for g in gens]
    lv = [levels(s, d) for s in states]
    start = tuple(range(n)); seen = {start: 0}; q = deque([start]); found = {}
    while q and len(seen) < budget:
        p = q.popleft(); L = seen[p]
        if L >= maxlen: continue
        for g in G:
            r = tuple(g[x] for x in p)
            if r in seen: continue
            seen[r] = L + 1; q.append(r)
            if not all(lv[r[i]][0][0] == lv[i][0][0] for i in range(n)): continue
            if d == 3 and not all(lv[r[i]][0][1] == lv[i][0][1] for i in range(n)): continue
            changed = Counter(); total = Counter()
            for i in range(n):
                q1 = lv[i][0][0]; total[q1] += 1
                deep = (lv[r[i]][0][d-1:], lv[r[i]][1]) if d == 3 else (lv[r[i]][0][1:], lv[r[i]][1])
                orig = (lv[i][0][d-1:], lv[i][1]) if d == 3 else (lv[i][0][1:], lv[i][1])
                if deep != orig: changed[q1] += 1
            if any(changed[a] > 0 for a in total) and any(changed[a] == 0 for a in total):
                found.setdefault("controlled gate", L + 1)
                return found, len(seen)
    return found, len(seen)

rich = json.load(open("../phase3/p31_rich.json")); rng = random.Random(5)
for _ in range(200):
    G0 = [[(v - 1) % 8, (v + 1) % 8, c] for v, c in enumerate(random_instance(8, rng))]
    P, ports, _ = V.pole(G0, rng.randrange(8)); A0 = from_pole(P, ports)
    if len(A0["states"]) >= 5: break
for gi in (0, 21, 6, 9):
    g = rich[gi]; P1, ports1, _ = V.pole(g["K"], g["r"])
    for d in (2, 3):
        t0 = time.time()
        try: A = S2.build_tower_automaton(P1, ports1, g["x"], tuple(g["perm"]), A0, d)
        except Exception as e: print(f"P'#{gi} depth {d}: build failed {type(e).__name__}"); continue
        found, explored = gate_search(A, d)
        print(f"P'#{gi} depth {d} ({len(A['states'])} states): {found or 'no controlled gate within budget'} (explored {explored}, {time.time()-t0:.0f}s)", flush=True)
