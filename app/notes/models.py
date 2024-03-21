from datetime import datetime
from typing import Optional

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
    day = models.DateField(verbose_name='дата')
    lesson_number = models.IntegerField(verbose_name='номер пары')
    text = models.CharField(verbose_name='текст')

    def __str__(self):
        return f'Заметка, ID: {self.pk}'

    @classmethod
    def get_note(cls, user: settings.AUTH_USER_MODEL, day: str, lesson_number: int) -> Optional['Note']:
        day = datetime.strptime(day, '%Y-%m-%d')
        note = Note.objects.filter(
            user=user,
            day=day,
            lesson_number=lesson_number,
        ).first()
        if note:
            return note
        return None
