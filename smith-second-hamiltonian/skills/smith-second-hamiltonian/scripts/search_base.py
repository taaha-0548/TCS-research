"""E21: exhaustive search for nested families with a larger base, using the exact method.
For a base K (cubic, Hamiltonian, exactly 3 Hamiltonian cycles), x, r with r not in N[x], wiring perm,
Hamiltonian cycle C of K and start (v0, d) with v0 not in N[x]:
   growth per level = rho(M_R), R = visit kinds reachable from the passages of K's walk through x;
   per-vertex base  = rho(M_R)^(1/(|K|-2)).
Everything is computed from the (|K|-1)-vertex pole K - r (Lemmas S, C)."""
import sys, itertools, time, json, random
import numpy as np
sys.path.insert(0, "../../../../paper")
import verify as V
from lollipop import all_instances, random_instance

def chord_adj(n, ch): return [[(v - 1) % n, (v + 1) % n, ch[v]] for v in range(n)]

def cycles_as_lists(adj, n):
    out = []
    for E in V.ham_cycles(adj):
        c = [0]; prev = None
        while len(c) < n:
            nxt = next(w for w in adj[c[-1]] if frozenset((c[-1], w)) in E and w != prev); prev = c[-1]; c.append(nxt)
        out.append(c)
    return out

def walk_passages(adj, cyc, x, xname):
    v0 = cyc[0]; path = list(cyc); pos = {v: i for i, v in enumerate(path)}; last = v0; P = set()
    while True:
        z, pred = path[-1], path[-2]
        w = next(u for u in adj[z] if u != pred and u != last)
        if w == v0: return P
        i = pos[w]; s = path[i + 1]
        if s == x or w == x:
            j = path.index(x); P.add((xname[path[j-1]] + xname[path[j+1]], "B1" if s == x else "B3"))
        path[i+1:] = path[i+1:][::-1]
        for j in range(i + 1, len(path)): pos[path[j]] = j
        last = w

def analyse(adj, n, best, tag, planar_fn):
    cycs = cycles_as_lists(adj, n)
    if len(cycs) != 3: return 0
    found = 0
    for r in range(n):
        P0, ports, idx = V.pole(adj, r); name = {p: "abc"[i] for i, p in enumerate(ports)}
        visits = {}
        for s, t in itertools.permutations(ports, 2):
            Q = V.ham_paths(P0, s, t)[0]
            for kd in ("B1", "B3"):
                out, Qn, cost, moves = V.visit(P0, ports, Q, kd)
                assert out == "TRANSMIT"                     # Lemma S
                visits[(name[s] + name[t], kd)] = moves
        keys = sorted(visits)
        for x in range(n):
            if x == r or x in adj[r]: continue
            for perm in itertools.permutations(range(3)):
                xname_P = {idx[u]: "abc"[perm[j]] for j, u in enumerate(adj[x])}
                M = np.array([[V.passages(visits[e], idx[x], xname_P).get(f, 0) for f in keys] for e in keys], float)
                xname_K = {u: "abc"[perm[j]] for j, u in enumerate(adj[x])}
                for c in cycs:
                    for st in range(n):
                        v0 = c[st]
                        if v0 == x or v0 in adj[x]: continue
                        for d in (1, -1):
                            cyc = [c[(st + d * t) % n] for t in range(n)]
                            ent = walk_passages(adj, cyc, x, xname_K)
                            if not ent: continue
                            Rs = {keys.index(e) for e in ent}; stack = list(Rs)
                            while stack:
                                i = stack.pop()
                                for j in np.nonzero(M[i])[0]:
                                    if j not in Rs: Rs.add(int(j)); stack.append(int(j))
                            Rl = sorted(Rs); rho = max(abs(np.linalg.eigvals(M[np.ix_(Rl, Rl)]))) if Rl else 0
                            base = rho ** (1 / (n - 2)) if rho > 1 else 1.0
                            found += 1
                            key = (round(base, 6),)
                            if base > best.get("base", 0) - 1e-12 or len(best.setdefault("top", [])) < 25:
                                rec = dict(base=base, rho=float(rho), n=n, adj=adj, x=x, r=r, perm=perm, cycle=cyc, tag=tag)
                                best.setdefault("top", []).append(rec)
                                best["top"] = sorted(best["top"], key=lambda q: -q["base"])[:25]
                                best["base"] = best["top"][0]["base"]
    return found

if __name__ == "__main__":
    import networkx as nx
    n = int(sys.argv[1]); mode = sys.argv[2] if len(sys.argv) > 2 else "all"; budget = float(sys.argv[3]) if len(sys.argv) > 3 else 1e9
    t0 = time.time(); best = {}; graphs = good = 0; seen = set(); goodlist = []
    src = all_instances(n) if mode == "all" else (random_instance(n, random.Random(int(sys.argv[4]) if len(sys.argv) > 4 else 1)) for _ in iter(int, 1))
    for ch in src:
        if time.time() - t0 > budget: break
        adj = chord_adj(n, ch); graphs += 1
        g = nx.Graph([(v, w) for v in range(n) for w in adj[v]])
        A = np.zeros((n, n))
        for v in range(n):
            for w in adj[v]: A[v][w] = 1
        cert = tuple(np.round(np.sort(np.linalg.eigvalsh(A)), 6))
        if cert in seen: continue
        seen.add(cert)
        planar = nx.check_planarity(g)[0]
        if analyse(adj, n, best, "planar" if planar else "nonplanar", None): good += 1; goodlist.append(adj)
    print(f"n={n}: chord matchings scanned {graphs}, distinct (spectrum) {len(seen)}, with exactly 3 Ham cycles {good}, {time.time()-t0:.0f}s")
    for q in best.get("top", [])[:8]:
        print(f"  base {q['base']:.6f}  rho {q['rho']:.5f}  {q['tag']:9s} x={q['x']} r={q['r']} perm={q['perm']}  K={q['adj']}")
    json.dump(best.get("top", []), open(f"e21_search_n{n}_{mode}.json", "w"), default=str)
    json.dump(goodlist, open(f"e21_three_cycle_graphs_n{n}.json", "w"))
