import sys

import ulogging as logging

sys.path.insert(0, "src/")
import henri  # isort:skip

logging.basicConfig(level=logging.DEBUG)
henri.run(port="8180")
