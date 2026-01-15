from bclearer_core.bie.infrastructure.types.bie_common_column_names import (
    BieCommonColumnNames,
)
from bclearer_core.constants.standard_constants import (
    HR_DATE_TIME_FORMAT,
)
from bclearer_core.infrastructure.session.app_run_session.app_run_session_objects import (
    AppRunSessionObjects,
)
from bclearer_core.infrastructure.session.app_run_session.enums.app_run_session_object_column_names import (
    AppRunSessionObjectColumnNames,
)
from bclearer_interop_services.b_dictionary_service.table_as_dictionary_service.table_as_dictionary_to_dataframe_converter import (
    convert_table_as_dictionary_to_dataframe,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_column_names import (
    BieColumnNames,
)
from pandas import DataFrame


def create_app_run_session_objects_table(
    app_run_session_object: AppRunSessionObjects,
) -> DataFrame:
    table_as_dictionary = {}

    __add_app_run_session_object_to_table(
        table_as_dictionary=table_as_dictionary,
        app_run_session_object=app_run_session_object,
    )

    table_as_dataframe = convert_table_as_dictionary_to_dataframe(
        table_as_dictionary=table_as_dictionary
    )

    return table_as_dataframe.astype(
        str
    )


def __add_app_run_session_object_to_table(
    table_as_dictionary: dict,
    app_run_session_object: AppRunSessionObjects,
) -> None:
    start_date_time = app_run_session_object.app_run_session_date_time.strftime(
        format=HR_DATE_TIME_FORMAT
    )

    app_run_session_object_row = {
        BieColumnNames.BIE_IDS.b_enum_item_name: app_run_session_object.bie_id,
        BieCommonColumnNames.BASE_HR_NAMES.b_enum_item_name: app_run_session_object.base_hr_name,
        BieCommonColumnNames.BIE_INFRASTRUCTURE_TYPE_IDS.b_enum_item_name: app_run_session_object.bie_type.item_bie_identity,
        AppRunSessionObjectColumnNames.START_DATE_TIMES.b_enum_item_name: start_date_time,
        AppRunSessionObjectColumnNames.OWNING_OS_USER_PROFILE_SESSION_BIE_IDS.b_enum_item_name: app_run_session_object.owning_os_user_profile_session.bie_id,
    }

    table_as_dictionary[
        len(table_as_dictionary)
    ] = app_run_session_object_row
