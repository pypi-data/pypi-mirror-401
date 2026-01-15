from bclearer_core.infrastructure.session.app_run_session.app_run_session_objects import (
    AppRunSessionObjects,
)
from bclearer_core.infrastructure.session.dataframes_dictionary.table_creators.app_run_session_objects_table_creator import (
    create_app_run_session_objects_table,
)
from bclearer_core.infrastructure.session.dataframes_dictionary.table_creators.operating_system_objects_table_creator import (
    create_operating_system_objects_table,
)
from bclearer_core.infrastructure.session.dataframes_dictionary.table_creators.os_user_profile_objects_table_creator import (
    create_os_user_profile_objects_table,
)
from bclearer_core.infrastructure.session.dataframes_dictionary.table_creators.os_user_profile_session_objects_table_creator import (
    create_os_user_profile_session_objects_table,
)
from bclearer_core.infrastructure.session.os_user_session.enums.session_object_column_names import (
    SessionObjectColumnNames,
)


def create_session_dataframes_dictionary(
    app_run_session_object: AppRunSessionObjects,
) -> dict:
    app_run_sessions_table = create_app_run_session_objects_table(
        app_run_session_object=app_run_session_object
    )

    operating_system_objects_table = (
        create_operating_system_objects_table()
    )

    os_user_profile_objects_table = (
        create_os_user_profile_objects_table()
    )

    os_user_profile_session_objects_table = (
        create_os_user_profile_session_objects_table()
    )

    dataframes_dictionary_keyed_on_string = {
        SessionObjectColumnNames.APP_RUN_SESSIONS.b_enum_item_name: app_run_sessions_table,
        SessionObjectColumnNames.OPERATING_SYSTEMS.b_enum_item_name: operating_system_objects_table,
        SessionObjectColumnNames.OS_USER_PROFILES.b_enum_item_name: os_user_profile_objects_table,
        SessionObjectColumnNames.OS_USER_PROFILE_SESSIONS.b_enum_item_name: os_user_profile_session_objects_table,
    }

    return dataframes_dictionary_keyed_on_string
