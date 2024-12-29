import random
from datetime import date
from typing import Any

from django.conf import settings
from django.forms import model_to_dict

from notes.models import Note
from tests.test_api.factories import ModelFactory, T
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

    def serialize(self, obj: T, **kwargs) -> dict[str, Any]:
        exclude = kwargs.get("exclude")
        if not exclude:
            kwargs["exclude"] = exclude = []

        if "expired_date" not in exclude:
            exclude.append("expired_date")

        json_obj = super().serialize(obj, **kwargs)

        if day := obj.day:
            json_obj["day"] = day.isoformat()

        return json_obj
