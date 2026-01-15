from bclearer_core.infrastructure.session.common.enums.operating_system_kind import (
    OperatingSystemKind,
)
from bclearer_core.infrastructure.session.common.platform_type_getter import (
    get_operating_system_kind,
)
from bclearer_core.infrastructure.session.user.bie_os_user_profile_types import (
    BieOsUserProfileTypes,
)


def get_bie_os_user_profile_type() -> (
    BieOsUserProfileTypes
):
    operating_system_kind = (
        get_operating_system_kind()
    )

    if (
        operating_system_kind
        is OperatingSystemKind.WINDOWS
    ):
        return (
            BieOsUserProfileTypes.BIE_WINDOWS_USER_PROFILE
        )

    if (
        operating_system_kind
        is OperatingSystemKind.LINUX
    ):
        return (
            BieOsUserProfileTypes.BIE_LINUX_USER_PROFILE
        )

    if (
        operating_system_kind
        is OperatingSystemKind.MACOS
    ):
        return (
            BieOsUserProfileTypes.BIE_MAC_OS_USER_PROFILE
        )

    return BieOsUserProfileTypes.NOT_SET
