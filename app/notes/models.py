from datetime import datetime, date, timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings


class Note(models.Model):
    class Meta:
        verbose_name = "заметка"
        verbose_name_plural = "заметки"
        ordering = ("text",)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notes",
        verbose_name="пользователь",
    )
    location = models.CharField(null=True, unique=True, verbose_name="расположение")
    text = models.TextField(verbose_name="текст")
    expired_date = models.DateField(null=True, verbose_name="дата удаления")

    def __str__(self):
        return f"Заметка, ID: {self.pk}"

    def clean(self):
        print(self.location)
        schedule_name, _, day, lesson_number = self.location.split(":")

        if schedule_name not in (
            settings.GROUP_SCHEDULE_NAME,
            settings.TEACHER_SCHEDULE_NAME,
        ):
            raise ValidationError(
                {
                    "schedule_name": f"Название расписания может быть {settings.GROUP_SCHEDULE_NAME} или {settings.TEACHER_SCHEDULE_NAME}"
                },
            )

        lesson_number = str(lesson_number)
        if not lesson_number.isdigit() or int(lesson_number) not in range(1, 8):
            raise ValidationError(
                {
                    "lesson_number": "Номер занятия может быть в диапазоне от 1 до 7 включительно"
                },
            )

        if isinstance(day, date):
            date_value = day
            now = date.today()
        else:
            date_value = datetime.strptime(day, "%Y-%m-%d")
            now = datetime.now()

        if not now - timedelta(weeks=1) <= date_value <= now + timedelta(weeks=3):
            raise ValidationError(
                {"day", "Неверная дата"},
            )
