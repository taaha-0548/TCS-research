"""Cycle 14.  Which automaton property of X makes T-down hold in P'[x <- X]?
Candidate D (double reflection): some state s' reached by a reflection reflects again on some
pair-consistent entry.  Hypothesis: T-down can fail only if D holds.  Check D on the random inner poles of
cycle 13 (violators had h = [1,1,3] / [1,3,3]) and on the depth-1..3 tower automata."""
import io, contextlib, json, random, sys
from collections import Counter
with contextlib.redirect_stdout(io.StringIO()):
    sys.argv = ["x"]
    import cycle6 as C6
    from cycle11 import build
    from selfsimilar2 import chord_adj
import verify as V
from tower import from_pole
from lollipop import random_instance
def D(A):
    hits = 0
    for (s, pr, kd), (o, s2, _) in A["table"].items():
        if o != "REFLECT": continue
        for (t, pr2, kd2), (o2, _, _) in A["table"].items():
            if t == s2 and o2 == "REFLECT": hits += 1; break
    return hits
def h(A): return sorted(Counter(A["pair"][s] for s in A["states"]).values())
rng = random.Random(13); seen = Counter()
inners = []
while len(inners) < 40:
    n = rng.choice([6, 8, 10]); K = chord_adj(n, random_instance(n, rng))
    try:
        P, ports, _ = V.pole(K, rng.randrange(n)); A = from_pole(P, ports)
    except Exception: continue
    if len(A["states"]) >= 2: inners.append(A)
for A in inners:
    seen[(str(h(A)), "D" if D(A) else "no D")] += 1
print("random inner poles (h, D):", dict(seen))
rich = json.load(open("../phase3/p31_rich.json")); rng = random.Random(5)
for _ in range(200):
    G0 = [[(v - 1) % 8, (v + 1) % 8, c] for v, c in enumerate(random_instance(8, rng))]
    P, ports, _ = V.pole(G0, rng.randrange(8)); A0 = from_pole(P, ports)
    if len(A0["states"]) >= 5: break
print("A0 base:", h(A0), "D-hits", D(A0))
for gi in (21, 0, 6, 15, 9):
    g = rich[gi]; P1, ports1, _ = V.pole(g["K"], g["r"])
    out = []
    for d in (1, 2, 3):
        A, _ = build(P1, ports1, g["x"], tuple(g["perm"]), A0, d)
        out.append((len(A["states"]), D(A)))
    print(f"tower P'#{gi}: (states, D-hits) by depth {out}", flush=True)

# --- Ret property: forward transmit t -e1-> s, reflection s -e2-> s', then backward type bwd(e1) at s' must transmit
from cycle6 import bwd
def ret_violations(A):
    T = A["table"]; byres = {}
    for (t, pr, kd), (o, s, _) in T.items():
        if o == "TRANSMIT": byres.setdefault(s, []).append((pr, kd))
    bad = tot = 0
    for (s, pr2, kd2), (o, s2, _) in T.items():
        if o != "REFLECT": continue
        for (pr1, kd1) in byres.get(s, []):
            eb = bwd(pr1, kd1); key = (s2, eb[0], eb[1])
            if key in T:
                tot += 1; bad += T[key][0] == "REFLECT"
    return bad, tot
print("\nRet property (violations/applicable):")
seenR = Counter()
for A in inners: seenR[(str(h(A)), ret_violations(A)[0] > 0)] += 1
print("random inner poles (h, Ret fails):", dict(seenR))
for gi in (21, 0, 6, 15, 9):
    g = rich[gi]; P1, ports1, _ = V.pole(g["K"], g["r"])
    print(f"tower P'#{gi}:", [ret_violations(build(P1, ports1, g["x"], tuple(g["perm"]), A0, d)[0]) for d in (1, 2, 3)], flush=True)
