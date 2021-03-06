# -*- coding: utf-8 -*-
"""
Angle-based combination algorithm.

.. moduleauthor:: Fabian Hirschmann <fabian@hirschm.net>
"""
from __future__ import print_function
import sys
import logging
from itertools import combinations

from algolab.util import angle_between, midpoint
from algolab.db import intersections, neighbors, merge_nodes

log = logging.getLogger(__name__)


def anglecombine(rg, epsilon, progress=True, keep_ids=[]):
    """
    Combines (nearly) parallel train tracks in a railway graph.

    :param keep_ids: ids to never throw out
    :type keep_ids: list of integers
    :param rg: the railway graph (collection) to work on
    :type rg: a :class:`~pymongo.collection.Collection`
    :param epsilon: an angle; should be rather small
    :type epsilon: float
    """
    # The stack: contains intersections to visit
    int_ids = list([n["_id"] for n in intersections(rg)])

    while int_ids:
        # Receive intersection from stack
        int_id = int_ids.pop(0)
        int_ = rg.find_one(int_id)
        if not int_:
            continue
        lon, lat = int_["loc"]

        if progress:
            sys.stdout.write("\rIntersections left: %d" % len(int_ids))

        for n_id_1, n_id_2 in combinations(neighbors(int_), 2):
            if n_id_1 in keep_ids or n_id_2 in keep_ids:
                continue
            # Neighbor 1
            n1 = rg.find_one(n_id_1)
            lon_n1, lat_n1 = n1["loc"]

            # Neighbor 2
            n2 = rg.find_one(n_id_2)
            lon_n2, lat_n2 = n2["loc"]

            angle = angle_between([lon_n1 - lon, lat_n1 - lat], [lon_n2 - lon, lat_n2 - lat])

            if angle and angle < epsilon:
                new_loc = midpoint(n1["loc"], n2["loc"])
                n1["loc"] = list(new_loc)
                rg.save(n1)
                merge_nodes(rg, n1["_id"], [n2["_id"]])

                # Insert current intersection at the bottom of the stack
                # so that it will be dealt with in the next step
                int_ids.insert(0, int_["_id"])

                int_ids.append(n1["_id"])
                break

    if progress:
        print()
