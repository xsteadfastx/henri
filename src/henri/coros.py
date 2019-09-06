import gc
import random

import uasyncio as asyncio
import ulogging as logging
from henri.app import APP


async def event_filler():
    while True:
        APP.push_event = random.randint(0, 100)
        logging.debug("queue: %s" % APP.push_event)
        await asyncio.sleep(0.3)


async def janitor():
    while True:
        logging.debug("clean memory")
        gc.collect()
        await asyncio.sleep(5)
