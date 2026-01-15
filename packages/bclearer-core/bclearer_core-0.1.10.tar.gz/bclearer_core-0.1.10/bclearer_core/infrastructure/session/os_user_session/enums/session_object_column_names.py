from enum import auto

from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_enums import (
    BieEnums,
)


# TODO: Rename to a better name. Maybe SessionObjectTableNames??
class SessionObjectColumnNames(
    BieEnums
):
    NOT_SET = auto()

    APP_RUN_SESSIONS = auto()

    OPERATING_SYSTEMS = auto()

    OS_USER_PROFILES = auto()

    OS_USER_PROFILE_SESSIONS = auto()
