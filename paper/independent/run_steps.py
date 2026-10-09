import sys, time
from core import *
kmax = int(sys.argv[1])
paper = {1:10,2:25,3:73,4:214,5:628,6:1849,7:5449,8:16060,9:47338,10:139537,11:411313,12:1212430}
for k in range(0, kmax+1):
    G = Gk(k); S0 = G.start_path()
    assert len(S0) == G.n == 8+6*k and len(set(S0)) == G.n
    assert all(S0[i+1] in G.adj[S0[i]] for i in range(G.n-1)) and S0[0] in G.adj[S0[-1]]
    assert G.labels[S0[0]] == (0,0) and G.labels[S0[1]] == (0,1) and G.labels[S0[-1]] == (0,7)
    t = time.time(); s, P = lollipop(G.adj, S0)
    extra = ''
    if k <= 7:
        s2, _ = lollipop_literal(G.adj, S0); extra = f' literal={s2}'
    print(k, G.n, s, paper.get(k), 'OK' if paper.get(k) in (None, s) else 'MISMATCH', extra, f'{time.time()-t:.1f}s', flush=True)
