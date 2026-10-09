"""T2 mechanism: attach-position uniformity and chord freshness along the lollipop walk."""
import random, sys, math

from lollipop import random_instance, neighbors

def walk(n, chord):
    path = list(range(n)); pos = {v: i for i, v in enumerate(path)}
    forb = 0; seen = set(); rec = []
    while True:
        z, prev = path[-1], path[-2]
        w = [x for x in neighbors(n, chord, z) if x != prev and x != forb][0]
        if w == 0: return rec
        i = pos[w]
        rec.append((i / n, frozenset((z, w)) in seen))
        seen.add(frozenset((z, w)))
        path[i+1:] = path[i+1:][::-1]
        for j in range(i+1, n): pos[path[j]] = j
        forb = w

rng = random.Random(7)
n, T = 1000, 300
bins = [0]*10; fresh = tot = 0; steps = []
early = [0]*10; ne = 0
for _ in range(T):
    r = walk(n, random_instance(n, rng)); steps.append(len(r))
    for k, (p, rep) in enumerate(r):
        bins[min(9, int(p*10))] += 1; tot += 1; fresh += (not rep)
        if k >= 20:   # skip burn-in
            early[min(9, int(p*10))] += 1; ne += 1
print("n", n, "mean steps/(n/2)", sum(steps)/T/(n/2))
print("attach-position decile freq (all):", [round(b/tot, 3) for b in bins])
print("attach-position decile freq (k>=20):", [round(b/ne, 3) for b in early])
print("fraction of steps using a never-before-used chord/edge:", round(fresh/tot, 4))
