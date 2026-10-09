"""E19: transducer table of the pole P_k = G_k - r at each level of the nested K=8 family.
With exactly 3 Ham cycles, P_k has one Ham path per port pair, so 6 oriented states.
Prints the outcome pattern (T/R + successor state) and the cost vector per level."""
import sys, json
from general import from_chord, lollipop_g, cyc_edges
from nested_fast import next_level, rotate_to
from transducer import visit_B1, visit_B3
sys.setrecursionlimit(10000)
CH = [4, 3, 6, 1, 0, 7, 2, 5]; X, R, PERM = 5, 2, (2, 0, 1)
L = int(sys.argv[1]) if len(sys.argv) > 1 else 8

def all_cycles(G, c0):
    pool = [tuple(c0)]; seen = {frozenset(cyc_edges(c0))}; i = 0
    while i < len(pool):
        c = list(pool[i]); i += 1
        for v in c[:6] + [c[len(c)//2]]:
            for d in (1, -1):
                _, out, _ = lollipop_g(G, rotate_to(c, v, d), max_steps=10**8)
                k = frozenset(cyc_edges(out))
                if k not in seen: seen.add(k); pool.append(tuple(out))
        if len(pool) >= 3 and i >= 3: break
    return [list(c) for c in pool]

def main():
  K = from_chord(8, CH); Kc = list(range(8)); G, Gc = K, Kc; rl = R; rows = []
  for lev in range(L + 1):
      cycles = all_cycles(G, Gc)
      keep = [v for v in range(len(G)) if v != rl]; idx = {v: j for j, v in enumerate(keep)}
      P = [[idx[w] for w in G[v] if w != rl] for v in keep]
      portsG = list(G[rl]); ports = [idx[p] for p in portsG]; name = {p: "abc"[k] for k, p in enumerate(ports)}
      states = []
      for c in cycles:
          c = rotate_to(c, rl, 1); hp = [idx[v] for v in c[1:]]
          states += [tuple(hp), tuple(hp[::-1])]
      def nm(Q): return name[Q[0]] + name[Q[-1]]
      table = {}
      for Q in sorted(states, key=nm):
          for kind, fn in (("B1", visit_B1), ("B3", visit_B3)):
              res, Qn, cost = fn(P, ports, Q)
              table[(nm(Q), kind)] = (res[0], nm(Qn), cost)
      pattern = tuple((k, v[0], v[1]) for k, v in sorted(table.items()))
      costs = [v[2] for k, v in sorted(table.items())]
      rows.append(dict(level=lev, n=len(G), ncycles=len(cycles), pattern=pattern, costs=costs))
      print(f"level {lev} n={len(G)} cycles={len(cycles)}  costs={costs}", flush=True)
      if lev == 0 or pattern != rows[-2]["pattern"]:
          print("   pattern:", " ".join(f"{q}/{t}:{o}>{s}" for (q, t), o, s in pattern))
      else:
          print("   pattern: same as previous level")
      if lev == L: break
      G, Gc = next_level(K, Kc, X, G, [Gc], rl, PERM); rl = R if R < X else R - 1
  json.dump(rows, open(f"e19_level_tables_L{L}.json", "w"), default=str, indent=1)


if __name__ == "__main__":
    main()
