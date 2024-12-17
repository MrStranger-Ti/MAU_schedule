import json

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from model_bakery import baker
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse

from tests.test_api.conftest import faker
from tests.test_api.test_mau_auth.test_serializers import user_serialized_data

User = get_user_model()

pytestmark = pytest.mark.django_db


class TestAdminViewSet:
    url = reverse("api_mau_auth:user-list")
    total_instances = 5

    def get_details_url(self, _id: int):
        return self.url + f"{_id}/"

    def test_list(self, admin_client, user_factory):
        user_factory(self.total_instances)

        response = admin_client.get(path=self.url)
        assert response.status_code == status.HTTP_200_OK

        response_data = json.loads(response.content)
        if users := response_data.get("results"):
            assert len(users) == self.total_instances + 1
        else:
            assert len(response_data) == self.total_instances + 1

    def test_create(self, admin_client, helper):
        fake_user = baker.prepare(User, _fill_optional=True)
        initial_data = {
            "full_name": "Petr Petrov Petrovich",
            "email": "test@mauniver.ru",
            "password": fake_user.password,
            "institute": 1,
            "course": fake_user.course,
            "group": fake_user.group,
        }
        expected_data = initial_data.copy()
        expected_data.pop("password")

        response = admin_client.post(path=self.url, data=initial_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

        response_data = json.loads(response.content)
        assert helper.in_expected(response_data, expected_data)

    def test_retrieve(self, admin_client, user_factory):
        user = user_factory()
        response = admin_client.get(self.get_details_url(user.pk))
        assert response.status_code == status.HTTP_200_OK

    def test_update(self, admin_client, user_factory, helper):
        user = user_factory()
        fake_user = baker.prepare(User, _fill_optional=True)
        json_data = {
            "full_name": "Petr Petrov Petrovich",
            "email": "testuser@mauniver.ru",
            "password": fake_user.password,
            "institute": 1,
            "course": fake_user.course,
            "group": fake_user.group,
        }
        response = admin_client.put(self.get_details_url(user.pk), data=json_data)
        assert response.status_code == status.HTTP_200_OK

        expected_data = json_data.copy()
        password = expected_data.pop("password", None)

        user.refresh_from_db()
        assert user.check_password(password)

        response_data = json.loads(response.content)
        assert helper.in_expected(response_data, expected_data)

    @pytest.mark.parametrize(
        ["field_name", "value"],
        [
            ("full_name", "Petr Petrov Petrovich"),
            ("course", None),
            ("institute", 1),
            ("group", None),
        ],
    )
    def test_partial_update(
        self,
        field_name,
        value,
        admin_client,
        user_factory,
        helper,
    ):
        user = user_factory()
        fake_user = baker.prepare(User, _fill_optional=True)
        fake_value = value or getattr(fake_user, field_name)
        expected_data = {field_name: fake_value}

        response = admin_client.patch(self.get_details_url(user.id), data=expected_data)
        assert response.status_code == status.HTTP_200_OK

        response_data = json.loads(response.content)
        assert helper.in_expected(response_data, expected_data)

    def test_delete(self, admin_client, user_factory):
        user = user_factory()

        response = admin_client.delete(self.get_details_url(user.id))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not User.objects.filter(pk=user.pk).exists()


class TestUserViewSet:
    url = reverse("api_mau_auth:me-detail")

    def test_retrieve(self, user_client, get_serialized_data):
        response = user_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

        user = User.objects.all().first()
        expected_data = get_serialized_data(user=user, exclude_fields=["password"])
        response_data = json.loads(response.content)
        assert response_data == expected_data

    def test_update(self, user_client, helper):
        json_data = {
            "full_name": "Test Test Test",
            "institute": 3,
            "course": 3,
            "group": "Some Group",
        }

        response = user_client.put(self.url, data=json_data)
        assert response.status_code == status.HTTP_200_OK

        response_data = json.loads(response.content)
        assert helper.in_expected(response_data, json_data)

    @pytest.mark.parametrize(
        "field",
        [
            {"full_name": "Test Test Test"},
            {"institute": 3},
            {"course": 3},
            {"group": "Some Group"},
        ],
    )
    def test_partial_update(self, field, user_client, helper):
        response = user_client.patch(self.url, data=field)
        assert response.status_code == status.HTTP_200_OK

        response_data = json.loads(response.content)
        assert helper.in_expected(response_data, field)


class TestRegisterAPIViews:
    def test_register(self, api_client):
        url = reverse("api_mau_auth:register")
        response = api_client.post(url, data=user_serialized_data)
        assert response.status_code == status.HTTP_201_CREATED

        users = User.objects.all()
        assert len(users) == 1
        assert user_serialized_data.get("email") == users.first().email

    def test_register_confirm(self, user_factory, api_client):
        user = user_factory()
        confirmation_url = user.get_confirmation_url("api_mau_auth:register-confirm")
        response = api_client.get(confirmation_url)
        assert response.status_code == status.HTTP_200_OK, confirmation_url


class TestObtainTokenAPIView:
    url = reverse("api_mau_auth:get-token")

    def test_token_in_data(self, api_client, create_user_with_credentials):
        credentials = {"password": "testuser", "email": "example@mauniver.ru"}
        create_user_with_credentials(**credentials)
        response = api_client.post(self.url, data=credentials)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("token")


class TestPasswordResetAPIViews:
    def test_password_reset(self, user_factory, api_client):
        user = user_factory()
        response = api_client.post(
            reverse("api_mau_auth:password-reset"),
            data={"email": user.email},
        )
        assert response.status_code == status.HTTP_200_OK

    def test_password_reset_confirm(self, user_factory, api_client):
        user = user_factory()
        Token.objects.create(user=user)
        confirmation_url = user.get_confirmation_url("api_mau_auth:password-set")
        new_password = faker.password()
        response = api_client.post(
            confirmation_url,
            data={"password1": new_password, "password2": new_password},
        )
        assert response.status_code == status.HTTP_200_OK

        user.refresh_from_db()
        assert user.check_password(new_password)
