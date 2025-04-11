from typing import Callable, Iterable, Any
from zoneinfo import ZoneInfo

import pytest
from django.contrib.auth import get_user_model

from mau_auth.models import MauUser

User: type[MauUser] = get_user_model()


@pytest.fixture
def get_user_serialized_data() -> Callable:
    def wrapper(user: User, exclude_fields: Iterable | None = None) -> dict[str, Any]:
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
