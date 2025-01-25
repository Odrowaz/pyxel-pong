from enum import IntEnum
import struct

class PacketType(IntEnum):
    ALIVE = 1
    POSITION = 2
    POINT = 3
    REQUEST_ID = 4
    SPAWN = 5