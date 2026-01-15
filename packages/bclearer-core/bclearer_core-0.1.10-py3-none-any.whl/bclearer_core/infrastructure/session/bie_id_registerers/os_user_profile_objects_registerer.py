from bclearer_core.infrastructure.session.user.os_user_profile_objects import (
    OsUserProfileObjects,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.infrastructure.registrations.bie_infrastructure_registries import (
    BieInfrastructureRegistries,
)


def register_os_user_profile_objects(
    bie_infrastructure_registry: BieInfrastructureRegistries,
) -> None:
    os_user_profile_object = (
        OsUserProfileObjects()
    )

    bie_infrastructure_registry.register_bie_object_and_type_instance(
        bie_object=os_user_profile_object
    )
