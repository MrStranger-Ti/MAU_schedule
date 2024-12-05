import json

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from model_bakery import baker

from tests.test_api.test_mau_auth.conftest import user_factory

User = get_user_model()

pytestmark = pytest.mark.django_db


class TestAdminViewSet:
    url = "/api/accounts/"
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
        helper.assert_match_data(response_data, expected_data)

    def test_retrieve(self, admin_client, user_factory):
        user = user_factory()
        response = admin_client.get(self.get_details_url(user.pk))
        assert response.status_code == status.HTTP_200_OK

    def test_update(self, admin_client, user_factory, helper):
        user = user_factory()
        fake_user = baker.prepare(User, _fill_optional=True)
        expected_data = {
            "full_name": "Petr Petrov Petrovich",
            "email": "testuser@mauniver.ru",
            "password": fake_user.password,
            "institute": 1,
            "course": fake_user.course,
            "group": fake_user.group,
        }

        response = admin_client.put(self.get_details_url(user.pk), data=expected_data)
        assert response.status_code == status.HTTP_200_OK, json.loads(response.content)

        response_data = json.loads(response.content)
        helper.assert_match_data(response_data, expected_data)

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
        helper.assert_match_data(response_data, expected_data)

    def test_delete(self, admin_client, user_factory):
        user = user_factory()

        response = admin_client.delete(self.get_details_url(user.id))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not User.objects.filter(pk=user.pk).exists()
