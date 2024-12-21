import json

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse

from mau_auth.models import MauUser
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

    def test_get_own_queryset(
        self,
        get_user_client,
        get_fake_request,
        get_note_serialized_data,
    ):
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

    def test_create(self, get_user_client, get_note_serialized_data, helper):
        user = UserFactory().make()
        client = get_user_client(user)
        note = NoteFactory(prepare=True).make()
        serialized_data = get_note_serialized_data(note)
        serialized_data.update({"user": user.id})

        response = client.post(self.url, data=serialized_data)
        assert response.status_code == status.HTTP_201_CREATED

        response_data = json.loads(response.content)
        assert helper.in_expected(response_data, serialized_data)

    def test_retrieve(self, get_user_client, get_note_serialized_data):
        user = UserFactory().make()
        client = get_user_client(user)
        note = NoteFactory().make(user=user)
        serialized_data = get_note_serialized_data(note)

        response = client.get(self.get_details_url(note.id))
        assert response.status_code == status.HTTP_200_OK

        response_data = json.loads(response.content)
        assert response_data == serialized_data

    def test_update(self):
        pass

    def test_partial_update(self):
        pass

    def test_delete(self):
        pass
