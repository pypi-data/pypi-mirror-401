"""Windows specific helpers related to user security information."""

import ctypes

import win32security
from bclearer_core.infrastructure.session.common.session_config import (
    UNIX_ADMIN_ACCOUNT_TYPE,
    UNIX_STANDARD_ACCOUNT_TYPE,
)


# TODO: Only have one public method per py file
def get_windows_user_sid():
    token = win32security.OpenProcessToken(
        ctypes.windll.kernel32.GetCurrentProcess(),
        win32security.TOKEN_QUERY,
    )

    user_info = win32security.GetTokenInformation(
        token, win32security.TokenUser
    )

    return user_info[0]


# TODO: where should this be?
def lookup_account_sid(user_sid):
    return (
        win32security.LookupAccountSid(
            None, user_sid
        )
    )


# TODO: should UNIX be in this
def translate_account_type(
    account_type_value,
):
    return (
        UNIX_ADMIN_ACCOUNT_TYPE
        if account_type_value
        == win32security.SidTypeUser
        else UNIX_STANDARD_ACCOUNT_TYPE
    )
