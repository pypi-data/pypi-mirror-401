from enum import auto

from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_infrastructure_types import (
    BieInfrastructureTypes,
)


class BieOsUserProfileSessionTypes(
    BieInfrastructureTypes
):
    NOT_SET = auto()

    BIE_OS_USER_PROFILE_SESSION = auto()
