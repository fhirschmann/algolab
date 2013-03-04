#!/usr/bin/env python
"""
Railway Graph enrichment

.. moduleauthor:: Michael Markert <markert.michael@googlemail.com>
"""
import csv
import logging

from algolab.stations import StationUsage, StationNotFound, RailwayNodeNotFound


def enriched_stations(stations, station_usage_path):
    """Return enriched station nodes based on how they are used so that their
    importance for a given zoom level can be assessed.

    :param stations: mongodb collection that contains a station collection
    :param station_usage_path: path to the stations usage file
    :returns: enriched stations
    :rtype: list(dict)
    """
    usage = StationUsage(station_usage_path, stations)
    enriched = []
    for eva, info in usage._routes_cache.iteritems():
        try:
            station = usage.get_node_id(eva)
            station['value'] = rate_node(info)
            station['connections'] = connections(info)
            enriched.append(station)
        except StationNotFound:
            logging.debug('Station with EVA %s not found in usage file %s',
                          id_, station_usage_path)
        except RailwayNodeNotFound:
            logging.debug('Station with EVA %s has no appropriate'
                          'railway node in collection %s',
                          id_, collection.name)
    return enriched


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
