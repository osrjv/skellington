import logging
from construct.core import Container
from skeltal.protocol import clientbound, serverbound
from skeltal.protocol.state import State

LOGGER = logging.getLogger(__name__)


def handshaking(connection):
    handshake = Container(
        _type=serverbound.Handshaking.Handshake,
        protocol_version=404,
        server_address=connection.address,
        server_port=connection.port,
        next_state=State.LOGIN,
    )
    connection.dispatch(handshake)
    connection.state(State.LOGIN)
    yield


def status(connection):
    raise NotImplementedError


def login(connection):
    login = Container(_type=serverbound.Login.LoginStart, name="testuser")
    connection.dispatch(login)

    while True:
        message = yield

        if message._type is clientbound.Login.SetCompression:
            connection.compression = message.threshold

        if message._type is clientbound.Login.LoginSuccess:
            connection.state(State.PLAY)


def play(connection):
    while True:
        message = yield

        if message._type == clientbound.Play.Disconnect:
            LOGGER.warn("Disconnected by server: %s", message.reason)
            connection.stop()

        if message._type == clientbound.Play.KeepAlive:
            LOGGER.debug("Heartbeat (id: %s)", message.id)
            response = Container(_type=serverbound.Play.KeepAlive, id=message.id)
            connection.dispatch(response)

        connection.registry.publish(message)


HANDLERS = {
    State.HANDSHAKING: handshaking,
    State.STATUS: status,
    State.LOGIN: login,
    State.PLAY: play,
}
