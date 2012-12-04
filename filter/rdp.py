#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from math import sqrt

import matplotlib.pyplot as plt


def pdist(p, p1, p2):
    """
    Calculate the perpendicular distance of `p1` to the 
    line given by `p1` and `p2`.

    The perpendicular distance from the point (x₁,y₁) to
    the line y = kx + m is given by

        d = |kx₁ - y₁ + m| / sqrt(k² + 1)
    """
    k = (p2[1] - p1[1]) / (p2[0] - p1[0])
    m = p1[1] - k * p1[0]

    return abs(k * p[0] - p[1] + m) / sqrt(k**2 + 1)


def rdp(points, epsilon=1):
    dmax = 0.0
    index = 0.0
    for i in xrange(2, len(points)):
        d = pdist(points[i], points[0], points[-1])
        if d > dmax:
            index = i
            dmax = d
    if dmax >= epsilon:
        return rdp(points[:index+1], epsilon) + rdp(points[index:], epsilon)
    else:
        return [points[0], points[-1]]



points = [(1,1), (2,2), (3,3), (4,3), (5,3), (6,5), (6,6), (7,9), (8,8)]

points2 = rdp(points, 0.8)

plt.plot(zip(*points)[0], zip(*points)[1], 'ro-')
plt.plot(zip(*points2)[0], zip(*points2)[1], 'go-')
plt.axis([0,10,0,10])
plt.show()
