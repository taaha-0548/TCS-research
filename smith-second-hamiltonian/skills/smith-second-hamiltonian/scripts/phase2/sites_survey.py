"""P2.2 (exploratory): how many sites does a host's line give each vertex?
Random hosts and structured families (prism, Moebius ladder, our nested family G_k)."""
import sys, random
from collections import Counter
sys.path.insert(0, ".."); sys.path.insert(0, "../../../../../paper")
from lollipop import random_instance
from linemirror import host_line
import verify as V

def sites_per_vertex(adj, cyc):
    line, moves = host_line(adj, cyc); c = Counter()
    for (z, w, s) in moves:
        c[s] += 1   # B1-type passage through s (endpoint becomes s)
        c[w] += 1   # B3-type passage through w (attachment)
    return len(line) - 1, c

def chord_adj(n, ch): return [[(v - 1) % n, (v + 1) % n, ch[v]] for v in range(n)]
rng = random.Random(1)
print("random hosts (cycle + random chords):")
for n in (50, 200, 800):
    mx = []; L = []
    for _ in range(30):
        adj = chord_adj(n, random_instance(n, rng)); l, c = sites_per_vertex(adj, list(range(n)))
        L.append(l); mx.append(max(c.values()) if c else 0)
    print(f"  n={n}: mean line length {sum(L)/len(L):.0f}, mean max sites/vertex {sum(mx)/len(mx):.1f}")
def prism(m):   # outer cycle 0..m-1, inner m..2m-1, spokes; Ham cycle via the standard zigzag
    adj = [[] for _ in range(2*m)]
    for i in range(m):
        for a, b in ((i, (i+1) % m), (m+i, m+(i+1) % m), (i, m+i)): adj[a].append(b); adj[b].append(a)
    cyc = list(range(m-1, -1, -1)) ; cyc = [0] + [m] + [m + i for i in range(m-1, 0, -1)] + list(range(m-1, 0, -1))
    return adj, cyc
for m in (6, 10, 20, 40):
    adj, cyc = prism(m)
    if all(cyc[(t+1) % len(cyc)] in adj[cyc[t]] for t in range(len(cyc))) and len(set(cyc)) == 2*m:
        l, c = sites_per_vertex(adj, cyc); print(f"  prism m={m}: line length {l}, max sites/vertex {max(c.values())}, total sites {sum(c.values())}")
V.KCYC = []
for E in V.ham_cycles(V.K):
    c = [0]; prev = None
    while len(c) < 8:
        nxt = next(w for w in V.K[c[-1]] if frozenset((c[-1], w)) in E and w != prev); prev = c[-1]; c.append(nxt)
    if c[1] != 1 and c[-1] == 1: c = [0] + c[1:][::-1]
    V.KCYC.append(c)
for k in (2, 4, 6):
    adj, Ck, _ = V.build(k); lab = {v: i for i, v in enumerate(adj)}; A = [[lab[w] for w in adj[v]] for v in adj]
    l, c = sites_per_vertex(A, [lab[v] for v in Ck]); top = c.most_common(3)
    print(f"  nested G_{k} (n={len(A)}): line length {l}, top sites/vertex {[t[1] for t in top]}")
