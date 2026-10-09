import itertools, time, sys
import networkx as nx
from core import *

def count_ham_cycles(adj, n):
    # cycles through vertex 0, counted with orientation fixed by forbidding reversal: count directed, divide by 2
    cnt = 0
    seen = [False]*n
    seen[0] = True
    def rec(u, depth):
        nonlocal cnt
        if depth == n:
            if 0 in adj[u]: cnt += 1
            return
        for w in adj[u]:
            if not seen[w]:
                seen[w] = True; rec(w, depth+1); seen[w] = False
    rec(0, 1)
    assert cnt % 2 == 0
    return cnt // 2

print('K ham cycles:', count_ham_cycles([sorted(KADJ[i]) for i in range(8)], 8))
# d: simplicity of P0
for p,q in itertools.combinations([1,3,6],2):
    hs = ham_paths(KADJ, P0V, p, q)
    print(f'P0 ham paths {PNAME[p]}{PNAME[q]} ({p}-{q}):', len(hs), hs)

# all cubic graphs on 8 vertices
graphs = []
def gen(edges, deg, lastu, lastv):
    for u in range(8):
        if deg[u] < 3: break
    else:
        graphs.append(list(edges)); return
    lo = lastv+1 if u == lastu else u+1
    for v in range(lo, 8):
        if deg[v] < 3:
            edges.append((u,v)); deg[u]+=1; deg[v]+=1
            gen(edges, deg, u, v)
            edges.pop(); deg[u]-=1; deg[v]-=1
gen([], [0]*8, -1, -1)
print('labelled cubic graphs on 8 vertices:', len(graphs))
reps = []
for E in graphs:
    g = nx.Graph(E)
    if not any(nx.is_isomorphic(g, h) for h in reps): reps.append(g)
print('cubic graphs on 8 vertices up to iso:', len(reps), 'connected:', sum(nx.is_connected(g) for g in reps))
Kg = nx.Graph(KEDGES)
for g in reps:
    if not nx.is_connected(g): continue
    adj = [sorted(g[i]) for i in range(8)]
    print('  hc=', count_ham_cycles(adj, 8), 'iso to K:', nx.is_isomorphic(g, Kg))

kmax_hc = int(sys.argv[1]); kmax_struct = int(sys.argv[2])
for k in range(0, kmax_struct+1):
    G = Gk(k); g = nx.Graph(G.edges)
    simple = len(G.edges) == len(set(frozenset(e) for e in G.edges)) and all(u != v for u,v in G.edges)
    cubic = all(len(set(G.adj[v])) == 3 for v in range(G.n)) and len(g) == G.n
    ec = nx.edge_connectivity(g); vc = nx.node_connectivity(g)
    pl, _ = nx.check_planarity(g)
    line = f'k={k} n={G.n} simple={simple} cubic={cubic} edge_conn={ec} vertex_conn={vc} planar={pl}'
    if k <= kmax_hc:
        t=time.time(); line += f' hamcycles={count_ham_cycles(G.adj, G.n)} ({time.time()-t:.1f}s)'
    # also P_k simplicity for small k
    if k <= 3:
        Pk = [i for i,l in enumerate(G.labels) if l != (0,2)]
        padj = {i:set(G.adj[i]) for i in range(G.n)}
        ports = [G.id[(0,1)], G.id[(0,3)], G.id[(0,6)]]
        line += ' P_k hp counts=' + str([len(ham_paths(padj, Pk, p, q)) for p,q in itertools.combinations(ports,2)])
    print(line, flush=True)
