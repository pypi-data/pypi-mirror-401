from enum import auto

from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_infrastructure_types import (
    BieInfrastructureTypes,
)


class BieOperatingSystemTypes(
    BieInfrastructureTypes
):
    NOT_SET = auto()

    BIE_WINDOWS = auto()

    BIE_LINUX = auto()

    BIE_MAC_OS = auto()
