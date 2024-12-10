import pytest
from django.contrib.auth import get_user_model

from mau_auth.api.serializers import AdminUserSerializer
from mau_auth.models import MauUser

pytestmark = pytest.mark.django_db

User: type[MauUser] = get_user_model()


class TestAdminUserSerializer:
    def test_serialize(self, user_factory, json_user):
        user = user_factory()
        expected_serialized_data = json_user(user, exclude_fields=["password"])
        serializer = AdminUserSerializer(instance=user)
        assert serializer.data == expected_serialized_data

    def test_deserialize(self, user_factory, json_user):
        user = user_factory()
        user.delete()
        serialized_data = json_user(
            user=user,
            exclude_fields=["id", "groups", "user_permissions"],
        )
        serializer = AdminUserSerializer(data=serialized_data)
        serializer.is_valid()
        assert serializer.is_valid()
        assert not serializer.errors
