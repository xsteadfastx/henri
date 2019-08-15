import gc
import random

import picoweb
import uasyncio as asyncio
import ulogging as logging

EQ = []


def create_ap():
    import network

    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid="henri")
    ap.ifconfig(("192.168.95.1", "255.255.255.0", "192.168.95.1", "192.168.95.1"))


def index(req, resp):
    yield from picoweb.start_response(resp)
    yield from resp.awrite(
        """\
<!DOCTYPE html>
<html>
<head>
<script>
var source = new EventSource("events");
source.onmessage = function(event) {
    document.getElementById("result").innerHTML = event.data + "<br>";
}
source.onerror = function(error) {
    console.log(error);
    document.getElementById("result").innerHTML += "EventSource error:" + error + "<br>";
}
</script>
</head>
<body>
<div id="result"></div>
</body>
</html>
"""
    )


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
        if EQ and len(EQ) > 10:
            await queue_cleaner()
        await asyncio.sleep(5)


async def queue_cleaner():
    global EQ
    items_to_remove = len(EQ) - 10
    del EQ[:items_to_remove]


def events(req, resp):
    """Serving events."""
    global EQ
    logging.info("Event source %r connected", resp)
    yield from resp.awrite("HTTP/1.0 200 OK\r\n")
    yield from resp.awrite("Content-Type: text/event-stream\r\n")
    yield from resp.awrite("\r\n")
    try:
        while True:
            if EQ:
                yield from resp.awrite("data: %s\n\n" % EQ.pop())
            yield from asyncio.sleep(0.1)
    except OSError:
        logging.info("Event source connection closed")
        yield from resp.aclose()


def run(host="0.0.0.0", port="80"):
    """Run webserver."""
    loop = asyncio.get_event_loop()
    loop.create_task(janitor())
    loop.create_task(event_filler())
    url_map = [("/", index), ("/events", events)]
    app = picoweb.WebApp(__name__, url_map)
    app.run(host=host, port=port, debug=True)
