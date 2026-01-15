import uuid

from bclearer_core.infrastructure.session.common.enums.operating_system_kind import (
    OperatingSystemKind,
)
from bclearer_core.infrastructure.session.common.platform_type_getter import (
    get_operating_system_kind,
)
from bclearer_core.infrastructure.session.common.session_config import (
    UNKNOWN_MACHINE_FALLBACK_PREFIX,
)
from bclearer_core.infrastructure.session.operating_system.helpers.linux.linux_machine_identifier import (
    get_linux_machine_identifier,
)
from bclearer_core.infrastructure.session.operating_system.helpers.macos.macos_machine_identifier import (
    get_macos_machine_identifier,
)


def get_machine_sid() -> str:
    operating_system_kind = (
        get_operating_system_kind()
    )

    if (
        operating_system_kind
        is OperatingSystemKind.WINDOWS
    ):
        from bclearer_core.infrastructure.session.operating_system.helpers.windows.windows_machine_sid import (
            get_windows_machine_sid,
        )

        return get_windows_machine_sid()

    if (
        operating_system_kind
        is OperatingSystemKind.LINUX
    ):
        return (
            get_linux_machine_identifier()
        )

    if (
        operating_system_kind
        is OperatingSystemKind.MACOS
    ):
        return (
            get_macos_machine_identifier()
        )

    return f"{UNKNOWN_MACHINE_FALLBACK_PREFIX}{uuid.getnode():012x}"
