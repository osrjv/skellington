import time
from skeltal.events import EventsRegistry
from skeltal.protocol.connection import ClientConnection


class Bot:
    def __init__(self, address, port):
        self.registry = EventsRegistry()
        self.client = ClientConnection(address, port, self.registry)

    def run_forever(self):
        self.client.start()
        while self.client.is_connected:
            time.sleep(1)

    def shutdown(self):
        self.client.stop()
