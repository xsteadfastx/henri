import picoweb
import uasyncio as asyncio
import ulogging as logging
from henri.app import APP
from henri.develop import process


@APP.route("/", methods=["GET", "POST"])
def index(req, resp):
    if req.method == "POST":
        yield from req.read_form_data()
        asyncio.get_event_loop().create_task(
            process(60, [60, 59, 58, 57, 56, 55, 54, 53, 52, 51, 50, 40, 30, 20, 10, 0])
        )
        print(req.form)
    yield from picoweb.start_response(resp)
    yield from APP.render_template(resp, "index.html")


@APP.route("/events")
def events(req, resp):
    logging.info("Event source %r connected", resp)
    yield from resp.awrite("HTTP/1.0 200 OK\r\n")
    yield from resp.awrite("Content-Type: text/event-stream\r\n")
    yield from resp.awrite("\r\n")
    try:
        while True:
            if APP.push_event:
                yield from resp.awrite("data: %s\n\n" % APP.push_event)
            yield from asyncio.sleep(0.1)
    except OSError:
        logging.info("Event source connection closed")
        yield from resp.aclose()
