#!/usr/bin/env python
"""
Railway Graph enrichment

.. moduleauthor:: Michael Markert <markert.michael@googlemail.com>
"""
import csv

from stations import _Stations

def enrich_with_routes(collection, station_path, routes_path):
    """
    Enrich the collection by adding a routes count based on the information
    found in the station and routes files.

    :param collection: mongodb collection that contains a railway graph
    :param station_path: path to the stations file
    :param routes_path: path to the routes file
    """
    stations = _Stations(station_path, collection)
    with open(routes_path) as routes_file:
        next(routes_file)
        reader = csv.reader(routes_file, delimiter=';')
        for line in reader:
            # TODO: await info from supervisor what unknown actually does
            start, end, unknown = line[:3] # compensate for trailing space
            for node in start, end:
                collection.update({'_id': stations.get_node_id(node.strip())},
                                  {'$inc': {'routes': 1}})
if __name__ == '__main__':
    import pymongo
    db = pymongo.Connection('127.0.0.1', 27017)
    rg = db['osm-data2']['railway_graph']
    enrich_with_routes(rg,
                       '../2_shortest_routes_finder/Stations.txt',
                       '../2_shortest_routes_finder/sgrv.csv')
