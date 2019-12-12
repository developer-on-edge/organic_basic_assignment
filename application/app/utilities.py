import os

from datetime import datetime, timezone

def convert_year_to_start_and_end_time(year):
    return (
        datetime(year, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        datetime(year, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
    )


def get_environment_variable(variable_name, ignore_key_error=False):
    upper_variable_name = variable_name.upper()
    if upper_variable_name not in os.environ:
        error_msg = 'Variable %s not in environment.' % upper_variable_name
        if ignore_key_error:
            return
        raise KeyError(error_msg)
    return os.environ[upper_variable_name]