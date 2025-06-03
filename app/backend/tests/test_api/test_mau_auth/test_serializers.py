from collections.abc import Callable

import pytest
from django.contrib.auth import get_user_model
from rest_framework.serializers import Serializer

from mau_auth.serializers import (
    AdminUserSerializer,
    AuthenticatedUserSerializer,
    RegisterConfirmationSerializer,
    AuthTokenSerializer,
    PasswordResetConfirmationSerializer,
)
from mau_auth.models import MauUser, TokenInfo
from tests.test_api.conftest import faker
from tests.test_api.test_mau_auth.factories import UserFactory

User: type[MauUser] = get_user_model()

pytestmark = pytest.mark.django_db

admin_serialized_data = {
    "full_name": "Petrov Petr Petrovich",
    "email": "testuser@mauniver.ru",
    "password": "testuser",
    "institute": 1,
    "course": 3,
    "group": "Some group",
    "is_superuser": True,
    "is_staff": True,
    "is_active": True,
}

user_serialized_data = {
    "full_name": "Petrov Petr Petrovich",
    "email": "testuser@mauniver.ru",
    "password": "testuser",
    "institute": 1,
    "course": 3,
    "group": "Some group",
}


class TestUserSerializers:
    @pytest.mark.parametrize(
        "serializer_class",
        [AdminUserSerializer, AuthenticatedUserSerializer],
    )
    def test_serialize(self, serializer_class, helper):
        user = UserFactory().make()
        expected_data = helper.serialize(user, exclude=["password"])
        serializer = serializer_class(instance=user)
        assert serializer.data == expected_data

    @pytest.mark.parametrize(
        ["serializer_class", "serialized_data"],
        [
            (AdminUserSerializer, admin_serialized_data),
            (AuthenticatedUserSerializer, user_serialized_data),
        ],
    )
    def test_deserialize(self, serializer_class, serialized_data, deserialize):
        serializer = deserialize(
            serializer_class=serializer_class,
            data=serialized_data,
            validate=False,
        )
        assert serializer.is_valid()
        assert not serializer.errors

    @pytest.mark.parametrize(
        ["serializer_class", "serialized_data"],
        [
            (AdminUserSerializer, admin_serialized_data),
            (AuthenticatedUserSerializer, user_serialized_data),
        ],
    )
    def test_deserialize_password_set(
        self,
        serializer_class,
        serialized_data,
        deserialize,
    ):
        user = deserialize(serializer_class=serializer_class, data=serialized_data)
        password = serialized_data.get("password", None)
        assert user.check_password(password)

    @pytest.mark.parametrize(
        "serializer_class",
        [AdminUserSerializer, AuthenticatedUserSerializer],
    )
    def test_deserialize_required_fields_fails(self, serializer_class, deserialize):
        required_fields = user_serialized_data
        for field_name in required_fields:
            serialized_data = required_fields.copy()
            serialized_data.pop(field_name, None)
            serializer = deserialize(
                serializer_class=serializer_class,
                data=serialized_data,
                validate=False,
            )
            assert not serializer.is_valid()
            assert serializer.errors


class TestAdminUserSerializer:
    def test_password_update_admin(self, deserialize):
        password_field = {"password": admin_serialized_data.get("password")}
        user = UserFactory().make()
        user = deserialize(
            serializer_class=AdminUserSerializer,
            instance=user,
            data=admin_serialized_data,
            partial=True,
        )
        assert user.check_password(password_field.get("password"))


class TestAuthenticatedUserSerializer:
    def test_authenticated_user_set_is_active_on_false(self, deserialize):
        user = deserialize(
            serializer_class=AuthenticatedUserSerializer,
            data=user_serialized_data,
        )
        assert not user.is_active

    @pytest.mark.parametrize(
        "wrong_field",
        [
            {"password": "testuser"},
            {"email": "example@mauniver.ru"},
        ],
    )
    def test_update_authenticated_user_fails(self, wrong_field):
        user = UserFactory().make()
        serialized_data = {
            "full_name": "Petrov Petr Petrovich",
            "institute": 1,
            "course": 3,
            "group": "Some group",
        }
        serialized_data.update(wrong_field)
        serializer = AuthenticatedUserSerializer(instance=user, data=serialized_data)
        assert not serializer.is_valid()
        assert serializer.errors


class TestRegisterConfirmationSerializer:
    def test_is_active_set_on_true(self, deserialize):
        user = UserFactory().make()
        uidb64, token = user.get_uidb64_and_token()
        TokenInfo.objects.create(user=user, token_type="register")
        user = deserialize(
            serializer_class=RegisterConfirmationSerializer,
            data={"uidb64": uidb64, "token": token},
        )
        assert user
        assert user.is_active


class TestPasswordResetConfirmationSerializer:
    def test_deserialize(self):
        user = UserFactory().make()
        uidb64, token = user.get_uidb64_and_token()
        TokenInfo.objects.create(user=user, token_type="password-reset")
        serializer = PasswordResetConfirmationSerializer(
            data={"uidb64": uidb64, "token": token},
        )
        assert serializer.is_valid()
        assert not serializer.errors


class TestAuthTokenSerializer:
    @pytest.fixture()
    def get_serializer(self, deserialize) -> Callable:
        def wrapper(**kwargs) -> Serializer:
            return deserialize(
                serializer_class=AuthTokenSerializer,
                validate=False,
                **kwargs,
            )

        return wrapper

    def test_deserialize(self, create_user_with_credentials, get_serializer):
        credentials = {
            "password": faker.password(),
            "email": faker.email(domain="mauniver.ru"),
        }
        user = create_user_with_credentials(**credentials)

        serializer = get_serializer(data=credentials)
        assert serializer.is_valid()
        assert not serializer.errors

        user.refresh_from_db()
        assert serializer.save() == user.auth_token.key

    @pytest.mark.parametrize(
        "credentials",
        [
            {},
            {"password": faker.password()},
            {"email": faker.email(domain="mauniver.ru")},
        ],
    )
    def test_deserialize_miss_credentials(
        self,
        credentials,
        create_user_with_credentials,
        get_serializer,
    ):
        create_user_with_credentials(**credentials)
        serializer = get_serializer(data=credentials)
        assert not serializer.is_valid()
        assert serializer.errors

    def test_deserialize_invalid_credentials(
        self,
        create_user_with_credentials,
        get_serializer,
    ):
        credentials = {
            "password": faker.password(),
            "email": faker.email(domain="mauniver.ru"),
        }
        create_user_with_credentials(**credentials)
        credentials.update(
            {"password": "anotherpwd", "email": "wrongemail@mauniver.ru"}
        )

        serializer = get_serializer(data=credentials)
        assert not serializer.is_valid()
        assert serializer.errors
