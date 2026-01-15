import getpass
import os
from typing import Tuple

from bclearer_core.infrastructure.session.common.enums.operating_system_kind import (
    OperatingSystemKind,
)
from bclearer_core.infrastructure.session.common.platform_type_getter import (
    get_operating_system_kind,
)
from bclearer_core.infrastructure.session.common.session_objects import (
    SessionObjects,
)
from bclearer_core.infrastructure.session.operating_system.operating_system_objects import (
    OperatingSystemObjects,
)
from bclearer_core.infrastructure.session.user.bie_os_user_profile_types import (
    BieOsUserProfileTypes,
)
from bclearer_core.infrastructure.session.user.helpers.bie_os_user_profile_type_getter import (
    get_bie_os_user_profile_type,
)
from bclearer_core.infrastructure.session.user.helpers.unix.unix_account_context import (
    get_unix_account_context,
)
from bclearer_core.infrastructure.session.user.helpers.user_sid_getter import (
    get_user_sid,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.bie_id_creation_facade import (
    BieIdCreationFacade,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)


class OsUserProfileObjects(
    SessionObjects
):
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(
                OsUserProfileObjects,
                cls,
            ).__new__(cls)

        return cls._instance

    def __init__(self):
        self.user_name = (
            self.__get_user_name()
        )

        self.user_sid = get_user_sid()

        (
            self.domain_name,
            self.account_type,
        ) = (
            self.__resolve_account_context()
        )

        os_user_profile_type = (
            get_bie_os_user_profile_type()
        )

        bie_id = self.__create_bie_id(
            os_user_profile_type=os_user_profile_type
        )

        super().__init__(
            bie_id=bie_id,
            base_hr_name=self.user_name,
            bie_infrastructure_type=os_user_profile_type,
        )

    @staticmethod
    def __get_user_name() -> str:
        try:
            return getpass.getuser()
        except Exception:
            return (
                os.environ.get(
                    "USERNAME"
                )
                or os.environ.get(
                    "USER"
                )
                or "unknown-user"
            )

    def __resolve_account_context(
        self,
    ) -> Tuple[str, str]:
        operating_system_kind = (
            get_operating_system_kind()
        )

        if (
            operating_system_kind
            is OperatingSystemKind.WINDOWS
        ):
            from bclearer_core.infrastructure.session.user.helpers.windows.windows_account_context import (
                get_windows_account_context,
            )

            return get_windows_account_context(
                self.user_sid
            )

        return (
            get_unix_account_context()
        )

    def __create_bie_id(
        self,
        os_user_profile_type: BieOsUserProfileTypes,
    ) -> BieIds:
        operating_system_object = (
            OperatingSystemObjects()
        )

        user_base_bie_id = BieIdCreationFacade.create_order_sensitive_bie_id_for_multiple_objects(
            input_objects=[
                os_user_profile_type.item_bie_identity,
                self.user_sid,
                operating_system_object.bie_operating_system_type.item_bie_identity,
            ]
        )

        return user_base_bie_id
