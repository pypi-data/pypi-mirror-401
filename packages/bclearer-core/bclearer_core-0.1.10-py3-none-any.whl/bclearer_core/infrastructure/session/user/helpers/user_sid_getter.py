from bclearer_core.infrastructure.session.common.enums.operating_system_kind import (
    OperatingSystemKind,
)
from bclearer_core.infrastructure.session.common.platform_type_getter import (
    get_operating_system_kind,
)
from bclearer_core.infrastructure.session.user.helpers.unix.user_identifier import (
    get_unix_user_sid,
)


def get_user_sid():
    operating_system_kind = (
        get_operating_system_kind()
    )

    if (
        operating_system_kind
        is OperatingSystemKind.WINDOWS
    ):
        from bclearer_core.infrastructure.session.user.helpers.windows.security import (
            get_windows_user_sid,
        )

        return get_windows_user_sid()

    if operating_system_kind in {
        OperatingSystemKind.LINUX,
        OperatingSystemKind.MACOS,
    }:
        return get_unix_user_sid()

    return get_unix_user_sid()
