"""Windows-specific helpers for OS user session identifiers."""

import ctypes


def get_windows_user_session_id() -> (
    int
):
    wts_get_active_console_session_id = (
        ctypes.windll.kernel32.WTSGetActiveConsoleSessionId
    )

    return (
        wts_get_active_console_session_id()
    )
