import picoweb
import uasyncio as asyncio
import ulogging as logging
from henri.app import APP
from henri.develop import create_agitate_list, process


@APP.route("/", methods=["GET", "POST"])
def index(req, resp):
    if req.method == "POST":
        yield from req.read_form_data()
        logging.debug(req.form)
        complete_seconds = int(req.form["full_process_time"]) * 60
        recur_interval = int(req.form["recur_interval"])
        agitate_list = yield from create_agitate_list(complete_seconds, recur_interval)
        # yield from APP.render_template(resp, "develop.html")
        yield from process(complete_seconds, agitate_list)
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
