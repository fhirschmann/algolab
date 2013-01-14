# -*- coding: utf-8 -*-
"""
Angle-based reduction algorithm.

.. moduleauthor:: Fabian Hirschmann <fabian@hirschm.net>
"""
from algolab.util import angle_between_points


def anglereduce(points, epsilon):
    """
    :type points: list of 3-tuples (x, y, id)
    :param epsilon: a threshold value with 0 <  ε <= 180.
    :type epsilon: a :class:`~decimal.Decimal`
    :returns: a list of 3-tuples (x, y, id)
    :rtype: list of 3-tuples

    This is a very simple recursive algorithm that removes a point in a curve
    that is approximated by series of `points`, if the angle between a point
    and its two adjacent neighbors is greater than a threshold `epsilon`.

    .. note::

        An interactive visualization of this algorithm, which shows
        the impact of different ε values, can be started by executing
        :file:`al_visualize_algo anglered`.
    """
    if len(points) < 3:
        return points

    if len(points[0]) != 3:
        raise ValueError("Points need to be a list of 3-tuples")

    if not (0 < epsilon <= 180):
        raise ValueError("Epsilon needs to be > 0 and <= 180 degrees")

    return _anglereduce(points, epsilon)


def _anglereduce(points, epsilon, pos=1):
    """
    Please use :anglereduce: instead.

    :param pos: the current position in the list;
    :type pos: integer
    """
    if len(points) - 1 == pos:
        # end of list reached
        return points

    # b       c
    #  \     /
    #  v\   /w
    #    \ /
    #     a
    a = points[pos][0:2]
    b = points[pos - 1][0:2]
    c = points[pos + 1][0:2]

    angle = angle_between_points(b, a, c)

    if angle and angle < epsilon:
        # keep the current point
        return _anglereduce(points, epsilon, pos + 1)
    else:
        # remove the current point
        return _anglereduce(points[:pos] + points[pos + 1:], epsilon, pos)
