"""Minimum e(G) for a single colour class that contains prescribed cliques ("frames").

G lives on n = r^2+1 vertices partitioned into blocks.  Blocks marked fixed are cliques of G; all other
pairs (between blocks, and inside free blocks) are decision variables.  Constraints:
  (A) alpha(G) <= r,   (C) every (r+1)-set spans <= C(r,2)+1 edges,
  (D, optional) every W of size k in D_sizes spans <= C(k,2) - (r-1) p_r(k) edges.
Minimise e(G); compare with M_r = C(n,2)/r.  Exact: CP-SAT master + lazy cuts with exact separation.

Frames of interest:
  'cover'  : r+1 fixed cliques (the blocking lemma),
  'furedi' : sizes (r+1, r, ..., r), first block free, others fixed (the Furedi frame at n = r^2+1)."""
import itertools, random, sys, time
from math import comb
from ortools.sat.python import cp_model

def p_turan(r, m):
    a, b = divmod(m, r); return r * comb(a, 2) + a * b

class Frame:
    def __init__(self, r, sizes, free):
        self.r, self.sizes, self.free = r, sizes, free
        self.part = [j for j, s in enumerate(sizes) for _ in range(s)]
        self.n = len(self.part)
        self.blocks = [[v for v in range(self.n) if self.part[v] == j] for j in range(len(sizes))]
        self.fixed = {(u, v) for j, B in enumerate(self.blocks) if not free[j] for u, v in itertools.combinations(B, 2)}
        self.var_pairs = [e for e in itertools.combinations(range(self.n), 2) if e not in self.fixed]

    def lim(self, k):
        return comb(k, 2) - (self.r - 1) * p_turan(self.r, k)

    def adjacency(self, E):
        A = [set() for _ in range(self.n)]
        for u, v in list(self.fixed) + list(E): A[u].add(v); A[v].add(u)
        return A

    def independent_sets(self, A, k, limit, rng):
        out = set()
        for _ in range(60 * limit):
            order = list(range(self.n)); rng.shuffle(order); S = []
            for v in order:
                if all(v not in A[u] for u in S): S.append(v)
            if len(S) >= k:
                out.add(tuple(sorted(S[:k])))
                if len(out) >= limit: break
        if out: return list(out)
        m = cp_model.CpModel(); y = [m.NewBoolVar("") for _ in range(self.n)]
        m.Add(sum(y) == k)
        for u in range(self.n):
            for v in A[u]:
                if u < v: m.AddBoolOr([y[u].Not(), y[v].Not()])
        s = cp_model.CpSolver(); s.parameters.num_workers = 4; s.parameters.max_time_in_seconds = 300
        st = s.Solve(m)
        if st == cp_model.OPTIMAL or st == cp_model.FEASIBLE: return [tuple(v for v in range(self.n) if s.Value(y[v]))]
        if st == cp_model.INFEASIBLE: return []
        raise RuntimeError("independent-set separation inconclusive")

    def dense_set(self, A, k, limit):
        m = cp_model.CpModel(); y = [m.NewBoolVar("") for _ in range(self.n)]; m.Add(sum(y) == k)
        z = []
        for u in range(self.n):
            for v in A[u]:
                if u < v:
                    w = m.NewBoolVar(""); m.AddImplication(w, y[u]); m.AddImplication(w, y[v]); z.append(w)
        m.Add(sum(z) >= limit + 1)
        s = cp_model.CpSolver(); s.parameters.num_workers = 4; s.parameters.max_time_in_seconds = 300
        st = s.Solve(m)
        if st == cp_model.INFEASIBLE: return None
        if st in (cp_model.OPTIMAL, cp_model.FEASIBLE): return tuple(v for v in range(self.n) if s.Value(y[v]))
        raise RuntimeError("dense-set separation inconclusive")

    def solve(self, D_sizes=(), timeout=900, seed=0):
        r = self.r; rng = random.Random(seed)
        indep, caps = [], []
        # seed cap cuts: each fixed block plus (r+1-|B|) outside vertices when that is 1 or 2
        for j, B in enumerate(self.blocks):
            need = r + 1 - len(B)
            if not self.free[j] and 1 <= need <= 2:
                for X in itertools.combinations([v for v in range(self.n) if v not in B], need):
                    caps.append(tuple(B) + X)
        base = len(self.fixed); t0 = time.time(); rounds = 0
        while True:
            rounds += 1
            m = cp_model.CpModel(); x = {e: m.NewBoolVar("") for e in self.var_pairs}
            def lits(S):
                return [x[e] for e in itertools.combinations(sorted(S), 2) if e in x]
            def nfixed(S):
                return sum(1 for e in itertools.combinations(sorted(S), 2) if e in self.fixed)
            for S in indep: m.AddBoolOr(lits(S))
            for S in caps: m.Add(sum(lits(S)) <= self.lim(len(S)) - nfixed(S))
            m.Minimize(sum(x.values()))
            s = cp_model.CpSolver(); s.parameters.num_workers = 4; s.parameters.max_time_in_seconds = timeout
            st = s.Solve(m)
            if st == cp_model.INFEASIBLE: return "INFEASIBLE", None, rounds, time.time() - t0
            if st != cp_model.OPTIMAL:
                return f"{s.StatusName(st)} lb={base + s.BestObjectiveBound()}", None, rounds, time.time() - t0
            E = [e for e in self.var_pairs if s.Value(x[e])]
            A = self.adjacency(E)
            I = self.independent_sets(A, r + 1, 300, rng)
            if I: indep.extend(I); continue
            bad = self.dense_set(A, r + 1, self.lim(r + 1))
            if bad: caps.append(bad); continue
            hit = False
            for k in D_sizes:
                bad = self.dense_set(A, k, self.lim(k))
                if bad: caps.append(bad); hit = True; break
            if hit: continue
            return base + len(E), E, rounds, time.time() - t0

if __name__ == "__main__":
    r = int(sys.argv[1]); kind = sys.argv[2]; useD = len(sys.argv) > 3 and sys.argv[3] == "D"
    n = r * r + 1; M = comb(n, 2) / r
    D_sizes = list(range(r + 2, 2 * r + 2)) if useD else []
    if kind == "furedi":
        frames = [((r + 1,) + (r,) * (r - 1), (True,) + (False,) * (r - 1))]
    else:
        from blocking_lemma import partitions
        frames = [(sz, (False,) * len(sz)) for sz in partitions(n, r + 1, r)]
    print(f"r={r} n={n} M_r={M:.1f} frame={kind} caps={'C+D' if useD else 'C'}", flush=True)
    for sizes, free in frames:
        F = Frame(r, sizes, free)
        val, E, rounds, dt = F.solve(D_sizes=D_sizes)
        tag = "" if not isinstance(val, int) else ("> M_r" if val > M else "<= M_r ***")
        print(f"  sizes={sizes} free={[j for j, f in enumerate(free) if f]}: min e(G)={val} {tag} [{rounds} rounds, {dt:.0f}s]", flush=True)
