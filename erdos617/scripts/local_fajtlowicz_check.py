"""Sanity check (not a proof) of the local Fajtlowicz / BRRS bound
    alpha(G) >= sum_u 2 / (d(u) + omega(u) + 1),   omega(u) = largest clique containing u,
on every graph in the networkx atlas (all graphs with <= 7 vertices).  Also reports the tight cases."""
import networkx as nx
from fractions import Fraction
from networkx.generators.atlas import graph_atlas_g

def alpha(G):
    return max((len(c) for c in nx.find_cliques(nx.complement(G))), default=0)

worst = None; tight = 0; n_graphs = 0
for G in graph_atlas_g()[1:]:
    n_graphs += 1
    cl = list(nx.find_cliques(G))
    om = {u: max(len(c) for c in cl if u in c) for u in G}
    bound = sum(Fraction(2, G.degree(u) + om[u] + 1) for u in G)
    a = alpha(G)
    if a < bound:
        print("COUNTEREXAMPLE", G.edges()); break
    if a == bound: tight += 1
    gap = a - bound
    if worst is None or gap < worst[0]: worst = (gap, G.number_of_nodes(), sorted(G.edges()))
print(f"checked {n_graphs} graphs (all graphs on <= 7 vertices); no counterexample; tight in {tight} graphs")
