"""
Segmentation algorithm for railway graphs.
"""
from db import node_for


def neighbors(node):
    return [s["id"] for s in node["successors"]]


def walk_from(node_id, segment, col):
    if node_id in segment:
        return segment

    unvisited = set(
            neighbors(
                node_for(node_id, col))).difference(segment)

    if len(unvisited) != 1:
        return segment + [node_id]

    segment.append(node_id)
    visit = iter(unvisited).next()

    return walk_from(visit, segment, col)


def segment(col):
    """
    Segments a railway graph.

    This is a very simple algorithm that extracts segments from a railway
    graph. A segment is defined by its bounds, which is either an endpoint
    or a switch.

    For example, running `segment` on the following railway graph

           A
          / \
         /   \
        B----C
       /
      /
     D

    will yield the following segments:
        [
          [A, ..., B]
          [A, ..., C]
          [B, ..., C]
          [D, ..., B]
        ]

    :param col: a collection cursor
    :type col : a :class:`~pymongo.collection.Collection`
    :returns: A list of lists (segments) of node ids
    """
    segments = []
    visited = set()

    for node in col.find():
        if node["_id"] in visited:
            continue

        neighbor_ids = neighbors(node)
        if len(neighbor_ids) != 2:
            # this node is either an endpoint or a switch
            for neighbor_id in neighbor_ids:
                if neighbor_id in visited:
                    continue
                segment = walk_from(neighbor_id, [node["_id"]], col)
                segments.append(segment)
                visited.update(segment)

    return segments
