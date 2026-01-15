from enum import auto

from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_enums import (
    BieEnums,
)


class OperatingSystemObjectColumnNames(
    BieEnums
):
    NOT_SET = auto()

    COMPUTER_NAMES = auto()

    MACHINE_SIDS = auto()
