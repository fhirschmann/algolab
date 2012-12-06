# -*- coding: utf-8 -*-
"""
This is an implementation of a very simple algorithm which
removes a point in a sequence of points if the angle between
a point and its two neighbors is greater than a certain threshold.
"""

import numpy as np


def anglereduce(points, epsilon):
    if len(points) < 3:
        return points

    keep = [points[0]]

    for i in xrange(1, len(points)-1):
        # b       c
        #  \     /
        #  v\   /w
        #    \ /
        #     a
        ax, ay = points[i]
        bx, by = points[i-1]
        cx, cy = points[i+1]

        v = np.array([bx - ax, by - ay])
        w = np.array([cx - ax, cy - ay])

        dot = np.dot(v, w)
        v_modulus = np.sqrt((v * v).sum())
        w_modulus = np.sqrt((w * w).sum())
        cos_angle = dot / v_modulus / w_modulus

        angle = np.arccos(cos_angle) * 360 / 2 / np.pi
        if angle <= epsilon:
            keep.append(points[i])

    keep.append(points[-1])
    return keep
