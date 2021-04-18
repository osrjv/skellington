from enum import IntEnum
from construct import (
    Bytes,
    Const,
    Container,
    FixedSized,
    GreedyBytes,
    IfThenElse,
    Long,
    Rebuild,
    Short,
    Struct,
    this,
    len_,
)
from skeltal.protocol.types import VarInt, VarString, Compressed


def build(threshold, packet_id, data):
    fields = Container(packet_id=packet_id, data=data)
    if threshold >= 0:
        size = VarInt.size(packet_id) + len(data)
        if size >= threshold:
            data = CompressedData.build(fields)
            fields = Container(data_length=size, data=data)
            return AboveThresholdMessage.build(fields)
        else:
            return BelowThresholdMessage.build(fields)
    else:
        return UncompressedMessage.build(fields)


class Handshaking(IntEnum):
    """Message IDs for Handshaking state."""

    Handshake = 0x00


class Status(IntEnum):
    """Message IDs for Status state."""

    Request = 0x00
    Ping = 0x01


class Login(IntEnum):
    """Message IDs for Login state."""

    LoginStart = 0x00
    EncryptionResponse = 0x01
    LoginPluginResponse = 0x02


class Play(IntEnum):
    """Message IDs for Play state."""

    TeleportConfirm = 0x00
    QueryBlockNBT = 0x01
    ChatMessage = 0x02
    ClientStatus = 0x03
    ClientSettings = 0x04
    TabComplete = 0x05
    ConfirmTransaction = 0x06
    EnchantItem = 0x07
    ClickWindow = 0x08
    CloseWindow = 0x09
    PluginMessage = 0x0A
    EditBook = 0x0B
    QueryEntityNBT = 0x0C
    UseEntity = 0x0D
    KeepAlive = 0x0E
    Player = 0x0F
    PlayerPosition = 0x10
    PlayerPositionAndLook = 0x11
    PlayerLook = 0x12
    VehicleMove = 0x13
    SteerBoat = 0x14
    PickItem = 0x15
    CraftRecipeRequest = 0x16
    PlayerAbilities = 0x17
    PlayerDigging = 0x18
    EntityAction = 0x19
    SteerVehicle = 0x1A
    RecipeBookData = 0x1B
    NameItem = 0x1C
    ResourcePackStatus = 0x1D
    AdvancementTab = 0x1E
    SelectTrade = 0x1F
    SetBeaconEffect = 0x20
    HeldItemChange = 0x21
    UpdateCommandBlock = 0x22
    UpdateCommandBlockMinecart = 0x23
    CreativeInventoryAction = 0x24
    UpdateStructureBlock = 0x25
    UpdateSign = 0x26
    Animation = 0x27
    Spectate = 0x28
    PlayerBlockPlacement = 0x29
    UseItem = 0x2A


# Containers

UncompressedMessage = Struct(
    "length" / Rebuild(VarInt, VarInt.size(this.packet_id) + len_(this.data)),
    "packet_id" / VarInt,
    "data" / Bytes(this.length - VarInt.size(this.packet_id)),
)


BelowThresholdMessage = Struct(
    "packet_length"
    / Rebuild(
        VarInt,
        VarInt.size(this.data_length) + VarInt.size(this.packet_id) + len_(this.data),
    ),
    "data_length" / Const(0, VarInt),
    "packet_id" / VarInt,
    "data" / GreedyBytes,
)

AboveThresholdMessage = Struct(
    "packet_length" / Rebuild(VarInt, VarInt.size(this.data_length) + len_(this.data)),
    "data_length" / VarInt,
    "data" / GreedyBytes,
)

CompressedData = Compressed(Struct("packet_id" / VarInt, "data" / GreedyBytes), "zlib")


# Handshaking

Handshake = Struct(
    "protocol_version" / VarInt,
    "server_address" / VarString,
    "server_port" / Short,
    "next_state" / VarInt,
)


# Status

Request = Struct()

Ping = Struct()


# Login

LoginStart = Struct("name" / VarString)

EncryptionResponse = Struct()

LoginPluginResponse = Struct()


# Play

TeleportConfirm = Struct()

QueryBlockNBT = Struct()

ChatMessage = Struct()

ClientStatus = Struct()

ClientSettings = Struct()

TabComplete = Struct()

ConfirmTransaction = Struct()

EnchantItem = Struct()

ClickWindow = Struct()

CloseWindow = Struct()

PluginMessage = Struct()

EditBook = Struct()

QueryEntityNBT = Struct()

UseEntity = Struct()

KeepAlive = Struct("id" / Long)

Player = Struct()

PlayerPosition = Struct()

PlayerPositionAndLook = Struct()

PlayerLook = Struct()

VehicleMove = Struct()

SteerBoat = Struct()

PickItem = Struct()

CraftRecipeRequest = Struct()

PlayerAbilities = Struct()

PlayerDigging = Struct()

EntityAction = Struct()

SteerVehicle = Struct()

RecipeBookData = Struct()

NameItem = Struct()

ResourcePackStatus = Struct()

AdvancementTab = Struct()

SelectTrade = Struct()

SetBeaconEffect = Struct()

HeldItemChange = Struct()

UpdateCommandBlock = Struct()

UpdateCommandBlockMinecart = Struct()

CreativeInventoryAction = Struct()

UpdateStructureBlock = Struct()

UpdateSign = Struct()

Animation = Struct()

Spectate = Struct()

PlayerBlockPlacement = Struct()

UseItem = Struct()
