"""Helpers for determining the current operating system as an enum."""

import platform

from bclearer_core.infrastructure.session.common.enums.operating_system_kind import (
    OperatingSystemKind,
)


# TODO: Harmonise file and public method name (and internal variable names)
def get_operating_system_kind() -> (
    OperatingSystemKind
):
    system_name = platform.system()

    if system_name == "Windows":
        return (
            OperatingSystemKind.WINDOWS
        )

    if system_name == "Linux":
        return OperatingSystemKind.LINUX

    if system_name == "Darwin":
        return OperatingSystemKind.MACOS

    return OperatingSystemKind.UNKNOWN
