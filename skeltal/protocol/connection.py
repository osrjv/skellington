import logging
import select
import socket
import threading
from construct import StreamError

from skeltal.protocol import clientbound, serverbound
from skeltal.protocol.handlers import HANDLERS
from skeltal.protocol.queue import SelectQueue
from skeltal.protocol.state import State

LOGGER = logging.getLogger(__name__)


class ClientConnection:
    SENTINEL = object()

    def __init__(self, address, port, registry):
        self.address = str(address)
        self.port = int(port)
        self.registry = registry

        self._thread = threading.Thread(target=self._connection_loop)
        self._state = None
        self._handler = None
        self._compression = -1
        self._stop = False

        self._queue = SelectQueue()
        self._socket = None
        self._stream = None

    @property
    def is_connected(self):
        return self._thread.is_alive()

    @property
    def compression(self):
        return self._compression

    @compression.setter
    def compression(self, value):
        self._compression = value
        LOGGER.debug(
            "%s compression (threshold: %s)",
            "Enabling" if value >= 0 else "Disabling",
            value,
        )

    def state(self, value):
        assert value in State, f"Invalid state: {value}"
        if self._state is not None:
            LOGGER.debug("Client state '%s' -> '%s'", self._state, value)
        else:
            LOGGER.debug("Client state '%s'", value)

        self._state = value
        self._handler = HANDLERS[value](self)
        self._handler.send(None)  # Prime generator

    def start(self):
        assert not self.is_connected, "Client already connected"

        LOGGER.info("Connecting to %s:%d", self.address, self.port)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self.address, self.port))

        self._stream = self._socket.makefile(mode="b")
        self._thread.start()

        self.state(State.HANDSHAKING)

    def stop(self):
        if not self._stop:
            self._stop = True
            self._queue.put(self.SENTINEL)

    def shutdown(self):
        LOGGER.info("Closing connection")

        try:
            self.stop()
            if self._thread.is_alive():
                self._thread.join(timeout=10)

        finally:
            if self._stream:
                self._stream.close()
            if self._socket:
                self._socket.close()
            self._queue.close()

    def dispatch(self, message):
        if not self.is_connected:
            raise RuntimeError("Client not connected")

        types = {
            State.HANDSHAKING: serverbound.Handshaking,
            State.STATUS: serverbound.Status,
            State.LOGIN: serverbound.Login,
            State.PLAY: serverbound.Play,
        }[self._state]

        LOGGER.trace("TX: %s", message._type)

        packet_id = message._type.value
        builder = getattr(serverbound, message._type.name)
        data = builder.build(message)

        self._queue.put((packet_id, data))

    def receive(self, packet_id, data):
        types = {
            State.HANDSHAKING: clientbound.Handshaking,
            State.STATUS: clientbound.Status,
            State.LOGIN: clientbound.Login,
            State.PLAY: clientbound.Play,
        }[self._state]

        message_type = types(packet_id)
        LOGGER.trace("RX: %s", message_type)

        parser = getattr(clientbound, message_type.name)
        message = parser.parse(data)
        message._type = message_type

        self._handler.send(message)

    def _connection_loop(self):
        while True:
            rlist, _, _ = select.select([self._socket, self._queue], [], [])
            if self._stop:
                break

            for sock in rlist:
                if sock is self._socket:
                    self._recv()
                elif sock is self._queue:
                    self._send()
                else:
                    raise RuntimeError(f"Unexpected readable socket: {sock}")

    def _recv(self):
        try:
            packet_id, data = clientbound.parse_stream(self._compression, self._stream)
            self.receive(packet_id, data)
        except StreamError as err:
            LOGGER.error("Failed to parse incoming message: %s", err)
            self._stop = True

    def _send(self):
        packet_id, data = self._queue.get()
        try:
            packet = serverbound.build(self._compression, packet_id, data)
            self._socket.sendall(packet)
        finally:
            self._queue.task_done()
