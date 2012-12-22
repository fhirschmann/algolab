import unittest2

from algolab.simplify import rdp, anglereduce
from algolab.data import *


class RDPTest(unittest2.TestCase):
    def test_horizontal_line(self):
        data = [(1, 1, 1), (2, 1, 2), (4, 1, 3), (6, 1, 4)]
        expected = [(1, 1, 1), (6, 1, 4)]
        self.assertEqual(rdp(data, 0), expected)
        self.assertEqual(rdp(data, 5), expected)

    def test_vertical_line(self):
        data = [(3, 1, 1), (3, 2, 2), (3, 5, 3), (3, 7, 4)]
        expected = [(3, 1, 1), (3, 7, 4)]
        self.assertEqual(rdp(data, 0), expected)
        self.assertEqual(rdp(data, 5), expected)


class AngleredTest(unittest2.TestCase):
    def test_horizontal_line(self):
        data = [(1, 1, 1), (2, 1, 2), (4, 1, 3), (6, 1, 4)]
        expected = [(1, 1, 1), (6, 1, 4)]
        self.assertEqual(anglereduce(data, 180), expected)
        self.assertEqual(anglereduce(data, 179.5), expected)
        self.assertEqual(anglereduce(data, 100), expected)
        self.assertEqual(anglereduce(data, 30), expected)
        self.assertEqual(anglereduce(data, 1), expected)

    def test_vertical_line(self):
        data = [(3, 1, 1), (3, 2, 2), (3, 5, 3), (3, 7, 4)]
        expected = [(3, 1, 1), (3, 7, 4)]
        self.assertEqual(anglereduce(data, 180), expected)
        self.assertEqual(anglereduce(data, 179.5), expected)
        self.assertEqual(anglereduce(data, 100), expected)
        self.assertEqual(anglereduce(data, 30), expected)
        self.assertEqual(anglereduce(data, 1), expected)

    def test_angle(self):
        data = [(1, 1, 1), (4, 1, 2), (30, 2, 3)]
        self.assertEquals(anglereduce(data, 150), [(1, 1, 1), (30, 2, 3)])
        self.assertEquals(anglereduce(data, 179), data)

    def test_angle2(self):
        data = [(1, 1, 1), (4, 1, 2), (30, -1, 3)]
        self.assertEquals(anglereduce(data, 150), [(1, 1, 1), (30, -1, 3)])
        self.assertEquals(anglereduce(data, 179), data)


class CompareTest(unittest2.TestCase):
    def test_compare(self):
        self.maxDiff = None
        self.assertEqual(rdp(npoints[5], 0)[:2], anglereduce(npoints[5], 180)[:2])
        self.assertEqual(rdp(npoints[4], 0)[:2], anglereduce(npoints[4], 180)[:2])
        self.assertEqual(rdp(npoints[3], 0)[:2], anglereduce(npoints[3], 180)[:2])
        self.assertEqual(rdp(npoints[2], 0)[:2], anglereduce(npoints[2], 180)[:2])
        self.assertEqual(rdp(npoints[1], 0)[:2], anglereduce(npoints[1], 180)[:2])
        self.assertEqual(rdp(npoints[0], 0)[:2], anglereduce(npoints[0], 180)[:2])
