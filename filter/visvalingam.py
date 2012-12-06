#!/usr/bin/env python
"""
This module provides an implementation of the algorithm proposed
by Visvalingam, M.

See http://www2.dcs.hull.ac.uk/CISRG/publications/DPs/DP10/DP10.html
"""

from __future__ import division
from util import edist, pdist

def triarea(a, b, c):
    """
    Calculates the area of a triangle.
    """
    return 0.5 * edist(a, b) * pdist(c, a, b)


def visvalingam(points, epsilon):
    pass
