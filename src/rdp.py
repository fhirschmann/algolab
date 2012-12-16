#!/usr/bin/env python
# -*- coding: utf-8 -*-

from util import pdist


def rdp(points, epsilon=0):
    """
    This is an implementation of the Ramer-Douglas-Peucker algorithm.

    :param points: a curve that is approximated by a series of points
    :type points: list of 3-tuples (x, y, ANY) where ANY is most likely the id
    :param epsilon: a threshold value with 0 <  ε < 180.
    :type epsilon: integer
    """
    if epsilon <= 0:
        return points

    if len(points) < 3:
        return points

    dmax = 0.0
    index = -1
    for i in xrange(1, len(points)):
        d = pdist(points[i], points[0], points[-1])
        if d > dmax:
            index = i
            dmax = d
    if dmax > epsilon:
        r1 = rdp(points[:index + 1], epsilon)
        r2 = rdp(points[index:], epsilon)
        return r1[:-1] + r2
    else:
        return [points[0], points[-1]]


def epsilon_linear(zoom, k=1.5):
    """
    A linear function which increments ε by a factor of `k` at each
    zoom decrement.
    """
    return k * (-zoom + 16)
