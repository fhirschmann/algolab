#!/usr/bin/env python
"""
Railway Graph enrichment

.. moduleauthor:: Michael Markert <markert.michael@googlemail.com>
"""
from __future__ import print_function

import csv
import logging

from collections import defaultdict, namedtuple
from operator import itemgetter

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


def generate_railviz_station_file(station_usage_path, path):
    """Generate a station file for railviz which lists the minimal zoomlevel on
    which the station should be displayed.

    :param station_usage_path: path to the stations usage file
    :param path: where to write the file to
    """
    partition = defaultdict(set)
    for eva, value, connections in enrich_stations(station_usage_path):
        if connections['class0']:
            partition[8].add(eva)
        if connections['class1'] or connections['class2']:
            partition[9].add(eva)
        if connections['regional'] or connections['s_bahn']:
            partition[11].add(eva)

        partition[12].add(eva)
    partition[10] = set(sorted(partition[11], key=itemgetter(1))[:1000])

    # disjoin the zoom levels
    for level, evas in sorted(partition.iteritems()):
        other_levels = [partition[l] for l in partition if l != level]
        for l in other_levels:
            l.difference_update(evas)

    del partition[8]            # always show ICE

    with open(path, 'w') as out:
        for level, evas in partition.iteritems():
            for eva in evas:
                print(eva, level, file=out)
