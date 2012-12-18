import unittest2

from pymongo import Connection

from algolab.rdp import *
from algolab.anglered import *
from algolab.db import *
from algolab.data import *
from algolab.segment import *


class AllTest(unittest2.TestCase):
    def setUp(self):
        self.col0 = Connection("127.0.0.1", 27017)["algolab-test"]["rg0"]
        self.col1 = Connection("127.0.0.1", 27017)["algolab-test"]["rg1"]
        self.col2 = Connection("127.0.0.1", 27017)["algolab-test"]["rg2"]
        self.col0.drop()
        self.col1.drop()
        self.col2.drop()

        create_rg(npoints3, self.col0, distance_function=edist)
        create_rg(npoints6, self.col0, distance_function=edist)

        create_rg(npoints3, self.col1, distance_function=edist)
        create_rg(npoints6, self.col1, distance_function=edist)
        create_rg(npoints4, self.col1, distance_function=edist)
        create_rg(npoints5, self.col1, distance_function=edist)

    def test_rdp(self):
        segments = segment(self.col0)
        for seg in segments:
            sloc = loc_for_mult(seg, self.col0)
            create_rg(rdp(sloc, 0), self.col2)

        self.assertEqual(self.col2.count(), 8)

    def test_rdp2(self):
        segments = segment(self.col1)

        for seg in segments:
            sloc = loc_for_mult(seg, self.col1)
            create_rg(rdp(sloc, 0), self.col2)

        self.assertEqual(self.col2.count(), 11)

    def test_rdp3(self):
        segments = segment(self.col1)
        for seg in segments:
            sloc = loc_for_mult(seg, self.col1)
            create_rg(rdp(sloc, 100000), self.col2)

        self.assertEqual(self.col2.count(), 8)

    def test_anglered(self):
        segments = segment(self.col1)
        for seg in segments:
            sloc = loc_for_mult(seg, self.col1)
            create_rg(anglereduce(sloc, 1), self.col2)

        self.assertEqual(self.col2.count(), 8)

    def test_anglered2(self):
        segments = segment(self.col1)
        for seg in segments:
            sloc = loc_for_mult(seg, self.col1)
            create_rg(anglereduce(sloc, 180), self.col2)

        self.assertEqual(self.col2.count(), 11)
