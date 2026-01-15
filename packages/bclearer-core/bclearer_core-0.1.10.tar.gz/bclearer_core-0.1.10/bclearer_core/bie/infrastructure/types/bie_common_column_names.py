from enum import auto

from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_enums import (
    BieEnums,
)


# TODO: needs to move to a general area
class BieCommonColumnNames(BieEnums):
    NOT_SET = auto()

    BASE_HR_NAMES = auto()

    BIE_DOMAIN_TYPE_NAMES = auto()

    BIE_SNAPSHOT_TYPE_NAMES = auto()

    BIE_INFRASTRUCTURE_TYPE_IDS = auto()

    BIE_DOMAIN_TYPE_IDS = auto()

    BIE_WHOLE_IDS = auto()

    BIE_PART_IDS = auto()

    BIE_SIGNATURE_SUM_IDS = auto()

    BIE_SNAPSHOT_TYPE_IDS = auto()
