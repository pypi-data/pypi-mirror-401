from bclearer_core.bie.infrastructure.types.bie_common_column_names import (
    BieCommonColumnNames,
)
from bclearer_core.infrastructure.session.operating_system.enums.operating_system_object_column_names import (
    OperatingSystemObjectColumnNames,
)
from bclearer_core.infrastructure.session.operating_system.operating_system_objects import (
    OperatingSystemObjects,
)
from bclearer_interop_services.b_dictionary_service.table_as_dictionary_service.table_as_dictionary_to_dataframe_converter import (
    convert_table_as_dictionary_to_dataframe,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_column_names import (
    BieColumnNames,
)
from pandas import DataFrame


def create_operating_system_objects_table() -> (
    DataFrame
):
    table_as_dictionary = (
        __get_operating_system_object_table_as_dictionary()
    )

    table_as_dataframe = convert_table_as_dictionary_to_dataframe(
        table_as_dictionary=table_as_dictionary
    )

    return table_as_dataframe.astype(
        str
    )


def __get_operating_system_object_table_as_dictionary() -> (
    dict
):
    operating_system_object = (
        OperatingSystemObjects()
    )

    operating_system_row = {
        BieColumnNames.BIE_IDS.b_enum_item_name: operating_system_object.bie_id,
        BieCommonColumnNames.BASE_HR_NAMES.b_enum_item_name: operating_system_object.base_hr_name,
        BieCommonColumnNames.BIE_INFRASTRUCTURE_TYPE_IDS.b_enum_item_name: operating_system_object.bie_type.item_bie_identity,
        OperatingSystemObjectColumnNames.COMPUTER_NAMES.b_enum_item_name: operating_system_object.computer_name,
        OperatingSystemObjectColumnNames.MACHINE_SIDS.b_enum_item_name: str(
            operating_system_object.machine_sid
        ),
    }

    table_as_dictionary = {
        0: operating_system_row
    }

    return table_as_dictionary
