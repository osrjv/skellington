import enum
import logging
import select
import socket
import threading
from construct import StreamError

from skeltal.protocol import clientbound, serverbound
from skeltal.protocol.message import UncompressedMessage, CompressedMessage
from skeltal.protocol.queue import SelectQueue

LOGGER = logging.getLogger(__name__)


class State(enum.IntEnum):
    HANDSHAKING = 0x00
    STATUS = 0x01
    LOGIN = 0x02
    PLAY = 0x03


def login(conn):
    handshake = {
        "type": "Handshake",
        "protocol_version": 404,
        "server_address": conn.address,
        "server_port": conn.port,
        "next_state": State.LOGIN,
    }
    conn.dispatch(handshake)
    conn.state(State.LOGIN)
    login = {
        "type": "LoginStart",
        "name": "testuser",
    }
    conn.dispatch(login)
    yield


class ClientConnection:
    SENTINEL = object()

    def __init__(self, address, port, registry):
        self.address = str(address)
        self.port = int(port)
        self.registry = registry

        self._thread = threading.Thread(target=self._connection_loop)
        self._state = State.HANDSHAKING
        self._compression = False
        self._stop = False

        self._queue = SelectQueue()
        self._socket = None
        self._stream = None

    @property
    def is_connected(self):
        return self._thread.is_alive()

    def state(self, value):
        assert value in State, f"Invalid state: {value}"
        LOGGER.info("Client state '%s' -> '%s'", self._state, value)
        self._state = value

    def start(self):
        assert not self.is_connected, "Client already connected"

        LOGGER.info("Connecting to %s:%d", self.address, self.port)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self.address, self.port))

        self._stream = self._socket.makefile(mode="b")
        self._thread.start()

    def stop(self):
        try:
            self._stop = True
            self._queue.put(self.SENTINEL)
            self._thread.join(timeout=10)
        finally:
            self._stream.close()
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

        message_type = message.pop("type")
        builder = getattr(serverbound, str(message_type))

        LOGGER.debug("TX: %s", message_type)

        packet_id = types[message_type]
        data = builder.build(message)

        self._queue.put({"packet_id": packet_id, "data": data})

    def receive(self, packet_id, data):
        types = {
            State.HANDSHAKING: clientbound.Handshaking,
            State.STATUS: clientbound.Status,
            State.LOGIN: clientbound.Login,
            State.PLAY: clientbound.Play,
        }[self._state]

        message_type = types(packet_id)
        LOGGER.debug("RX: %s", message_type)

        if str(message_type) == "Login.SetCompression":
            self._compression = True
        if str(message_type) == "Login.LoginSuccess":
            self.state(State.PLAY)

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
            if self._compression:
                msg = CompressedMessage.parse_stream(self._stream)
                self.receive(msg.compressed.packet_id, msg.compressed.data)
            else:
                msg = UncompressedMessage.parse_stream(self._stream)
                self.receive(msg.packet_id, msg.data)
        except StreamError as err:
            LOGGER.error("Failed to incoming parse message: %s", err)
            self._stop = True

    def _send(self):
        msg = self._queue.get()
        try:
            packet = UncompressedMessage.build(msg)
            self._socket.sendall(packet)
        finally:
            self._queue.task_done()
