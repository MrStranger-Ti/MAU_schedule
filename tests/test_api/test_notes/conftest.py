from datetime import date
from typing import Callable, Any, Iterable
from zoneinfo import ZoneInfo

import pytest
from django.contrib.auth import get_user_model

from mau_auth.models import MauUser
from notes.models import Note

User: type[MauUser] = get_user_model()


@pytest.fixture
def get_note_serialized_data() -> Callable:
    def wrapper(note: Note) -> dict[str, Any]:
        json_data = {
            "schedule_name": note.schedule_name,
            "group": note.group,
            "day": note.day.isoformat(),
            "lesson_number": note.lesson_number,
            "text": note.text,
        }

        if note.id:
            json_data["id"] = note.id

        if note.expired_date:
            json_data["expired_date"] = note.expired_date.isoformat()

        if note.user.id:
            json_data["user"] = note.user.id

        return json_data

    return wrapper
