import re
from difflib import SequenceMatcher

from django.contrib.auth.password_validation import (
    UserAttributeSimilarityValidator,
    exceeds_maximum_length_ratio,
    MinimumLengthValidator,
    CommonPasswordValidator,
    NumericPasswordValidator,
)
from django.core.exceptions import ValidationError, FieldDoesNotExist
from django.conf import settings


def validate_full_name(value: str) -> None:
    if not re.fullmatch(r"[ЁА-ЯA-Z]\w+\s[ЁА-ЯA-Z]\w+\s[ЁА-ЯA-Z]\w+\s?", value):
        raise ValidationError("ФИО должно быть в формате Фамилия Имя Отчество")


def validate_email(value: str) -> None:
    if not any(value.endswith(domain) for domain in settings.MAU_DOMAINS):
        raise ValidationError(
            "Почта может быть только со следующими доменами: masu.edu.ru, mstu.edu.ru, mauniver.ru"
        )


class CustomUserAttributeSimilarityValidator(UserAttributeSimilarityValidator):
    def validate(self, password, user=None):
        if not user:
            return

        password = password.lower()
        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if not value or not isinstance(value, str):
                continue
            value_lower = value.lower()
            value_parts = re.split(r"\W+", value_lower) + [value_lower]
            for value_part in value_parts:
                if exceeds_maximum_length_ratio(
                    password, self.max_similarity, value_part
                ):
                    continue
                if (
                    SequenceMatcher(a=password, b=value_part).quick_ratio()
                    >= self.max_similarity
                ):
                    try:
                        verbose_name = str(
                            user._meta.get_field(attribute_name).verbose_name
                        )
                    except FieldDoesNotExist:
                        verbose_name = attribute_name
                    raise ValidationError(
                        "Пароль слишком похож на %(verbose_name)s",
                        code="password_too_similar",
                        params={"verbose_name": verbose_name},
                    )


class CustomMinimumLengthValidator(MinimumLengthValidator):
    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                "Длина пароля должна быть минимум 8 символов",
                code="password_too_short",
                params={"min_length": self.min_length},
            )


class CustomCommonPasswordValidator(CommonPasswordValidator):
    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise ValidationError(
                "Пароль слишком простой",
                code="password_too_common",
            )


class CustomNumericPasswordValidator(NumericPasswordValidator):
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                "Пароль не должен состоять только из чисел",
                code="password_entirely_numeric",
            )
