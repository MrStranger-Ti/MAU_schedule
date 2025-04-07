import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse

from schedule.api.mixins import ParserResponseViewMixin
from schedule.parser import ParserResponse
from tests.test_api.test_mau_auth.factories import UserFactory


@pytest.fixture
def mock_get_response(mocker):
    mocker.patch(
        "schedule.api.views.ParserResponseViewMixin.get_response",
        return_value=Response(data="test data"),
    )


class TestParserResponseViewMixin:
    parser_response_data = "test data"
    error_text = "Some error."

    def test_get_response_200(self):
        obj = ParserResponseViewMixin()
        parser_response = ParserResponse(data=self.parser_response_data)

        response = obj.get_response(parser_response)
        assert isinstance(response, Response)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == self.parser_response_data

    def test_get_response_400(self, mocker):
        obj = ParserResponseViewMixin()
        requests_response_mock = mocker.Mock()
        requests_response_mock.status_code == 200
        parser_response = ParserResponse(
            error=self.error_text,
            response=requests_response_mock,
        )

        response = obj.get_response(parser_response)
        assert isinstance(response, Response)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (detail_msg := response.data.get("detail"))
        assert detail_msg == self.error_text

    def test_get_response_503(self):
        obj = ParserResponseViewMixin()
        parser_response = ParserResponse(error=self.error_text)

        response = obj.get_response(parser_response)
        assert isinstance(response, Response)
        assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
        assert (detail_msg := response.data.get("detail"))
        assert detail_msg == self.error_text


@pytest.mark.django_db
def test_group_schedule_api_view(mock_get_response, mocker, get_user_client):
    mock = mocker.patch("schedule.api.views.get_group_schedule")
    user = UserFactory().make()
    client = get_user_client(user)

    period = "test_period"
    url = reverse("api_schedule:group-schedule")
    response = client.get(url, query_params={"period": period})

    assert response.status_code == 200
    mock.assert_called_once()
    mock.assert_called_with(
        institute=user.institute.name,
        course=user.course,
        group=user.group,
        period=period,
    )


@pytest.mark.django_db
def test_teacher_links_api_view(mock_get_response, mocker, get_user_client):
    mock = mocker.patch("schedule.api.views.get_teachers_keys")
    user = UserFactory().make()
    client = get_user_client(user)

    name = "test_name"
    url = reverse("api_schedule:teachers-keys")
    response = client.get(url, query_params={"name": name})

    assert response.status_code == 200
    mock.assert_called_once()
    mock.assert_called_with(name=name)


@pytest.mark.django_db
def test_teacher_schedule_api_view(mock_get_response, mocker, get_user_client):
    mock = mocker.patch("schedule.api.views.get_teacher_schedule")
    user = UserFactory().make()
    client = get_user_client(user)

    teacher_key = "test_teacher_key"
    period = "test_period"
    url = reverse("api_schedule:teacher-schedule", kwargs={"teacher_key": teacher_key})
    response = client.get(url, query_params={"period": period})

    assert response.status_code == 200
    mock.assert_called_once()
    mock.assert_called_with(teacher_key=teacher_key, period=period)


@pytest.mark.django_db
def test_schedule_periods_api_view(mock_get_response, mocker, get_user_client):
    mock = mocker.patch("schedule.api.views.get_periods")
    user = UserFactory().make()
    client = get_user_client(user)

    url = reverse("api_schedule:periods")
    response = client.get(url)

    assert response.status_code == 200
    mock.assert_called_once()
