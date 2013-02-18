"""
Segmentation algorithm for railway graphs.

.. moduleauthor:: Fabian Hirschmann <fabian@hirschm.net>
"""
import logging

from algolab.segment import Segmenter
from algolab.db import node_for, nodes_with_num_neighbors_ne, neighbors

from algolab.util import angle_between_ll


class ESSegmenter(Segmenter):
    """
    Endpoint or Switch Segmenter - segments a railway graph.

    This is a very simple algorithm that extracts segments from a railway
    graph. A segment is defined by its bounds, which is either an endpoint
    or a switch.

    For example, running `segment` on the following railway graph

    .. plot::

        from algolab.data import points
        from pylab import *

        title("Segmentation visualization")
        for i in [2, 3]:
            plot(zip(*points[i])[0], zip(*points[i])[1], 'o-')
        show()

    will yield the segments:

    >>> from algolab.data import npoints
    >>> from algolab.db import create_rg
    >>> from algolab.segment import ESSegmenter
    >>> from pymongo import Connection
    >>> col = Connection("127.0.0.1", 27017)["test"]["test"]
    >>> col.drop()
    >>> for i in [2, 3]: create_rg(npoints[i], col)
    >>> list(ESSegmenter(col).segments_as_coordinates)
    [[[1, 1], [2, 1], [3, 1]], [[4, 1], [3, 1]], [[3, 0], [3, 1]], [[3, 1], [3, 5]]]
    """
    def __init__(self, collection):
        """
        :param collection: a collection cursor
        :type collection: a :class:`~pymongo.collection.Collection`
        """
        self.collection = collection

        # endpoints and switches
        self.es = nodes_with_num_neighbors_ne(collection, 2)
        self._estimated = int(self.es.count() * 1.3)

        # All of the visited nodes
        self.visited = set()
        self.visited_intersections = set()
        self.visited_endpoints = set()
        self.x = set()

    @property
    def visited_intersections_and_endpoints(self):
        return self.visited_intersections.union(self.visited_endpoints)

    def _walk_from(self, node, segment):
        if node["_id"] in segment:
            return segment

        unvisited = set(neighbors(node)).difference(
            [s["_id"] for s in segment])

        if len(unvisited) != 1:
            return segment + [node]

        segment.append(node)
        visit = iter(unvisited).next()

        return self._walk_from(node_for(visit, self.collection), segment)

    def _visit(self, segment):
        if len(segment[0]["successors"]) > 2:
            self.visited_intersections.add(segment[0]["_id"])
        elif len(segment[0]["successors"]) == 1:
            self.visited_endpoints.add(segment[0]["_id"])

        self.visited.update([s["_id"] for s in segment])

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
        for node in self.es:
            neighbor_ids = neighbors(node)

            for neighbor_id in neighbor_ids:
                neighbor = node_for(neighbor_id, self.collection)

                if neighbor_id in self.visited:
                    # Without the following, intersection to intersection
                    # connections will not be picked up
                    if neighbor_id in self.visited_intersections_and_endpoints:
                        continue
                    if len(neighbor["successors"]) < 3:
                        continue
                if not neighbor:
                    logging.error("%i's neighbor %i does not exist.",
                                  node["_id"], neighbor_id)
                segment = self._walk_from(neighbor, [node])
                self._visit(segment)
                yield segment


class StationESSegmenter(ESSegmenter):
    """
    Just like :class:`~algolab.segment.ESSegmenter`, except that segments
    will be divided into sub-segments if they contain stations.
    """
    def __init__(self, station_collection, *args, **kwargs):
        self.station_ids = set([s["_id"] for s in station_collection.find()])
        super(StationESSegmenter, self).__init__(*args, **kwargs)

    @property
    def segments(self):
        for seg in super(StationESSegmenter, self).segments:

            seg2 = []

            for node in seg:
                seg2.append(node)

                if node["_id"] in self.station_ids:
                    if len(seg2) > 1:
                        yield seg
                        seg2 = []
            if len(seg2) > 1:
                yield seg2
