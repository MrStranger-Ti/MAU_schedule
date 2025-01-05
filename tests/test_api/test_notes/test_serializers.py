from datetime import date, timedelta

import pytest

from notes.api.serializers import NoteSerializer
from tests.test_api.test_mau_auth.factories import UserFactory
from tests.test_api.test_notes.factories import NoteFactory

pytestmark = pytest.mark.django_db


class TestNoteSerializer:
    def test_serialize(self, helper):
        factory = NoteFactory()
        note = factory.make()
        expected_data = factory.serialize(note)
        serializer = NoteSerializer(instance=note)

        assert helper.in_expected(serializer.data, expected_data)

    def test_deserialize(self, serialized_note):
        serializer = NoteSerializer(data=serialized_note)
        serializer.is_valid()

        assert serializer.is_valid()
        assert not serializer.errors

    @pytest.mark.parametrize(
        "wrong_field",
        [
            {
                "schedule_name": "some_name",
                "lesson_number": 0,
                "lesson_number": 8,
                "day": date.today() - timedelta(weeks=2),
                "day": date.today() + timedelta(weeks=4),
            },
        ],
    )
    def test_deserialize_fails(self, wrong_field, serialized_note):
        serialized_note.update(wrong_field)
        serializer = NoteSerializer(data=serialized_note)

        assert not serializer.is_valid()
        assert serializer.errors

    def test_deserialize_miss_user_fail(self, serialized_note):
        serialized_note.pop("user", None)
        serializer = NoteSerializer(data=serialized_note)

        assert not serializer.is_valid()
        assert serializer.errors.get("user")

    def test_update_with_user_fail(self, serialized_note):
        user = UserFactory().make()
        note = NoteFactory(prepare=True).make(user=user)
        serializer = NoteSerializer(instance=note, data=serialized_note)

        assert not serializer.is_valid()
        assert serializer.errors.get("user")
