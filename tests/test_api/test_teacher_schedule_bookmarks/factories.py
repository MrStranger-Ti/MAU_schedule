from typing import Any

from teacher_schedule_bookmarks.models import TeacherScheduleBookmark
from tests.test_api.factories import ModelFactory, T
from tests.test_api.test_mau_auth.factories import UserFactory


class TeacherScheduleBookmarkFactory(ModelFactory):
    model = TeacherScheduleBookmark

    def get_kwargs(self) -> dict[str, Any] | None:
        kwargs = super().get_kwargs()
        kwargs.update(
            {
                "_fill_optional": True,
                "user": UserFactory().make(),
            }
        )
        return kwargs
