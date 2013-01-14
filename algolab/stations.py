#!/usr/bin/env python
"""
Provides utilities to work with station data.

.. moduleauthor:: Michael Markert <markert.michael@googlemail.com>
"""

class _Stations(object):
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
    def __init__(self, station_path, collection):
        """

        :param station_path: path to file describing stations
        :param collection: mongodb collection containing railway graph nodes
        """
        self._station_path = station_path
        self._cache = {}
        self._station_file = open(station_path)
        self._reset_file()
        self._station_reader = csv.reader(self._station_file, delimiter='|')
        self._collection = collection

    def get_node_id(self, id_):
        """
        Return the document id of the nearest railway graph node.

        :param id_: id of station
        """
        if id_ not in self._cache:
            longitude, latitude = self._get_location(self._pad_id(id_))
            doc = self._collection.find_one({'loc': {'$near': [longitude, latitude]}})
            self._cache[id_] = doc['_id']
        return self._cache[id_]

    def _get_location(self, id_):
        """
        :param id_: id of station
        :returns: longitude and latitude of station
        """
        entry = self._search_entry(id_)
        locations = entry[3].split()
        return float(locations[1]), float(locations[2])

    def _search_entry(self, id_):
        """
        :param id_: station to look for
        :returns: the entry for the station id_
        """
        self._reset_file()      # RFI: only reset pointer if necessary
        for entry in self._station_reader:
            if self._equal_ids(self._get_id(entry), id_):
                return entry

    def _reset_file(self):
        self._station_file.seek(0)
        next(self._station_file)

    @staticmethod
    def _get_id(entry):
        return entry[0].split('%')[-1]

    @staticmethod
    def _pad_id(id_):
        return '%07d' % int(id_)

    @staticmethod
    def _equal_ids(left, right):
        # someone really fucked that file up ...
        return left == right or (left[0] == '0' and
                               left[1:] == right)
