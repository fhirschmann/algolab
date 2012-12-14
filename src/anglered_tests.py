import unittest2

from anglered import *


class LineTest(unittest2.TestCase):
    def test_horizontal_line(self):
        data = [(1, 1, 1), (2, 1, 2), (4, 1, 3), (6, 1, 4)]
        expected = [(1, 1, 1), (6, 1, 4)]
        self.assertEqual(anglereduce(data, 180), expected)
        self.assertEqual(anglereduce(data, 179.5), expected)
        self.assertEqual(anglereduce(data, 100), expected)
        self.assertEqual(anglereduce(data, 30), expected)
        self.assertEqual(anglereduce(data, 0), expected)

    def test_vertical_line(self):
        data = [(3, 1, 1), (3, 2, 2), (3, 5, 3), (3, 7, 4)]
        expected = [(3, 1, 1), (3, 7, 4)]
        self.assertEqual(anglereduce(data, 180), expected)
        self.assertEqual(anglereduce(data, 179.5), expected)
        self.assertEqual(anglereduce(data, 100), expected)
        self.assertEqual(anglereduce(data, 30), expected)
        self.assertEqual(anglereduce(data, 0), expected)

    def test_angle(self):
        data = [(1, 1, 1), (4, 1, 2), (30, 2, 3)]
        self.assertEquals(anglereduce(data, 150), [(1, 1, 1), (30, 2, 3)])
        self.assertEquals(anglereduce(data, 179), data)

    def test_angle2(self):
        data = [(1, 1, 1), (4, 1, 2), (30, -1, 3)]
        self.assertEquals(anglereduce(data, 150), [(1, 1, 1), (30, -1, 3)])
        self.assertEquals(anglereduce(data, 179), data)
