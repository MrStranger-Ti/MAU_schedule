import json
from datetime import date

import pytest
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import status
from rest_framework.reverse import reverse

from mau_auth.models import MauUser
from notes.models import Note
from tests.test_api.test_mau_auth.factories import UserFactory
from tests.test_api.test_notes.factories import NoteFactory

User: type[MauUser] = get_user_model()

pytestmark = pytest.mark.django_db


class TestNoteViewSet:
    url = reverse("api_notes:note-list")

    def get_details_url(self, _id):
        return f"{self.url}{_id}/"

    def test_authenticated_user_perm(self, get_user_client, helper):
        assert helper.has_permission(client=get_user_client(), url=self.url)

    def test_unauthenticated_user_perm(self, api_client, helper):
        assert not helper.has_permission(client=api_client, url=self.url)

    def test_list(self, get_user_client):
        user = UserFactory().make()
        NoteFactory(quantity=5).make(user=user)

        client = get_user_client(user=user)
        response = client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

        response_data = json.loads(response.content)
        if notes := response_data.get("results"):
            assert len(notes) == 5
        else:
            assert len(response_data) == 5

    def test_get_own_queryset(self, get_user_client, get_fake_request):
        for _ in range(3):
            NoteFactory(quantity=5).make()

        user = UserFactory().make()
        notes_ids = sorted(
            note_id.id for note_id in NoteFactory(quantity=5).make(user=user)
        )

        client = get_user_client(user)
        response = client.get(self.url)
        response_notes_ids = sorted(
            note_data.get("id")
            for note_data in json.loads(response.content).get("results")
        )
        assert notes_ids == response_notes_ids

    def test_create(self, get_user_client, helper):
        user = UserFactory().make()
        note_factory = NoteFactory(prepare=True)
        note = note_factory.make()
        serialized_data = note_factory.serialize(note, exclude=["id"])
        serialized_data.update({"user": user.id})

        client = get_user_client(user)
        response = client.post(self.url, data=serialized_data)
        assert response.status_code == status.HTTP_201_CREATED

        response_data = json.loads(response.content)
        assert helper.in_expected(response_data, serialized_data)

    def test_retrieve(self, get_user_client, helper):
        user = UserFactory().make()
        note_factory = NoteFactory()
        note = note_factory.make(user=user)
        expected_data = note_factory.serialize(note)

        client = get_user_client(user)
        response = client.get(self.get_details_url(note.id))
        assert response.status_code == status.HTTP_200_OK

        response_data = json.loads(response.content)
        assert helper.in_expected(response_data, expected_data)

    def test_update(self, get_user_client, helper):
        user = UserFactory().make()
        note = NoteFactory().make(user=user)

        fake_note_factory = NoteFactory(prepare=True)
        fake_note = fake_note_factory.make()
        serialized_data = fake_note_factory.serialize(fake_note, exclude=["id", "user"])

        client = get_user_client(user)
        response = client.put(self.get_details_url(note.id), data=serialized_data)
        assert response.status_code == status.HTTP_200_OK

        response_data = json.loads(response.content)
        assert helper.in_expected(response_data, serialized_data)

    @pytest.mark.parametrize(
        "field",
        [
            {"schedule_name": settings.TEACHER_SCHEDULE_NAME},
            {"group": "some group"},
            {"day": date.today().isoformat()},
            {"lesson_number": 3},
            {"text": "some text"},
        ],
    )
    def test_partial_update(self, field, get_user_client, helper):
        user = UserFactory().make()
        client = get_user_client(user)
        note = NoteFactory().make(user=user)

        response = client.patch(self.get_details_url(note.id), data=field)
        assert response.status_code == status.HTTP_200_OK

        response_data = json.loads(response.content)
        assert helper.in_expected(response_data, field)

    def test_delete(self, get_user_client):
        user = UserFactory().make()
        note = NoteFactory().make(user=user)

        client = get_user_client(user)
        response = client.delete(self.get_details_url(note.id))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Note.objects.filter(id=note.id).exists()
