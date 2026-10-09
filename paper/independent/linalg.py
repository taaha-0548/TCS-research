import sympy as sp
from fractions import Fraction as F
T = ['ab/B1','ab/B3','ac/B1','ac/B3','ba/B1','ba/B3','bc/B1','bc/B3','ca/B1','ca/B3','cb/B1','cb/B3']
c0 = [3,10,5,10,3,10,5,10,3,6,3,6]
Mrows = """0 0 0 0 0 0 0 0 0 1 0 0
1 0 1 1 0 0 1 1 0 0 0 0
0 1 1 0 0 0 0 0 0 0 0 0
0 1 1 0 0 1 1 0 0 0 1 0
0 0 0 0 0 0 0 0 1 0 0 0
0 1 1 0 0 0 0 0 0 1 1 0
0 0 0 1 0 0 1 0 0 0 0 0
1 0 0 1 0 0 1 0 0 0 0 1
0 0 0 0 1 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 1
0 0 0 1 0 0 1 0 0 0 0 0"""
M = [list(map(int, r.split())) for r in Mrows.split('\n')]
# consistency of M rows with Table 2 passage lists
tab2 = {'ab/B1':(3,'ca/B3'),'ab/B3':(10,'ab/B1, ac/B1, ac/B3, bc/B1, bc/B3'),'ac/B1':(5,'ab/B3, ac/B1'),
'ac/B3':(10,'ab/B3, ac/B1, ba/B3, bc/B1, cb/B1'),'ba/B1':(3,'ca/B1'),'ba/B3':(10,'ab/B3, ac/B1, ca/B3, cb/B1'),
'bc/B1':(5,'ac/B3, bc/B1'),'bc/B3':(10,'ab/B1, ac/B3, bc/B1, cb/B3'),'ca/B1':(3,'ba/B1'),'ca/B3':(6,'ab/B3, ac/B1'),
'cb/B1':(3,'cb/B3'),'cb/B3':(6,'ac/B3, bc/B1')}
for i,t in enumerate(T):
    cost, ps = tab2[t]
    row = [0]*12
    for p in ps.split(', '): row[T.index(p)] += 1
    assert row == M[i], (t, row, M[i]); assert cost == c0[i]
print('M and c0 agree with Table 2')
Ms = sp.Matrix(M); lam = sp.symbols('lam')
cp = Ms.charpoly(lam).as_expr()
claimed = lam**2*(lam-1)**2*(lam+1)**2*(lam**2+1)*(lam**4-2*lam**3-2*lam**2-2*lam-1)
print('charpoly:', sp.factor(cp))
print('charpoly == claimed:', sp.expand(cp - claimed) == 0)
q = sp.Poly(lam**4-2*lam**3-2*lam**2-2*lam-1, lam)
print('quartic irreducible over Q:', q.is_irreducible, sp.factor_list(q.as_expr()))
roots = []
for fac, mult in sp.factor_list(cp)[1]:
    roots += list(sp.Poly(fac, lam).nroots(n=30)) * mult
assert len(roots) == 12
mods = sorted([abs(complex(r)) for r in roots], reverse=True)
print('eigenvalue moduli:', [f'{m:.6f}' for m in mods])
rho = max(r for r in sp.real_roots(q))
rv = sp.N(rho, 25)
print('rho =', rv, ' rho^(1/6) =', sp.N(rho**sp.Rational(1,6), 15), ' 2nd largest modulus', mods[1])
# recursion
c = c0[:]; steps = {1: 4 + c0[T.index('ca/B3')]}
for k in range(2, 16):
    c = [c0[i] + sum(M[i][j]*c[j] for j in range(12)) for i in range(12)]
    steps[k] = 4 + c[T.index('ca/B3')]
print('recursion steps:', steps)
# reachable set
start = T.index('ca/B3'); R = {start}; stack=[start]
while stack:
    i = stack.pop()
    for j in range(12):
        if M[i][j] and j not in R: R.add(j); stack.append(j)
print('R complement:', [T[i] for i in range(12) if i not in R])
Rl = sorted(R)
u = {'ab/B1':77,'ab/B3':442,'ac/B1':227,'ac/B3':442,'ba/B3':330,'bc/B1':227,'bc/B3':330,'ca/B3':227,'cb/B1':77,'cb/B3':227}
assert set(u) == {T[i] for i in Rl}
assert all(M[i][j] == 0 for i in Rl for j in range(12) if j not in R)
def check(uvec, ratio):
    worst = None
    for i in Rl:
        lhs = sum(M[i][j]*uvec[T[j]] for j in Rl)
        r = F(lhs) / F(uvec[T[i]])
        worst = r if worst is None or r < worst else worst
    return worst >= ratio, worst
ok, worst = check(u, F(2947,1000)); print('Table 3 u: M_R u >= 2.947 u:', ok, 'min ratio', worst, float(worst))
ok2, _ = check(u, F(29477,10000)); print('Table 3 u: M_R u >= 2.9477 u:', ok2)
# Perron eigenvector on R
MR = sp.Matrix([[M[i][j] for j in Rl] for i in Rl])
print('rho(M_R) charpoly factor:', sp.factor(MR.charpoly(lam).as_expr()))
ev = (MR - rv*sp.eye(len(Rl))).nullspace(simplify=False) if False else None
import mpmath
mpmath.mp.dps = 40
A = mpmath.matrix([[M[i][j] for j in Rl] for i in Rl])
E, V = mpmath.eig(A)
idx = max(range(len(E)), key=lambda t: mpmath.re(E[t]))
v = [mpmath.re(V[t, idx]) for t in range(len(Rl))]
s = sum(v); v = [x/s for x in v]
print('Perron eigval', mpmath.nstr(E[idx], 20), 'vector', [mpmath.nstr(x, 8) for x in v])
for scale in [10**3, 10**4, 10**5, 10**6]:
    w = {T[Rl[t]]: int(mpmath.nint(v[t]*scale)) for t in range(len(Rl))}
    ok3, worst3 = check(w, F(29477,10000))
    print(f'rounded Perron (scale {scale}):', w, 'certifies 2.9477:', ok3, 'min ratio', float(worst3))
    if ok3: break
for scale in [10**7, 10**8, 10**9, 10**10, 10**12]:
    w = {T[Rl[t]]: int(mpmath.nint(v[t]*scale)) for t in range(len(Rl))}
    ok3, worst3 = check(w, F(29477,10000))
    print(f'rounded Perron (scale {scale}):', w, 'certifies 2.9477:', ok3, 'min ratio', mpmath.nstr(mpmath.mpf(worst3.numerator)/worst3.denominator, 12))
    if ok3: print('CERTIFICATE', w); break
import networkx as nx
D = nx.DiGraph([(T[i],T[j]) for i in Rl for j in Rl if M[i][j]])
print('M_R strongly connected:', nx.is_strongly_connected(D), 'nodes', D.number_of_nodes())
print('min c0/u on R:', min(F(c0[i], u[T[i]]) for i in Rl))
