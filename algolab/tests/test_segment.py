import unittest2

from pymongo import Connection

from algolab.segment import *
from algolab.data import *
from algolab.util import *
from algolab.db import create_rg


class SegmentTest(unittest2.TestCase):
    def setUp(self):
        self.col0 = Connection("127.0.0.1", 27017)["algolab-test"]["rg0"]
        self.col1 = Connection("127.0.0.1", 27017)["algolab-test"]["rg1"]
        self.col2 = Connection("127.0.0.1", 27017)["algolab-test"]["rg2"]
        self.col0.drop()
        self.col1.drop()
        self.col2.drop()
        create_rg(npoints[2], self.col0, distance_function=edist)

    def test_already_segmented(self):
        self.assertEqual(segment(self.col0)[0], range(0, len(npoints[2])))

    def test_already_segmented2(self):
        create_rg(npoints[3], self.col1)
        self.assertEqual(segment(self.col1)[0], [4, 2, 5])

    def test_already_segmented3(self):
        create_rg(npoints[4], self.col1)
        self.assertEqual(segment(self.col1)[0], [6, 2])

    def test_switch_segment(self):
        create_rg(npoints[3], self.col0, distance_function=edist)

        intersect = npoints[3][1]
        n = self.col0.find_one(intersect[2])

        self.assertEqual(len(n["successors"]), 4)
        self.assertTrue({"distance": 1, "id": 1} in n["successors"])
        self.assertTrue({"distance": 1, "id": 3} in n["successors"])
        self.assertTrue({"distance": 1, "id": 4} in n["successors"])
        self.assertTrue({"distance": 4, "id": 5} in n["successors"])
