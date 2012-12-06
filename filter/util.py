#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from math import sqrt


def edist(a, b):
    """
    Calculates the euclidean distance between two points `a` and `b`.
    """
    ax, ay = a
    bx, by = b
    return sqrt((ax - bx)**2 + (ay - by)**2)


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
        return abs(ay - by)


    k = (by - ay) / (bx - ax)
    m = ay - k * ax

    return abs(k * px - py + m) / sqrt(k**2 + 1)


def triarea(a, b, c):
    """
    Calculates the area of a triangle.
    """
    return 0.5 * edist(a, b) * pdist(c, a, b)


def segment(lst, nodeid):
    """
    Returns the segment the node is in. If the node is not currently
    associated with a segment, `None` is returned.

    :returns: The segment of the node
    """
    for seg in lst:
        if nodeid in seg:
            return seg
    return None


def extract_segments(db):
    """
    Extracts segments from a railway graph.

    A segment is a sequence of points where the start and end points
    have either no or more than one successor in the railway graph.

    :param rg: railway graph
    :type rg: dict
    """
    segments = []

    for node in db.find():
        seg = segment(segments, node["_id"])
        if not seg:
            seg = {node["_id"]: node["loc"]}
            segments.append(seg)

        for successor in node["successors"]:
            if successor["id"] not in seg:
                seg[successor["id"]] = db.find_one({"_id" : successor["id"]})["loc"]

    return segments
    return [s.values() for s in segments]
