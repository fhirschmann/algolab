#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from math import sqrt

import numpy as np
from scipy.spatial.distance import euclidean


def edist(a, b):
    """
    Calculates the euclidean distance between two points `a` and `b`.
    """
    return euclidean(np.array(a), np.array(b))


def pdist(p, a, b):
    """
    Calculate the perpendicular distance of `p` to the
    line given by the points `a` and `b`.

    The perpendicular distance from the point (x₁,y₁) to
    the line y = kx + m is given by

        d = |kx₁ - y₁ + m| / sqrt(k² + 1)
    """
    if a == b:
        return edist(p, a)

    ax, ay = a
    bx, by = b
    px, py = p

    if (ax == bx):
        return abs(ax - px)

    k = (by - ay) / (bx - ax)
    m = ay - k * ax

    return abs(k * px - py + m) / sqrt(k ** 2 + 1)


def triarea(a, b, c):
    """
    Calculates the area of a triangle.
    """
    return 0.5 * edist(a, b) * pdist(c, a, b)


def default(value, replacement):
    """
    Check if ``value`` is ``None`` and then return ``replacement`` or else
    ``value``.

    :param value: value to check
    :param replacement: default replacement for value
    :returns: return the value or replacement if value is None
    """
    return value if value is not None else replacement


def epsilon_linear(zoom, k=1.5):
    """
    A linear function which increments ε by a factor of `k` at each
    zoom decrement.
    """
    return k * (-zoom + 16)
