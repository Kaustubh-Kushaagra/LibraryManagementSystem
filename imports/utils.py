from .constants import COLUMN_ALIASES


def get_value(row_data, field):

    aliases = COLUMN_ALIASES.get(field, [])

    for alias in aliases:

        if alias in row_data:

            return row_data[alias]

    return None