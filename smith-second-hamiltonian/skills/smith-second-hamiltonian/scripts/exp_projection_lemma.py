"""E13: total projection test for the Mirror Lemma (route R1).
Every G-state (Ham path from v0) is projected to an H-state:
  type A  (endpoint outside X, 2 cut edges):  contract the X-subpath to x
  type B1 (endpoint in X, 1 cut edge):          contract X to x (endpoint x)
  type B3 (endpoint in X, 3 cut edges, Y1 X1 Y2 X2): drop X2, contract X1 -> Y1 x Y2
Claim: every G-step maps to an H-step (edge of H's state graph) or to the same H-state.
Usage: python3 exp_projection_lemma.py [hosts_per_pole]"""
import random, sys, json
from collections import Counter
from lollipop import random_instance
from general import from_chord, substitute
from exp_3pole_transparency import poles, pole_from_cubic, random_cubic_ham

def segments(path, X):
    segs = []
    for v in path:
        inx = v in X
        if not segs or segs[-1][0] != inx: segs.append([inx, [v]])
        else: segs[-1][1].append(v)
    return segs

def proj(path, X, x):
    segs = segments(path, X)
    kinds = [k for k, _ in segs]
    if kinds == [False, True, False]: t = "A"
    elif kinds == [False, True]: t = "B1"
    elif kinds == [False, True, False, True]: t = "B3"
    else: raise AssertionError(kinds)
    if t == "B3": segs = segs[:3]
    out = []
    for inx, vs in segs: out += [x] if inx else vs
    return t, tuple(out)

def h_neighbors(H, S, v0):
    """Neighbours of state S in H's lollipop state graph (rotations at the endpoint)."""
    e = S[-1]; prev = S[-2]; pos = {v: i for i, v in enumerate(S)}; out = []
    for w in H[e]:
        if w == prev or w == v0: continue
        i = pos[w]; out.append(S[:i+1] + S[i+1:][::-1])
    return out

def g_states(G, c0):
    v0 = c0[0]; path = list(c0); n = len(path); pos = {v: i for i, v in enumerate(path)}
    forb = v0; out = [tuple(path)]
    while True:
        z, prev = path[-1], path[-2]
        w = [u for u in G[z] if u != prev and u != forb][0]
        if w == v0: return out
        i = pos[w]; path[i+1:] = path[i+1:][::-1]
        for j in range(i+1, n): pos[path[j]] = j
        forb = w; out.append(tuple(path))

hosts = int(sys.argv[1]) if len(sys.argv) > 1 else 150
rng = random.Random(13)
allpoles = dict(poles)
for k in range(12):   # extra random poles of sizes 12-16
    m = rng.choice([12, 14, 16]); allpoles[f"rand{m}-v#{k}"] = pole_from_cubic(random_cubic_ham(m, rng), 0)
summary = {}
for name, (padj, ports) in allpoles.items():
    if name.startswith("petersen"): continue
    steps = bad = 0; trans = Counter(); typ = Counter()
    for _ in range(hosts):
        n = rng.choice([10, 14, 20, 30]); chord = random_instance(n, rng)
        H = from_chord(n, chord); C = list(range(n)); x = rng.randrange(2, n - 1)
        if x == chord[0]: continue
        perm = list(ports); rng.shuffle(perm)
        G, cycles, X = substitute(H, C, x, padj, perm)
        for c0 in cycles[:4]:
            st = g_states(G, c0)
            pr = [proj(s, X, x) for s in st]
            for (t1, a), (t2, b) in zip(pr, pr[1:]):
                steps += 1; typ[t1 + ">" + t2] += 1
                if a == b: trans["stay"] += 1
                elif b in h_neighbors(H, a, 0): trans["H-step"] += 1
                else: bad += 1
    summary[name] = dict(steps=steps, violations=bad, outcomes=dict(trans), types=dict(typ))
    print(f"{name:14s} steps={steps:6d} violations={bad}  {dict(trans)}  {dict(typ)}")
json.dump(summary, open("e13_projection.json", "w"), indent=1)
