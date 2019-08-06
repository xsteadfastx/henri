import ulogging as logging
from henri import Henri

logging.basicConfig(level=logging.DEBUG)

HENRI = Henri()
HENRI.create_ap()
HENRI.run()
