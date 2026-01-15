"""Unix specific account context helpers."""

import os
from typing import Tuple

from bclearer_core.infrastructure.session.common.session_config import (
    UNIX_ADMIN_ACCOUNT_TYPE,
    UNIX_DEFAULT_DOMAIN_NAME,
    UNIX_STANDARD_ACCOUNT_TYPE,
)

try:
    import pwd
except (
    ImportError
):  # pragma: no cover - platforms without pwd
    pwd = None


def get_unix_account_context() -> (
    Tuple[str, str]
):
    if pwd:
        try:
            user_info = pwd.getpwuid(
                os.getuid()
            )
        except KeyError:
            user_info = None
    else:
        user_info = None

    full_name = ""
    if user_info and user_info.pw_gecos:
        full_name = (
            user_info.pw_gecos.split(
                ","
            )[0].strip()
        )

    domain_name = (
        full_name
        or UNIX_DEFAULT_DOMAIN_NAME
    )
    account_type = (
        UNIX_ADMIN_ACCOUNT_TYPE
        if os.getuid() == 0
        else UNIX_STANDARD_ACCOUNT_TYPE
    )

    return domain_name, account_type
