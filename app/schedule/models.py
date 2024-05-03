from django.db import models

from django.conf import settings


class TeacherScheduleVisitingHistory(models.Model):
    class Meta:
        verbose_name = 'история посещения'
        verbose_name_plural = 'история посещений'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teachers_history',
        verbose_name='пользователь',
    )
    teacher_name = models.CharField(
        verbose_name='ФИО преподавателя',
    )
    teacher_key = models.CharField(
        verbose_name='Ключ преподавателя',
    )
    visited_at = models.DateTimeField(
        auto_now=True,
    )
