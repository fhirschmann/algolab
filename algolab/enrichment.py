#!/usr/bin/env python
"""
Railway Graph enrichment

.. moduleauthor:: Michael Markert <markert.michael@googlemail.com>
"""
import csv
import logging

from algolab.stations import StationUsage, StationNotFound, RailwayNodeNotFound

VALUE_ATTRIBUTE = 'value'
CONNECTION_ATTRIBUTE = 'connections'

def enrich_with_usage(stations, station_usage_path):
    """Enrich the stations based on how they are used so that their importance
    for a given zoom level can be assessed.

    :param stations: mongodb collection that contains a station collection
    :param station_usage_path: path to the stations usage file
    """
    usage = StationUsage(station_usage_path, stations)
    for eva, info in usage._routes_cache.iteritems():
        try:
            station = usage.get_node_id(eva)
            station[VALUE_ATTRIBUTE] = rate_node(info)
            station[CONNECTION_ATTRIBUTE] = connections(info)
            stations.save(station)
        except StationNotFound:
            logging.debug('Station with EVA %s not found in usage file %s',
                          id_, station_usage_path)
        except RailwayNodeNotFound:
            logging.debug('Station with EVA %s has no appropriate'
                          'railway node in collection %s',
                          id_, collection.name)


def rate_node(route_info):
    """
    :param successors: neighbors of node
    :param route_info: information about quantity and quality of routes
    :type route_info: :class:`algolab.stations.RouteInfo`
    :returns: the value of the node
    :rtype: int
    """
    value = 0
    value += 100 * route_info.class0
    value += 70 * route_info.class1
    value += 50 * route_info.class2
    value += 25 * route_info.regional
    value += 15 * route_info.s_bahn
    value += 5 * route_info.tram

    return value

def connections(route_info):
    """Return a dictionary describing which connections a node with
    ``routes_info`` has.

    :param route_info: information about quantity and quality of routes
    :type route_info: :class:`algolab.stations.RouteInfo`
    :returns: the connections
    :rtype: dict
    """
    return {'class0': route_info.class0 > 0,
            'class1': route_info.class1 > 0,
            'class2': route_info.class2 > 0,
            'regional': route_info.regional > 0,
            's_bahn': route_info.s_bahn > 0,
            'tram': route_info.tram > 0,
        }


def clear_valuation(rg):
    """Clear the valuation of a railway graph.

    :param rg: collection to remove valuation from
    :type rg: :class:`~pymongo.collection.Collection`
    """
    for node in rg.find_node():
        del node[VALUE_ATTRIBUTE]
        rg.save(node)
