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

    def test_deserialize(self):
        user = UserFactory().make()
        factory = NoteFactory(prepare=True)
        note = factory.make(user=user)
        serialized_data = factory.serialize(note)
        serializer = NoteSerializer(data=serialized_data)
        serializer.is_valid()

        assert serializer.is_valid()
        assert not serializer.errors

    def test_deserialize_fails(self):
        pass
