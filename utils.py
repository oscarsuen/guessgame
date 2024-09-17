import json


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
