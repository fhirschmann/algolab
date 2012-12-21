#!/usr/bin/env python
from pymongo import Connection
from algolab.segment import Segmenter
from algolab.db import intersections, endpoints, create_rg, nodes_with_num_neighbors


if __name__ == "__main__":
    db = Connection("localhost", 27017)["osm-data"]
    rg0 = db["railway_graph"]
    rg1 = db["railway_graph_test"]
    rg1.drop()

    print "Intersections before: %s" % intersections(rg0).count()
    print "Double intersections before: %s" % nodes_with_num_neighbors(rg0, 3).count()
    print "Triplet Intersection before %s" % nodes_with_num_neighbors(rg0, 4).count()
    print "Endpoints before: %s" % endpoints(rg0).count()
    print "Nodes before: %s" % rg0.count()

    segs = Segmenter(rg0)
    i = 0
    e = 0
    s = set()
    for seg in segs.segments_as_triplets:
        i += 1
        e += create_rg(seg, rg1)
        s.update([t[2] for t in seg])
    print "Segments: %s" % i
    print "Individual nodes: %s" % len(s)

    print "Intersections after: %s" % intersections(rg1).count()
    print "Double intersections after: %s" % nodes_with_num_neighbors(rg1, 3).count()
    print "Triplet ntersections after: %s" % nodes_with_num_neighbors(rg1, 4).count()
    print "Endpoints after: %s" % endpoints(rg1).count()
    print "Nodes after: %s" % rg1.count()
    print "Number of existing nodes modified: %s" % e
