""" This module immplements the measures described in:

        Evaluation Measures for Relevance and Credibility in Ranked Lists
        Christina Lioma, Jakob Grue Simonsen, and Birger Larsen (2017)
        ACM SIGIR International Conference on the Theory of
        Information Retrieval, pg. 91-98.

    For TYPE I measures, the parameter `rankings` is expected to be a list of
    3-tuples, where the elements in each 3-tuple represent a documents rank
    positions, as listed in the article.

        elem    description
        ------------------------------------------------------
        1       rank position in the input ranking
        2       rank position in the ideal relevance ranking
        3       rank position in the ideal credibility ranking

    It is also expected that `rankings` is sorted by the first element.

    For TYPE II measures, the parameter `scores` is expected to be a list of
    3-tuples, where the elements in each 3-tuple are as follows:

            elem    description
        ------------------------------------------------------
        1       i, the document's rank position in the input ranking
        2       relevance score for the document at rank i for some query
        3       credibility score for the document at rank i for some query

    It is also expected that `scores` is sorted by the first element.
"""
from __future__ import division, print_function
import math

__author__ = "Andrew Tristan Parli"
__version__ = "1.0.1"


""" TYPE I: RANK POSITION MEASURES """

def monus(a, b):
    """ monus operator """

    # sanity check, input parameters
    if (a < 0) or (b < 0):
        print("Warning: Monus operation expects two non-negative values but " +
              "received {} and {}".format(a,b))
        raise ValueError

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
        raise ValueError
    if nu < 0:
        print("Warning: Local Rank Error (LRE) expected a non-negative nu " +
              "but received {}".format(nu))
        raise ValueError
    if (mu + nu) <= 0:
        print("Warning: Local Rank Error (LRE) expected mu + nu > 0 " +
              "but received {} + {} is {}".format(mu, nu, mu + nu))
        raise ValueError

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
        raise ValueError

    if nu < 0:
        print("Warning: Local Rank Error (LRE) expected a non-negative nu " +
              "but received {}".format(nu))
        raise ValueError

    if (mu + nu) <= 0:
        print("Warning: Local Rank Error (LRE) expected mu + nu > 0 " +
              "but received {} + {} is {}".format(mu, nu, mu + nu))
        raise ValueError

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


""" TYPE II: DOCUMENT SCORE MEASURES """

def wcs(scores, n, _lambda):
    """ Weighted Cumulative Score (WCS) """
    if (_lambda < 0.0) or (_lambda > 1.0):
        print("Warning: Weighted Cumulative Score (WCS) expected a lambda " +
              "in the range [0,1] but received {}".format(_lambda))
        raise ValueError

    _sum = 0.0
    for i in xrange(n):
       a = 1.0 / math.log(1 + (i + 1), 2)
       _, zr, zc = scores[i]
       b = (_lambda * zr) + ((1.0 - _lambda) * zc)
       _sum += a * b

    return _sum


def iwcs(scores, n, _lambda):
    """ Ideal Weighted Cumulative Score (NWCS) """
    ideal = dict()
    for (i, zr, zc) in scores:
        zrc = (_lambda * zr) + ((1 - _lambda) * zc)
        ideal.setdefault(zrc, [])
        ideal[zrc].append((i,zr,zc))
    ks = ideal.keys()
    ks.sort(reverse=True)

    # create the ideal scores list from sorted zrc values
    ideal_rank = list()
    for k in ks:
        for vals in ideal[k]:
            ideal_rank.append(vals)
    return wcs(ideal_rank, n, _lambda)


def nwcs(scores, n, _lambda):
    """ Normalised Weighted Cumulative Score (NWCS) """
    n = len(scores)
    _wcs = wcs(scores, n, _lambda)
    _iwcs = iwcs(scores, n, _lambda)
    return _wcs / _iwcs


def cam(mr, mc, _lambda):
    """ Convex aggregating measure (CAM) """
    return (_lambda * mr) + ((1.0 - _lambda) * mc)


def wham(mr, mc, _lambda):
    """ Weighted harmonic mean aggregating measure (WHAM) """
    if (mr == 0.0) or (mc == 0.0):
        return 0.0
    return 1.0 / ( (_lambda * (1.0 / mr)) + ((1.0 - _lambda) * (1.0 / mc)) )
