from utils import *
from z3 import *
from math import lcm

set_param("parallel.enable", True)


def zmin(gen):
    # m = next(gen)
    # for v in gen:
    #     # m = If(m <= v, m, v)
    #     m = If(v < m, v, m)
    # # return simplify(m)
    # return m
    def zminl(lst):
        n = len(lst)
        if n == 1:
            return lst[0]
        m1 = zminl(lst[:n//2])
        m2 = zminl(lst[n//2:])
        return If(m1 < m2, m1, m2)
    # return zminl(list(gen))
    return simplify(zminl(list(gen)))


def v(p):
    if not p:
        return RealVal(0)
    if len(p) == 1:
        return RealVal(1)
    rtn = RealVal(1) + zmin(
        Sum(p[:k]) * v(p[:k]) + Sum(p[k+1:]) * v(p[k+1:])
        for k in range(len(p))
    )/Sum(p)
    # rtn = 1 + zmin(
    #     (lts := Sum(p[:k])) * v([pi/lts for pi in p[:k]]) +
    #     (gts := Sum(p[k+1:])) * v([pi/gts for pi in p[k+1:]])
    #     for k in range(len(p))
    # )
    return simplify(rtn)


def problem(N, full=False, uv=False, filename=None, **kwargs):
    s = Solver()
    pvar = RealVector('p', N)
    ueq = Real('u')
    if uv:
        vvar = [[Real(f"v__{i}__{j}") for j in range(i, N+1)] for i in range(N+1)]
        def getv(i, j):
            return vvar[i][j-i]
        uvar = [[[Real(f"u__{i}__{j}__{k}") for k in range(i, j)] for j in range(i, N+1)] for i in range(N+1)]
        def getu(i, j, k):
            return uvar[i][j-i][k-i]

    for pi in pvar:
        if full or N == 1:
            s.add(pi >= 0)
        else:
            s.add(pi > 0)
            s.add(pi < 1)
    s.add(Sum(pvar) == 1)

    if not full:
        for i in range(N//2):
            s.add(pvar[i] == pvar[-i-1])

    if not full:
        for i in range(1, (N+1)//2):
            s.add(pvar[i-1] > pvar[i])

    if uv:
        for i in range(N+1):
            for j in range(i, N+1):
                for k in range(i, j):
                    s.add(getu(i, j, k) == 1 + (Sum(pvar[i:k])*getv(i,k)+Sum(pvar[k+1:j])*getv(k+1,j))/Sum(pvar[i:j]))

        for i in range(N+1):
            for j in range(i, N+1):
                if i == j:
                    s.add(getv(i, j) == 0)
                    continue
                s.add(Or(*(getv(i, j) == getu(i, j, k) for k in range(i, j))))
                s.add(And(*(getv(i, j) <= getu(i, j, k) for k in range(i, j))))
                # for k in range(i, j):
                #     s.add(getv(i, j) <= getu(i, j, k))

    for k in range(N if full else (N+1)//2):
        if uv:
            s.add(getu(0, N, k) == ueq)
        else:
            uk = RealVal(1) + Sum(pvar[:k]) * v(pvar[:k]) + Sum(pvar[k+1:]) * v(pvar[k+1:])
            uk = simplify(uk)
            s.add(uk == ueq)

    if filename is not None:
        with open(filename, 'w') as f:
            f.write(s.sexpr())
            f.write("(check-sat)\n")
            f.write("(get-model)\n")
    return s


def solution(m, printing=True, **kwargs):
    json_d = {}
    N = len([n for d in m.decls() if (n := d.name()).startswith("p__") and n[3:].isdigit()])
    json_d['N'] = N
    p = RealVector('p', N)
    u = Real('u')
    pr = [m[pi].as_fraction() for pi in p]
    d = lcm(*(pi.denominator for pi in pr))
    ns = [pi.numerator*round(d/pi.denominator) for pi in pr]
    json_d['p_nums'] = ns
    json_d['p_den'] = d
    if printing:
        print(f"p = {ns}/{d}")
    ur = m[u].as_fraction()
    if printing:
        print(f"v = {ur}")
    assert ur == vr(pr)
    json_d['v_num'] = ur.numerator
    json_d['v_den'] = ur.denominator
    return json_d


def solveprob(N, printing=True, **kwargs):
    if printing:
        print(f"N = {N}")
    prob = problem(N, **kwargs)
    if printing:
        print("problem generated")
        # print(s)
    check = prob.check()
    if printing:
        print("problem solved")
    if check != CheckSatResult(True):
        if printing:
            print("UNSAT")
        return
    model = prob.model()
    # if printing:
    #     print(model)
    return solution(model, printing=printing, **kwargs)
