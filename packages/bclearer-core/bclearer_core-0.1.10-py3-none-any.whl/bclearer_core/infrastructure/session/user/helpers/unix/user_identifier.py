"""Unix specific helpers for retrieving user identifiers."""

import os


def get_unix_user_sid() -> str:
    return str(os.getuid())
