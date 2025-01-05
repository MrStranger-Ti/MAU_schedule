import pytest
from django.contrib.auth import get_user_model

from mau_auth.models import MauUser
from tests.test_api.test_mau_auth.factories import UserFactory
from tests.test_api.test_notes.factories import NoteFactory

User: type[MauUser] = get_user_model()


@pytest.fixture
def serialized_note():
    user = UserFactory().make()
    factory = NoteFactory(prepare=True)
    note = factory.make(user=user)
    return factory.serialize(note)
