import unittest2

from pymongo import Connection

from algolab.data import npoints, points
from algolab.combine import anglecombine
from algolab.db import create_rg
from algolab.util import edist


class CombineTest(unittest2.TestCase):
    def setUp(self):
        self.col0 = Connection("127.0.0.1", 27017)["algolab-test"]["rg0"]
        self.col1 = Connection("127.0.0.1", 27017)["algolab-test"]["rg1"]
        self.col0.drop()
        self.col1.drop()

    def create_rg_for(self, datasets, col=None):
        for n in datasets:
            create_rg(npoints[n], col if col else self.col0, distance_function=edist)

    def test_simple_combine(self):
        self.create_rg_for([12, 13])
        anglecombine(self.col0, 20)
        self.assertEqual(self.col0.count(), 7)
        self.assertDictContainsSubset({
            0: [1, 1],
            1: [2, 1],
            2: [3.0, 1.15],
            3: [4.0, 1.15],
            4: [5.0, 1.15],
            5: [6, 1],
            6: [7, 1]}, {n["_id"]: n["loc"] for n in self.col0.find()})

    def test_combine_2switches(self):
        self.create_rg_for([12, 13, 15])
        anglecombine(self.col0, 20)
        self.assertEqual(self.col0.count(), 8)
        self.assertDictContainsSubset({
            0: [1, 1],
            1: [2, 1],
            2: [3.0, 1.15],
            3: [4.0, 1.15],
            4: [5.0, 1.15],
            5: [6, 1],
            12: [4, 4],
            6: [7, 1]}, {n["_id"]: n["loc"] for n in self.col0.find()})
