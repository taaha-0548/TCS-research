"""P3.1 survey: for random gadgets P' with a slot x (x not a port), classify the cell procedures.
Metrics per P':  memory = max number of local states (P'-paths) on one port pair;
  calls = max number of calls in one visit;  answer-sensitive = the outcome or the new local state
  depends on the child's answers;  branching = different answers lead to different later calls."""
import sys, random, itertools, time, json
from collections import Counter
sys.path.insert(0, "../phase1"); sys.path.insert(0, ".."); sys.path.insert(0, "../../../../../paper")
import verify as V
from lollipop import random_instance
from procedure import procedure
def chord_adj(n, ch): return [[(v - 1) % n, (v + 1) % n, ch[v]] for v in range(n)]

def analyse(P1, ports1, x, perm):
    xname = {u: "abc"[perm[j]] for j, u in enumerate(P1[x])}
    name = {p: "abc"[i] for i, p in enumerate(ports1)}
    states = []
    for s, t in itertools.permutations(ports1, 2): states += V.ham_paths(P1, s, t)
    if not states: return None
    perpair = Counter(frozenset((name[Q[0]], name[Q[-1]])) for Q in states)
    memory = max(perpair.values()) // 2 if perpair else 0
    maxcalls = 0; sensitive = False; branching = False
    for Q in states:
        for kd in ("B1", "B3"):
            pr = procedure(P1, ports1, x, xname, Q, kd)
            if not pr: continue
            maxcalls = max(maxcalls, max(len(c) for _, c, _, _ in pr))
            results = {(o, f) for _, _, o, f in pr}
            if len(results) > 1: sensitive = True
            # branching: two answer sequences sharing a prefix lead to different next calls
            # branching: after the same earlier answers, the answer to call i changes what happens
            # next (the next call, or the end of the visit)
            nxt = {}
            for ans, calls, o, f in pr:
                for i in range(len(ans)):
                    key = (ans[:i], ans[i])
                    nxt.setdefault(ans[:i], {}).setdefault(ans[i], set()).add(calls[i+1] if i + 1 < len(calls) else ("end", o, f))
            for pre, d in nxt.items():
                if "T" in d and "R" in d and d["T"] != d["R"]: branching = True
    return dict(memory=memory, calls=maxcalls, sensitive=sensitive, branching=branching, n=len(P1))

if __name__ == "__main__":
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1); t0 = time.time(); S = Counter(); best = []
    while time.time() - t0 < float(sys.argv[2] if len(sys.argv) > 2 else 100):
        n = rng.choice([8, 10, 12, 14]); K = chord_adj(n, random_instance(n, rng)); r = rng.randrange(n)
        P1, ports1, _ = V.pole(K, r)
        cand = [v for v in range(len(P1)) if v not in ports1]
        if not cand: continue
        x = rng.choice(cand); perm = list(range(3)); rng.shuffle(perm)
        a = analyse(P1, ports1, x, perm)
        if a is None: continue
        S[(a["n"], "mem>1" if a["memory"] > 1 else "mem=1", "sensitive" if a["sensitive"] else "-", "branching" if a["branching"] else "-")] += 1
        if a["memory"] > 1 and a["sensitive"] and a["branching"]: best.append(dict(K=K, r=r, x=x, perm=perm, **a))
    for k, v in sorted(S.items()): print(k, v)
    json.dump(best[:50], open("p31_rich.json", "w"))
    print("rich gadgets (memory>1, answer-sensitive, branching):", len(best))
