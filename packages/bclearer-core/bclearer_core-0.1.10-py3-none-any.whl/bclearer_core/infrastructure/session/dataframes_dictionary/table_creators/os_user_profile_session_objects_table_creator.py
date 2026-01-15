from bclearer_core.bie.infrastructure.types.bie_common_column_names import (
    BieCommonColumnNames,
)
from bclearer_core.constants.standard_constants import (
    HR_DATE_TIME_FORMAT,
)
from bclearer_core.infrastructure.session.os_user_session.enums.os_user_profile_session_object_column_names import (
    OsUserProfileSessionObjectColumnNames,
)
from bclearer_core.infrastructure.session.os_user_session.os_user_profile_session_objects import (
    OsUserProfileSessionObjects,
)
from bclearer_interop_services.b_dictionary_service.table_as_dictionary_service.table_as_dictionary_to_dataframe_converter import (
    convert_table_as_dictionary_to_dataframe,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_column_names import (
    BieColumnNames,
)
from pandas import DataFrame


def create_os_user_profile_session_objects_table() -> (
    DataFrame
):
    table_as_dictionary = (
        __get_os_user_profile_session_object_table_as_dictionary()
    )

    table_as_dataframe = convert_table_as_dictionary_to_dataframe(
        table_as_dictionary=table_as_dictionary
    )

    return table_as_dataframe.astype(
        str
    )


def __get_os_user_profile_session_object_table_as_dictionary() -> (
    dict
):
    os_user_profile_session_object = (
        OsUserProfileSessionObjects()
    )

    session_start_date_time = os_user_profile_session_object.session_start_date_time.strftime(
        format=HR_DATE_TIME_FORMAT
    )

    os_user_profile_session_object_row = {
        BieColumnNames.BIE_IDS.b_enum_item_name: os_user_profile_session_object.bie_id,
        BieCommonColumnNames.BASE_HR_NAMES.b_enum_item_name: os_user_profile_session_object.base_hr_name,
        BieCommonColumnNames.BIE_INFRASTRUCTURE_TYPE_IDS.b_enum_item_name: os_user_profile_session_object.bie_type.item_bie_identity,
        OsUserProfileSessionObjectColumnNames.WINDOWS_SESSION_IDS.b_enum_item_name: os_user_profile_session_object.windows_session_id,
        OsUserProfileSessionObjectColumnNames.SESSION_START_DATE_TIMES.b_enum_item_name: session_start_date_time,
        OsUserProfileSessionObjectColumnNames.OWNING_OS_USER_PROFILE_BIE_IDS.b_enum_item_name: os_user_profile_session_object.owning_os_user_profile.bie_id,
        OsUserProfileSessionObjectColumnNames.OWNING_OPERATING_SYSTEM_BIE_IDS.b_enum_item_name: os_user_profile_session_object.owning_operating_system_object.bie_id,
    }

    table_as_dictionary = {
        0: os_user_profile_session_object_row
    }

    return table_as_dictionary
