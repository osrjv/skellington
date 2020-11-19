from itertools import count
from construct.core import stream_read, stream_write, singleton
from construct import Construct, PascalString, int2byte, byte2int


@singleton
class VarInt(Construct):
    """Minecraft-specific 32bit signed VarInt type."""

    BITS = 32
    MAX_SIZE = 5

    @classmethod
    def bytesize(cls, value):
        """Calculate bytesize of integer as VarInt."""
        if value == 0:
            return 1

        if value < 0:
            value += 2 ** cls.BITS

        idx = 0
        while value:
            value >>= 7
            idx += 1

        return idx

    def _parse(self, stream, context, path):
        result = 0

        for idx in count():
            read = byte2int(stream_read(stream, 1, path))
            value = read & 0b01111111
            result |= value << (7 * idx)

            if not read & 0b10000000:
                break
            if idx >= self.MAX_SIZE:
                raise ValueError("VarInt larger than expected")

        # Convert from unsigned to signed
        if result & (1 << (self.BITS - 1)):
            result -= 2 ** self.BITS

        return result

    def _build(self, obj, stream, context, path):
        value = obj

        # Convert from signed to unsigned
        if value < 0:
            value += 2 ** self.BITS

        for idx in count():
            temp = value & 0b01111111
            value >>= 7
            if value:
                temp |= 0b10000000
            stream_write(stream, int2byte(temp), 1, path)

            if not value:
                break
            if idx >= self.MAX_SIZE:
                raise ValueError("VarInt larger than expected")

        return obj


VarString = PascalString(VarInt, "utf8")
