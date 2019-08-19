import network
import tinydns


def create_ap():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid="henri")
    ap.ifconfig(("192.168.95.1", "255.255.255.0", "192.168.95.1", "192.168.95.1"))


def create_dns():
    dns = tinydns.Server(domains={"henri.processor": "192.168.95.1"})
    dns.run(host="192.168.95.1", port=53)
