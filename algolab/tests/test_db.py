import unittest2

from pymongo import Connection

from algolab.db import *
from algolab.data import *


class DBTest(unittest2.TestCase):
    def setUp(self):
        self.col0 = Connection("127.0.0.1", 27017)["algolab-test"]["rg0"]
        self.col1 = Connection("127.0.0.1", 27017)["algolab-test"]["rg1"]
        self.col0.drop()
        self.col1.drop()

    def test_create_rg(self):
        create_rg(npoints, self.col0)

        for i, point in enumerate(points):
            self.assertEqual(node_for(i, self.col0)["loc"], point)

        for i in xrange(1, len(points) - 1):
            self.assertEqual(len(node_for(i, self.col0)["successors"]), 2)

        self.assertEqual(len(node_for(0, self.col0)["successors"]), 1)
        self.assertEqual(len(node_for(len(points) - 1, self.col0)["successors"]), 1)

    def test_create_rg_switch(self):
        create_rg(npoints3, self.col0)
        create_rg(npoints4, self.col0)

        self.assertEqual(self.col0.count(), len(npoints3) + len(npoints4) - 1)

    def test_apply_reduction0(self):
        create_rg(npoints, self.col0)

        apply_reduction([0, len(points) - 1], self.col0, self.col1)
        self.assertEqual(self.col1.count(), 2)

    def test_apply_reduction1(self):
        create_rg(npoints, self.col0)

        apply_reduction([0, 10, len(points) - 1], self.col0, self.col1)
        self.assertEqual(self.col1.count(), 3)

        self.assertEqual([n["_id"] for n in self.col1.find()], [0, 10, len(points) - 1])
