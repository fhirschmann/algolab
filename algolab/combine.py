# -*- coding: utf-8 -*-
"""
Angle-based combination algorithm.

.. moduleauthor:: Fabian Hirschmann <fabian@hirschm.net>
"""
from itertools import combinations

from algolab.util import angle_between, midpoint
from algolab.db import intersections, neighbors, merge_nodes, empty, create_rg


def anglecombine(rg, epsilon):
    """
    Combines (nearly) parallel train tracks in a railway graph.

    :param rg: the railway graph (collection) to work on
    :type rg: a :class:`~pymongo.collection.Collection`
    :param epsilon: an angle (should be < 15°)
    :type epsilon: float
    """
    int_ids = list([n["_id"] for n in intersections(rg)])

    while int_ids:
        int_ = rg.find_one(int_ids.pop(0))
        if not int_:
            continue
        ix, iy = int_["loc"]

        for n_id_1, n_id_2 in combinations(neighbors(int_), 2):
            # Neighbor 1
            n1 = rg.find_one(n_id_1)
            n1x, n1y = n1["loc"]

            # Neighbor 2
            n2 = rg.find_one(n_id_2)
            n2x, n2y = n2["loc"]

            angle = angle_between([n1x - ix, n1y - iy], [n2x - ix, n2y - iy])

            if angle and angle < epsilon:
                new_loc = midpoint(n1["loc"], n2["loc"])
                n1["loc"] = list(new_loc)
                rg.save(n1)
                merge_nodes(rg, n1["_id"], [n2["_id"]])

                int_ids.insert(0, int_["_id"])
                int_ids.append(n1["_id"])
                break
