"""Enumeration of supported operating system kinds."""

from enum import Enum, auto


# TODO 20251002 - should this be a subclass of BEnums or BieEnums???
class OperatingSystemKind(Enum):
    WINDOWS = auto()
    LINUX = auto()
    MACOS = auto()
    UNKNOWN = auto()
