#!/usr/bin/env python
"""
Provides utilities to work with station data.

.. moduleauthor:: Michael Markert <markert.michael@googlemail.com>
"""
import csv
import logging

from pymongo import GEO2D

from algolab.util import distance

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
        station_number%id|name|shortcut|location numbers

    `id` is 7 digit number padded with zeroes
    `location numbers` are several numbers, important are number 2 and 3:
                    longitude and latitude

    `id` is referenced within the routes file to describe route endpoints.
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

    def get_node_id(self, id_):
        """
        Return the document id of the nearest railway graph node.

        :param id_: id of station
        """
        if id_ not in self._id_cache:
            longitude, latitude = self._get_location(id_)
            doc = self._select_node_near(longitude, latitude)
            if doc:
                self._id_cache[id_] = doc['_id']
            else:
                raise RailwayNodeNotFound('There is no railway graph node'
                                          'sufficiently near to EVA %s' % id_)

        try:
            return self._id_cache[id_]
        except KeyError:
            raise RailwayNodeNotFound('There is no railway graph node'
                                      'sufficiently near to EVA %s' % id_)

    def _select_node_near(self, longitude, latitude, max_distance=1000):
        """Return the rg node that is nearest to longitude and latitude but
        within max_distance.

        :param longitude: target longitude
        :param latitude: target latitude
        :param max_distance: maximal distance (unit depends on document
                             coordinate system)
        """
        return self._collection.find_one({'loc':
                                          {
                                              # order is important
                                              '$maxDistance': max_distance,
                                              '$near': [longitude, latitude]
                                          }
                                      })

    def _get_location(self, id_):
        """
        :param id_: id of station
        :returns: longitude and latitude of station
        :rtype: tuple(float, float)
        """
        entry = self._search_entry(id_)
        locations = entry[3].split()
        return float(locations[1]), float(locations[2])

    def _search_entry(self, id_):
        """
        :param id_: station to look for
        :returns: the entry for the station id_
        """
        self._reset_file()
        for entry in self._station_reader:
            if self._equal_ids(self._get_id(entry), id_):
                return entry
        raise StationNotFound('Station ID (EVA) %s not found' % id_)

    def _reset_file(self):
        self._station_file.seek(0)
        next(self._station_file)

    def _fill_cache(self):
        """Fill the cache with every station in file."""
        for entry in self._station_reader:
            if len(entry) < 4:  # ignore malformed entries
                continue
            id_ = self._get_id(entry)
            locations = entry[3].split()
            longitude, latitude = float(locations[1]), float(locations[2])
            if longitude == latitude == 0.0: # ignore malformed coordinates
                continue
            doc = self._select_node_near(longitude, latitude)
            if doc:
                self._id_cache[id_] = doc['_id']

    @staticmethod
    def _get_id(entry):
        return entry[0].split('%')[-1]

    @staticmethod
    def _pad_id(id_):
        return '%07d' % int(id_)

    @staticmethod
    def _equal_ids(left, right):
        return left == right or left == Stations._pad_id(right)

class StationUsage(Stations):
    """Abstraction for the station usage file.

    A station usage file has the following structure::

        head # describes the columns
        ...

        ID;name;longitude;latitude;#events;#class0;#class1;#class2;#class3

    `id` is 7 digit number padded with zeroes
    #events describes the amount of events occuring at the station
    #classN describes the amount of events with class N (does not have to sum
    up with #events)
    """
    def __init__(self, station_usage_path, collection, cache=True):
        """
        :param station_usage_path: path to file describing stations and their
                                   usage
        :param collection: mongodb collection containing railway graph nodes
        :param cache: fill cache before searching
        """
        super(StationUsage, self).__init__(station_usage_path, collection, False)
        # patch up reader, uses other delimiter
        self._station_reader = csv.reader(self._station_file, delimiter=';')
        self._value_cache = dict()
        if cache:
            self._fill_cache()

    def get_id_value(self, id_):
        """
        :param id_: id of station
        :returns: valuation of type
        :rtype: int
        """
        if id_ not in self._value_cache:
            node_id = self.get_node_id(id_)
            successors = self._collection.find_one(node_id)['successors']
            entry = self._search_entry(id_)
            self._value_cache[id_] = self._value(successors, entry[5:9])

        return self._value_cache[id_]

    def _fill_cache(self):
        """Fill the caches with every station in file."""
        for entry in self._station_reader:
            if len(entry) < 4:  # ignore malformed entries
                continue
            id_ = self._get_id(entry)
            longitude, latitude = float(entry[2]), float(entry[3])
            if longitude == latitude == 0.0: # ignore malformed entries
                continue

            doc = self._select_node_near(longitude, latitude)
            if doc:
                self._id_cache[id_] = doc['_id']
                self._value_cache[id_] = self._value(doc['successors'], entry[5:9])

    @staticmethod
    def _value(successors, routes):
        """Value a node based on the numbers of its successors and routes
        (according to their types).
        """
        value = 0
        if len(successors) == 1:
            value += 50
        value += 10 * int(routes[0]) # class0
        value += 5 * int(routes[1]) # class1
        value += 3 * int(routes[2]) # class2
        value += int(routes[3])     # class3

        return value

    def _get_location(self, id_):
        """
        :param id_: id of station
        :returns: longitude and latitude of station
        :rtype: tuple(float, float)
        """
        entry = self._search_entry(id_)
        longitude, latitude = float(entry[2]), float(entry[3])
        return longitude, latitude

def build_rg_from_routes(base_collection, target_collection,
                         station_path, routes_path):
    """Construct a simplified rg from routes and station information based on the
    rg contained in base_collection.

    A node of the base collection is only included if its coordinates correspond
    to a station that is included in the routes and stations files.

    :param base_collection: mongodb collection containing rg nodes to base new
                            rg on
    :param target_collection: mongodb collection to write the simplified rg to
    :param station_path: path to the stations file
    :param routes_path: path to the routes file

    """
    stations = Stations(station_path, base_collection)
    with open(routes_path) as routes_file:
        next(routes_file)
    target_collection.create_index([('loc', GEO2D)])
        reader = csv.reader(routes_file, delimiter=';')
        for line in reader:
            start, end, type_ = line[:3] # compensate for trailing space
            start_node = base_collection.find_one(stations.get_node_id(start.strip()))
            end_node = base_collection.find_one(stations.get_node_id(end.strip()))

            dist = distance(start_node['loc'], end_node['loc'])
            successors = {'id': end_node['_id'], 'distance': dist}, \
                         {'id': start_node['_id'], 'distance': dist}
            nodes = target_collection.find_one(start_node['_id']), \
                    target_collection.find_one(end_node['_id'])
            ids = start_node['_id'], end_node['_id']
            locs = start_node['loc'], end_node['loc']
            for node, successor, id_, loc in zip(nodes, successors, ids, locs):
                if node and successor['id'] not in set(s['id']
                                                for s in node['successors']):
                    node['successors'].append(successor)
                    target_collection.save(node)
                else:
                    target_collection.insert({'_id': id_,
                                              'loc': loc,
                                              'successors': [successor]
                                          })

def build_station_collection(base_collection,
                             target_collection,
                             station_path, routes_path,
                             filter=None):
    """
    :param base_collection: mongodb collection containing rg nodes to tune
                            coordinates to
    :param target_collection: mongodb collection to write the stations to
    :param station_path: path to the stations file
    :param routes_path: path to the routes file
    :param filter: filtering function to include a node in the collection
    :type filter: None or function (eva, longitude, latitude) -> bool
    """
    stations = Stations(station_path, base_collection)
    if filter is None:
        filter = lambda eva, lon, lat: True
    target_collection.create_index([('loc', GEO2D)])
    with open(routes_path) as routes_file:
        next(routes_file)
        reader = csv.reader(routes_file, delimiter=';')
        for line in reader:
            esas = [x.strip() for x in line[:2]]
            for esa in esas:
                try:
                    node = base_collection.find_one(stations.get_node_id(esa))
                    if filter(esa, *node['loc']):
                        target_collection.insert(
                            {'_id': node['_id'],
                             'loc': node['loc'],
                             'successos': node['successors'],
                             'esa': esa})
                except StationNotFound:
                    logging.debug('Station with EVA %s not found in station'
                                  'file %s', esa, station_path)
                except RailwayNodeNotFound:
                    logging.debug('Station with EVA %s has no appropriate'
                                  'railway node in collection %s',
                                  esa, base_collection.name)
