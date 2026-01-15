from bclearer_core.infrastructure.session.operating_system.operating_system_objects import (
    OperatingSystemObjects,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.infrastructure.registrations.bie_infrastructure_registries import (
    BieInfrastructureRegistries,
)


def register_operating_system_objects(
    bie_infrastructure_registry: BieInfrastructureRegistries,
) -> None:
    operating_system_object = (
        OperatingSystemObjects()
    )

    bie_infrastructure_registry.register_bie_object_and_type_instance(
        bie_object=operating_system_object
    )
