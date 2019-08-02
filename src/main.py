import config
import network


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


def create_ap():
    """Create AP for client to connect to."""
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid="henri")
    ap.ifconfig(("192.168.95.1", "255.255.255.0", "192.168.95.1", "192.168.95.1"))


create_ap()
