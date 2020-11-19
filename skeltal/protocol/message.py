from construct import (
    Bytes,
    Compressed,
    FixedSized,
    GreedyBytes,
    IfThenElse,
    Rebuild,
    Struct,
    this,
    len_,
)

from skeltal.protocol.types import VarInt


def size_(field):
    return VarInt.bytesize(field)


UncompressedMessage = Struct(
    "length" / Rebuild(VarInt, size_(this.packet_id) + len_(this.data)),
    "packet_id" / VarInt,
    "data" / Bytes(this.length - size_(this.packet_id)),
)

CompressedMessage = Struct(
    "packet_length" / Rebuild(VarInt, size_(this.data_length) + len_(this.compressed)),
    "data_length" / VarInt,
    "compressed"
    / FixedSized(
        lambda this: this.packet_length - size_(this.data_length),
        IfThenElse(
            this.data_length > 0,
            Compressed(Struct("packet_id" / VarInt, "data" / GreedyBytes), "zlib"),
            Struct("packet_id" / VarInt, "data" / GreedyBytes),
        ),
    ),
)
