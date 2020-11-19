from enum import IntEnum
from construct import Struct, Bytes
from skeltal.protocol.types import VarInt


class Handshaking(IntEnum):
    """Message IDs for Handshaking state."""


class Status(IntEnum):
    """Message IDs for Status state."""

    Response = 0x00
    Pong = 0x01


class Login(IntEnum):
    """Message IDs for Login state."""

    Disconnect = 0x00
    EncryptionRequest = 0x01
    LoginSuccess = 0x02
    SetCompression = 0x03
    LoginPluginRequest = 0x04


class Play(IntEnum):
    """Message IDs for Play state."""

    SpawnObject = 0x00
    SpawnExperienceOrb = 0x01
    SpawnGlobalEntity = 0x02
    SpawnMob = 0x03
    SpawnPainting = 0x04
    SpawnPlayer = 0x05
    Animation = 0x06
    Statistics = 0x07
    BlockBreakAnimation = 0x08
    UpdateBlockEntity = 0x09
    BlockAction = 0x0A
    BlockChange = 0x0B
    BossBar = 0x0C
    ServerDifficulty = 0x0D
    ChatMessage = 0x0E
    MultiBlockChange = 0x0F
    TabComplete = 0x10
    DeclareCommands = 0x11
    ConfirmTransaction = 0x12
    CloseWindow = 0x13
    OpenWindow = 0x14
    WindowItems = 0x15
    WindowProperty = 0x16
    SetSlot = 0x17
    SetCooldown = 0x18
    PluginMessage = 0x19
    NamedSoundEffect = 0x1A
    Disconnect = 0x1B
    EntityStatus = 0x1C
    NBTQueryResponse = 0x1D
    Explosion = 0x1E
    UnloadChunk = 0x1F
    ChangeGameState = 0x20
    KeepAlive = 0x21
    ChunkData = 0x22
    Effect = 0x23
    Particle = 0x24
    JoinGame = 0x25
    MapData = 0x26
    Entity = 0x27
    EntityRelativeMove = 0x28
    EntityLookAndRelativeMove = 0x29
    EntityLook = 0x2A
    VehicleMove = 0x2B
    OpenSignEditor = 0x2C
    CraftRecipeResponse = 0x2D
    PlayerAbilities = 0x2E
    CombatEvent = 0x2F
    PlayerInfo = 0x30
    FacePlayer = 0x31
    PlayerPositionAndLook = 0x32
    UseBed = 0x33
    UnlockRecipes = 0x34
    DestroyEntities = 0x35
    RemoveEntityEffect = 0x36
    ResourcePackSend = 0x37
    Respawn = 0x38
    EntityHeadLook = 0x39
    SelectAdvancementTab = 0x3A
    WorldBorder = 0x3B
    Camera = 0x3C
    HeldItemChange = 0x3D
    DisplayScoreboard = 0x3E
    EntityMetadata = 0x3F
    AttachEntity = 0x40
    EntityVelocity = 0x41
    EntityEquipment = 0x42
    SetExperience = 0x43
    UpdateHealth = 0x44
    ScoreboardObjective = 0x45
    SetPassengers = 0x46
    Teams = 0x47
    UpdateScore = 0x48
    SpawnPosition = 0x49
    TimeUpdate = 0x4A
    Title = 0x4B
    StopSound = 0x4C
    SoundEffect = 0x4D
    PlayerListHeaderAndFooter = 0x4E
    CollectItem = 0x4F
    EntityTeleport = 0x50
    Advancements = 0x51
    EntityProperties = 0x52
    EntityEffect = 0x53
    DeclareRecipes = 0x54
    Tags = 0x55