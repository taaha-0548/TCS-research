"""Host-independent transducer of a 3-pole (route R2), derived from the Mirror Lemma proof.

Internal state of X between visits: a Hamiltonian path Q of X between two ports, oriented
from the port nearer v0 (p_in) to the other (p_out).  Two kinds of visit:
  B1(Q): the walk deletes the entry cut edge at p_in; X is re-rooted at p_out and the endpoint
         wanders inside X until it leaves through a cut edge: through p_in = REFLECT,
         through the third port = TRANSMIT.
  B3(Q): the walk adds the unused cut edge at the third port c; X splits into X1 (p_in..c) and
         X2 (from p_out); the walk ping-pongs; TRANSMIT iff the number of X1-rotations is odd.
Output of a visit: (TRANSMIT/REFLECT, new oriented path Q', internal steps)."""
import itertools

def ham_paths_between(padj, s, t):
    m = len(padj); out = []
    def dfs(p, seen):
        v = p[-1]
        if len(p) == m:
            if v == t: out.append(tuple(p))
            return
        for w in padj[v]:
            if w not in seen and (w != t or len(p) == m - 1):
                seen.add(w); p.append(w); dfs(p, seen); p.pop(); seen.remove(w)
    dfs([s], {s}); return out

def rot(R, w, z_idx_map=None):
    i = R.index(w); return R[:i+1] + R[i+1:][::-1]

def visit_B1(padj, ports, Q):
    a, b = Q[0], Q[-1]; c = [p for p in ports if p not in (a, b)][0]
    R = list(Q[::-1]); forb = ("cut", a); steps = 0
    while True:
        z = R[-1]; prev = R[-2] if len(R) > 1 else ("cut", b)
        cands = [w for w in padj[z] if w != prev and w != forb]
        if z in ports and z != b: cands.append(("cut", z))
        cands = [w for w in cands if w != forb and w != prev]
        assert len(cands) == 1, (z, cands)
        w = cands[0]
        if isinstance(w, tuple):
            return ("REFLECT" if z == a else "TRANSMIT"), tuple(R), steps
        R = rot(R, w); forb = w; steps += 1

def visit_B3(padj, ports, Q):
    a, b_out = Q[0], Q[-1]; c = [p for p in ports if p not in (a, b_out)][0]
    i = Q.index(c)
    X1 = list(Q[:i+1]); X2 = list(Q[i+1:][::-1])      # X1: a..c (exit port pb=c); X2 from b_out
    pb = c; forb = c; k = 0; steps = 0
    while True:
        z = X2[-1]; prev = X2[-2] if len(X2) > 1 else None
        cands = [w for w in padj[z] if w != prev and w != forb]
        assert len(cands) == 1, (z, cands, X1, X2)
        w = cands[0]; steps += 1
        if w in X2:
            X2 = rot(X2, w)
        elif w == pb:
            newQ = tuple(X1 + X2[::-1])
            return ("TRANSMIT" if k % 2 == 1 else "REFLECT"), newQ, steps
        else:
            j = X1.index(w)
            nX1 = X1[:j+1] + X2[::-1]; nX2 = X1[j+1:][::-1]
            pb = nX1[-1]; X1, X2 = nX1, nX2; k += 1
        forb = w

def transducer(padj, ports):
    states = []
    for s, t in itertools.permutations(ports, 2):
        states += ham_paths_between(padj, s, t)
    table = {}
    for Q in states:
        table[Q] = {"B1": visit_B1(padj, ports, Q), "B3": visit_B3(padj, ports, Q)}
    return table

def summary(table):
    n = len(table); refl = sum(v[k][0] == "REFLECT" for v in table.values() for k in v)
    changed = sum(set(v[k][1]) and v[k][1] not in (Q, Q[::-1]) for Q, v in table.items() for k in v)
    return dict(oriented_states=n, reflect_entries=refl, state_changing_entries=changed)

if __name__ == "__main__":
    from exp_3pole_transparency import poles
    for name, (padj, ports) in poles.items():
        if name.startswith("petersen"): continue
        T = transducer(padj, ports); print(f"{name:16s} {summary(T)}")
