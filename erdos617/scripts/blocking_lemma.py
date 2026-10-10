"""Blocking lemma experiment (approach 3 in README).

Setting: the minority colour G of a balanced r-colouring of K_{r^2+1} is a disjoint union of r+1
cliques V_0..V_r (sizes s_j <= r, sum r^2+1) plus cross edges E+.  Requirements:
  (A) alpha(G) <= r   <=>  every transversal (one vertex per clique) contains an E+ edge,
  (C) every (r+1)-set spans <= C(r,2)+1 edges of G,
  (D) optional: every W spans <= D_r(|W|) = C(|W|,2) - (r-1) p_r(|W|) edges (other colours' Turan bound).
We compute the minimum |E+| exactly (CP-SAT + lazy constraint generation with exact separation) and compare
e(G) = sum C(s_j,2) + |E+| with the minority budget M_r = C(r^2+1,2)/r.
If every partition gives e(G) > M_r, this clique-cover family cannot be a minority colour."""
import itertools, os, sys, time
DECIDE_CAP = os.environ.get("DECIDE_CAP")  # if set: feasibility of e(G) <= DECIDE_CAP
from math import comb
from ortools.sat.python import cp_model

def p_turan(r, m):
    a, b = divmod(m, r); return r * comb(a, 2) + a * b

def partitions(total, parts, cap):
    def rec(left, k, mx):
        if k == 0:
            if left == 0: yield ()
            return
        for s in range(min(mx, left - (k - 1)), 0, -1):
            if s * k < left: break
            for rest in rec(left - s, k - 1, s): yield (s,) + rest
    yield from rec(total, parts, cap)

class Instance:
    def __init__(self, r, sizes):
        self.r, self.sizes = r, sizes
        self.part = [j for j, s in enumerate(sizes) for _ in range(s)]
        self.n = len(self.part)
        self.blocks = [[v for v in range(self.n) if self.part[v] == j] for j in range(len(sizes))]
        self.cross = [(u, v) for u, v in itertools.combinations(range(self.n), 2) if self.part[u] != self.part[v]]
        self.cap = comb(r, 2) + 1

    def adj(self, E):
        A = [[False] * self.n for _ in range(self.n)]
        for B in self.blocks:
            for u, v in itertools.combinations(B, 2): A[u][v] = A[v][u] = True
        for u, v in E: A[u][v] = A[v][u] = True
        return A

    def independent_transversal(self, A):
        chosen = []
        def dfs(j):
            if j == len(self.blocks): return True
            for v in self.blocks[j]:
                if all(not A[v][u] for u in chosen):
                    chosen.append(v)
                    if dfs(j + 1): return True
                    chosen.pop()
            return False
        return list(chosen) if dfs(0) else None

    def many_transversals(self, A, limit):
        """Up to `limit` distinct independent transversals (randomised DFS orders)."""
        import random
        out = set(); rng = random.Random(len(self.blocks))
        T = self.independent_transversal(A)
        if T is None: return []
        out.add(tuple(T))
        tries = 0
        while len(out) < limit and tries < 4 * limit:
            tries += 1
            order = list(range(len(self.blocks))); rng.shuffle(order)
            chosen = []
            def dfs(i):
                if i == len(order): return True
                B = self.blocks[order[i]][:]; rng.shuffle(B)
                for v in B:
                    if all(not A[v][u] for u in chosen):
                        chosen.append(v)
                        if dfs(i + 1): return True
                        chosen.pop()
                return False
            if dfs(0): out.add(tuple(sorted(chosen)))
        return list(out)

    def densest(self, A, k, limit):
        """A k-set with more than `limit` edges, or None (exact, via CP-SAT)."""
        m = cp_model.CpModel(); y = [m.NewBoolVar("") for _ in range(self.n)]
        m.Add(sum(y) == k)
        z = {}
        for u, v in itertools.combinations(range(self.n), 2):
            if A[u][v]:
                z[(u, v)] = m.NewBoolVar(""); m.AddImplication(z[(u, v)], y[u]); m.AddImplication(z[(u, v)], y[v])
        m.Maximize(sum(z.values()))
        s = cp_model.CpSolver(); s.parameters.num_workers = 4; s.parameters.max_time_in_seconds = 120
        st = s.Solve(m)
        if st == cp_model.OPTIMAL and s.ObjectiveValue() <= limit: return None
        if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) and s.ObjectiveValue() > limit:
            return [v for v in range(self.n) if s.Value(y[v])]
        raise RuntimeError(f"densest-subgraph separation inconclusive: {s.StatusName(st)}")

    def solve(self, use_D=False, D_sizes=(), timeout=600, verbose=False):
        r = self.r
        transversals, capsets = [], []
        # seed: clique + outside vertices, the binding cap sets
        for B in self.blocks:
            s = len(B); need = r + 1 - s
            if 1 <= need <= 2:
                for X in itertools.combinations([v for v in range(self.n) if v not in B], need):
                    capsets.append(tuple(B) + X)
        t0 = time.time(); rounds = 0
        while True:
            rounds += 1
            m = cp_model.CpModel(); x = {e: m.NewBoolVar("") for e in self.cross}
            within = lambda S: sum(1 for u, v in itertools.combinations(sorted(S), 2) if self.part[u] == self.part[v])
            for T in transversals:
                m.AddBoolOr([x[(min(a, b), max(a, b))] for a, b in itertools.combinations(T, 2)])
            for S, lim in capsets_lim(capsets, self, use_D):
                m.Add(sum(x[(a, b)] for a, b in itertools.combinations(sorted(S), 2) if self.part[a] != self.part[b])
                      <= lim - within(S))
            if DECIDE_CAP is not None: m.Add(sum(x.values()) <= int(DECIDE_CAP) - sum(comb(q, 2) for q in self.sizes))
            else: m.Minimize(sum(x.values()))
            s = cp_model.CpSolver(); s.parameters.num_workers = 4; s.parameters.max_time_in_seconds = timeout
            st = s.Solve(m)
            if st == cp_model.INFEASIBLE:
                return None, "INFEASIBLE (e(G) > cap)", rounds, time.time() - t0
            if st != cp_model.OPTIMAL and not (DECIDE_CAP is not None and st == cp_model.FEASIBLE):
                return None, f"{s.StatusName(st)} bound={s.BestObjectiveBound()}", rounds, time.time() - t0
            E = [e for e in self.cross if s.Value(x[e])]
            A = self.adj(E)
            Ts = self.many_transversals(A, 400)
            if Ts: transversals.extend(Ts); continue
            bad = self.densest(A, r + 1, self.cap)
            if bad is not None: capsets.append(tuple(bad)); continue
            if use_D:
                found = False
                for k in D_sizes:
                    lim = comb(k, 2) - (r - 1) * p_turan(r, k)
                    bad = self.densest(A, k, lim)
                    if bad is not None: capsets.append(tuple(bad)); found = True; break
                if found: continue
            if verbose: print(f"    rounds={rounds}", flush=True)
            return len(E), E, rounds, time.time() - t0

def capsets_lim(capsets, inst, use_D):
    r = inst.r
    for S in capsets:
        k = len(S)
        lim = comb(k, 2) - (r - 1) * p_turan(r, k)     # = C(r,2)+1 when k = r+1
        yield S, lim

if __name__ == "__main__":
    r = int(sys.argv[1]); use_D = len(sys.argv) > 2 and sys.argv[2] == "D"
    n = r * r + 1; M = comb(n, 2) / r
    D_sizes = [k for k in range(r + 2, 2 * r + 2)] if use_D else ()
    print(f"r={r} n={n} M_r={M:.1f}  (caps: {'(C)+(D) up to 2r+1' if use_D else '(C) only'})", flush=True)
    for sizes in partitions(n, r + 1, r):
        inst = Instance(r, sizes); inner = sum(comb(s, 2) for s in sizes)
        val, E, rounds, dt = inst.solve(use_D=use_D, D_sizes=D_sizes)
        if val is None:
            print(f"  sizes={sizes} inner={inner}: {E} ({dt:.0f}s)", flush=True); continue
        tot = inner + val
        print(f"  sizes={sizes} inner={inner} min|E+|={val} (s_min^2={min(sizes)**2}) "
              f"e(G)={tot}  {'> M_r' if tot > M else '<= M_r  ***'}  [{rounds} rounds, {dt:.0f}s]", flush=True)
