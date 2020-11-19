import pytest
from construct import Construct
from skeltal.protocol.types import VarInt

VARINT = [
    (0, [0x00]),
    (1, [0x01]),
    (2, [0x02]),
    (127, [0x7F]),
    (128, [0x80, 0x01]),
    (255, [0xFF, 0x01]),
    (2147483647, [0xFF, 0xFF, 0xFF, 0xFF, 0x07]),
    (-1, [0xFF, 0xFF, 0xFF, 0xFF, 0x0F]),
    (-2147483648, [0x80, 0x80, 0x80, 0x80, 0x08]),
]


@pytest.mark.parametrize("value, data", VARINT)
def test_varint_build(value, data):
    assert VarInt.build(value) == bytes(data)


@pytest.mark.parametrize("value, data", VARINT)
def test_varint_parse(value, data):
    assert VarInt.parse(bytes(data)) == value


@pytest.mark.parametrize("value, data", VARINT)
def test_varint_sizeof(value, data):
    assert VarInt.bytesize(value) == len(data)
