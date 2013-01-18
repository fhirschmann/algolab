#!/usr/bin/env python
"""
Railway Graph enrichment

.. moduleauthor:: Michael Markert <markert.michael@googlemail.com>
"""
import csv

from algolab.stations import StationUsage

def enrich_with_routes(collection, station_usage_path, routes_path):
    """
    Enrich the collection by adding a routes count based on the information
    found in the station and routes files.

    :param collection: mongodb collection that contains a railway graph
    :param station_usge_path: path to the stations usage file
    :param routes_path: path to the routes file
    """
    stations = StationUsage(station_usage_path, collection)
    with open(routes_path) as routes_file:
        next(routes_file)
        reader = csv.reader(routes_file, delimiter=';')
        for line in reader:
            start, end, type_ = line[:3] # compensate for trailing space
            for node in start, end:
                node = node.strip()
                collection.update(stations.get_node_id(node),
                                  {'$inc': {'value': stations.get_value(node)}})
