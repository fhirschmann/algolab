import unittest2

from pymongo import Connection

from algolab.db import *
from algolab.data import *
from algolab.util import *


class DBTest(unittest2.TestCase):
    def setUp(self):
        self.col0 = Connection("127.0.0.1", 27017)["algolab-test"]["rg0"]
        self.col1 = Connection("127.0.0.1", 27017)["algolab-test"]["rg1"]
        self.col0.drop()
        self.col1.drop()

    def test_create_rg(self):
        create_rg(npoints[0], self.col0)

        for i, point in enumerate(points[0]):
            self.assertEqual(node_for(i, self.col0)["loc"], point)

        for i in xrange(1, len(points[0]) - 1):
            self.assertEqual(len(node_for(i, self.col0)["successors"]), 2)

        self.assertEqual(len(node_for(0, self.col0)["successors"]), 1)
        self.assertEqual(len(node_for(len(points[0]) - 1, self.col0)["successors"]), 1)

    def test_create_rg_dist(self):
        create_rg(npoints[2], self.col0, distance_function=edist)

        for node in self.col0.find():
            for neig in node["successors"]:
                self.assertEqual(neig["distance"], 1)

    def test_create_rg_switch(self):
        create_rg(npoints[2], self.col0)
        create_rg(npoints[3], self.col0)

        self.assertEqual(self.col0.count(), len(npoints[2]) + len(npoints[3]) - 1)

    def test_create_rg_switch2(self):
        create_rg(npoints[3], self.col0)
        create_rg(npoints[4], self.col0)

        self.assertEqual(self.col0.count(), len(npoints[4]) + len(npoints[3]) - 1)

    def test_create_rg_switch3(self):
        create_rg(npoints[2], self.col0)
        create_rg(npoints[3], self.col0)
        create_rg(npoints[5], self.col0)

        self.assertEqual(self.col0.count(),
                len(npoints[2]) + len(npoints[3]) + len(npoints[5]) - 2)

    def test_create_rg_from0(self):
        create_rg(npoints[0], self.col0)

        create_rg_from([0, len(npoints[0]) - 1], self.col0, self.col1)
        self.assertEqual(self.col1.count(), 2)

    def test_create_rg_from1(self):
        create_rg(npoints[0], self.col0)

        create_rg_from([0, 10, len(npoints[0]) - 1], self.col0, self.col1)
        self.assertEqual(self.col1.count(), 3)

        self.assertEqual([n["_id"] for n in self.col1.find()], [0, 10, len(points[0]) - 1])
