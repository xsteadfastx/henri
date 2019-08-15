import sys
import unittest

sys.path.insert(0, "tests")
sys.path.insert(0, "src")

TESTS = ["test_henri"]
FAILURES_NUM = 0

for test in TESTS:
    try:
        m = __import__(test)
        unittest.main(module=m)
    except SystemExit as e:
        if str(e) == "True":
            FAILURES_NUM += 1

if FAILURES_NUM > 0:
    sys.exit(1)
