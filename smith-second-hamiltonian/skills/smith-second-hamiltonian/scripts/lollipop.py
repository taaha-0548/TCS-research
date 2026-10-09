"""Thomason's lollipop algorithm for Smith's problem, plus tools for experiments.

A cubic Hamiltonian graph with a known Hamiltonian cycle is represented, without loss of
generality, with vertices 0..n-1, the cycle 0-1-...-(n-1)-0, and a perfect matching of
chords ("chord[v]" is v's third neighbour).  Every Hamiltonian cubic graph with a marked
Hamiltonian cycle has exactly this form, up to relabelling.

Main entry points
  lollipop(n, chord, v0=0, dirn=+1) -> (steps, second_cycle)
  is_ham_cycle(n, chord, cycle)     -> bool  (independent verifier)
  random_instance(n, rng)           -> chord
  all_instances(n)                  -> generator over all labelled chord matchings
Run `python3 lollipop.py` for the self-test.
"""
import random


def neighbors(n, chord, v):
    return ((v - 1) % n, (v + 1) % n, chord[v])


def valid_chord(n, chord):
    """Simple cubic graph: chord is a fixed-point-free involution avoiding cycle edges."""
    for v in range(n):
        u = chord[v]
        if u is None or u == v or chord[u] != v or u in ((v - 1) % n, (v + 1) % n):
            return False
    return True


def lollipop(n, chord, v0=0, dirn=+1, max_steps=None):
    """Run Thomason's lollipop algorithm.

    Fixed vertex v0 and fixed first edge (v0, v0+dirn).  The start path is the given
    cycle with the edge (z, v0) removed, where z = v0 - dirn.  Each step adds the unique
    edge at the current endpoint that is neither on the path nor the edge just deleted,
    forming a lollipop, then deletes the cycle edge at the attachment vertex that leads
    toward the old endpoint.  It stops when the added edge goes to v0, closing a
    Hamiltonian cycle.

    Returns (steps, cycle): the number of lollipop rotations and the vertex sequence of
    the second Hamiltonian cycle (starting at v0, first edge to v0+dirn).
    """
    path = [(v0 + dirn * i) % n for i in range(n)]
    pos = {v: i for i, v in enumerate(path)}
    forbidden = v0  # the endpoint's "just deleted" neighbour
    steps = 0
    while True:
        z = path[-1]
        prev = path[-2]
        cands = [w for w in neighbors(n, chord, z) if w != prev and w != forbidden]
        assert len(cands) == 1, (z, cands)  # exactly one in a simple cubic graph
        w = cands[0]
        if w == v0:
            return steps, path[:]
        i = pos[w]
        tail = path[i + 1:]
        tail.reverse()
        path[i + 1:] = tail
        for j in range(i + 1, n):
            pos[path[j]] = j
        forbidden = w
        steps += 1
        if max_steps is not None and steps > max_steps:
            return None, None


def edges_of_cycle(cycle):
    m = len(cycle)
    return {frozenset((cycle[i], cycle[(i + 1) % m])) for i in range(m)}


def base_cycle_edges(n):
    return {frozenset((i, (i + 1) % n)) for i in range(n)}


def is_ham_cycle(n, chord, cycle):
    if sorted(cycle) != list(range(n)):
        return False
    return all(cycle[(i + 1) % n] in neighbors(n, chord, cycle[i]) for i in range(n))


def random_instance(n, rng):
    """Uniformly random chord matching avoiding cycle edges (rejection sampling)."""
    assert n % 2 == 0 and n >= 4
    while True:
        perm = list(range(n))
        rng.shuffle(perm)
        chord = [None] * n
        ok = True
        for k in range(0, n, 2):
            a, b = perm[k], perm[k + 1]
            if (a - b) % n in (1, n - 1):
                ok = False
                break
            chord[a], chord[b] = b, a
        if ok:
            return chord


def all_instances(n):
    """All labelled chord matchings of the n-cycle."""
    def rec(chord, free):
        if not free:
            yield chord[:]
            return
        a = free[0]
        for b in free[1:]:
            if (a - b) % n in (1, n - 1):
                continue
            chord[a], chord[b] = b, a
            rest = [x for x in free if x != a and x != b]
            yield from rec(chord, rest)
            chord[a] = chord[b] = None
    yield from rec([None] * n, list(range(n)))


def count_ham_cycles_through(n, chord, a, b):
    """Brute-force count of Hamiltonian cycles through edge {a,b} (small n only)."""
    count = 0
    visited = [False] * n
    visited[a] = visited[b] = True

    def dfs(v, depth):
        nonlocal count
        if depth == n:
            if a in neighbors(n, chord, v):
                count += 1
            return
        for w in neighbors(n, chord, v):
            if not visited[w]:
                visited[w] = True
                dfs(w, depth + 1)
                visited[w] = False
    dfs(b, 2)
    return count


if __name__ == "__main__":
    rng = random.Random(1)
    for n in range(6, 41, 2):
        for _ in range(200):
            ch = random_instance(n, rng)
            assert valid_chord(n, ch)
            for v0 in (0, 3 % n):
                for d in (1, -1):
                    s, cyc = lollipop(n, ch, v0, d)
                    assert is_ham_cycle(n, ch, cyc), "not Hamiltonian"
                    assert edges_of_cycle(cyc) != base_cycle_edges(n), "same cycle"
                    assert frozenset((v0, (v0 + d) % n)) in edges_of_cycle(cyc), "fixed edge lost"
    # Smith's theorem sanity check: even number of Hamiltonian cycles through each edge.
    for _ in range(50):
        n = rng.choice([8, 10, 12])
        ch = random_instance(n, rng)
        for v in range(n):
            for w in neighbors(n, ch, v):
                assert count_ham_cycles_through(n, ch, v, w) % 2 == 0
    print("self-test passed")
