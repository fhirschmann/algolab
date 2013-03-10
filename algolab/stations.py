#!/usr/bin/env python
"""
Provides utilities to work with station data.

.. moduleauthor:: Michael Markert <markert.michael@googlemail.com>
"""
from __future__ import division, print_function

import csv
import logging

from collections import defaultdict, namedtuple
from operator import itemgetter

from pymongo import GEO2D

from algolab.db import copy, merge_nodes, empty
from algolab.util import distance, meter2rad

log = logging.getLogger(__name__)


class StationNotFound(Exception):
    """Indicates that a station is not contained in a stations or station usage
    file.
    """
    pass

class RailwayNodeNotFound(Exception):
    """Indicates that a appropriate railway graph node could not be found.
    """
    pass


class Stations(object):
    """
    Abstraction for the stations file.

    A station file has the following structure::

        head # number, will be ignored
        ...
        station_number%eva|name|shortcut|location numbers

    `eva` is 7 digit number padded with zeroes
    `location numbers` are several numbers, important are number 2 and 3:
                    longitude and latitude

    `eva` is referenced within the routes file to describe route endpoints.
    """
    def __init__(self, station_path, collection, cache=True):
        """

        :param station_path: path to file describing stations
        :param collection: mongodb collection containing railway graph nodes
        :param cache: fill cache before searching
        """
        self._station_path = station_path
        self._id_cache = {}
        self._station_file = open(station_path)
        self._reset_file()
        self._station_reader = csv.reader(self._station_file, delimiter='|')
        self._collection = collection
        if cache:
            self._fill_cache()

    def get_node_id(self, eva):
        """
        Return the document id of the nearest railway graph node.

        :param eva: eva of station
        """
        if eva not in self._id_cache:
            longitude, latitude = self._get_location(eva)
            doc = self._select_node_near(longitude, latitude)
            if doc:
                self._id_cache[eva] = doc['_id']
        try:
            return self._id_cache[eva]
        except KeyError:
            raise RailwayNodeNotFound('There is no railway graph node'
                                      'sufficiently near to EVA %s' % eva)

    def _select_node_near(self, longitude, latitude, max_distance=500):
        """Return the rg node that is nearest to longitude and latitude but
        within max_distance.

        :param longitude: target longitude
        :param latitude: target latitude
        :param max_distance: maximal distance (unit depends on document
                             coordinate system)
        """
        return self._collection.find_one(
            {'loc':
             {
                 # order is important
                 '$maxDistance': meter2rad(max_distance),
                 '$nearSphere': [longitude, latitude]
             }})

    def _get_location(self, eva):
        """
        :param eva: eva of station
        :returns: longitude and latitude of station
        :rtype: tuple(float, float)
        """
        entry = self._search_entry(eva)
        locations = entry[3].split()
        return float(locations[1]), float(locations[2])

    def _search_entry(self, eva):
        """
        :param eva: station eva to look for
        :returns: the entry for the station
        """
        self._reset_file()
        for entry in self._station_reader:
            if self._equal_evas(self._get_eva(entry), eva):
                return entry
        raise StationNotFound('Station ID (EVA) %s not found' % eva)

    def _reset_file(self):
        self._station_file.seek(0)
        next(self._station_file)

    def _fill_cache(self):
        """Fill the cache with every station in file."""
        for entry in self._station_reader:
            if len(entry) < 4:  # ignore malformed entries
                continue
            eva = self._get_eva(entry)
            locations = entry[3].split()
            longitude, latitude = float(locations[1]), float(locations[2])
            if longitude == latitude == 0.0: # ignore malformed coordinates
                continue
            doc = self._select_node_near(longitude, latitude)
            if doc:
                self._id_cache[eva] = doc['_id']
            else:
                log.debug("EVA '%s' could not be assigned to a node.", eva)

    @staticmethod
    def _get_eva(entry):
        return entry[0].split('%')[-1]

    @staticmethod
    def _pad_eva(eva):
        return '%07d' % int(eva)

    @staticmethod
    def _equal_evas(left, right):
        return left == right or left == Stations._pad_eva(right)


def build_station_collection(base_collection,
                             target_collection,
                             station_path, routes_path,
                             filter=None):
    """
    Build a station collection from a station file but only include stations
    that are as mentioned endpoints in the routes file.

    :param base_collection: mongodb collection containing rg nodes to tune
                            coordinates to
    :param target_collection: mongodb collection to write the stations to
    :param routes_path: path to the routes file
    :param filter: filtering function to include a node in the collection
    :type filter: None or function (eva, longitude, latitude) -> bool
    """
    empty(target_collection)
    stations = Stations(station_path, base_collection)
    target_collection.ensure_index([('loc', GEO2D)])
    if filter is None:
        filter = lambda eva, lon, lat: True
    with open(routes_path) as routes_file:
        size = sum(1 for line in routes_file) - 1
    with open(routes_path) as routes_file:
        next(routes_file)
        reader = csv.reader(routes_file, delimiter=';')
        for i, line in enumerate(reader, 1):
            print ('\rProcessing route %d of %d (%.2f%%)' %
                   (i, size, (i / size) * 100), end='')
            evas = [x.strip() for x in line[:2]]
            for eva in evas:
                try:
                    node = base_collection.find_one(stations.get_node_id(eva))
                    if filter(eva, *node['loc']):
                        target_collection.insert(
                            {'_id': node['_id'],
                             'loc': node['loc'],
                             'eva': eva})
                except StationNotFound:
                    log.debug('Station with EVA %s not found in station' +
                              'file %s', eva, station_path)
                except RailwayNodeNotFound:
                    log.debug('Station with EVA %s has no appropriate' +
                              'railway node in collection %s',
                              eva, base_collection.name)

def build_station_collection_from_stations(base_collection, target_collection,
                                           station_path, filter=None):
    """
    Build a station collection from a station file.

    :param base_collection: mongodb collection containing rg nodes to tune
                            coordinates to
    :param target_collection: mongodb collection to write the stations to
    :param station_path: path to the stations file
    :param filter: filtering function to include a node in the collection
    :type filter: None or function (eva, longitude, latitude) -> bool
    """
    empty(target_collection)
    stations = Stations(station_path, base_collection)
    target_collection.ensure_index([('loc', GEO2D)])
    if filter is None:
        filter = lambda eva, lon, lat: True
    size = len(stations._id_cache)
    for i, entry in enumerate(stations._id_cache.iteritems(), 1):
        print ('\rProcessing station %d of %d (%.2f%%)' %
               (i, size, (i / size) * 100), end='')
        eva, id_ = entry
        try:
            node = base_collection.find_one(id_)
            if filter(eva, *node['loc']):
                target_collection.insert(
                    {'_id': node['_id'],
                     'loc': node['loc'],
                     'eva': eva})
        except RailwayNodeNotFound:
            log.debug('Station with EVA %s has no appropriate' +
                      'railway node in collection %s',
                      eva, base_collection.name)
    print()


def cluster_stations(cluster_collection, station_collection, target_collection,
                     max_distance=None):
    """Cluster railway graph nodes to near station nodes.

    All railway graph nodes (in ``cluster_collection``) will be subsumed by the
    nearest station and successors will be updated accordingly.

    Stations will never be clustered to another station.

    The `cluster_collection` will be copied to the target collection emptying it
    by that.

    `cluster_collection` should contain all nodes present in the
    `station_collection`.

    :param cluster_collection: railway graph collection to cluster
    :param station_collection: collection containing stations
    :param target_collection: collection for clustered railway graph
    :param max_distance: maximal distance to subsume other nodes (in meters)
    :type max_distance: int or float or None

    """
    copy(cluster_collection, target_collection)
    target_collection.ensure_index([('loc', GEO2D)])
    stations = station_collection.count()
    if stations == 0:
        raise ValueError("Station collection is empty!")
    for i, station in enumerate(station_collection.find(), 1):
        print('\rClustering Station %d of %d (%.2f%%)' %
              (i, stations, i / stations * 100), end='')
        if not cluster_collection.find_one(station['_id']):
            log.error('Railway graph does not contain ID %s, will ignore it',
                      station['_id'])
            continue
        near_query = {'loc': {'$nearSphere': station['loc']}}
        if max_distance is not None:
            near_query['loc']['$maxDistance'] = meter2rad(max_distance)
        near_nodes = (n for n in station_collection.find(near_query)
                      if n['_id'] != station['_id'])
        try:
            nearest_node = next(near_nodes)
            radius = distance(station['loc'], nearest_node['loc']) / 2
        except StopIteration:
            log.warning('No valid cluster endpoint for node %d (EVA %s) found.%s',
                        station['_id'], station['eva'],
                        '' if max_distance is None
                        else 'Falling back to maximal distance: %d m')
            if max_distance is not None:
                radius = max_distance
            else:
                continue

        candidates = target_collection.find({'loc':
                                             { '$within':
                                               { '$centerSphere':
                                                 [station['loc'], meter2rad(radius)]}}})
        merge_ids = [c['_id'] for c in candidates if not
                     # don't merge stations
                     station_collection.find_one(c['_id'])]
        merge_nodes(target_collection, station['_id'], merge_ids)
    print() # stop with clean newline


def crop_station_file(station_path, destination,
                      north, south, west, east):
    """Crop a station file (station or station usage) so that it only contains
    coordinates within the supplied bounding box.

    :param station_path: path to the station file
    :param destination: path of the cropped stations
    :param north: northern boundary
    :param south: southern boundary
    :param west: west boundary
    :param east: east boundary
    """
    with open(station_path) as in_, open(destination, 'w') as out:
        head = next(in_)
        out.write(head)
        if head.count(';') > 0:
            extract = lambda line: [float(coord) for coord
                               in line.split(';')[2:4]]
        else:
            extract = lambda line: [float(coord) for coord
                               in (line.split('|')[-1]).split()[1:3]]
        for line in in_:
            x, y = extract(line)
            if west <= x <= east and south <= y <= north:
                out.write(line)

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
    partition[10] = set(sorted(partition[11], key=itemgetter(1))[:2000])

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
