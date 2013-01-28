import unittest2

from pymongo import Connection

from algolab.db import *
from algolab.data import *
from algolab.util import *


# PLEASE NOTE:
#
# It is highly recommended to execute
#     al_visualize_data --datasets DATASET [DATASETS ...]]
#
# For example, to understand test_merge, you may want to execute
#     al_visualize_data --datasets 2 3 4 5


class DBTest(unittest2.TestCase):
    def setUp(self):
        self.col0 = Connection("127.0.0.1", 27017)["algolab-test"]["rg0"]
        self.col1 = Connection("127.0.0.1", 27017)["algolab-test"]["rg1"]
        self.col0.drop()
        self.col1.drop()

    def create_rg_for(self, datasets, col=None):
        for n in datasets:
            create_rg(npoints[n], col if col else self.col0, distance_function=edist)

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
        self.create_rg_for([2, 3, 5])

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

    def test_merge_nodes(self):
        self.create_rg_for([2, 3, 4, 5])

        count_before = self.col0.count()
        self.assertEqual(count_before, 12)

        neighbors_before = self.col0.find_one(2)["successors"]
        self.assertEqual(len(neighbors_before), 7)

        merge_nodes(self.col0, 2, [1, 4], distance_function=edist)
        self.assertEqual(self.col0.count(), count_before - 2)

        # We now have this number of neighbors because we inherited
        # the neighbors of the nodes we merge with and remove these
        # nodes as neighbors at the same time. You have too look
        # at the data (al_visualize_data).
        self.assertEqual(len(self.col0.find_one(2)["successors"]),
                len(neighbors_before) - 1)
        self.assertItemsEqual([s["id"] for s in self.col0.find_one(2)["successors"]],
                [0, 6, 3, 5, 8, 9])

    def test_dedup(self):
        self.create_rg_for([2, 3, 4, 5])
        count_before = self.col0.count()

        self.col0.insert({"loc": points[2][1], "successors": []})
        self.assertEqual(self.col0.count(), count_before + 1)

        dedup(self.col0)
        self.assertEqual(self.col0.count(), count_before)

    def test_dedup2(self):
        self.create_rg_for([2, 3, 4, 5])
        count_before = self.col0.count()

        self.col0.insert({"_id": 100, "loc": points[2][1], "successors": [
            {"id": 99, "distance": 1}]})
        self.col0.insert({"_id": 99, "loc": [2, 0], "successors": [
            {"id": 100, "distance": 1}]})

        dedup(self.col0, distance_function=edist)
        self.assertEqual(self.col0.count(), count_before + 1)
        self.assertIn(self.col0.find_one(99)["successors"][0]["id"],
                      [npoints[2][1][2], 100])

    def test_copy(self):
        self.create_rg_for([2, 3, 4, 5])
        copy(self.col0, self.col1)
        self.assertEqual(self.col0.count(), self.col1.count())
        self.assertItemsEqual([n["_id"] for n in self.col0.find()],
                              [n["_id"] for n in self.col1.find()])
