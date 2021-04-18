import enum
import logging
from abc import ABC, abstractmethod
from construct.core import Container

from skeltal.protocol import clientbound, serverbound
from skeltal.protocol.state import State

LOGGER = logging.getLogger(__name__)


class Handler(ABC):
    def __init__(self, conn, events):
        self.conn = conn
        self.events = events

    @abstractmethod
    def start(self):
        """Called when state is changed."""
        raise NotImplemented

    @abstractmethod
    def handle(self, message):
        """Called when message is received."""
        raise NotImplemented


class Handshaking(Handler):
    def start(self):
        handshake = Container(
            _type=serverbound.Handshaking.Handshake,
            protocol_version=404,  # 1.13.2
            server_address=self.conn.address,
            server_port=self.conn.port,
            next_state=State.Login,
        )
        self.conn.dispatch(handshake)
        self.conn.state(State.Login)

    def handle(self, message):
        raise RuntimeError(f"Unexpected message during handshake: {message}")


class Status(Handler):
    def start(self):
        raise NotImplemented

    def handler(self, message):
        raise NotImplemented


class Login(Handler):
    def start(self):
        login = Container(_type=serverbound.Login.LoginStart, name="testuser")
        self.conn.dispatch(login)

    def handle(self, message):
        if message._type is clientbound.Login.SetCompression:
            self.conn.compression = message.threshold

        if message._type is clientbound.Login.LoginSuccess:
            self.conn.state(State.Play)


class Play(Handler):
    def start(self):
        # TODO: Subscribe to all serverbound messages
        pass

    def handle(self, message):
        if message._type == clientbound.Play.Disconnect:
            LOGGER.warn("Disconnected by server: %s", message.reason)
            self.conn.stop()

        if message._type == clientbound.Play.KeepAlive:
            LOGGER.debug("Heartbeat (id: %s)", message.id)
            response = Container(_type=serverbound.Play.KeepAlive, id=message.id)
            self.conn.dispatch(response)

        self.events.publish(message)


HANDLERS = {
    State.Handshaking: Handshaking,
    State.Status: Status,
    State.Login: Login,
    State.Play: Play,
}
