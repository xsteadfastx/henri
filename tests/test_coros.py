import sys
import unittest

import tools

sys.path.insert(0, "../src")
import henri.coros  # isort:skip


class TestCoros(unittest.TestCase):
    def test_queue_cleaner(self):
        henri.coros.EQ = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        tools.AsyncTestRunner().run(henri.coros.queue_cleaner(10))
        self.assertEqual(henri.coros.EQ, [3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        self.assertEqual(len(henri.coros.EQ), 10)
