import unittest2

from anglered.util import *


class TriAreaTest(unittest2.TestCase):
    def test_1(self):
        self.assertEqual(triarea((1, 1), (5, 1), (3, 5)), 8)
