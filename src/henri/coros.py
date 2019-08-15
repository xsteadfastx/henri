import gc
import random

import uasyncio as asyncio
import ulogging as logging

from .app import EQ


async def event_filler():
    global EQ
    while True:
        EQ.append(random.randint(0, 100))
        logging.debug("queue: %s" % EQ)
        await asyncio.sleep(0.3)


async def janitor():
    while True:
        logging.debug("clean memory")
        gc.collect()
        logging.debug("clean EQ")
        if EQ and len(EQ) > 3:
            await queue_cleaner(3)
        await asyncio.sleep(5)


async def queue_cleaner(num):
    global EQ
    items_to_remove = len(EQ) - num
    del EQ[:items_to_remove]
