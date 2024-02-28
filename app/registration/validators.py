import re


def validate_full_name(value: str) -> bool:
    if re.fullmatch(r'([A-ЯA-Z]\w+){3}', value):
        return True
    return False
