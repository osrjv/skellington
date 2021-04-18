import enum


class State(enum.IntEnum):
    HANDSHAKING = 0x00
    STATUS = 0x01
    LOGIN = 0x02
    PLAY = 0x03
