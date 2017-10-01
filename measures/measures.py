from future import __division__
from future import __print_function__
import math

def monus(a, b):
""" This is the monus operator from Equation 1 """

    # sanity check, input parameters
    if (a < 0) or (b < 0):
        print("Warning: Monus operation expects two non-negative values but " +
              "received {} and {}".format(a,b))
        throw ValueError

    # the main calculation
    if a <= b:
        return 0.0
    else:
        return 1.0 * (a - b)


def lre(rankings, mu, nu):
""" This is the Local Rank Error (LRE) measure from Equation 4 """

    n = len(rankings)

    # trivial case
    if n == 1.0:
        return 0.0

    # sanity check, input parameters
    if mu < 0:
        print("Warning: Local Rank Error (LRE) expected a non-negative mu " +
              "but received {}".format(mu))
        throw ValueError
    if nu < 0:
        print("Warning: Local Rank Error (LRE) expected a non-negative nu " +
              "but received {}".format(nu))
        throw ValueError
    if (mu + nu) <= 0:
        print("Warning: Local Rank Error (LRE) expected mu + nu > 0 " +
              "but received {} + {} is {}".format(mu, nu, mu + nu))
        throw ValueError

    # non-trivial calculation, note we use zero-indexing so we need i+1
    res = 0.0

    for i in xrange(n-1):
        (_, r1, c1) = rankings[i]
        (_, r2, c2) = rankings[i+1]
        epsilon_r = monus(r1, r2)
        epsilon_c = monus(c1, c2)
        a = 1.0 / log(1 + (i+1), 2)
        b = ((mu + epsilon_r)*(v + epsilon_c) - (mu * nu))
        res += a * b

    return res


def nlre(rankings, mu, nu):
""" This is the Normalized Local Rank Error (NLRE) measure from Equation 5 """
    return 1 - (lre(rankings, mu, nu) / clre(rankings, mu, nu))


def clre(rankings, mu, nu):
""" This is the normalization constant C_LRE from Equation 6 """

