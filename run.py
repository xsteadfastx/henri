import sys

import ulogging as logging

sys.path.insert(0, "src/")
import henri.__main__  # isort:skip

logging.basicConfig(level=logging.DEBUG)
henri.__main__.main(port="8180")
