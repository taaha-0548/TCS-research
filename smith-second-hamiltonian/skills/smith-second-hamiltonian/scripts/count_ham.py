import sys
from general import from_chord
from nested_fast import next_level
sys.setrecursionlimit(10000)
CH = [4, 3, 6, 1, 0, 7, 2, 5]; X, R, PERM = 5, 2, (2, 0, 1)
def count(A):
    n = len(A); seen = [False]*n; seen[0] = True; path = [0]; c = [0]
    def dfs():
        v = path[-1]
        if len(path) == n:
            if 0 in A[v]: c[0] += 1
            return
        # prune: an unvisited vertex with < 2 available neighbours (other than path ends) is dead
        for w in A[v]:
            if not seen[w]:
                seen[w] = True; path.append(w); dfs(); path.pop(); seen[w] = False
    dfs(); return c[0] // 2
K = from_chord(8, CH); Kc = list(range(8)); G, Gc = K, Kc; rl = R
for lev in range(5):
    print(f"level {lev}: n={len(G)} Hamiltonian cycles={count(G)}", flush=True)
    G, Gc = next_level(K, Kc, X, G, [Gc], rl, PERM); rl = R if R < X else R - 1
