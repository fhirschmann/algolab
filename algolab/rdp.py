# -*- coding: utf-8 -*-
from decimal import Decimal

from algolab.util import pdist


def rdp(points, epsilon=0):
    """
    This is an implementation of the Ramer-Douglas-Peucker algorithm.

    :param points: a curve that is approximated by a series of points
    :type points: list of 3-tuples (x, y, id)
    :param epsilon: a threshold value with ε ≥ 0.
    :type epsilon: a :class:`~decimal.Decimal`
    """
    if len(points) < 3:
        return points

    dmax = Decimal(0.0)
    index = -1
    for i in xrange(1, len(points)):
        d = pdist(points[i][:2], points[0][:2], points[-1][:2])
        if d > dmax:
            index = i
            dmax = d
    if dmax > epsilon:
        r1 = rdp(points[:index + 1], epsilon)
        r2 = rdp(points[index:], epsilon)
        return r1[:-1] + r2
    else:
        return [points[0], points[-1]]
