import unittest2

from pymongo import Connection

from algolab.segment import Segmenter as S
from algolab.data import *
from algolab.util import *
from algolab.db import create_rg


class SegmentTest(unittest2.TestCase):
    def create_rg_for(self, datasets, col=None):
        for n in datasets:
            create_rg(npoints[n], col if col else self.col0, distance_function=edist)

    def setUp(self):
        self.col0 = Connection("127.0.0.1", 27017)["algolab-test"]["rg0"]
        self.col1 = Connection("127.0.0.1", 27017)["algolab-test"]["rg1"]
        self.col2 = Connection("127.0.0.1", 27017)["algolab-test"]["rg2"]
        self.col0.drop()
        self.col1.drop()
        self.col2.drop()
        create_rg(npoints[2], self.col0, distance_function=edist)

    def test_already_segmented(self):
        self.assertEqual(list(S(self.col0).segment_ids)[0], range(0, len(npoints[2])))

    def test_already_segmented2(self):
        create_rg(npoints[3], self.col1)
        self.assertEqual(list(S(self.col1).segment_ids)[0], [4, 2, 5])

    def test_already_segmented3(self):
        create_rg(npoints[4], self.col1)
        self.assertEqual(list(S(self.col1).segment_ids)[0], [6, 2])

    def test_switch_segment(self):
        create_rg(npoints[3], self.col0, distance_function=edist)

        intersect = npoints[3][1]
        n = self.col0.find_one(intersect[2])

        self.assertEqual(len(n["successors"]), 4)
        self.assertTrue({"distance": 1, "id": 1} in n["successors"])
        self.assertTrue({"distance": 1, "id": 3} in n["successors"])
        self.assertTrue({"distance": 1, "id": 4} in n["successors"])
        self.assertTrue({"distance": 4, "id": 5} in n["successors"])

    def test_switch_segment2(self):
        self.create_rg_for([2, 3, 4, 5])
        self.assertItemsEqual(list(S(self.col0).segment_ids),
                [[0, 1, 2], [2, 3], [2, 4], [2, 5],
                    [2, 6], [2, 8, 7], [2, 9, 10, 11]])

    def test_switch_segment3(self):
        self.create_rg_for([2, 3, 4, 5, 6, 7])
        self.assertItemsEqual(list(S(self.col0).segment_ids),
                [[0, 1, 2], [2, 3], [2, 4], [2, 5],
                    [2, 6], [7, 8, 2], [11, 10, 9, 2],
                    [2, 12], [13, 15], [13, 16], [2, 13], [13, 14]])
        self.assertEqual(len(list(S(self.col0).segment_ids)), 12)
