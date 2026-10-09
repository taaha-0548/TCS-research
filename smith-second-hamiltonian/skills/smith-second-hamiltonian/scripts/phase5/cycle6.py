"""Cycle 6: realisability of a gate word as an actual line of sites.
Find the shortest controlled-gate word w = e_1..e_L (BFS with parent pointers) for a tower; lay out a
line of L sites of the tower gadget with forward types e_i (backward types by the site rule); run the
exact single-gadget line-mirror dynamics from each state compatible with site 1's left pair; compare the
final state with the group action of the word (sigma_{e_L} ... sigma_{e_1})."""
import sys, json, random, itertools
from collections import Counter, deque
sys.path.insert(0, "../phase3"); sys.path.insert(0, "../phase1"); sys.path.insert(0, ".."); sys.path.insert(0, "../../../../../paper")
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import selfsimilar2 as S2
import verify as V
from tower import from_pole
from lollipop import random_instance
def third(p): return next(c for c in "abc" if c not in p)
def bwd(pr, kd): return ((third(pr), pr[1]), kd) if kd == "B1" else ((pr[0], third(pr)), kd)
TYPES = [(pr, kd) for pr in itertools.permutations("abc", 2) for kd in ("B1", "B3")]

def sigma_table(A):
    out = []
    for (pr, kd) in TYPES:
        eb = bwd(pr, kd); m = {}
        for s in A["states"]:
            if A["pair"][s] == frozenset(pr): m[s] = A["table"][(s, pr, kd)][1]
            elif A["pair"][s] == frozenset(eb[0]): m[s] = A["table"][(s, eb[0], eb[1])][1]
            else: m[s] = s
        out.append(m)
    return out

def levels(s, d):
    out = []
    for _ in range(d): key, s = s; out.append(key)
    return out, s

def shortest_gate(A, d, budget=200000):
    sig = sigma_table(A); S = A["states"]; idx = {s: i for i, s in enumerate(S)}; n = len(S)
    G = [[idx[m[s]] for s in S] for m in sig]; lv = [levels(s, d) for s in S]
    start = tuple(range(n)); par = {start: None}; q = deque([start])
    while q and len(par) < budget:
        p = q.popleft()
        for gi, g in enumerate(G):
            r = tuple(g[x] for x in p)
            if r in par: continue
            par[r] = (p, gi); q.append(r)
            if not all(lv[r[i]][0][0] == lv[i][0][0] for i in range(n)): continue
            ch = Counter(); tot = Counter()
            for i in range(n):
                tot[lv[i][0][0]] += 1
                if (lv[r[i]][0][1:], lv[r[i]][1]) != (lv[i][0][1:], lv[i][1]): ch[lv[i][0][0]] += 1
            if any(ch[a] for a in tot) and any(ch[a] == 0 for a in tot):
                word = []; x = r
                while par[x] is not None: x, gi2 = par[x]; word.append(gi2)
                return list(reversed(word)), r
    return None, None

def run_line(A, word, s0):
    st = s0; i, d, path = 0, 1, []
    while 0 <= i < len(word):
        pr, kd = TYPES[word[i]]
        typ = (pr, kd) if d > 0 else bwd(pr, kd)
        key = (st, typ[0], typ[1])
        if key not in A["table"]: return None, path
        o, st, _ = A["table"][key]; path.append((i, d, o[0]))
        if o == "REFLECT": d = -d
        i += d
    return (st, "far" if i >= len(word) else "start"), path

rich = json.load(open("../phase3/p31_rich.json")); rng = random.Random(5)
for _ in range(200):
    G0 = [[(v - 1) % 8, (v + 1) % 8, c] for v, c in enumerate(random_instance(8, rng))]
    P, ports, _ = V.pole(G0, rng.randrange(8)); A0 = from_pole(P, ports)
    if len(A0["states"]) >= 5: break
for gi in (21, 9):
    g = rich[gi]; P1, ports1, _ = V.pole(g["K"], g["r"])
    A = S2.build_tower_automaton(P1, ports1, g["x"], tuple(g["perm"]), A0, 2)
    word, r = shortest_gate(A, 2)
    S = A["states"]; idx = {s: i for i, s in enumerate(S)}
    print(f"P'#{gi}: gate word length {len(word)}: {[TYPES[w] for w in word]}")
    first = TYPES[word[0]][0]; C = Counter()
    for s in S:
        if A["pair"][s] != frozenset(first): continue
        res, path = run_line(A, word, s)
        if res is None: C["pair-inconsistent line"] += 1; continue
        st, end = res
        target = S[r[idx[s]]]
        refl = sum(1 for _, _, o in path if o == "R")
        C[("exit " + end, "matches word action" if st == target else "differs", "reflections=" + str(min(refl, 3)))] += 1
    for k, v in sorted(C.items(), key=str): print("   ", k, v)
