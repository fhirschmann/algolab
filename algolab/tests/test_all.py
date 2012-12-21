import unittest2

from pymongo import Connection

from algolab.rdp import *
from algolab.anglered import *
from algolab.db import *
from algolab.data import *
from algolab.segment import Segmenter as S
from algolab.util import *


class AllTest(unittest2.TestCase):
    def setUp(self):
        self.col0 = Connection("127.0.0.1", 27017)["algolab-test"]["rg0"]
        self.col1 = Connection("127.0.0.1", 27017)["algolab-test"]["rg1"]
        self.col2 = Connection("127.0.0.1", 27017)["algolab-test"]["rg2"]
        self.col0.drop()
        self.col1.drop()
        self.col2.drop()

        create_rg(npoints[2], self.col0, distance_function=edist)
        create_rg(npoints[5], self.col0, distance_function=edist)

        create_rg(npoints[2], self.col1, distance_function=edist)
        create_rg(npoints[5], self.col1, distance_function=edist)
        create_rg(npoints[3], self.col1, distance_function=edist)
        create_rg(npoints[4], self.col1, distance_function=edist)

    def test_rdp(self):
        segments = S(self.col0).segments
        for seg in segments:
            sloc = locs_for(seg, self.col0)
            create_rg(rdp(sloc, 0), self.col2)

        self.assertEqual(self.col2.count(), 8)

    def test_rdp2(self):
        segments = S(self.col1).segments

        for seg in segments:
            sloc = locs_for(seg, self.col1)
            create_rg(rdp(sloc, 0), self.col2)

        self.assertEqual(self.col2.count(), 11)

    def test_rdp3(self):
        segments = S(self.col1).segments
        for seg in segments:
            sloc = locs_for(seg, self.col1)
            create_rg(rdp(sloc, 100000), self.col2)

        self.assertEqual(self.col2.count(), 8)

    def test_anglered(self):
        segments = S(self.col1).segments
        for seg in segments:
            sloc = locs_for(seg, self.col1)
            create_rg(anglereduce(sloc, 1), self.col2)

        self.assertEqual(self.col2.count(), 8)

    def test_anglered2(self):
        segments = S(self.col1).segments
        for seg in segments:
            sloc = locs_for(seg, self.col1)
            create_rg(anglereduce(sloc, 180), self.col2)

        self.assertEqual(self.col2.count(), 11)

#    def test_segment_create_rg(self):
        #self.col0.drop()
        #self.col1.drop()
        #for i in [1, 3]:
            #create_rg(npoints[i], self.col0, distance_function=edist)

        #for seg in S(self.col0).segments_as_triplets:
            #create_rg(seg, self.col1, distance_function=edist)
        #self.assertEqual(self.col0.count(), self.col1.count())
        #for n in self.col0.find():
            #self.assertTrue(self.col1.find(n))
        #for n in self.col1.find():
            #self.assertTrue(self.col0.find(n))

        #for n in self.col0.find():
            #print n["_id"]
            #self.assertItemsEqual(n["successors"], self.col1.find_one(n["_id"])["successors"])
