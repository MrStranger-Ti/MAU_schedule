import re

from django.core.exceptions import ValidationError


def validate_full_name(value: str) -> None:
    if not re.fullmatch(r'([A-ЯA-Z]\w+\s?){3}', value):
        raise ValidationError('ФИО должно быть в формате "Петров Петр Петрович"')
