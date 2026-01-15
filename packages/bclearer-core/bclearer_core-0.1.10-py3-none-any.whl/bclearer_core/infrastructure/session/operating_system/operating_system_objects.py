import socket

from bclearer_core.infrastructure.session.common.session_objects import (
    SessionObjects,
)
from bclearer_core.infrastructure.session.operating_system.helpers.bie_operating_system_type_getter import (
    get_bie_operating_system_type,
)
from bclearer_core.infrastructure.session.operating_system.helpers.machine_sid_getter import (
    get_machine_sid,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.bie_id_creation_facade import (
    BieIdCreationFacade,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)


class OperatingSystemObjects(
    SessionObjects
):
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(
                OperatingSystemObjects,
                cls,
            ).__new__(cls)

        return cls._instance

    def __init__(self):
        # TODO: get: Computer Name, Machine SID
        # NOTE: Install date deprecated
        # TODO: get bie operating system type (enum) - use standard getter
        # TODO: check it is machine name
        self.computer_name = (
            socket.gethostname()
        )

        self.machine_sid = (
            get_machine_sid()
        )

        self.bie_operating_system_type = (
            get_bie_operating_system_type()
        )

        # TODO: The following attributes have still not been agreed
        # TODO: If this changes after updates we may not want it to identify this object - discuss

        # NOTE: Install date deprecated
        # self.install_date = \
        #     get_os_install_date()

        # NOTE: version deprecated
        # self.version = \
        #     platform.version()

        # NOTE: release deprecated
        # self.release = \
        #     platform.release()

        # NOTE: operating_system_name deprecated
        # self.name = \
        #     self.__get_operating_system_name()

        base_bie_id = (
            self.__create_bie_id()
        )

        super().__init__(
            bie_id=base_bie_id,
            base_hr_name=self.computer_name,
            bie_infrastructure_type=self.bie_operating_system_type,
        )

    def __create_bie_id(self) -> BieIds:
        bie_id = BieIdCreationFacade.create_order_sensitive_bie_id_for_multiple_objects(
            input_objects=[
                self.bie_operating_system_type.item_bie_identity,
                self.machine_sid,
            ]
        )

        return bie_id
