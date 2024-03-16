import re

from django.core.exceptions import ValidationError
from django.conf import settings


def validate_full_name(value: str) -> None:
    if not re.fullmatch(r'[ЁА-ЯA-Z]\w+\s[ЁА-ЯA-Z]\w+\s[ЁА-ЯA-Z]\w+\s?', value):
        raise ValidationError('ФИО должно быть в формате Фамилия Имя Отчество')


def validate_email(value: str) -> None:
    if not any(value.endswith(domain) for domain in settings.MAU_DOMAINS):
        raise ValidationError('Почта может быть только со следующими доменами: masu.edu.ru, mstu.edu.ru, mauniver.ru')
