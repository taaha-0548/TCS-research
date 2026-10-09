"""Connectivity, cyclic edge-connectivity (small cuts), planarity and Ham-cycle count hints
for the first levels of the nested K=8 family."""
import networkx as nx
from general import from_chord
from nested_fast import next_level
CH = [4, 3, 6, 1, 0, 7, 2, 5]; X, R, PERM = 5, 2, (2, 0, 1)
K = from_chord(8, CH); Kc = list(range(8)); G, Gc = K, Kc; rl = R
for lev in range(13):
    g = nx.Graph([(v, w) for v in range(len(G)) for w in G[v]])
    print(f"level {lev}: n={len(G)} vertex-conn={nx.node_connectivity(g)} edge-conn={nx.edge_connectivity(g)} "
          f"planar={nx.check_planarity(g)[0]} bipartite={nx.is_bipartite(g)} girth3={any(len(c)==3 for c in nx.cycle_basis(g))}")
    G, Gc = next_level(K, Kc, X, G, [Gc], rl, PERM); rl = R if R < X else R - 1
