from datetime import datetime, date, timedelta
from typing import Optional

from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings


class Note(models.Model):
    class Meta:
        verbose_name = 'заметка'
        verbose_name_plural = 'заметки'
        ordering = 'text',

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notes',
        verbose_name='пользователь',
    )
    schedule_name = models.CharField(null=True, verbose_name='название таблицы')
    group = models.CharField(null=True, verbose_name='группа')
    day = models.DateField(verbose_name='дата')
    lesson_number = models.IntegerField(verbose_name='номер пары')
    text = models.CharField(verbose_name='текст')
    expired_date = models.DateField(null=True, verbose_name='Дата удаления')

    def __str__(self):
        return f'Заметка, ID: {self.pk}'

    def clean(self):
        if self.schedule_name not in (settings.GROUP_SCHEDULE_NAME, settings.TEACHER_SCHEDULE_NAME):
            raise ValidationError(
                {'schedule_name': f'Название расписания может быть {settings.GROUP_SCHEDULE_NAME} или {settings.TEACHER_SCHEDULE_NAME}'},
            )

        lesson_number = str(self.lesson_number)
        if not lesson_number.isdigit() or int(lesson_number) not in range(1, 8):
            raise ValidationError(
                {'lesson_number': 'Номер занятия может быть в диапазоне от 1 до 7 включительно'},
            )

        if isinstance(self.day, date):
            date_value = self.day
            now = date.today()
        else:
            date_value = datetime.strptime(self.day, '%Y-%m-%d')
            now = datetime.now()

        if not now - timedelta(weeks=1) <= date_value <= now + timedelta(weeks=3):
            raise ValidationError(
                {'day', 'Неверная дата'},
            )
