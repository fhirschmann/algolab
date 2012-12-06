# -*- coding: utf-8 -*-

import numpy as np


def anglereduce(points, epsilon, pos=1):
    """
    This is a very simple recursive algorithm that removes a point in a curve
    that is approximated by series of `points`, if the angle between a point
    and its two adjacent neighbors is smaller than a threshold `epsilon`.

    :param points: a curve that is approximated by a series of points
    :type points: list of lists
    :param epsilon: a threshold value with 0 <  ε < 180.
    :type epsilon: integer
    :param pos: the current position in the list;
    """
    if len(points) - 1 == pos:
        # end of list reached
        return points

    # b       c
    #  \     /
    #  v\   /w
    #    \ /
    #     a
    ax, ay = points[pos]
    bx, by = points[pos-1]
    cx, cy = points[pos+1]

    v = np.array([bx - ax, by - ay])
    w = np.array([cx - ax, cy - ay])

    dot = np.dot(v, w)
    v_modulus = np.sqrt((v * v).sum())
    w_modulus = np.sqrt((w * w).sum())
    cos_angle = dot / v_modulus / w_modulus

    angle = np.arccos(cos_angle) * 360 / 2 / np.pi
    if angle <= epsilon:
        # keep the current point
        return anglereduce(points, epsilon, pos + 1)
    else:
        # remove the current point
        return anglereduce(points[:pos] + points[pos + 1:], epsilon, pos)
