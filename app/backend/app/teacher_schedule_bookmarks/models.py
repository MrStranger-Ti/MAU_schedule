from django.db import models

from django.conf import settings


class TeacherScheduleBookmark(models.Model):
    class Meta:
        verbose_name = "история посещения"
        verbose_name_plural = "история посещений"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookmarks",
        verbose_name="пользователь",
    )
    teacher_name = models.CharField(verbose_name="ФИО преподавателя")
    teacher_key = models.CharField(verbose_name="Ключ преподавателя")
    created_at = models.DateTimeField(auto_now_add=True)
