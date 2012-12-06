#!/usr/bin/env python
# -*- coding: utf-8 -*-

from util import pdist


def rdp(points, epsilon=1):
    if epsilon <= 0:
        return points

    dmax = 0.0
    index = 0
    for i in xrange(2, len(points) - 1):
        d = pdist(points[i], points[0], points[-1])
        if d > dmax:
            index = i
            dmax = d
    if dmax >= epsilon:
        r1 = rdp(points[:index], epsilon)
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
