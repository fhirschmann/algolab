"""
Segmentation algorithm for railway graphs.
"""
import logging

from db import node_for, nodes_with_num_neighbors_ne, neighbors


def walk_from(node, segment, col):
    if node["_id"] in segment:
        return segment

    unvisited = set(neighbors(node)).difference(
        [s["_id"] for s in segment])

    if len(unvisited) != 1:
        return segment + [node]

    segment.append(node)
    visit = iter(unvisited).next()

    return walk_from(node_for(visit, col), segment, col)


class Segmenter(object):
    """
    Segments a railway graph.

    This is a very simple algorithm that extracts segments from a railway
    graph. A segment is defined by its bounds, which is either an endpoint
    or a switch.

    For example, running `segment` on the following railway graph

    .. graphviz::

        graph seg {
            a -- b -- d;
            b -- c;
            a -- c;
        }

    will yield the following segments::

        [
          [a, ..., b]
          [a, ..., c]
          [b, ..., c]
          [d, ..., b]
        ]
    """
    def __init__(self, collection):
        """
        :param collection: a collection cursor
        :type collection: a :class:`~pymongo.collection.Collection`
        """
        self.collection = collection

        # endpoints and switches
        self.es = nodes_with_num_neighbors_ne(collection, 2)
        self._estimated = int(self.es.count() / 0.96)

    @property
    def estimated_num_segments(self):
        """
        The estimated number of segments (based on the number
        of switches and endpoints).

        :returns: estimated number of segments
        :rtype: integer
        """
        return self._estimated

    @property
    def segments(self):
        """
        A python generator that generates segments
        (lists of nodes) lazily.

        :returns: segment generator
        :rtype: generator
        """
        visited = set()

        for node in self.es:
            neighbor_ids = neighbors(node)

            for neighbor_id in neighbor_ids:
                if neighbor_id in visited:
                    continue
                neighbor = node_for(neighbor_id, self.collection)
                if not neighbor:
                    logging.error("%i's neighbor %i does not exist.",
                                  node["_id"], neighbor_id)
                segment = walk_from(neighbor, [node], self.collection)
                visited.update([s["_id"] for s in segment])
                visited.add(node["_id"])
                yield segment

    @property
    def segments_as_triplets(self):
        """
        Equal to :py:obj:`.segments`, except that this is a list
        of triplets (lon, lat, id).
        """
        for segment in self.segments:
            yield [n["loc"] + [n["_id"]] for n in segment]

    @property
    def segment_ids(self):
        """
        Equal to :py:obj:`.segments`, except that this is a list
        of ids.
        """
        for segment in self.segments:
            yield [n["_id"] for n in segment]
