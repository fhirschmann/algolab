# -*- coding: utf-8 -*-
"""
Miscellaneous utilities.

.. moduleauthor:: Fabian Hirschmann <fabian@hirschm.net>
"""

from __future__ import division
import logging
from math import sqrt, cos, sin, radians, atan2
from contextlib import contextmanager
from datetime import datetime
from functools import wraps

import numpy as np
from numpy.linalg import norm
from scipy.spatial.distance import euclidean
from proj import Proj
proj = Proj(proj='utm', ellps='WGS84')

EARTH_RADIUS = 6378137
PRECISION = 10

log = logging.getLogger(__name__)


def memoized(f):
    """
    Decorator that provides memoization, i.e. a cache that saves the result of
    a function call and returns them if called with the same arguments.

    The function will not be evaluated if the arguments are present in the
    cache.
    """
    cache = {}

    @wraps(f)
    def _memoized(*args, **kwargs):
        key = tuple(args) + tuple(kwargs.items())
        try:
            if key in cache:
                return cache[key]
        except TypeError:       # if passed an unhashable type evaluate directly
            return f(*args, **kwargs)
        ret = f(*args, **kwargs)
        cache[key] = ret
        return ret
    return _memoized


def lonlat2xy(lon, lat):
    """
    Performs cartographic transformations (converts from
    longitude, latitude to native map projection x, y.
    """
    return proj(lon, lat)


def edist(a, b):
    """
    Calculates the euclidean distance between two points `a` and `b`.

    >>> edist([3, 5], [3, 2])
    3.0

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

    >>> pdist([2, 0], [0, 2], [4, 2])
    2.0

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

    >>> triarea([1, 1], [5, 1], [3, 5])
    8.0

    :param a: first point
    :type a: sequence of two integers/floats; a coordinate
    :param b: second point
    :type b: sequence of two integers/floats; a coordinate
    :param c: third point
    :type c: sequence of two integers/floats; a coordinate
    """
    return 0.5 * edist(a, b) * pdist(c, a, b)


def midpoint(a, b):
    """
    Calculates the midpoint of a line segment defined by the
    points `a` and `b`.

    >>> list(midpoint([2, 1], [4, 5]))
    [3.0, 3.0]

    :param a: a coordinate
    :rtype a: a sequence of two integers/floats
    :param b: a coordinate
    :rtype a: a sequence of two integers/floats
    """
    return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)


def angle_between(v1, v2):
    """
    Calculates the angle between vector `v1` and vector `v2`.

    >>> round(angle_between((0, 5), (1, 1)))
    45.0

    :param v1: a vector
    :type v1: sequence of two integers/floats
    :param v2: another vector
    :type v2: sequence of two integers/floats
    :returns: the angle in degrees
    :rtype: float
    """
    v = np.array(v1)
    w = np.array(v2)

    norm_v = norm(v)
    norm_w = norm(w)

    cos_angle = np.around(np.dot(v, w) / norm_v / norm_w, PRECISION)

    if not -1 <= cos_angle <= 1:
        return None
    else:
        return np.around(np.arccos(cos_angle) * 360 / 2 / np.pi, PRECISION)


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
def log_progress(name, log_function=log.info):
    log_function("-" * 50)
    log_function("=> Starting step '%s'" % name)
    now = datetime.now()
    yield
    log_function("<= Step '%s' finished (took %s)." % (
        name, datetime.now() - now))


def log_change(u, v, log_function=log.info):
    change = ((v - u) / v) * 100 if v is not 0 else 0
    log_function("Reduced to %i nodes from %i nodes. "
                 "Change: -%i (-%.3f%%)" % (u, v, v - u, change))
