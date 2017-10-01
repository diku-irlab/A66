from future import __division__
from future import __print_function__
import math


def monus(a, b):
    """ monus operator """

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


def lre(rankings, n, mu, nu):
    """ Local Rank Error (LRE) """

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

    # non-trivial calculation, note using zero-indexing so we need i+1
    _sum = 0.0
    for i in xrange(n-1):
        (_, r1, c1) = rankings[i]
        (_, r2, c2) = rankings[i+1]
        epsilon_r = monus(r1, r2)
        epsilon_c = monus(c1, c2)
        a = 1.0 / math.log(1 + (i+1), 2)
        b = ((mu + epsilon_r)*(v + epsilon_c) - (mu * nu))
        _sum += a * b
    return _sum


def clre(n, mu, nu):
    """ Normalisation constant (C_LRE) """
    limit = math.floor((n/2) - 1)
    _sum = 0.0
    for j in xrange(limit):
        x = n - (2 * j) - 1
        num = (x**2) + ((mu + nu) * x)
        denom = 1 + math.log(1 + j, 2)
        _sum += num / denom
    return _sum


def nlre(rankings, mu, nu):
    """ Normalised Local Rank Error (NLRE) """
    n = len(rankings)
    _lre = lre(rankings, n, mu, nu)
    _clre = clre(n, mu, nu)
    return 1.0 - (_lre / _clre)


def gre(rankings, n, mu, nu):
    """ Global Rank Error (GRE) """

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

    # non-trivial calculation, note using zero-indexing so we need i+1
    _sumRel = 0.0
    _sumCred = 0.0
    for i in xrange(n-1):
        (_, r1, c1) = rankings[i]
        (_, r2, c2) = rankings[i+1]
        epsilon_r = monus(r1, r2)
        epsilon_c = monus(c1, c2)
        a = 1.0 / math.log(1 + (i+1), 2)
        _sumRel += a * epsilon_r
        _sumCred += a * epsilon_c
    return (1.0 + (mu * _semRel)) * (1 + (nu * _sumCred)) - 1


def cgre(n, mu, nu):
    """ Normalisation constant (C_GRE) """

    limit = math.floor((n/2) - 1)
    _sum = 0.0
    for j in xrange(limit):
        num = n - (2 * j) - 1
        denom = 1 + math.log(1 + j, 2)
        _sum += num / denom
    return ((mu * nu) * (_sum**2)) + ((mu + nu) * _sum)


def ngre(rankings, mu, nu):
    """ Normalised Global Rank Error (NGRE) """
    n = len(rankings)
    _gre = gre(rankings, n, mu, nu)
    _cgre = cgre(n, mu, nu)
    return 1.0 - (_gre / _cgre)
