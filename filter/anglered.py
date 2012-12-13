# -*- coding: utf-8 -*-

import numpy as np


def anglereduce(points, epsilon, pos=1):
    """
    This is a very simple recursive algorithm that removes a point in a curve
    that is approximated by series of `points`, if the angle between a point
    and its two adjacent neighbors is smaller than a threshold `epsilon`.

    :param points: a curve that is approximated by a series of points
    :type points: list of 3-tuples (x, y, ANY) where ANY is most likely the id
    :param epsilon: a threshold value with 0 <  ε < 180.
    :type epsilon: integer
    :param pos: the current position in the list;
    """
    if len(points) < 2:
        return points

    if len(points) - 1 == pos:
        # end of list reached
        return points

    # b       c
    #  \     /
    #  v\   /w
    #    \ /
    #     a
    ax, ay, _ = points[pos]
    bx, by, _ = points[pos-1]
    cx, cy, _ = points[pos+1]

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


def anglereduce_col(point_ids, epsilon, source, target):
    """
    This is similar to `anglereduce`, except that it works on the
    mongodb.

    WARNING: This will delete all entries in the `target` collection

    :param point_ids: a sequence of point ids
    :type point_ids: list of integers
    :param epsilon: a threshold value with 0 <  ε < 180.
    :type epsilon: integer
    :param source: a collection cursor
    :type source: a :class:`~pymongo.collection.Collection`
    :param target: a collection cursor
    :type target: a :class:`~pymongo.collection.Collection`
    """
    points = []

    for point_id in point_ids:
        p = source.find_one({"_id": point_id})
        points.append((p["loc"][0], p["loc"][1], p["_id"]))

    reduced = anglereduce(points, epsilon)

    for p in reduced:
        x, y, i = p
        target.insert({"_id": i, "loc": [x, y]})
