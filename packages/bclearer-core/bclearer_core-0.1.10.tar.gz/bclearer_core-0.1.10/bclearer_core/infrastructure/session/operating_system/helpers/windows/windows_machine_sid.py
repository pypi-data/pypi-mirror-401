"""Windows-specific helpers for machine identification."""

import ctypes

from bclearer_core.infrastructure.session.common.session_config import (
    WINDOWS_BUILTIN_ADMINISTRATORS_SID,
    WINDOWS_SECURITY_MAX_SID_SIZE,
)


# TODO: Harmonise file and public method name (and internal variable names)
def get_windows_machine_sid() -> str:
    sid = ctypes.create_string_buffer(
        WINDOWS_SECURITY_MAX_SID_SIZE
    )
    sid_size = ctypes.c_ulong(
        WINDOWS_SECURITY_MAX_SID_SIZE
    )

    if not ctypes.windll.advapi32.CreateWellKnownSid(
        WINDOWS_BUILTIN_ADMINISTRATORS_SID,
        None,
        sid,
        ctypes.byref(sid_size),
    ):
        raise ctypes.WinError()

    sid_string = ctypes.c_wchar_p()

    if not ctypes.windll.advapi32.ConvertSidToStringSidW(
        sid, ctypes.byref(sid_string)
    ):
        raise ctypes.WinError()

    machine_sid = (
        sid_string.value.rsplit("-", 1)[
            0
        ]
    )
    ctypes.windll.kernel32.LocalFree(
        sid_string
    )

    return machine_sid
