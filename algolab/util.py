#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from decimal import Decimal


def edist(a, b):
    """
    Calculates the euclidean distance between two points `a` and `b`.
    """
    ax, ay = map(Decimal, a)
    bx, by = map(Decimal, b)
    return Decimal((ax - bx) ** 2 + (ay - by) ** 2).sqrt()


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

    ax, ay = map(Decimal, a)
    bx, by = map(Decimal, b)
    px, py = map(Decimal, p)

    if (ax == bx):
        return abs(ax - px)

    k = (by - ay) / (bx - ax)
    m = ay - k * ax

    return abs(k * px - py + m) / Decimal(k ** 2 + 1).sqrt()


def triarea(a, b, c):
    """
    Calculates the area of a triangle.
    """
    return Decimal(0.5) * edist(a, b) * pdist(c, a, b)


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
