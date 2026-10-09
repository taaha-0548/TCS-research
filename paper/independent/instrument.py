import itertools, random, sys
import networkx as nx
from core import *

def run_instrumented(adj, S0, Xset, xv, lab):
    """lab: vertex -> K label (for X vertices). Returns list of visit dicts."""
    events = []
    def rec(P, z, w, s):
        i = P.index(x_) if False else None
        events.append((tuple(P), z, w, s))
    x_ = xv
    steps, _ = lollipop(adj, S0, record=rec)
    visits = []; cur = None
    def proj(P):
        out = []
        for v in P:
            if v in Xset:
                if not out or out[-1] != 'x': out.append('x')
            else: out.append(v)
        if P[-1] in Xset and out.count('x') == 2: out.pop()   # pi of a B3 state: Y1 x Y2
        assert out.count('x') == 1
        return tuple(out)
    for t, (P, z, w, s) in enumerate(events, start=1):
        Pafter_end = s
        if cur is None and z not in Xset and s in Xset:
            kind = 'B3' if w in Xset else 'B1'
            Q = [v for v in P if v in Xset]
            # check contiguity (type A)
            idx = [j for j,v in enumerate(P) if v in Xset]
            assert idx == list(range(idx[0], idx[-1]+1))
            pin, pout = PNAME[lab[Q[0]]], PNAME[lab[Q[-1]]]
            cur = dict(type=f'{pin}{pout}/{kind}', kind=kind, t0=t, Q=''.join(str(lab[v]) for v in Q),
                       steps=[], passages=[], entry_passage=False, S=proj(P), pin=Q[0])
        if cur is not None:
            # passage detection
            mark = ''
            if s == xv or w == xv:
                j = P.index(xv); u, v = P[j-1], P[j+1]
                pk = 'B1' if s == xv else 'B3'
                cur['passages'].append(f'{WNAME[lab[u]]}{WNAME[lab[v]]}/{pk}')
                mark = '†' if s == xv else '‡'
                if t == cur['t0']: cur['entry_passage'] = True
            if t > cur['t0']:
                cur['steps'].append((t, f'{lab.get(z,"?")}{lab.get(w,"?")}' + mark, z in Xset and s not in Xset))
            if t == cur['t0']:
                cur['Sstar'] = None  # filled from next event
            if t == cur['t0'] + 1 or (t > cur['t0'] and cur.get('Sstar') is None):
                cur['Sstar'] = proj(P)  # state after entry = state before step t0+1
            if t > cur['t0'] and z in Xset and s not in Xset:
                cur['t1'] = t
                cur['cost'] = t - cur['t0'] - (1 if cur['kind'] == 'B1' else 0)
                Q2 = P[:P.index(w)+1] + P[:P.index(w):-1]
                after = proj(Q2)
                if cur['kind'] == 'B1':
                    cur['transmit'] = (z != cur['pin'])
                else:
                    assert after in (cur['S'], cur['Sstar'])
                    cur['transmit'] = (after == cur['Sstar'])
                lst = [st for (tt, st, ex) in cur['steps'] if cur['kind'] == 'B3' or tt < t]
                cur['listing'] = ' '.join(lst)
                visits.append(cur); cur = None
    assert cur is None
    return steps, visits

def summarize(visits, table):
    for v in visits:
        key = v['type']
        rec = (v['cost'], tuple(sorted(v['passages'])), v['Q'], v['listing'], v['entry_passage'], v['transmit'])
        table.setdefault(key, set()).add(rec)

if __name__ == '__main__':
    table = {}
    # 1) innermost copy of G_k
    for k in range(1, 9):
        G = Gk(k)
        Xset = {G.id[(k,l)] for l in P0V}
        lab = {i: G.labels[i][1] for i in range(G.n)}
        steps, visits = run_instrumented(G.adj, G.start_path(), Xset, G.id[(k,5)], lab)
        summarize(visits, table)
        print('G_k innermost copy k=%d: %d visits, types seen %s' % (k, len(visits), sorted({v['type'] for v in visits})))
    seen_Gk = set(table)
    # 2) generic hosts H[y <- P0]
    def ham_cycles(H):
        nodes = list(H); n = len(nodes); s0 = nodes[0]; res = []
        def rec(path, seen):
            u = path[-1]
            if len(path) == n:
                if s0 in H[u] and path[1] < path[-1]: res.append(list(path))
                return
            for w in H[u]:
                if w not in seen:
                    seen.add(w); path.append(w); rec(path, seen); path.pop(); seen.discard(w)
        rec([s0], {s0}); return res
    hosts = []
    for E in [KEDGES]: hosts.append(nx.Graph(E))
    hosts.append(nx.cubical_graph()); hosts.append(nx.petersen_graph()); hosts.append(nx.complete_graph(4))
    hosts.append(nx.circular_ladder_graph(5)); hosts.append(nx.moebius_kantor_graph()); hosts.append(nx.dodecahedral_graph())
    rng = random.Random(1)
    for n in [8,10,12,14]:
        for _ in range(4):
            hosts.append(nx.random_regular_graph(3, n, seed=rng.randrange(10**9)))
    nruns = 0
    for H in hosts:
        H = nx.convert_node_labels_to_integers(H)
        if not nx.is_connected(H): continue
        cycles = ham_cycles(H)[:6]
        for y in H:
            Ny = sorted(H[y])
            for perm in itertools.permutations([1,3,6]):
                wire = dict(zip(Ny, perm))
                verts = [v for v in H if v != y] + [('p',l) for l in P0V]
                id_ = {v:i for i,v in enumerate(verts)}
                adj = [[] for _ in verts]
                def add(a,b): adj[id_[a]].append(id_[b]); adj[id_[b]].append(id_[a])
                for a,b in H.edges():
                    if y not in (a,b): add(a,b)
                for a,b in KEDGES:
                    if R not in (a,b): add(('p',a),('p',b))
                for q,p in wire.items(): add(q,('p',p))
                Xset = {id_[('p',l)] for l in P0V}
                lab = {id_[('p',l)]: l for l in P0V}
                for C in cycles:
                    n = len(C)
                    for i in range(n):
                        for d in (1,-1):
                            seq = [C[(i+d*j) % n] for j in range(n)]
                            v0 = seq[0]
                            if v0 == y or v0 in H[y]: continue
                            S = []
                            for j,v in enumerate(seq):
                                if v == y:
                                    S += [id_[('p',l)] for l in p0_path(wire[seq[j-1]], wire[seq[(j+1)%n]])]
                                else: S.append(id_[v])
                            steps, visits = run_instrumented(adj, S, Xset, id_[('p',5)], lab)
                            summarize(visits, table); nruns += 1
    print('generic host runs:', nruns)
    paperA = {
'ab/B1':('1076543','13 40 75‡',3,'ca/B3'),
'ab/B3':('1076543','57 65‡ 40 76† 54 31 07† 56 75‡ 43',10,'ab/B1, ac/B1, ac/B3, bc/B1, bc/B3'),
'ac/B1':('1340756','10 45‡ 76† 57 04',5,'ab/B3, ac/B1'),
'ac/B3':('1340756','45‡ 76† 57 01 34† 56 70 45‡ 67† 56',10,'ab/B3, ac/B1, ba/B3, bc/B1, cb/B1'),
'ba/B1':('3456701','31 04† 57',3,'ca/B1'),
'ba/B3':('3456701','75‡ 67 04† 56 70 13 45‡ 76† 57 01',10,'ab/B3, ac/B1, ca/B3, cb/B1'),
'bc/B1':('3104576','34 07† 56 75‡ 40',5,'ac/B3, bc/B1'),
'bc/B3':('3104576','07† 56 75‡ 43 10 76† 54 07 65‡ 76',10,'ab/B1, ac/B3, bc/B1, cb/B3'),
'ca/B1':('6570431','67† 54 01',3,'ba/B1'),
'ca/B3':('6570431','10 45‡ 76† 57 04 31',6,'ab/B3, ac/B1'),
'cb/B1':('6754013','65‡ 70 43',3,'cb/B3'),
'cb/B3':('6754013','34 07† 56 75‡ 40 13',6,'ac/B3, bc/B1')}
    entry_dagger = {'ab/B3'}
    print()
    for t in sorted(paperA, key=lambda s: ['ab/B1','ab/B3','ac/B1','ac/B3','ba/B1','ba/B3','bc/B1','bc/B3','ca/B1','ca/B3','cb/B1','cb/B3'].index(s)):
        recs = table.get(t)
        if not recs:
            print(t, 'NOT OBSERVED'); continue
        hostind = len(recs) == 1
        (cost, pas, Q, listing, ep, tr) = next(iter(recs))
        Qp, Lp, cp, pp = paperA[t]
        ok = (Q == Qp and listing == Lp and cost == cp and pas == tuple(sorted(pp.split(', '))) and ep == (t in entry_dagger))
        print(f"{t}: host-independent={hostind} cost={cost} transmit={tr} Q={Q} entry†={ep} passages={', '.join(pas)} listing='{listing}' in_Gk={t in seen_Gk} -> {'MATCH' if ok else 'DIFF vs paper: '+str(paperA[t])}")
