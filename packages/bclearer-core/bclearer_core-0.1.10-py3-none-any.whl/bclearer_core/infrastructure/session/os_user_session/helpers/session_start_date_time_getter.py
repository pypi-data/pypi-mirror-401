import datetime

import psutil


def get_user_session_start_date_time(
    user_name: str,
) -> datetime.datetime:
    user = __get_user_by_name(
        user_name=user_name
    )

    if not user:
        return datetime.datetime.fromtimestamp(
            psutil.boot_time()
        )

    user_session_start_date_time = (
        user.started
    )

    user_session_start_date_time_formatted = datetime.datetime.fromtimestamp(
        user_session_start_date_time
    )

    return user_session_start_date_time_formatted


def __get_user_by_name(user_name: str):
    for user in psutil.users():
        if user.name == user_name:
            return user

    return None
