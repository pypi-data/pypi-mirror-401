from bclearer_core.constants.standard_constants import (
    HR_DATE_TIME_FORMAT,
    HR_NAME_COMPONENT_DIVIDER,
)
from bclearer_core.infrastructure.session.common.session_objects import (
    SessionObjects,
)
from bclearer_core.infrastructure.session.operating_system.operating_system_objects import (
    OperatingSystemObjects,
)
from bclearer_core.infrastructure.session.os_user_session.bie_os_user_profile_session_types import (
    BieOsUserProfileSessionTypes,
)
from bclearer_core.infrastructure.session.os_user_session.helpers.session_id_getter import (
    get_os_user_session_id,
)
from bclearer_core.infrastructure.session.os_user_session.helpers.session_start_date_time_getter import (
    get_user_session_start_date_time,
)
from bclearer_core.infrastructure.session.user.os_user_profile_objects import (
    OsUserProfileObjects,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.bie_id_creation_facade import (
    BieIdCreationFacade,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)


class OsUserProfileSessionObjects(
    SessionObjects
):
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(
                OsUserProfileSessionObjects,
                cls,
            ).__new__(cls)

        return cls._instance

    def __init__(self):
        session_identifier = (
            get_os_user_session_id()
        )

        self.session_id = (
            session_identifier
        )

        self.windows_session_id = (
            session_identifier
        )

        self.owning_os_user_profile = (
            OsUserProfileObjects()
        )

        self.owning_operating_system_object = (
            OperatingSystemObjects()
        )

        # TODO: Every time it runs it retrieves a different value (very similar though), but it should retrieve exactly
        #  the same if it's run within the same user session
        self.session_start_date_time = get_user_session_start_date_time(
            user_name=self.owning_os_user_profile.user_name
        )

        # TODO: What enum to use? What design?
        self.os_user_session_type = (
            BieOsUserProfileSessionTypes.BIE_OS_USER_PROFILE_SESSION
        )

        bie_id = self.__create_bie_id()

        base_hr_name = (
            self.owning_operating_system_object.base_hr_name
            + HR_NAME_COMPONENT_DIVIDER
            + self.owning_os_user_profile.base_hr_name
            + HR_NAME_COMPONENT_DIVIDER
            + self.session_start_date_time.strftime(
                format=HR_DATE_TIME_FORMAT
            )
        )

        super().__init__(
            bie_id=bie_id,
            base_hr_name=base_hr_name,
            bie_infrastructure_type=BieOsUserProfileSessionTypes.BIE_OS_USER_PROFILE_SESSION,
        )

    def __create_bie_id(self) -> BieIds:
        bie_id = BieIdCreationFacade.create_order_sensitive_bie_id_for_multiple_objects(
            input_objects=[
                self.os_user_session_type.item_bie_identity,
                self.windows_session_id,
                self.session_start_date_time,
                self.owning_operating_system_object.bie_id,
            ]
        )

        return bie_id
