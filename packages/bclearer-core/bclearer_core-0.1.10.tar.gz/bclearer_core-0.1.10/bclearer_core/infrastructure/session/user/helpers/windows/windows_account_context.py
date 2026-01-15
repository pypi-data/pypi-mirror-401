"""Windows specific account context helpers."""

from typing import Tuple

from bclearer_core.infrastructure.session.user.helpers.windows.security import (
    lookup_account_sid,
    translate_account_type,
)


def get_windows_account_context(
    user_sid,
) -> Tuple[str, str]:
    (
        account_name,
        domain_name,
        account_type_value,
    ) = lookup_account_sid(user_sid)

    account_type = translate_account_type(
        account_type_value=account_type_value
    )

    return (
        domain_name or account_name,
        account_type,
    )
