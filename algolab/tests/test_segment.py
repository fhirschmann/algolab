import unittest2

from pymongo import Connection

from algolab.segment import *
from algolab.data import *
from algolab.db import create_rg


class SegmentTest(unittest2.TestCase):
    def setUp(self):
        self.col0 = Connection("127.0.0.1", 27017)["algolab-test"]["rg0"]
        self.col0.drop()
        create_rg(npoints3, self.col0)

    def test_already_segmented(self):
        self.assertEqual(segment(self.col0)[0], range(0, len(npoints3)))
