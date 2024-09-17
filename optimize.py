from utils import *
from fractions import Fraction
from math import lcm, floor
from functools import cache
import json
import numpy as np
from scipy.special import logit, expit
from scipy.optimize import minimize

rng = np.random.default_rng()


def mirror(p, n):
    assert (n+1)//2 == len(p) or n == len(p)
    return p if n == len(p) else np.concatenate((p, p[n-len(p)-1::-1]))


def v(p, n, u=False):
    p = np.array(p)
    p = mirror(p, n)
    @cache
    def s(i, j):
        return sum(p[i:j])
    @cache
    def w(i, j):
        # if i == j:
        if (t := s(i, j)) == 0:
            return 0
        return 1 + min(
            s(i, k) * w(i, k) + s(k+1, j) * w(k+1, j)
            for k in range(i, j)
        )/t
    return (1 + s(0, k)*w(0, k) + s(k+1, n)*w(k+1, n) for k in range(n)) if u else w(0, n)


def optim(N, full=False, decr=True, tol=1e-10, randinit=0, **kwargs):
    def fun(x):
        p = x[:-1]
        u = x[-1]
        rtn = sum((uk-u)**2 for uk in v(p, N, u=True))
        return rtn
    n = N if full else (N+1)//2
    if full or N < 7:
        p0 = tuple(1/N for _ in range(n))
    else:
        p0 = (0.32, 0.08) + tuple(0.8/(N-4) for _ in range(n-2))
    p0 = np.array(p0)
    p0 = expit(rng.normal(loc=logit(p0), scale=randinit))
    u0 = v(p0, N)
    x0 = np.append(p0, u0)
    cons = [{'type': 'ineq', 'fun': lambda x: x[i]} for i in range(n)]
    if full:
        sumf = lambda x: sum(x[:-1]) - 1
    else:
        sumf = lambda x: 2*sum(x[:-1]) - (N%2)*x[-2] - 1
    cons.append({'type': 'eq', 'fun': sumf})
    if decr:
        cons.extend({'type': 'ineq', 'fun': lambda x: x[i]-x[i+1]} for i in range(n-1))
    return minimize(fun, x0, constraints=cons, tol=tol, options=kwargs)


def fractionalize(p, denom=500, frac_tol=5e-3, **kwargs):
    p = np.array(p)
    frac_tol = frac_tol * len(p)
    # fracs = [Fraction(pi).limit_denominator(denom) for pi in p]
    # d_lcm = lcm(*(f.denominator for f in fracs))
    # d_max = max(*(f.denominator for f in fracs))
    # if d_lcm != d_max:
    #     return None
    # return fracs
    fracs_min = None
    err_min = None
    for d in range(floor(1/min(p)), denom):
        ns = p*d
        err = sum(np.abs(ns-np.round(ns))) #/d
        if err_min is None or err < err_min:
            ns = [round(n) for n in np.round(ns)]
            if sum(ns) == d:
                fracs_min = ns, d
                err_min = err
                if err_min < frac_tol:
                    break
    return None if fracs_min is None else [Fraction(n, fracs_min[1]) for n in fracs_min[0]]


def solution(m, N, printing=True, **kwargs):
    json_d = {}
    json_d['N'] = N
    ps = m.x[:-1]
    us = m.x[-1]
    assert (N+1)//2 == len(ps) or N == len(ps)
    if N > len(ps):
        ps = np.concatenate((ps,ps[N-len(ps)-1::-1]))

    fracs = fractionalize(ps, **kwargs)
    if fracs is None:
        return
    un = list(v(fracs, N, u=True))
    uf = min(un)
    vf = vr(fracs)
    d_lcm = lcm(*(f.denominator for f in fracs))
    if uf != vf or any(uk != uf for uk in un):
        if printing:
            print("fractional sol unsat")
            print(ps*d_lcm)
            print(f"un = {un}")
            print(f"uf = {uf}")
            print(f"vf = {vf}")
        return

    ns = [pi.numerator*round(d_lcm/pi.denominator) for pi in fracs]
    json_d['p_nums'] = ns
    json_d['p_den'] = d_lcm
    if printing:
        print(f"p = {ns}/{d_lcm}")
        print(f"v = {vf}")
    json_d['v_num'] = vf.numerator
    json_d['v_den'] = vf.denominator
    return json_d


kwargs = {"denom": 5000,
          "randinit": 0.1,
          "tol": 1e-15,
          "maxiter": 500}


def exact(N, maxtries=3, printing=True, **kwargs):
    def get():
        if printing:
            print(f"N = {N}")
        m = optim(N, **kwargs)
        if printing:
            print("Optimization done")
            # print(m)
        if not m.success:
            if printing:
                print("Minimization failed")
            return
        sol = solution(m, N, printing=printing, **kwargs)
        if printing:
            print(sol)
        return sol
    for _ in range(maxtries):
        rtn = get()
        if rtn:
            break
    return rtn


def approx(N, maxtries=3, printing=True, **kwargs):
    def get():
        json_d = {}
        json_d['N'] = N
        if printing:
            print(f"N = {N}")
        m = optim(N, **kwargs)
        json_d['success'] = bool(m.success)
        if printing:
            print("success" if m.success else "failure")
        p = m.x[:-1]
        p = mirror(p, N)
        json_d['p'] = p.tolist()
        u = m.x[-1]
        w = vr(p)
        json_d['u'] = u
        json_d['v'] = w
        if printing:
            print(f"p = {p}")
            print(f"u = {u}")
            print(f"v = {w}")
        return json_d
    for _ in range(maxtries):
        rtn = get()
        if rtn['success']:
            break
    return rtn
