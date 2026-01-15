from bclearer_core.bie.infrastructure.types.bie_common_column_names import (
    BieCommonColumnNames,
)
from bclearer_core.infrastructure.session.os_user_session.enums.os_user_profile_object_column_names import (
    OsUserProfileObjectColumnNames,
)
from bclearer_core.infrastructure.session.user.os_user_profile_objects import (
    OsUserProfileObjects,
)
from bclearer_interop_services.b_dictionary_service.table_as_dictionary_service.table_as_dictionary_to_dataframe_converter import (
    convert_table_as_dictionary_to_dataframe,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_column_names import (
    BieColumnNames,
)
from pandas import DataFrame


def create_os_user_profile_objects_table() -> (
    DataFrame
):
    table_as_dictionary = (
        __get_os_user_profile_object_table_as_dictionary()
    )

    table_as_dataframe = convert_table_as_dictionary_to_dataframe(
        table_as_dictionary=table_as_dictionary
    )

    return table_as_dataframe.astype(
        str
    )


def __get_os_user_profile_object_table_as_dictionary() -> (
    dict
):
    os_user_profile_object = (
        OsUserProfileObjects()
    )

    os_user_profile_row = {
        BieColumnNames.BIE_IDS.b_enum_item_name: os_user_profile_object.bie_id,
        BieCommonColumnNames.BASE_HR_NAMES.b_enum_item_name: os_user_profile_object.base_hr_name,
        BieCommonColumnNames.BIE_INFRASTRUCTURE_TYPE_IDS.b_enum_item_name: os_user_profile_object.bie_type.item_bie_identity,
        OsUserProfileObjectColumnNames.USER_NAMES.b_enum_item_name: os_user_profile_object.user_name,
        OsUserProfileObjectColumnNames.USER_SIDS.b_enum_item_name: str(
            os_user_profile_object.user_sid
        ),
        OsUserProfileObjectColumnNames.DOMAIN_NAMES.b_enum_item_name: os_user_profile_object.domain_name,
        OsUserProfileObjectColumnNames.ACCOUNT_TYPES.b_enum_item_name: os_user_profile_object.account_type,
    }

    table_as_dictionary = {
        0: os_user_profile_row
    }

    return table_as_dictionary
