from typing import Callable, Any

import pytest
import faker

from django.contrib.auth import get_user_model

from rest_framework.request import Request
from rest_framework.serializers import Serializer
from rest_framework.test import APIClient, APIRequestFactory


from mau_auth.models import MauUser
from tests.helpers import Helper
from tests.test_api.test_mau_auth.factories import UserFactory

User: type[MauUser] = get_user_model()

faker = faker.Faker()


@pytest.fixture
def request_client() -> APIRequestFactory:
    return APIRequestFactory()


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def create_user_with_credentials() -> Callable:
    def wrapper(password: str | None = None, email: str | None = None) -> User:
        user = UserFactory().make()

        if password:
            user.set_password(password)

        if email:
            user.email = email

        user.save()
        return user

    return wrapper


@pytest.fixture
def get_user_client(api_client) -> Callable:
    def wrapper(user: User = UserFactory().make()) -> APIClient:
        api_client.force_authenticate(user=user)
        return api_client

    return wrapper


@pytest.fixture
def admin_client(api_client) -> APIClient:
    admin = UserFactory().make()
    admin.is_superuser = True
    admin.is_staff = True
    admin.save()
    api_client.force_authenticate(user=admin)
    return api_client


@pytest.fixture()
def helper() -> Helper:
    return Helper()


@pytest.fixture
def get_fake_request(request_client) -> Callable:
    def wrapper(url: str = "/api/") -> Request:
        return request_client.get(url)

    return wrapper


@pytest.fixture
def deserialize(get_fake_request) -> Callable:
    def wrapper(serializer_class: Serializer, validate: bool = True, **kwargs) -> Any:
        if "request" not in kwargs:
            kwargs.update(context={"request": get_fake_request()})

        serializer = serializer_class(**kwargs)

        if validate:
            serializer.is_valid()
            return serializer.save()

        return serializer

    return wrapper
