#!/usr/bin/env python
"""
Railway Graph enrichment

.. moduleauthor:: Michael Markert <markert.michael@googlemail.com>
"""
import csv
import logging

from collections import namedtuple

from algolab.stations import StationUsage, StationNotFound, RailwayNodeNotFound


RoutesInfo = namedtuple('RoutesInfo', ['class0', 'class1', 'class2', 'class3',
                                       'regional', 's_bahn', 'tram'])


def enrich_stations(station_usage_path):
    """Return enriched stations based on how they are used so that their
    importance for a given zoom level can be assessed.

    :param station_usage_path: path to the stations usage file
    :returns: enriched stations (eva, value, connections)
    :rtype: generator of 3-tuple
    """
    with open(station_usage_path) as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)
        for line in reader:
            info = RoutesInfo(*[int(r) if r else 0 for r in line[5:-1]])
            yield line[0], rate_node(info), connections(info)


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
