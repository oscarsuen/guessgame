import json
from functools import cache


def vr(p):
    if sum(p) == 0:
        return 0
    # return 1 + min(
    #     (lts := sum(p[:k])) * vr([q/lts for q in p[:k]]) +
    #     (gts := sum(p[k+1:])) * vr([q/gts for q in p[k+1:]])
    #     for k in range(len(p))
    # )
    return 1 + min(
        sum(p[:k]) * vr(p[:k]) + sum(p[k+1:]) * vr(p[k+1:])
        for k in range(len(p))
    )/sum(p)


def tree(p, ki=None):
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
    def rec(i, j):
        if s(i, j) == 0:
            return
        ks = min(range(i, j), key=lambda k:
            s(i, k) * w(i, k) + s(k+1, j) * w(k+1, j))
        return (ks, rec(i, ks), rec(ks+1, j))
    # return rec(0, len(p))
    return rec(0, len(p)) if ki is None else (ki, rec(0, ki), rec(ki+1, len(p)))


def to_latex(d):
    p_str = ", ".join(f"\\frac{{{n}}}{{{d['p_den']}}}" for n in d['p_nums'])
    return f"${d['N']}$ | $\\frac{{{d['v_num']}}}{{{d['v_den']}}}\\approx{d['v_num']/d['v_den']:.3f}$ | $[{p_str}]$"


def gen_df(f, ns, filename=None, **kwargs):
    df = [f(n, **kwargs) for n in ns]
    df = [row for row in df if row is not None]
    if filename is not None:
        with open(filename, 'w') as f:
            json.dump(df, f, indent=4)
    return df


def get_sol(filename, N):
    with open(filename, 'r') as f:
        df = json.load(f)
    try:
        return next(d for d in df if d['N'] == N)
    except StopIteration:
        return
