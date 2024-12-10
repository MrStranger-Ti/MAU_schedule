from typing import Callable

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from rest_framework.test import APIClient
from model_bakery import baker
from faker import Faker

from mau_auth.models import MauInstitute

User = get_user_model()

faker = Faker()


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def user_factory() -> Callable:
    def wrapper(n: int = 1) -> list[User] | User:
        test_data = baker.make(
            _model=User,
            _quantity=n,
            _fill_optional=True,
            full_name="Petrov Petr Petrovich",
            institute=baker.make(MauInstitute),
            groups=baker.make(Group, _quantity=5),
            user_permissions=baker.make(Permission, _quantity=5),
        )

        for instance in test_data:
            instance.email = instance.email.split("@")[0] + "@mauniver.ru"
            instance.save()

        if n == 1:
            return test_data[0]
        return test_data

    return wrapper


@pytest.fixture
def user_client(api_client, user_factory) -> APIClient:
    user = user_factory()
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin_client(api_client, user_factory) -> APIClient:
    admin = user_factory()
    admin.is_superuser = True
    admin.is_staff = True
    admin.save()
    api_client.force_authenticate(user=admin)
    return api_client


class Helper:
    def assert_match_data(self, response_data, expected_data):
        for field_name, value in expected_data.items():
            assert field_name in response_data
            assert response_data[field_name] == value


@pytest.fixture()
def helper() -> Helper:
    return Helper()
