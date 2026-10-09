"""Realisability of nested cavity machines in hosts: in a host's line, take vertices with exactly two
sites; their site intervals [first, second]; find the longest chain of properly nested intervals
among vertices pairwise at distance >= 3 and away from v0 (greedy longest-chain DP on nesting)."""
import sys, random
from collections import defaultdict, deque
sys.path.insert(0, "../phase2"); sys.path.insert(0, ".."); sys.path.insert(0, "../../../../../paper")
from lollipop import random_instance
from linemirror import host_line
def chord_adj(n, ch): return [[(v - 1) % n, (v + 1) % n, ch[v]] for v in range(n)]
def dist_all(adj):
    D = []
    for a in range(len(adj)):
        d = {a: 0}; q = deque([a])
        while q:
            u = q.popleft()
            for w in adj[u]:
                if w not in d: d[w] = d[u] + 1; q.append(w)
        D.append(d)
    return D

def chain(adj, cyc):
    line, moves = host_line(adj, cyc); sites = defaultdict(list)
    for i, (z, w, s) in enumerate(moves):
        sites[s].append(i); sites[w].append(i)
    v0 = cyc[0]; D = dist_all(adj)
    iv = [(v, l[0], l[1]) for v, l in sites.items() if len(l) == 2 and v != v0 and v not in adj[v0]]
    iv.sort(key=lambda t: t[1] - t[2])          # outer (wide) intervals first
    best = []                                    # DP: longest nested chain with distance constraint (greedy beam)
    chains = [[]]
    for v, a, b in sorted(iv, key=lambda t: t[2] - t[1], reverse=True):
        new = []
        for ch in chains:
            if not ch or (ch[-1][1] < a and b < ch[-1][2] and all(D[v][u] >= 3 for u, _, _ in ch)):
                new.append(ch + [(v, a, b)])
        chains = sorted(chains + new, key=len, reverse=True)[:200]
    return len(line) - 1, max(len(c) for c in chains)

rng = random.Random(3)
for n in (40, 80, 160, 320, 640):
    res = [chain(chord_adj(n, random_instance(n, rng)), list(range(n))) for _ in range(12)]
    print(f"n={n}: mean line {sum(r[0] for r in res)/len(res):.0f}, longest nested chain: mean {sum(r[1] for r in res)/len(res):.1f}, max {max(r[1] for r in res)}", flush=True)
