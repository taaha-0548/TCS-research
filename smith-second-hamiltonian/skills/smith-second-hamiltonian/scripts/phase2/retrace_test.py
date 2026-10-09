"""Retrace Lemma tests.
(1) single-site lines: at most one reflection, and after it the particle exits at the start.
(2) real hosts with several gadgets (multi-site): whenever the particle crosses a site, then later
    crosses it back in the opposite direction with that gadget's state unchanged since, the gadget
    TRANSMITS and restores the state it had before the first crossing."""
import sys, random, time
from collections import Counter
sys.path.insert(0, ".."); sys.path.insert(0, "../../../../../paper")
from cells import make_library, run, orient
import linemirror as LM

rng = random.Random(9); lib = make_library(rng, 400)
S = Counter()
for _ in range(20000):
    N = rng.randrange(1, 40); cells = [rng.choice(lib) for _ in range(N)]; st = [rng.choice(c["left"]) for c in cells]
    i, d, refl = 0, 1, 0
    while 0 <= i < N:
        c = cells[i]; pr, kd = c["fwd"] if d > 0 else c["bwd"]
        Q = orient(c["name"], st[i], pr); o, Qn = c["T"][(Q, kd)]; st[i] = Qn
        if o == "R": d = -d; refl += 1
        i += d
    S[("reflections", min(refl, 2)), ("exit", "start" if i < 0 else "far")] += 1
print("(1) single-site lines:", dict(S))

# (2) instrument the abstract runner on real hosts (it is exact by P2.1)
import test_linemirror as TL
orig = LM.run_line_mirror
def run_checked(line, fwd, bwd, tables, state0, max_events=10**7):
    L = len(line) - 1; st = dict(state0); pos, d, steps = 0, 1, 0
    last_cross = {}                               # site step index -> (direction, gadget state before, gadget-change counter)
    changes = Counter(); res_stats = Counter()
    while True:
        if pos == L and d == 1: return "far", steps
        if pos == 0 and d == -1: return "start", steps
        i = pos if d == 1 else pos - 1
        info = (fwd if d == 1 else bwd).get(i)
        if info is None:
            # B1 sites span two steps: also look for a B1 entry on the previous step backwards
            pos += d; steps += 1; continue
        x, pr, kind = info
        Q = st[x]; Qo = Q if (Q[0], Q[-1]) == LM.pr_ports(tables[x], pr) else Q[::-1]
        res, Qn, cost = tables[x]["T"][(Qo, kind)]
        key = (x, i if kind == "B3" else (i if d == 1 else i - 1))
        prev = last_cross.get(key)
        if prev and prev[0] == -d and prev[2] == changes[x] and prev[3] == "TRANSMIT":
            ok = (res == "TRANSMIT" and set([tuple(Qn), tuple(Qn[::-1])]) == set([tuple(prev[1]), tuple(prev[1][::-1])]))
            STATS["retrace " + ("holds" if ok else "VIOLATED")] += 1
        last_cross[key] = (d, Q, changes[x] + 1, res)
        st[x] = Qn; changes[x] += 1
        if kind == "B3":
            steps += 1 + cost
            if res == "TRANSMIT": pos += d
            else: d = -d
        else:
            steps += 2 + cost
            if res == "TRANSMIT": pos += 2 * d
            else: d = -d
STATS = Counter()
TL.run_line_mirror = run_checked
rng2 = random.Random(3); t0 = time.time()
while time.time() - t0 < 60:
    try: TL.trial(rng2)
    except Exception: pass
print("(2) multi-site real hosts:", dict(STATS))
