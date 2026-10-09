"""E21 re-run with exact isomorphism dedup (the original deduplicated by adjacency spectrum, which can
merge non-isomorphic cospectral graphs).  Same analysis as search_base.py.
Usage: python3 search_iso.py n"""
import sys, json, time
import numpy as np, networkx as nx
from search_base import analyse, all_instances, chord_adj
n = int(sys.argv[1]); t0 = time.time(); best = {}; buckets = {}; graphs = reps = good = 0; cospec = 0
for ch in all_instances(n):
    adj = chord_adj(n, ch); graphs += 1
    g = nx.Graph([(v, w) for v in range(n) for w in adj[v]])
    if g.number_of_edges() != 3 * n // 2: continue          # skip multigraph chord choices, as in search_base
    A = nx.to_numpy_array(g, nodelist=range(n))
    key = tuple(np.round(np.sort(np.linalg.eigvalsh(A)), 6))
    B = buckets.setdefault(key, [])
    if any(nx.is_isomorphic(g, h) for h in B): continue
    if B: cospec += 1
    B.append(g); reps += 1
    if analyse(adj, n, best, "planar" if nx.check_planarity(g)[0] else "nonplanar", None): good += 1
print(f"n={n}: matchings {graphs}, iso classes {reps} (of which {cospec} cospectral with an earlier class), "
      f"spectra {len(buckets)}, exactly 3 Ham cycles {good}, {time.time()-t0:.0f}s")
for q in best.get("top", [])[:5]:
    print(f"  base {q['base']:.6f}  rho {q['rho']:.5f}  {q['tag']:9s} x={q['x']} r={q['r']} perm={q['perm']}")
