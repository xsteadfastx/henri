try:
    import machine

    PIN = machine.Pin(26)
    SERVO = machine.PWM(PIN, freq=50)
except ImportError:
    PIN = None
    SERVO = None

import uasyncio as asyncio
import ulogging as logging
from henri.app import APP


async def agitate():
    logging.info("moving servo motor")
    SERVO.duty(1)
    await asyncio.sleep(0.5)
    SERVO.duty(130)
    await asyncio.sleep(0.5)


async def process(seconds, agitate_list, agitate_generator, sleep_generator):
    """Negative process runner.

    Args:
        seconds (int): Full process seconds.
        agitate_list (list): List with seconds on which to agitate.
        agitate_generator (generator): The async generator that agitates the servo.
        sleep_generator (generator): Normally the uasyncio.sleep generator.

    """
    counter = seconds
    while counter != 0:
        logging.debug("second: {}".format(counter))
        if counter in agitate_list:
            APP.push_event = "AGITATE!"
            await agitate_generator()
            logging.debug("AGITATE")
        else:
            APP.push_event = str(counter)
            await sleep_generator(1)
        counter -= 1
    APP.push_event = "DONE"


async def create_agitate_list(complete_seconds, recur_interval):
    """Creates a agitate list object.

    Args:
        complete_seconds (int): Full development time.
        recur_interval (int): After the full minute agitation this needs to be 60 or
            30 seconds.

    Returns:
        list: A list contains seconds on which a agitation accures.

    """
    agitate_list = list(reversed(range(complete_seconds - 60, complete_seconds)))
    counter = complete_seconds - 60 - recur_interval
    while counter != 0:
        agitate_list.extend(list(reversed(range(counter - 10, counter))))
        counter -= recur_interval

    return agitate_list
