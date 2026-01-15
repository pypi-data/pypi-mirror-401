from datetime import datetime

from bclearer_core.constants.standard_constants import (
    HR_DATE_TIME_FORMAT,
    HR_NAME_COMPONENT_DIVIDER,
)
from bclearer_core.infrastructure.session.app_run_session.bie_app_run_session_types import (
    BieAppRunSessionTypes,
)
from bclearer_core.infrastructure.session.common.session_objects import (
    SessionObjects,
)
from bclearer_core.infrastructure.session.os_user_session.os_user_profile_session_objects import (
    OsUserProfileSessionObjects,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.bie_id_creation_facade import (
    BieIdCreationFacade,
)


class AppRunSessionObjects(
    SessionObjects
):
    def __init__(
        self,
        bie_app_run_session_type: BieAppRunSessionTypes,
    ):  # TODO: needs to be integrated (called by) into the b_application_runner
        self.bie_app_run_session_type = (
            bie_app_run_session_type
        )

        self.owning_os_user_profile_session = (
            OsUserProfileSessionObjects()
        )

        # TODO: the app run session timestamp is not the same date time than the os user session
        self.app_run_session_date_time = (
            datetime.now()
        )

        # TODO: Design a bie id - get to work with other OSs
        bie_id = BieIdCreationFacade.create_order_sensitive_bie_id_for_multiple_objects(
            input_objects=[
                bie_app_run_session_type.item_bie_identity,
                self.owning_os_user_profile_session.bie_id,
                self.app_run_session_date_time,
            ]
        )

        base_hr_name = (
            self.owning_os_user_profile_session.owning_operating_system_object.base_hr_name
            + HR_NAME_COMPONENT_DIVIDER
            + self.owning_os_user_profile_session.owning_os_user_profile.base_hr_name
            + HR_NAME_COMPONENT_DIVIDER
            + self.app_run_session_date_time.strftime(
                format=HR_DATE_TIME_FORMAT
            )
        )

        super().__init__(
            bie_id=bie_id,
            base_hr_name=base_hr_name,
            bie_infrastructure_type=bie_app_run_session_type,
        )
