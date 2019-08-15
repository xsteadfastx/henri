import sys
import unittest

import tools

sys.path.insert(0, "../src")
import henri  # isort:skip


class TestHenri(unittest.TestCase):
    def test_queue_cleaner(self):
        henri.EQ = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        tools.AsyncTestRunner().run(henri.queue_cleaner())
        self.assertEqual(henri.EQ, [3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        self.assertEqual(len(henri.EQ), 10)
