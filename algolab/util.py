#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import logging
from math import sqrt, cos, sin, radians, atan2
from contextlib import contextmanager
from datetime import datetime

import numpy as np
from scipy.spatial.distance import euclidean

EARTH_RADIUS = 6378137


def edist(a, b):
    """
    Calculates the euclidean distance between two points `a` and `b`.

    :param a: first point
    :type a: sequence of two integers/floats; a coordinate
    :param b: second point
    :type b: sequence of two integers/floats; a coordinate
    """
    return euclidean(np.array(a), np.array(b))


def gcdist(a, b):
    """
    Calculates the great circle distance between `a` and `b`.

    :param a: first point
    :type a: sequence of two integers/floats; a coordinate
    :param b: second point
    :type b: sequence of two integers/floats; a coordinate
    """
    lat1, lon1 = a
    lat2, lon2 = b

    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)

    a = (sin(dLat / 2) * sin(dLat / 2) +
            cos(radians(lat1)) * cos(radians(lat2)) *
            sin(dLon / 2) * sin(dLon / 2))
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return EARTH_RADIUS * c


def pdist(p, a, b):
    """
    Calculate the perpendicular distance of `p` to the
    line given by the points `a` and `b`.

    The perpendicular distance from the point (x₁,y₁) to
    the line y = kx + m is given by::

        d = |kx₁ - y₁ + m| / sqrt(k² + 1)

    :param a: first point
    :type a: sequence of two integers/floats; a coordinate
    :param b: second point
    :type b: sequence of two integers/floats; a coordinate
    :param p: third point
    :type p: sequence of two integers/floats; a coordinate
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

    :param a: first point
    :type a: sequence of two integers/floats; a coordinate
    :param b: second point
    :type b: sequence of two integers/floats; a coordinate
    :param c: third point
    :type c: sequence of two integers/floats; a coordinate
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


def raise_or_return(obj, exception, msg):
    """
    Raises `exception` if `obj` is None.

    :param obj: object to check/return
    :type obj: object
    :param exception: the exception to throw
    :type excpetion: `Exception`
    :param msg: message to pass to the exception
    :type msg: string
    """
    if obj is None:
        raise exception(msg)
    return obj


@contextmanager
def log_progress(name, log_function=logging.info):
    log_function("-" * 50)
    log_function("=> Starting step '%s'" % name)
    now = datetime.now()
    yield
    log_function("<= Step '%s' finished (took %s)." % (
        name, datetime.now() - now))


def log_change(u, v, log_function=logging.info):
    log_function("Reduced to %i nodes from %i nodes: - %.3f%%" % (u, v, ((v - u) / v) * 100))
