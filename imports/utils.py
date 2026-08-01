from .constants import COLUMN_ALIASES


def get_value(row_data, field):
    aliases = COLUMN_ALIASES.get(field, [])

    # Normalize Excel headers once
    normalized_row = {
        str(key).replace("\xa0", " ").strip(): value
        for key, value in row_data.items()
    }

    for alias in aliases:
        alias = alias.replace("\xa0", " ").strip()

        if alias in normalized_row:
            return normalized_row[alias]

    return None