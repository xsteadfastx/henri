import gc

import uasyncio as asyncio
import ulogging as logging
from henri.app import APP


async def janitor():
    while True:
        logging.debug("clean memory")
        gc.collect()
        await asyncio.sleep(5)
