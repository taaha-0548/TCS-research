"""A7: graph class of the independently built family: cubic, 3-connected, planar; and an exhaustive
count of Hamiltonian cycles (pruned DFS: every unvisited vertex must keep >= 2 usable neighbours)."""
import sys, time
sys.path.insert(0, "..")
import networkx as nx
from a3_family import build

def count_ham(adj, budget_s):
    V = list(adj); n = len(V); lab = {v: i for i, v in enumerate(V)}; A = [[lab[w] for w in adj[v]] for v in V]
    seen = [False] * n; seen[0] = True; path = [0]; cnt = [0]; t0 = time.time()
    def ok():
        end = path[-1]
        for v in range(n):
            if not seen[v]:
                free = sum(1 for w in A[v] if not seen[w] or w == end or w == 0)
                if free < 2: return False
        return True
    def dfs():
        if time.time() - t0 > budget_s: raise TimeoutError
        v = path[-1]
        if len(path) == n:
            if 0 in A[v]: cnt[0] += 1
            return
        for w in A[v]:
            if not seen[w]:
                seen[w] = True; path.append(w)
                if ok(): dfs()
                path.pop(); seen[w] = False
    dfs(); return cnt[0] // 2

for k in range(0, 13):
    adj, cycles = build(k); g = nx.Graph([(v, w) for v in adj for w in adj[v]])
    props = dict(n=len(adj), cubic=all(len(set(a)) == 3 for a in adj.values()),
                 conn=nx.node_connectivity(g) if k <= 10 else "skip", planar=nx.check_planarity(g)[0])
    try: hc = count_ham(adj, 40) if k <= 7 else "skip"
    except TimeoutError: hc = "timeout"
    print(f"k={k}: {props}  Hamiltonian cycles (exhaustive)={hc}", flush=True)
