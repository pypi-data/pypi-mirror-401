"""Unix specific helpers for user session identifiers."""

import os


def get_unix_session_id() -> int:
    if hasattr(os, "getsid"):
        try:
            return os.getsid(0)
        except OSError:
            pass

    return os.getpid()
