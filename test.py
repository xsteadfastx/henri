import sys
import unittest

sys.path.insert(0, "tests")
sys.path.insert(0, "src")

TESTS = ["test_foobar", "test_henri"]
FAILURES_NUM = 0

for test in TESTS:
    try:
        m = __import__(test)
        unittest.main(module=m)
    except BaseException:
        FAILURES_NUM += 1

sys.exit(FAILURES_NUM > 0)
