from enum import auto

from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_enums import (
    BieEnums,
)


class OsUserProfileObjectColumnNames(
    BieEnums
):
    NOT_SET = auto()

    USER_NAMES = auto()

    USER_SIDS = auto()

    DOMAIN_NAMES = auto()

    ACCOUNT_TYPES = auto()
