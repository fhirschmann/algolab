#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from math import sqrt


def pdist(p, p1, p2):
    """
    Calculate the perpendicular distance of `p` to the 
    line given by `p1` and `p2`.

    The perpendicular distance from the point (x₁,y₁) to
    the line y = kx + m is given by

        d = |kx₁ - y₁ + m| / sqrt(k² + 1)
    """
    if p1 == p2:
        return sqrt((p[0] - p1[0])**2 + (p[1] - p1[1]))

    k = (p2[1] - p1[1]) / (p2[0] - p1[0])
    m = p1[1] - k * p1[0]

    return abs(k * p[0] - p[1] + m) / sqrt(k**2 + 1)


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
                seg[successor["id"]] = db.find({"_id" : successor["id"]})[0]["loc"]

    return segments
