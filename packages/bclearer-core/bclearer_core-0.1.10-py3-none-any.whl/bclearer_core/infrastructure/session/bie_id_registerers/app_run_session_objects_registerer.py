from bclearer_core.infrastructure.session.app_run_session.app_run_session_objects import (
    AppRunSessionObjects,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.infrastructure.registrations.bie_infrastructure_registries import (
    BieInfrastructureRegistries,
)


def register_app_run_session_objects(
    bie_infrastructure_registry: BieInfrastructureRegistries,
    app_run_session_object: AppRunSessionObjects,
) -> None:
    bie_infrastructure_registry.register_bie_object_and_type_instance(
        bie_object=app_run_session_object
    )

    bie_infrastructure_registry.register_bie_whole_part_in_bie_infrastructure_registry(
        bie_object_whole=app_run_session_object.owning_os_user_profile_session,
        bie_object_part=app_run_session_object,
    )
