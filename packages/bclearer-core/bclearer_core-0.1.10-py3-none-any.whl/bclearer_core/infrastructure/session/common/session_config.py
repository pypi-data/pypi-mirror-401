"""Configuration constants for infrastructure session helpers."""

from pathlib import Path

WINDOWS_SECURITY_MAX_SID_SIZE = 68
WINDOWS_BUILTIN_ADMINISTRATORS_SID = 26

LINUX_MACHINE_ID_PATHS = (
    Path("/etc/machine-id"),
    Path("/var/lib/dbus/machine-id"),
)
LINUX_MACHINE_ID_FALLBACK_PREFIX = (
    "linux-mac-"
)

MACOS_IOREG_COMMAND = [
    "ioreg",
    "-rd1",
    "-c",
    "IOPlatformExpertDevice",
]
MACOS_IOREG_UUID_PATTERN = (
    r'"IOPlatformUUID" = "([^"]+)"'
)
MACOS_MACHINE_FALLBACK_PREFIX = (
    "macos-mac-"
)

UNKNOWN_MACHINE_FALLBACK_PREFIX = (
    "unknown-machine-"
)

UNIX_DEFAULT_DOMAIN_NAME = "LOCAL"
UNIX_ADMIN_ACCOUNT_TYPE = (
    "Administrator"
)
UNIX_STANDARD_ACCOUNT_TYPE = "User"
