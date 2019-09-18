import gc

import uasyncio as asyncio
from henri import coros, views
from henri.app import APP


def main(**params):
    gc.collect()
    import ulogging as logging

    logging.basicConfig(level=logging.DEBUG)

    # Preload templates to avoid memory fragmentation issues
    gc.collect()
    APP._load_template("index.html")
    gc.collect()

    import micropython

    micropython.mem_info()

    loop = asyncio.get_event_loop()
    # loop.create_task(coros.event_filler())
    loop.create_task(coros.janitor())
    APP.run(debug=True, **params)
