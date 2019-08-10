import sys
import unittest

import tools
import uasyncio as asyncio

sys.path.insert(0, "../src")
import foobar  # isort:skip


class TestFoobar(unittest.TestCase):
    def test_foo(self):
        self.assertEqual(tools.AsyncTestRunner().run(foobar.foo()), "bar")


if __name__ == "__main__":
    unittest.main()
