from bclearer_core.bie.top.bie_objects import (
    BieObjects,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_domain_types import (
    BieDomainTypes,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)


class BieDomainObjects(BieObjects):
    def __init__(
        self,
        bie_id: BieIds,
        base_hr_name: str,
        bie_domain_type: BieDomainTypes,
    ):
        super().__init__(
            bie_id,
            base_hr_name=base_hr_name,
            bie_type=bie_domain_type,
        )
