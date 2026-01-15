from bclearer_core.bie.infrastructure.bie_infrastructure_objects import (
    BieInfrastructureObjects,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_infrastructure_types import (
    BieInfrastructureTypes,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)


class SessionObjects(
    BieInfrastructureObjects
):
    def __init__(
        self,
        bie_id: BieIds,
        base_hr_name: str,
        bie_infrastructure_type: BieInfrastructureTypes,
    ):
        super().__init__(
            bie_id,
            base_hr_name=base_hr_name,
            bie_infrastructure_type=bie_infrastructure_type,
        )
