"""Independent brute-force check of the r=7 single-colour example:
G = complement(C5[3]) + 5 disjoint K_7 on 50 vertices.
Claims: alpha(G) = 7, every 8-set spans <= C(7,2)+1 = 22 edges, and e(G) = 165 < M_7 = 175."""
import itertools
from math import comb
import networkx as nx

r = 7
G = nx.Graph()
G.add_nodes_from(range(50))
part = {v: v // 3 for v in range(15)}                       # C5 blow-up parts 0..4, three vertices each
for u, v in itertools.combinations(range(15), 2):
    if (part[u] - part[v]) % 5 not in (1, 4):
        G.add_edge(u, v)                                     # B = complement of the blow-up
for c in range(5):
    G.add_edges_from(itertools.combinations(range(15 + 7 * c, 22 + 7 * c), 2))

print("n =", G.number_of_nodes(), " e(G) =", G.number_of_edges(), " M_7 =", comb(50, 2) / 7)
alpha = max(len(c) for c in nx.find_cliques(nx.complement(G)))
print("alpha(G) =", alpha)

# An 8-set S meets B in s vertices; the rest lies in the K_7 blocks, where edges are maximised by
# putting all of it in one block (at most 7 there).  So max e(S) = max_s [maxB(s) + C(8-s,2)] for s>=1,
# and C(7,2) for s=0 (7 in one block, 1 in another).
best = comb(7, 2)
for s in range(1, 9):
    eB = max(G.subgraph(S).number_of_edges() for S in itertools.combinations(range(15), s))
    best = max(best, eB + comb(8 - s, 2))
cap = comb(r, 2) + 1
print("max edges in an 8-set =", best, " cap =", cap, "OK" if best <= cap else "VIOLATED")
