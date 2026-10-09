"""Composition Lemma tests (session 3).

Claim (Composition Lemma).  Let P be a 3-pole and X a 3-pole inside P whose cut edges lie
inside P.  Suppose X is TRANSPARENT-SIMPLE: one Ham path per port pair and every visit TRANSMITs.
Then for every host, the walk on H[x<-P] is the walk on H[x<-P/X] with each passage through the
contracted vertex x stretched by X's visit cost; hence P has the same outcome table as P/X and
    c_P = c_{P/X} + M c_X,
where M[e][f] = number of passages of kind f through x during a visit of kind e to P/X.

For the nested family P_{k+1}/P_k = K - r = P_0, so M and the table come from the 7-vertex P_0.

This file computes M directly from P/X (tiny), with explicit move logs."""
from collections import Counter
from transducer import rot

def visit_moves(P, ports, Q, kind):
    """Replay a visit on pole P and log every move as (pieces_before, z, w, s, new_endpoint).
    pieces_before: tuple of path pieces inside P in path order (1 piece for B1/A, 2 for B3).
    The ENTRY move is logged first: B1 entry deletes the entry cut edge at Q[0];
    B3 entry adds the cut edge at the third port c."""
    a, b = Q[0], Q[-1]; c = [p for p in ports if p not in (a, b)][0]; log = []
    if kind == "B1":
        log.append(((tuple(Q),), "OUT", "OUT", a, a))          # deletes q_in - a; endpoint a
        Rr = list(Q[::-1]); forb = ("cut", a)
        while True:
            z = Rr[-1]; prev = Rr[-2] if len(Rr) > 1 else ("cut", b)
            cands = [w for w in P[z] if w != prev and w != forb]
            if z in ports and z != b: cands.append(("cut", z))
            w = [u for u in cands if u != forb and u != prev][0]
            if isinstance(w, tuple):
                log.append(((tuple(Rr),), z, "OUT", "OUT", "OUT")); return log
            i = Rr.index(w); s = Rr[i+1]
            log.append(((tuple(Rr),), z, w, s, s)); Rr = rot(Rr, w); forb = w
    i = Q.index(c); s0 = Q[i+1]
    log.append(((tuple(Q),), "OUT", c, s0, s0))                # adds q_c - c, deletes c - s0
    X1 = list(Q[:i+1]); X2 = list(Q[i+1:][::-1]); pb = c; forb = c
    while True:
        z = X2[-1]; prev = X2[-2] if len(X2) > 1 else None
        w = [u for u in P[z] if u != prev and u != forb][0]
        if w in X2:
            j = X2.index(w); s = X2[j+1]; log.append(((tuple(X1), tuple(X2)), z, w, s, s)); X2 = rot(X2, w)
        elif w == pb:
            log.append(((tuple(X1), tuple(X2)), z, w, "OUT", "OUT")); return log
        else:
            j = X1.index(w); s = X1[j+1]
            log.append(((tuple(X1), tuple(X2)), z, w, s, s))
            nX1 = X1[:j+1] + X2[::-1]; nX2 = X1[j+1:][::-1]; pb = nX1[-1]; X1, X2 = nX1, nX2
        forb = w

def passages_through_vertex(log, x, xname):
    """Passages through single vertex x: kind B1 when a move makes x the endpoint by deleting
    x's entry edge (s == x); kind B3 when a move attaches to x (w == x).  The passage's state is
    the oriented pair (port name of x's predecessor, of x's successor) in the path before the move.
    xname maps x's neighbours (in P) to the inner pole's port names."""
    out = Counter()
    for pieces, z, w, s, newend in log:
        seq = [v for pc in pieces for v in pc]
        if s == x or w == x:
            for pc in pieces:
                if x in pc:
                    j = pc.index(x); pred, succ = pc[j-1], pc[j+1]
            out[(xname[pred] + xname[succ], "B1" if s == x else "B3")] += 1
    return out
