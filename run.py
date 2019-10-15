import sys

import uasyncio as asyncio
import ulogging as logging
import umock

sys.path.insert(0, "src/")
import henri.__main__  # isort:skip
import henri.develop  # isort:skip


async def mock_agitate():
    logging.debug("THIS IS A SIMULATED AGITATION")
    await asyncio.sleep(1)


logging.basicConfig(level=logging.DEBUG)
with umock.MonkeyPatch(henri.develop, "agitate", mock_agitate):
    henri.__main__.main(port="8180")
