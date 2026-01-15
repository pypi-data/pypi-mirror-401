from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_types import (
    BieTypes,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)


class BieObjects:
    def __init__(
        self,
        bie_id: BieIds,
        base_hr_name: str,
        bie_type: BieTypes,
    ):
        self.bie_id = bie_id

        self.base_hr_name = base_hr_name

        self.bie_type = bie_type

    def __hash__(self):
        return hash(
            self.bie_id.int_value
        )
