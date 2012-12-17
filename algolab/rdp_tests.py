import unittest2

from anglered.rdp import *


class LineTest(unittest2.TestCase):
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
