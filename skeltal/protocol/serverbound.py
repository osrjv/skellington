from enum import IntEnum
from construct import Struct, Short
from skeltal.protocol.types import VarInt, VarString


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


Handshake = Struct(
    "protocol_version" / VarInt,
    "server_address" / VarString,
    "server_port" / Short,
    "next_state" / VarInt,
)

LoginStart = Struct("name" / VarString)
