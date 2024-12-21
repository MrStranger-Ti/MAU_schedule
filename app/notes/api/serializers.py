from datetime import date, datetime, timedelta

from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from notes.models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"
        read_only_fields = ["id", "expired_date"]

    def validate_schedule_name(self, value: str) -> str:
        if value not in (
            settings.GROUP_SCHEDULE_NAME,
            settings.TEACHER_SCHEDULE_NAME,
        ):
            raise ValidationError(
                f"Schedule_name must be {settings.GROUP_SCHEDULE_NAME} "
                f"or {settings.TEACHER_SCHEDULE_NAME}"
            )

        return value

    def validate_lesson_number(self, value: int) -> int:
        if value not in range(1, 8):
            raise ValidationError(
                "Lesson number must be in the range from 1 to 7.",
            )

        return value

    def validate_day(self, value: date) -> date:
        now = date.today()
        if not now - timedelta(weeks=1) <= value <= now + timedelta(weeks=3):
            raise ValidationError("Invalid day")

        return value
