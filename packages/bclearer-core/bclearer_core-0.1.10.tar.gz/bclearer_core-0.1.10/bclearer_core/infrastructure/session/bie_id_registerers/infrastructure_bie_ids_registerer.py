from bclearer_core.infrastructure.session.app_run_session.app_run_session_objects import (
    AppRunSessionObjects,
)
from bclearer_core.infrastructure.session.bie_id_registerers.app_run_session_objects_registerer import (
    register_app_run_session_objects,
)
from bclearer_core.infrastructure.session.bie_id_registerers.operating_system_objects_registerer import (
    register_operating_system_objects,
)
from bclearer_core.infrastructure.session.bie_id_registerers.os_user_profile_objects_registerer import (
    register_os_user_profile_objects,
)
from bclearer_core.infrastructure.session.bie_id_registerers.os_user_profile_session_objects_registerer import (
    register_os_user_profile_session_objects,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.infrastructure.registrations.bie_infrastructure_registries import (
    BieInfrastructureRegistries,
)


def register_infrastructure_bie_ids(
    bie_infrastructure_registry: BieInfrastructureRegistries,
    app_run_session_object: AppRunSessionObjects,
) -> None:
    register_app_run_session_objects(
        bie_infrastructure_registry=bie_infrastructure_registry,
        app_run_session_object=app_run_session_object,
    )

    register_operating_system_objects(
        bie_infrastructure_registry=bie_infrastructure_registry
    )

    register_os_user_profile_objects(
        bie_infrastructure_registry=bie_infrastructure_registry
    )

    register_os_user_profile_session_objects(
        bie_infrastructure_registry=bie_infrastructure_registry
    )
