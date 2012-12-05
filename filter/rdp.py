#!/usr/bin/env python
# -*- coding: utf-8 -*-

from util import pdist


def rdp(points, epsilon=1):
    if epsilon <= 0:
        return points

    dmax = 0.0
    index = 0
    for i in xrange(1, len(points) - 1):
        d = pdist(points[i], points[0], points[-1])
        if d > dmax:
            index = i
            dmax = d
    if dmax >= epsilon:
        return rdp(points[:index+1], epsilon) + rdp(points[index:], epsilon)
    else:
        return [points[0], points[-1]]


def epsilon_linear(zoom, k=1.5):
    """
    A linear function which increments ε by a factor of `k` at each
    zoom increment.
    """
    return k * zoom
