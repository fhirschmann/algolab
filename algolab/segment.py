"""
Segmentation algorithm for railway graphs.
"""
import logging

from db import node_for, nodes_with_num_neighbors_ne


def neighbors(node):
    return [s["id"] for s in node["successors"]]


def walk_from(node_id, segment, col):
    if node_id in segment:
        return segment

    node = node_for(node_id, col)
    if not node:
        logging.error("No such node: %i" % node_id)
        return segment
    else:
        unvisited = set(
                neighbors(
                    node_for(node_id, col))).difference([s["_id"] for s in segment])

    if len(unvisited) != 1:
        return segment + [node]

    segment.append(node)
    visit = iter(unvisited).next()

    return walk_from(visit, segment, col)


class Segmenter(object):
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
    """
    def __init__(self, collection):
        """
        :param collection: a collection cursor
        :type collection : a :class:`~pymongo.collection.Collection`
        """
        self.collection = collection

        # endpoints and switches
        self.es = nodes_with_num_neighbors_ne(collection, 2)
        self._estimated = int(self.es.count() / 0.96)

    @property
    def estimated_num_segments(self):
        """
        Returns the estimated number of segments (based on the number
        of switches and endpoints).

        :returns: estimated number of segments
        :rtype: integer
        """
        return self._estimated

    @property
    def segments(self):
        visited = set()

        es = nodes_with_num_neighbors_ne(self.collection, 2)

        for node in es:
            neighbor_ids = neighbors(node)

            for neighbor_id in neighbor_ids:
                if neighbor_id in visited:
                    continue
                segment = walk_from(neighbor_id,
                        [node], self.collection)
                visited.update([s["_id"] for s in segment])
                visited.add(node["_id"])
                yield segment

    @property
    def segments_as_triplets(self):
        for segment in self.segments:
            yield [n["loc"] + [n["_id"]] for n in segment]
