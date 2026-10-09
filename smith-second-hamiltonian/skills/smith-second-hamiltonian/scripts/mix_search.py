"""E22: mixed nested families.  Level k uses gadget g_k = (K, x, r, perm); P_k = (K - r)[x <- P_{k-1}].
All P_k stay simple (Lemma C(a)), so c_k = c0(g_k) + M(g_k) c_{k-1}.  For a periodic word g_1..g_p the
growth per period is rho(M(g_1)...M(g_p)) and the per-vertex base is rho^(1/sum(|K_i| - 2)).
Rows of M are visits of the outer pole (named by its ports), columns visits of the inner pole."""
import sys, json, itertools, time
import numpy as np
sys.path.insert(0, "../../../../paper")
import verify as V

def gadget_mats(adj):
    n = len(adj); out = []
    for r in range(n):
        P0, ports, idx = V.pole(adj, r); name = {p: "abc"[i] for i, p in enumerate(ports)}
        visits = {}
        for s, t in itertools.permutations(ports, 2):
            Q = V.ham_paths(P0, s, t)[0]
            for kd in ("B1", "B3"): visits[(name[s] + name[t], kd)] = V.visit(P0, ports, Q, kd)
        keys = sorted(visits)
        for x in range(n):
            if x == r or x in adj[r]: continue
            for perm in itertools.permutations(range(3)):
                xn = {idx[u]: "abc"[perm[j]] for j, u in enumerate(adj[x])}
                M = np.array([[V.passages(visits[e][3], idx[x], xn).get(f, 0) for f in keys] for e in keys])
                c0 = np.array([visits[e][2] for e in keys])
                out.append(dict(n=n, x=x, r=r, perm=perm, M=M, c0=c0, adj=adj))
    return out

def rho(A): return float(max(abs(np.linalg.eigvals(A))))

if __name__ == "__main__":
    lib = []
    for n in (8, 10, 12):
        for adj in json.load(open(f"e21_three_cycle_graphs_n{n}.json")): lib += gadget_mats(adj)
    uniq = {}
    for g in lib:
        key = (g["n"], g["M"].tobytes())
        if key not in uniq: uniq[key] = g
    lib = list(uniq.values()); print("distinct gadget matrices:", len(lib), {n: sum(g["n"] == n for g in lib) for n in (8, 10, 12)})
    single = sorted(((rho(g["M"]) ** (1 / (g["n"] - 2)), i) for i, g in enumerate(lib)), reverse=True)
    print("best single gadget: base %.6f (n=%d)" % (single[0][0], lib[single[0][1]]["n"]))
    t0 = time.time()
    # period 2: all pairs among the top-N gadgets by single base plus all 8-vertex ones
    top = sorted(set([i for _, i in single[:300]] + [i for i, g in enumerate(lib) if g["n"] == 8]))
    best2 = []
    for i, j in itertools.combinations_with_replacement(top, 2):
        gi, gj = lib[i], lib[j]
        b = rho(gi["M"] @ gj["M"]) ** (1 / (gi["n"] + gj["n"] - 4))
        best2.append((b, i, j))
    best2.sort(reverse=True)
    print(f"period 2 ({len(best2)} pairs, {time.time()-t0:.0f}s): best base %.6f" % best2[0][0], [(lib[i]["n"], lib[i]["x"], lib[i]["r"], lib[i]["perm"]) for i in best2[0][1:]])
    # beam search over longer periods (cyclic words), beam of best prefixes
    beam = [((i,), lib[i]["M"].astype(float), lib[i]["n"] - 2) for _, i in single[:60]] + [((i, j), lib[i]["M"] @ lib[j]["M"], lib[i]["n"] + lib[j]["n"] - 4) for _, i, j in best2[:60]]
    bestw = max(((rho(P) ** (1 / s), w) for w, P, s in beam))
    for L in range(3, 9):
        cand = []
        for w, P, s in beam:
            for k in top:
                g = lib[k]; Pn = P @ g["M"]; sn = s + g["n"] - 2
                cand.append((rho(Pn) ** (1 / sn), w + (k,), Pn, sn))
        cand.sort(key=lambda t: -t[0]); beam = [(w, P, s) for _, w, P, s in cand[:80]]
        if cand[0][0] > bestw[0]: bestw = (cand[0][0], cand[0][1])
        print(f"period {L}: best base in beam %.6f   overall best %.6f  ({time.time()-t0:.0f}s)" % (cand[0][0], bestw[0]), flush=True)
    w = bestw[1]
    print("best word:", [(lib[k]["n"], lib[k]["x"], lib[k]["r"], lib[k]["perm"]) for k in w])
    json.dump(dict(base=bestw[0], word=[dict(n=lib[k]["n"], x=lib[k]["x"], r=lib[k]["r"], perm=lib[k]["perm"], adj=lib[k]["adj"]) for k in w]), open("e22_mix_best.json", "w"))
