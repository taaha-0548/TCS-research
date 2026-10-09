"""Phase 2 / P2.1: the line-mirror system.

Host H (cubic, Hamiltonian cycle C, start v0 = C[0]) with marked vertices M (each to be replaced by a
3-pole).  The host's walk is the line S_0 -> S_1 -> ... -> S_L.  A *site* of x in M is
  B1 site: a state S_i whose endpoint is x (entered by S_{i-1} -> S_i, left by S_i -> S_{i+1});
  B3 site: a step S_i -> S_{i+1} that attaches to x.
Traversed forwards (rightwards) or backwards (leftwards), a site presents a visit type
(oriented pair of x's neighbours -> port names, kind) to x's gadget.

Line-mirror system: a particle starts at position 0 moving right; at each site it hands the
gadget the visit type for its direction; TRANSMIT -> continue, REFLECT -> reverse; it stops at
either end.  `run_line_mirror` simulates this using the gadgets' transducer tables and returns
(end, steps); `real_walk` runs the actual lollipop walk on G = H[x <- X for x in M]."""
import sys
sys.path.insert(0, ".."); sys.path.insert(0, "../../../../../paper")

def host_line(adj, cyc):
    v0 = cyc[0]; path = list(cyc); last = v0; line = [tuple(path)]; moves = []
    pos = {v: i for i, v in enumerate(path)}
    while True:
        z, pred = path[-1], path[-2]
        w = next(u for u in adj[z] if u != pred and u != last)
        if w == v0: return line, moves
        i = pos[w]; s = path[i+1]; moves.append((z, w, s))
        path[i+1:] = path[i+1:][::-1]
        for j in range(i+1, len(path)): pos[path[j]] = j
        last = w; line.append(tuple(path))

def rotation_between(A, B):
    """(z, w, s) for the rotation A -> B (B = A[..w] + rev(A[s..z]))."""
    j = 0
    while A[j] == B[j]: j += 1
    w = A[j-1]; s = A[j]; z = A[-1]; return z, w, s

def site_types(adj, line, M, port_name):
    """For each step i (S_i -> S_{i+1}) list the passages through marked vertices, forwards and
    backwards.  port_name[x][u] = port name ('a','b','c') of X attached to neighbour u of x."""
    fwd, bwd = {}, {}
    for i in range(len(line) - 1):
        for (A, B, store) in ((line[i], line[i+1], fwd), (line[i+1], line[i], bwd)):
            z, w, s = rotation_between(A, B)
            for x in M:
                if s == x or w == x:
                    j = A.index(x); pr = port_name[x][A[j-1]] + port_name[x][A[j+1]]
                    store[i] = (x, pr, "B1" if s == x else "B3")
    return fwd, bwd

def run_line_mirror(line, fwd, bwd, tables, state0, max_events=10**7):
    """Abstract simulation on the line.  Positions are states 0..L; the particle sits on a state
    and moves to a neighbour.  A B1 passage of x on step i -> i+1 (endpoint becomes x at i+1) is
    resolved at state i+1: the gadget decides whether the walk continues to i+2 or returns to i.
    A B3 passage on step i -> i+1 is resolved on the step: TRANSMIT -> move, REFLECT -> stay at i
    and reverse direction.  Costs are added from the tables.  Returns (end, steps)."""
    L = len(line) - 1; st = dict(state0); pos, d, steps = 0, +1, 0
    global LAST_REFLECTIONS; LAST_REFLECTIONS = []
    while True:
        if pos == L and d == +1: return "far", steps
        if pos == 0 and d == -1: return "start", steps
        i = pos if d == +1 else pos - 1          # step index being traversed
        info = (fwd if d == +1 else bwd).get(i)
        if info is None:
            pos += d; steps += 1; continue
        x, pr, kind = info
        Q = st[x]; Qo = Q if (Q[0], Q[-1]) == pr_ports(tables[x], pr) else Q[::-1]
        res, Qn, cost = tables[x]["T"][(Qo, kind)]; st[x] = Qn
        if kind == "B3":
            steps += 1 + cost
            if res == "TRANSMIT": pos += d
            else: d = -d; LAST_REFLECTIONS.append(x)
        else:                                    # B1: entry step + cost + exit step
            steps += 2 + cost
            if res == "TRANSMIT": pos += 2 * d
            else: d = -d; LAST_REFLECTIONS.append(x)   # back where we came from
        if steps > max_events: raise RuntimeError

def pr_ports(tab, pr):
    return tab["port"][pr[0]], tab["port"][pr[1]]
