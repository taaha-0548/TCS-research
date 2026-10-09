"""Phase 1 / P1.1: exact composition for 3-poles WITH memory.

Given the contracted pole P' (adjacency P1, ports1), an interior vertex x of P' (N(x) inside P'),
and the transducer table TX of an arbitrary 3-pole X substituted at x (wiring: j-th neighbour of
x in P1[x] order -> X-port perm[j]), compute every visit of P = P'[x <- X] by simulating the visit
on P' and handing each passage through x to X's table:
  B1 passage (a rotation deletes w-x, making x the endpoint): X decides the exit port; the walk then
     rotates at x along the edge to the neighbour attached to that port (exit = entry port means
     REFLECT: the rotation undoes the previous one).
  B3 passage (a rotation would attach to x): TRANSMIT -> perform it; REFLECT -> do not; either way
     the previous attachment becomes x.
X's internal path is carried as state.  Costs: P'-moves (with the visit conventions) + X costs."""
import sys
sys.path.insert(0, "../../../../../paper")
import verify as V

def rot(seq, w):
    i = seq.index(w); return seq[:i+1] + seq[i+1:][::-1]

class Inner:
    """Substituted pole X at vertex x of P'.  port_of[u] = X-port attached to P'-neighbour u."""
    def __init__(self, x, TX, port_of, QX):
        self.x, self.TX, self.port_of, self.QX = x, TX, port_of, tuple(QX)
        self.nb_of = {p: u for u, p in port_of.items()}
    def oriented(self, pred, succ):
        a, b = self.port_of[pred], self.port_of[succ]
        Q = self.QX
        if Q[0] == a and Q[-1] == b: return Q
        if Q[0] == b and Q[-1] == a: return Q[::-1]
        raise AssertionError("X state inconsistent with P' path")
    def visit(self, pred, succ, kind):
        Qo = self.oriented(pred, succ)
        res, Qn, k = self.TX[(Qo, kind)]
        self.QX = tuple(Qn); return res, Qn, k

def neighbours_in(seq, v):
    i = seq.index(v); return seq[i-1], seq[i+1]

def composed_visit(P1, ports1, Q1, kind, inner):
    """Q1: oriented path of P' (contains x).  Returns (outcome, Q1_final, cost, QX_final)."""
    x = inner.x
    a, b = Q1[0], Q1[-1]; c = next(p for p in ports1 if p not in (a, b)); cost = 0
    if kind == "B1":
        Rr = list(Q1[::-1]); last = ("cut", a)
        while True:
            z = Rr[-1]
            if z == x:                                    # endpoint inside X: X chooses the exit
                pred = Rr[-2]
                raise AssertionError("endpoint at x outside a passage")
            pred = Rr[-2]
            cand = [w for w in P1[z] if w != pred and w != last]
            if z in ports1 and z != b and last != ("cut", z): cand.append(("cut", z))
            assert len(cand) == 1, (z, cand)
            w = cand[0]
            if isinstance(w, tuple):
                return ("REFLECT" if z == a else "TRANSMIT"), tuple(Rr), cost, inner.QX
            j = Rr.index(w); s = Rr[j+1]
            if w == x:                                    # B3 passage
                p_, s_ = neighbours_in(Rr, x)
                res, Qn, k = inner.visit(p_, s_, "B3"); cost += 1 + k
                if res == "TRANSMIT": Rr = rot(Rr, w)
                last = x; continue
            if s == x:                                    # B1 passage: rotate, then X picks exit
                succ_x = Rr[j+2] if j + 2 < len(Rr) else None
                Rr = rot(Rr, w); cost += 1
                # now x is the endpoint; its predecessor in the new path:
                pred_x = Rr[-2]
                # orientation: X traversed from w (entry side) to the other neighbour (old successor)
                res, Qn, k = inner.visit(w, succ_x, "B1"); cost += k
                q = inner.nb_of[Qn[-1]]                   # exit neighbour
                Rr = rot(Rr, q); cost += 1; last = q; continue
            Rr = rot(Rr, w); last = w; cost += 1
    i = Q1.index(c); X1, X2 = list(Q1[:i+1]), list(Q1[i+1:][::-1]); pb = c; last = c; flips = 0
    if Q1[i+1] == x:                                      # the entry itself is a B1 passage of X
        succ_x = Q1[i+2]
        res, Qn, k = inner.visit(c, succ_x, "B1"); cost += k
        q = inner.nb_of[Qn[-1]]
        X1, X2, pb, flips, done, out = step_B3(P1, X1, X2, pb, flips, q, x)
        cost += 1; last = q
        if done: return out_B3(flips, X1, X2), out, cost, inner.QX
    while True:
        z = X2[-1]; pred = X2[-2] if len(X2) > 1 else None
        w = next(u for u in P1[z] if u != pred and u != last)
        if w == x:                                        # B3 passage
            p_, s_ = piece_neighbours(X1, X2, x)
            res, Qn, k = inner.visit(p_, s_, "B3"); cost += 1 + k
            if res == "TRANSMIT":
                X1, X2, pb, flips, done, out = step_B3(P1, X1, X2, pb, flips, w, x)
                if done: return out_B3(flips, X1, X2), out, cost, inner.QX
            last = x; continue
        s = succ_in_pieces(X1, X2, w)
        if s == x:                                        # B1 passage
            succ_x = succ_in_pieces(X1, X2, x)
            X1, X2, pb, flips, done, out = step_B3(P1, X1, X2, pb, flips, w, x); cost += 1
            assert not done
            res, Qn, k = inner.visit(w, succ_x, "B1"); cost += k
            q = inner.nb_of[Qn[-1]]
            X1, X2, pb, flips, done, out = step_B3(P1, X1, X2, pb, flips, q, x); cost += 1; last = q
            if done: return out_B3(flips, X1, X2), out, cost, inner.QX
            continue
        X1, X2, pb, flips, done, out = step_B3(P1, X1, X2, pb, flips, w, x); cost += 1; last = w
        if done: return out_B3(flips, X1, X2), out, cost, inner.QX

def piece_neighbours(X1, X2, v):
    for pc in (X1, X2):
        if v in pc:
            j = pc.index(v); return pc[j-1], pc[j+1]
    raise AssertionError

def succ_in_pieces(X1, X2, w):
    for pc in (X1, X2):
        if w in pc:
            j = pc.index(w); return pc[j+1] if j + 1 < len(pc) else "out"
    raise AssertionError

def step_B3(P1, X1, X2, pb, flips, w, x):
    """One rotation at the endpoint (end of X2) along w, in a B3 state.  Returns updated pieces and
    whether this was the exit (w == pb), with the final A-type path."""
    if w in X2:
        return X1, rot(X2, w), pb, flips, False, None
    if w == pb:
        return X1, X2, pb, flips, True, tuple(X1 + X2[::-1])
    j = X1.index(w); nX1 = X1[:j+1] + X2[::-1]; nX2 = X1[j+1:][::-1]
    return nX1, nX2, nX1[-1], flips + 1, False, None

def out_B3(flips, X1, X2):
    return "TRANSMIT" if flips % 2 else "REFLECT"
