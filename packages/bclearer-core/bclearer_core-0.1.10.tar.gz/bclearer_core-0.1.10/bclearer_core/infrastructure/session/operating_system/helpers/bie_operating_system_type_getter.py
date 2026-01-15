from bclearer_core.infrastructure.session.common.enums.operating_system_kind import (
    OperatingSystemKind,
)
from bclearer_core.infrastructure.session.common.platform_type_getter import (
    get_operating_system_kind,
)
from bclearer_core.infrastructure.session.operating_system.bie_operating_system_types import (
    BieOperatingSystemTypes,
)


def get_bie_operating_system_type() -> (
    BieOperatingSystemTypes
):
    operating_system_kind = (
        get_operating_system_kind()
    )

    if (
        operating_system_kind
        is OperatingSystemKind.WINDOWS
    ):
        return (
            BieOperatingSystemTypes.BIE_WINDOWS
        )

    if (
        operating_system_kind
        is OperatingSystemKind.LINUX
    ):
        return (
            BieOperatingSystemTypes.BIE_LINUX
        )

    if (
        operating_system_kind
        is OperatingSystemKind.MACOS
    ):
        return (
            BieOperatingSystemTypes.BIE_MAC_OS
        )

    return (
        BieOperatingSystemTypes.NOT_SET
    )
