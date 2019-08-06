import config
import network
import picoweb
import uasyncio as asyncio
import ulogging as logging


def do_connect():
    """Connect to existing AP."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("connecting to network...")
        wlan.connect(config.WIFI_ESSID, config.WIFI_PASSWORD)
        while not wlan.isconnected():
            pass
        print("network config: ", wlan.ifconfig())


class Henri:
    """We love you Henri Cartier-Bresson."""

    def __init__(self):
        self.ap_ip = "192.168.95.1"
        self.push_queue = set()
        self.app = picoweb.WebApp(__name__)

    def create_ap(self):
        """Create AP for client to connect to."""
        access_point = network.WLAN(network.AP_IF)
        access_point.active(True)
        access_point.config(essid="henri")
        access_point.ifconfig((self.ap_ip, "255.255.255.0", self.ap_ip, self.ap_ip))

    def index(self, req, resp):  # pylint: disable=unused-argument,no-self-use
        """Serving index site."""
        await picoweb.start_response(resp)
        await resp.awrite(
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

    def events(self, req, resp):
        """Serving events."""
        logging.info("Event source %r connected", resp)
        await resp.awrite("HTTP/1.0 200 OK\r\n")
        await resp.awrite("Content-Type: text/event-stream\r\n")
        await resp.awrite("\r\n")
        i = 0
        try:
            while True:
                await resp.awrite("data: %d\n\n" % i)
                await asyncio.sleep(1)
                i += 1
        except OSError:
            logging.info("Event source connection closed")
            await resp.aclose()

    def run(self):
        """Run webserver."""
        self.app.url_map = [("/", self.index), ("/events", self.events)]
        self.app.run(host="0.0.0.0", port="80", debug=True)
