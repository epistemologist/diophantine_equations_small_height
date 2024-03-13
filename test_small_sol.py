from sage.all import *
import sys
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count


R = PolynomialRing(ZZ, names=("x", "y",))
(x, y,) = R.gens()

EQNS = [
    -x**4 + x*y + y**3 - 4,
    -x**4 - 2*x + y**3 - y**2 - 2,
    -x**4 + x*y + y**3 - y + 4,
    -x**4 + x*y - x + y**3 - 2,
    -x**4 - 2*x + y**3 + y**2 + 2,
    -x**4 + x*y - x + y**3 - 4,
    -x**4 - x + y**3 + y - 4,
    -x**4 + x*y + y**3 - y**2 - 2,
    -x**4 + x*y + x + y**3 + 4,
    -x**4 - 2*x + y**3 - y + 2,
    -x**4 - x + y**3 + y - 6,
    -x**4 - x**2 + x*y + y**3 - 2,
    -x**4 + x*y + y**3 + y**2 - 1,
    -x**4 - x + y**3 + y + 6,
    -x**4 - x + y**3 - y**2 + y - 2,
    -x**4 + x*y - x + y**3 - 3,
    -x**4 - x + y**3 + 2*y - 4,
    -x**4 - x + y**3 + y**2 + y - 2,
    -x**4 + x*y + x + y**3 + 3,
    -x**4 - 2*x + y**3 + y - 4,
    -x**4 - x + y**3 + y**2 - y - 2,
    -x**4 + x*y - x + y**3 + 3,
    -x**4 - 2*x + y**3 + y + 4,
    -x**4 + x*y - x + y**3 - y - 2,
    -x**4 + x*y + x + y**3 + y - 1,
    -x**4 + x*y + y**3 + y - 4,
    -x**4 + x**2 - x + y**3 - y - 2,
    -x**4 - x + y**3 + y**2 - 4,
    -x**4 + x*y + y**3 - y - 4,
    -x**4 + x**2 - x + y**3 - y + 2
]


def get_roots_mod_n(poly, N):
    # Given polynomial P(x,y) and modulo N
    # returns {(x,y): P(x,y) = 0 (mod N)}
    return {(x_, y_)
            for x_ in range(N)
            for y_ in poly.subs(x=x_).change_ring(Integers(N)).univariate_polynomial().roots(multiplicities=False)
            }


def gen_congruent_values(interval, residues, mod):
    # Given interval [A,B] and a list of residues `residues` modulo `mod`
    # Returns a generator of values in interval that are congruent to a residue in `residues` modulo `mod`
    lo, hi = interval
    residues = sorted(residues)
    start = (lo//mod) * mod
    while start <= hi:
        for res in residues:
            if lo <= start+res <= hi:
                yield start + res
        start += mod
    return None


SOL_MAX = 10**8
MOD = 2*3*5*7*11*13
ITER_MOD = 10**3


def find_sol(eqn_no, eqn):
    # Get possible residues for x and y
    print(f"{eqn_no}, Finding modular roots...", file=sys.stderr)
    roots_mod_n = get_roots_mod_n(eqn, MOD)
    possible_x_residues = {i[0] for i in roots_mod_n}
    possible_y_residues = {i[1] for i in roots_mod_n}
    # Brute force x
    X_LEN = (2*SOL_MAX)//MOD * len(possible_x_residues) + 10
    for i, x_ in enumerate(gen_congruent_values([-SOL_MAX, SOL_MAX], possible_x_residues, MOD)):
        if i % ITER_MOD == 0:
            print(f"{eqn_no} x: {i}/{X_LEN}, {i/X_LEN}", file=sys.stderr)
        poly_fixed_x = eqn.subs(x=x_).univariate_polynomial()
        possible_y_vals = poly_fixed_x.roots(multiplicities=False)
        if possible_y_vals:
            print(f"SOLUTION FOUND: eqn:{eqn}, x={x_}, y={possible_y_vals}")
            return True
    # Brute force y
    Y_LEN = (2*SOL_MAX)//MOD * len(possible_x_residues) + 10
    for i, y_ in enumerate(gen_congruent_values([-SOL_MAX, SOL_MAX], possible_x_residues, MOD)):
        if i % ITER_MOD == 0:
            print(f"{eqn_no} y: {i}/{Y_LEN}, {i/Y_LEN}", file=sys.stderr)
        poly_fixed_y = eqn.subs(y=y_).univariate_polynomial()
        possible_x_vals = poly_fixed_y.roots(multiplicities=False)
        if possible_x_vals:
            print(f"SOLUTION FOUND: eqn:{eqn}, x={possible_x_vals}, y={y_}")
            return True
    print(f"No solution found!: eqn:{eqn}")
    return False


def worker(args):
    return find_sol(*args)


with ProcessPoolExecutor(max_workers=4) as executor:
    for res in executor.map(
            worker,
            [(i, eqn) for i, eqn in enumerate(EQNS)]
    ):
        print(res)
