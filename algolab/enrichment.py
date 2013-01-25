#!/usr/bin/env python
"""
Railway Graph enrichment

.. moduleauthor:: Michael Markert <markert.michael@googlemail.com>
"""
import csv
import logging

from algolab.stations import StationUsage, StationNotFound, RailwayNodeNotFound

def enrich_with_routes(collection, station_usage_path, routes_path):
    """
    Enrich the collection by adding a routes count based on the information
    found in the station and routes files.

    :param collection: mongodb collection that contains a railway graph
    :param station_usage_path: path to the stations usage file
    :param routes_path: path to the routes file
    """
    stations = StationUsage(station_usage_path, collection)
    with open(routes_path) as routes_file:
        next(routes_file)
        reader = csv.reader(routes_file, delimiter=';')
        for line in reader:
            start, end, type_ = line[:3] # compensate for trailing space
            for node in start, end:
                id_ = node.strip()
                try:
                    collection.update({'_id': stations.get_node_id(id_)},
                                      {'$inc':
                                       {'value': stations.get_id_value(id_)}})
                except StationNotFound:
                    logging.debug('Station with EVA %s not found in usage file %s',
                                  id_, station_usage_path)
                except RailwayNodeNotFound:
                    logging.debug('Station with EVA %s has no appropriate'
                                  'railway node in collection %s',
                                  id_, collection.name)
