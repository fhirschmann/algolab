# -*- coding: utf-8 -*-
"""
The Ramer-Douglas-Peucker Algorithm.

.. moduleauthor:: Fabian Hirschmann <fabian@hirschm.net>
"""
from decimal import Decimal

from algolab.util import pdist


def rdp(points, epsilon=0):
    """
    This is an implementation of the
    `Ramer-Douglas-Peucker algorithm <http://en.wikipedia.org/wiki/Ramer%E2%80%93Douglas%E2%80%93Peucker_algorithm>`_.

    :param points: a curve that is approximated by a series of points
    :type points: list of 3-tuples (x, y, id)
    :param epsilon: a threshold value with ε ≥ 0.
    :type epsilon: a float or :class:`~decimal.Decimal`
    :returns: a list of 3-tuples (x, y, id)
    :rtype: list of 3-tuples

    The following figure animates the algorithm:

    .. image:: img/rdp.gif

    .. note::

        An interactive visualization of this algorithm, which shows
        the impact of different ε values, can be started by executing
        :file:`al_visualize_algo rdp`.
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
