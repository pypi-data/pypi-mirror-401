from enum import auto

from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_infrastructure_types import (
    BieInfrastructureTypes,
)


class BieOsUserProfileTypes(
    BieInfrastructureTypes
):
    NOT_SET = auto()

    BIE_WINDOWS_USER_PROFILE = auto()

    BIE_LINUX_USER_PROFILE = auto()

    BIE_MAC_OS_USER_PROFILE = auto()
