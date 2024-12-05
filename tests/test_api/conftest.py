import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from model_bakery import baker

User = get_user_model()


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def admin_client(api_client) -> APIClient:
    user = baker.make(
        _model=User,
        is_superuser=True,
        is_staff=True,
    )
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def user_client(api_client) -> APIClient:
    user = baker.make(_model=User)
    api_client.force_authenticate(user=user)
    return api_client


class Helper:
    def assert_match_data(self, response_data, expected_data):
        for field_name, value in expected_data.items():
            assert field_name in response_data
            assert response_data[field_name] == value


@pytest.fixture()
def helper() -> Helper:
    return Helper()
