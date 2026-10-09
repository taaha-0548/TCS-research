from core import *
paper = """0 1 2 3 4 6' 5' 7' 0' 4' 3' 1' 6 7
0 1 2 3 4 6' 5' 7' 0' 4' 3' 7 6 1'
0 1 2 3 4 6' 5' 7' 0' 1' 6 7 3' 4'
0 1 2 3 4 6' 5' 4' 3' 7 6 1' 0' 7'
0 1 2 3 4 6' 7' 0' 1' 6 7 3' 4' 5'
0 1 2 3 4 6' 7' 5' 4' 3' 7 6 1' 0'
0 1 2 3 4 6' 7' 5' 4' 0' 1' 6 7 3'
0 1 2 3 4 6' 7' 5' 4' 0' 1' 3' 7 6
0 1 2 6 7 3' 1' 0' 4' 5' 7' 6' 4 3
0 1 3 4 6' 7' 5' 4' 0' 1' 3' 7 6 2
0 1 3 2 6 7 3' 1' 0' 4' 5' 7' 6' 4""".split('\n')
rots = ["-","7,3'","1',0'","4',5'","7',6'","5',7'","0',4'","3',1'","6,2","3,1","2,3"]
G = Gk(1)
name = lambda i: f"{G.labels[i][1]}" + ("'" if G.labels[i][0] == 1 else '')
steps, trace = lollipop_literal(G.adj, G.start_path())
print('steps', steps)
allok = True
for t, P in enumerate(trace):
    s = ' '.join(name(v) for v in P)
    rot = '-' if t == 0 else f"{name(trace[t-1][-1])},{name(P[len(P)-1-0] if False else [w for w in trace[t-1] if True][[i for i in range(len(P)) if P[i]!=trace[t-1][i]][0]-1])}"
    inner = G.labels[P[-1]][0] == 1
    ok = (s == paper[t]) and rot == rots[t]
    allok &= ok
    print(t, rot, '*' if inner else ' ', s, 'OK' if ok else f'DIFF paper: {rots[t]} | {paper[t]}')
print('all match:', allok)
