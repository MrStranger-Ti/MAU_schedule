import pytest
from django.contrib.auth import get_user_model

from mau_auth.models import MauUser
from tests.test_api.test_notes.factories import NoteFactory

User: type[MauUser] = get_user_model()


@pytest.fixture
def serialized_note(helper):
    note = NoteFactory(prepare=True).make()
    serialized = helper.serialize(note)
    return serialized
