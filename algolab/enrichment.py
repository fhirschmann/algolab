#!/usr/bin/env python
"""
Railway Graph enrichment

.. moduleauthor:: Michael Markert <markert.michael@googlemail.com>
"""
import csv
import logging

from algolab.stations import StationUsage, StationNotFound, RailwayNodeNotFound

VALUE_ATTRIBUTE = 'value'

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
            for id_ in start, end:
                id_ = id_.strip()
                try:
                    node = collection.find(stations.get_node_id(id_))
                    collection.update({'_id': node['_id']},
                                      {'$inc':
                                       {VALUE_ATTRIBUTE:
                                        rate_node(node['successors'],
                                                  stations.get_id_routes(id_))}})
                except StationNotFound:
                    logging.debug('Station with EVA %s not found in usage file %s',
                                  id_, station_usage_path)
                except RailwayNodeNotFound:
                    logging.debug('Station with EVA %s has no appropriate'
                                  'railway node in collection %s',
                                  id_, collection.name)


def rate_node(successors, routes):
    """
    :param successors:
    :type successors:
    :param routes:
    :type routes:
    :returns: the value of the node
    :rtype: int
    """
    value = 0
    if len(successors) == 1:
        value += 50
    value += 10 * routes[0] # class0
    value += 5 * routes[1]  # class1
    value += 3 * routes[2]  # class2
    value += routes[3]      # class3

    return value
