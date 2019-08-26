import gc
import random

import henri.app
import uasyncio as asyncio
import ulogging as logging


async def event_filler():
    while True:
        henri.app.EQ = random.randint(0, 100)
        logging.debug("queue: %s" % henri.app.EQ)
        await asyncio.sleep(0.3)


async def janitor():
    while True:
        logging.debug("clean memory")
        gc.collect()
        await asyncio.sleep(5)
