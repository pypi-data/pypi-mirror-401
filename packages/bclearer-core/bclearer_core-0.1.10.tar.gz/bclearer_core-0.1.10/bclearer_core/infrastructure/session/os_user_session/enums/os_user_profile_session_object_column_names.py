from enum import auto

from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_enums import (
    BieEnums,
)


class OsUserProfileSessionObjectColumnNames(
    BieEnums
):
    NOT_SET = auto()

    WINDOWS_SESSION_IDS = auto()

    SESSION_START_DATE_TIMES = auto()

    OWNING_OS_USER_PROFILE_BIE_IDS = (
        auto()
    )

    OWNING_OPERATING_SYSTEM_BIE_IDS = (
        auto()
    )
