import sys
import unittest

sys.path.insert(0, "tests")
sys.path.insert(0, "src")

TESTS = ["test_foobar"]

for test in TESTS:
    m = __import__(test)
    unittest.main(module=m)
