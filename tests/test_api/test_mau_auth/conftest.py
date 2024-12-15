import re
from typing import Callable, Iterable
from zoneinfo import ZoneInfo

import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.core.handlers.wsgi import WSGIRequest
from rest_framework.reverse import reverse

from mau_auth.models import MauUser

User: type[MauUser] = get_user_model()


@pytest.fixture
def get_serialized_data() -> Callable:
    def wrapper(
        user: User,
        exclude_fields: Iterable | None = None,
    ) -> User:
        date_joined = user.date_joined.astimezone(tz=ZoneInfo("Europe/Moscow"))
        last_login = user.last_login.astimezone(tz=ZoneInfo("Europe/Moscow"))
        json_data = {
            "id": user.id,
            "password": "testuser",
            "last_login": last_login.isoformat(),
            "is_superuser": user.is_superuser,
            "full_name": user.full_name,
            "email": user.email,
            "course": user.course,
            "group": user.group,
            "is_staff": user.is_staff,
            "is_active": user.is_active,
            "date_joined": date_joined.isoformat(),
            "institute": user.institute.pk,
            "groups": (
                [instance.id for instance in user.groups.all()] if user.id else []
            ),
            "user_permissions": (
                [instance.id for instance in user.user_permissions.all()]
                if user.id
                else []
            ),
        }

        if exclude_fields:
            for exclude_field in exclude_fields:
                json_data.pop(exclude_field, None)

        return json_data

    return wrapper


@pytest.fixture
def get_confirmation_url() -> Callable:
    def wrapper() -> str:
        message = mail.outbox[0].body
        match = re.search(r"http.+\s?", message)
        return match.group()

    return wrapper


@pytest.fixture
def get_uidb64_and_token_from_last_message(get_confirmation_url) -> Callable:
    def wrapper() -> tuple[str, str]:
        confirmation_url = get_confirmation_url()
        split_url = confirmation_url.split("/")
        if split_url[-1] not in ("", "\n"):
            return split_url[-2], split_url[-1]

        return split_url[-3], split_url[-2]

    return wrapper
