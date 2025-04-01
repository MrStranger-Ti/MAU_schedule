import pytest
import json

from faker import Faker

from rest_framework import status
from rest_framework.reverse import reverse

from teacher_schedule_bookmarks.models import TeacherScheduleBookmark
from tests.test_api.test_mau_auth.factories import UserFactory
from tests.test_api.test_teacher_schedule_bookmarks.factories import (
    TeacherScheduleBookmarkFactory,
)

pytestmark = pytest.mark.django_db

faker = Faker()


class TestTeacherScheduleBookmarkViewSet:
    url = reverse("api_teacher_schedule_bookmarks:bookmark-list")

    def get_details_url(self, _id):
        return f"{self.url}{_id}/"

    def test_authenticated_user_perm(self, get_user_client, helper):
        assert helper.has_permission(client=get_user_client(), url=self.url)

    def test_unauthenticated_user_perm(self, api_client, helper):
        assert not helper.has_permission(client=api_client, url=self.url)

    def test_get_own_queryset(self, get_user_client, helper):
        factory = TeacherScheduleBookmarkFactory(quantity=5)
        TeacherScheduleBookmarkFactory(quantity=5).make()

        user = UserFactory().make()
        user_bookmarks = factory.make(user=user)

        client = get_user_client(user=user)
        response = client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

        expected_data = helper.serialize_all(user_bookmarks)
        assert helper.equals_expected_and_response(expected_data, response)

    def test_list(self, get_user_client, helper):
        user = UserFactory().make()
        bookmarks = TeacherScheduleBookmarkFactory(quantity=5).make(user=user)

        client = get_user_client(user=user)
        response = client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

        expected_data = helper.serialize_all(bookmarks)
        assert helper.equals_expected_and_response(expected_data, response)

    def test_create(self, get_user_client, helper):
        prepared_bookmark = TeacherScheduleBookmarkFactory(prepare=True).make()
        serialized_prepared_bookmark = helper.serialize(
            prepared_bookmark,
            exclude=["id"],
        )

        client = get_user_client()
        response = client.post(self.url, data=serialized_prepared_bookmark)
        assert response.status_code == status.HTTP_201_CREATED

        bookmark = TeacherScheduleBookmark.objects.all().first()
        assert bookmark

        expected_data = helper.serialize(bookmark)
        assert helper.equals_expected_and_response(expected_data, response)

    def test_retrieve(self, get_user_client, helper):
        user = UserFactory().make()
        bookmark = TeacherScheduleBookmarkFactory().make(user=user)

        client = get_user_client(user=user)
        response = client.get(self.get_details_url(bookmark.id))
        assert response.status_code == status.HTTP_200_OK

        expected_data = helper.serialize(bookmark)
        assert helper.equals_expected_and_response(expected_data, response)

    def test_update(self, get_user_client, helper):
        user = UserFactory().make()
        bookmark = TeacherScheduleBookmarkFactory().make(user=user)

        new_bookmark = TeacherScheduleBookmarkFactory(prepare=True).make()
        new_data = helper.serialize(new_bookmark, exclude=["id"])

        client = get_user_client(user=user)
        response = client.put(self.get_details_url(bookmark.id), data=new_data)
        assert response.status_code == status.HTTP_200_OK

        bookmark.refresh_from_db()
        expected_data = helper.serialize(bookmark)
        assert helper.equals_expected_and_response(expected_data, response)

    @pytest.mark.parametrize(
        "partial_data",
        [
            {"teacher_name": faker.name()},
            {"teacher_key": faker.text()},
        ],
    )
    def test_partial_update(self, partial_data, get_user_client, helper):
        user = UserFactory().make()
        bookmark = TeacherScheduleBookmarkFactory().make(user=user)

        client = get_user_client(user=user)
        response = client.patch(self.get_details_url(bookmark.id), data=partial_data)
        assert response.status_code == status.HTTP_200_OK

        bookmark.refresh_from_db()
        expected_data = helper.serialize(bookmark)
        assert helper.equals_expected_and_response(expected_data, response)

    def test_delete(self, get_user_client):
        user = UserFactory().make()
        bookmark = TeacherScheduleBookmarkFactory().make(user=user)

        client = get_user_client(user=user)
        response = client.delete(self.get_details_url(bookmark.id))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not TeacherScheduleBookmark.objects.all().exists()
