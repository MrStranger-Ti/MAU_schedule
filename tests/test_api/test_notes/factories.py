import random
from datetime import date
from typing import Any

from django.conf import settings

from notes.models import Note
from tests.test_api.factories import ModelFactory
from tests.test_api.test_mau_auth.factories import UserFactory


class NoteFactory(ModelFactory):
    model = Note

    def get_kwargs(self) -> dict[str:Any]:
        return {
            "_fill_optional": True,
            "user": UserFactory(prepare=self.prepare).make(),
            "schedule_name": random.choice(
                [settings.GROUP_SCHEDULE_NAME, settings.TEACHER_SCHEDULE_NAME]
            ),
            "day": date.today(),
            "lesson_number": random.randint(1, 7),
            "expired_date": None,
        }
