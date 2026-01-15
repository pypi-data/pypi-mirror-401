"""Platform aware user session identifier helpers."""

from bclearer_core.infrastructure.session.common.enums.operating_system_kind import (
    OperatingSystemKind,
)
from bclearer_core.infrastructure.session.common.platform_type_getter import (
    get_operating_system_kind,
)
from bclearer_core.infrastructure.session.os_user_session.helpers.unix.unix_session_identifier import (
    get_unix_session_id,
)


def get_os_user_session_id() -> int:
    operating_system_kind = (
        get_operating_system_kind()
    )

    if (
        operating_system_kind
        is OperatingSystemKind.WINDOWS
    ):
        from bclearer_core.infrastructure.session.os_user_session.helpers.windows.windows_user_session_id_getter import (
            get_windows_user_session_id,
        )

        return (
            get_windows_user_session_id()
        )

    return get_unix_session_id()
