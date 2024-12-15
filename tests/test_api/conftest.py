from typing import Callable, Any

import pytest
import faker

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from rest_framework.serializers import Serializer
from rest_framework.test import APIClient, APIRequestFactory
from model_bakery import baker

from mau_auth.models import MauInstitute, MauUser

User: type[MauUser] = get_user_model()

faker = faker.Faker()


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def request_client() -> APIRequestFactory:
    return APIRequestFactory()


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
            instance.set_password(instance.password)

        User.objects.bulk_update(test_data, ["email"])

        if n == 1:
            return test_data[0]
        return test_data

    return wrapper


@pytest.fixture
def create_user_with_credentials(user_factory) -> Callable:
    def wrapper(password: str | None = None, email: str | None = None) -> User:
        user = user_factory()

        if password:
            user.set_password(password)

        if email:
            user.email = email

        user.save()
        return user

    return wrapper


@pytest.fixture
def prepare_user_factory() -> Callable:
    def wrapper(n: int = 1) -> list[User] | User:
        test_data = baker.prepare(
            _model=User,
            _quantity=n,
            _fill_optional=True,
            full_name="Petrov Petr Petrovich",
            institute=baker.prepare(_model=MauInstitute),
            groups=baker.prepare(_model=Group, _quantity=5),
            user_permissions=baker.prepare(_model=Permission, _quantity=5),
        )

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
    def in_expected(self, response_data: dict, expected_data: dict) -> bool:
        for field_name, value in expected_data.items():
            if field_name not in response_data or response_data[field_name] != value:
                return False

        return True


@pytest.fixture()
def helper() -> Helper:
    return Helper()


@pytest.fixture
def fake_request(request_client):
    return request_client.get("api/")


@pytest.fixture
def deserialize(fake_request) -> Callable:
    def wrapper(serializer_class: Serializer, validate: bool = True, **kwargs) -> Any:
        if "request" not in kwargs:
            kwargs.update(context={"request": fake_request})

        serializer = serializer_class(**kwargs)

        if validate:
            serializer.is_valid()
            return serializer.save()

        return serializer

    return wrapper
