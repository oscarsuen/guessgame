# Guessing Game Problem

_Inspired by (stolen from) an interview question posed by Steve Ballmer found on [John Graham-Cumming's blog](https://blog.jgc.org/2024/09/steve-ballmers-binary-search-interview.html) and [HackerNews](https://news.ycombinator.com/item?id=41434637)._

## Problem
Let there by two players, a _Picker_ and a _Guesser_.  The _Picker_ chooses a number between $1$ and $N$ (inclusive).  The _Guesser_ then pays the _Picker_ \$1 to guess a number.  The _Picker_ then responds with either "Correct", "Lower", or "Higher".  This repeats, with the _Guesser_ paying \$1 per guess and the _Picker_ responding, until the _Guesser_ finds the number.  How much should the _Picker_ pay the _Guesser_ for her to choose to play this game?

## Analysis
Given a probability vector $p$ of length $n$, if the _Guesser_ chooses $k$, the expected number of guesses is

$$
U_n^k(p) =
    \left( \sum_{i\lt k} p_i \right) V_{k-1} \left( \left[ \frac{p_j}{\sum_{i\lt k} p_i} \middle| j\lt k \right] \right) +
    p_k +
    \left( \sum_{i\gt k} p_i \right) V_{n-k} \left( \left[ \frac{p_j}{\sum_{i\gt k} p_i} \middle| j\gt k \right] \right)
$$

where $V_n$ is the optimal choice

$$V_n(p) = \min_{1\leq k\leq n} U_n^k(p)$$

The _Guesser_ cannot credibly deviate from the optimal choices after the first guess, so her strategy is some distribution $q_N$ over $[N]$.  The _Picker_'s strategy is also a probability vector $p_N$.  There is then a symmetric Nash equilibrium for this game where both the _Guesser_ and the _Picker_ play $p_N^*$.  (_Credit to Wing Suen for explaining the game theory reasoning to me,_)

We can find the distribution $p_N^\*$ that solves the game by solving the system of equations

$$U_N^1(p^\*) = U_N^2(p^\*) = \cdots = U_N^N(p^\*)$$

which then gives the solution to the problem $V_N^\*=U_N^k(p^\*)$.

## Solutions
$N$ | $V_N^\*$ | $p_N^\*$
-|-|:-:
$1$ | $1$ | $[1]$
$2$ | $\frac32=1.5$ | $[\frac12, \frac12]$
$3$ | $\frac95=1.8$ | $[\frac25, \frac15, \frac25]$
$4$ | $2$ | $[\frac38, \frac18, \frac18, \frac38]$
$5$ | $\frac{15}{7}\approx2.143$ | $[\frac{10}{28}, \frac{3}{28}, \frac{2}{28}, \frac{3}{28}, \frac{10}{28}]$
$6$ | $\frac94=2.25$ | $[\frac{7}{20}, \frac{2}{20}, \frac{1}{20}, \frac{1}{20}, \frac{2}{20}, \frac{7}{20}]$
$7$ | $\frac73\approx2.333$ | $[\frac{30}{87}, \frac{8}{87}, \frac{4}{87}, \frac{3}{87}, \frac{4}{87}, \frac{8}{87}, \frac{30}{87}]$
$8$ | $\frac{12}{5}=2.4$ | $[\frac{24}{70}, \frac{6}{70}, \frac{3}{70}, \frac{2}{70}, \frac{2}{70}, \frac{3}{70}, \frac{6}{70}, \frac{24}{70}]$
$9$ | $\frac{777}{317}\approx2.451$ | $[\frac{108}{317}, \frac{27}{317}, \frac{12}{317}, \frac{8}{317}, \frac{7}{317}, \frac{8}{317}, \frac{12}{317}, \frac{27}{317}, \frac{108}{317}]$
$10$ | $\frac{779}{312}\approx2.497$ | $[\frac{318}{936}, \frac{77}{936}, \frac{34}{936}, \frac{21}{936}, \frac{18}{936}, \frac{18}{936}, \frac{21}{936}, \frac{34}{936}, \frac{77}{936}, \frac{318}{936}]$
$11$ | $\frac{1368}{539}\approx2.538$ | $[\frac{2192}{6468}, \frac{516}{6468}, \frac{223}{6468}, \frac{138}{6468}, \frac{111}{6468}, \frac{108}{6468}, \frac{111}{6468}, \frac{138}{6468}, \frac{223}{6468}, \frac{516}{6468}, \frac{2192}{6468}]$
$12$ | $\frac{5031}{1957}\approx2.571$ | $[\frac{1324}{3914}, \frac{309}{3914}, \frac{129}{3914}, \frac{77}{3914}, \frac{60}{3914}, \frac{58}{3914}, \frac{58}{3914}, \frac{60}{3914}, \frac{77}{3914}, \frac{129}{3914}, \frac{309}{3914}, \frac{1324}{3914}]$
$13$ | $\frac{2879}{1109}\approx2.596$ | $[\frac{3368}{9981}, \frac{795}{9981}, \frac{316}{9981}, \frac{183}{9981}, \frac{141}{9981}, \frac{126}{9981}, \frac{123}{9981}, \frac{126}{9981}, \frac{141}{9981}, \frac{183}{9981}, \frac{316}{9981}, \frac{795}{9981}, \frac{3368}{9981}]$
$14$ | $\frac{23291}{8894}\approx2.619$ | $[\frac{8988}{26682}, \frac{2129}{26682}, \frac{842}{26682}, \frac{449}{26682}, \frac{326}{26682}, \frac{325}{26682}, \frac{282}{26682}, \frac{282}{26682}, \frac{325}{26682}, \frac{326}{26682}, \frac{449}{26682}, \frac{842}{26682}, \frac{2129}{26682}, \frac{8988}{26682}]$
$15$ | $\frac{6800}{2573}\approx2.643$ | $[\frac{36338}{108066}, \frac{8517}{108066}, \frac{3358}{108066}, \frac{1800}{108066}, \frac{1260}{108066}, \frac{1167}{108066}, \frac{1119}{108066}, \frac{948}{108066}, \frac{1119}{108066}, \frac{1167}{108066}, \frac{1260}{108066}, \frac{1800}{108066}, \frac{3358}{108066}, \frac{8517}{108066}, \frac{36338}{108066}]$
$16$ | $\frac{176758}{66339}\approx2.664$ | $[\frac{44597}{132678}, \frac{10298}{132678}, \frac{4085}{132678}, \frac{2182}{132678}, \frac{1519}{132678}, \frac{1319}{132678}, \frac{1226}{132678}, \frac{1113}{132678}, \frac{1113}{132678}, \frac{1226}{132678}, \frac{1319}{132678}, \frac{1519}{132678}, \frac{2182}{132678}, \frac{4085}{132678}, \frac{10298}{132678}, \frac{44597}{132678}]$

Solutions for $N\leq6$ found by Z3.  Remainder found by `scipy.optimize.minimize` and checked by computing $U_N^k(p)$ exactly.

## Repo
### [`pick-choose.nb`](z3solve.py)
Exploratory work in a Mathematica notebook.  Solves up to $N=4$.

### [`z3solve.py`](z3solve.py)
Requirements: [z3-solver](https://github.com/Z3Prover/z3)

`solveprob(N)` returns dictionary of solution for $N$.

Solutions up to $N=6$ computable.

### [`optimize.py`](optimize.py)
Requirements: [SciPy](https://scipy.org/)

`exact(N)` and `approx(N)` return dictionaries of either exact or approximate solutions for $N$.

Exact solutions up to $N=16$ computable.  Approximate solutions up to $N\approx40$ computable.

## TODOs/Ideas/Issues
- SciPy
    - [ ] Other packages: [NLopt](https://nlopt.readthedocs.io/en/latest/), [ALGLIB](https://www.alglib.net/)
    - [x] For each call of `v(p)` cache intermediate calls with dynamic programming.  (`functools.cache` causes unhashable `ndarray` error)
    - [x] Remove unnecessary `p[i]`s.
    - [x] Convert to `Fraction`s.
    - [x] Find nice way to find rational solution from approximate one.
    - [x] Better initial guess.
    - [ ] Objective function scaling
    - [x] JSON output when solution found
- Z3
    - [ ] Other packages: [CVC](https://cvc5.github.io/docs-ci/docs-main/), [pySMT](https://pysmt.readthedocs.io/en/latest/index.html), [sbv](https://hackage.haskell.org/package/sbv)
    - [ ] Figure out what `/0` is in solution.
    - [ ] Remove unnecesary `p[i]` instead of adding equality constraint.
    - [ ] Figure out if adding `p[i]<1` constraint helps.
    - [ ] Find a way to benchmark ($N=6$ too fast and $N=7$ too slow).
    - [ ] [Horn Clause Solver](https://theory.stanford.edu/~nikolaj/programmingz3.html#sec-horn-clause-solver) for $V_k$ function.  Might have to compute for each $k$.
    - [ ] Add variables for `v(i, j)`
