from datetime import timedelta

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.conf import settings


class Note(models.Model):
    class Meta:
        verbose_name = "note"
        verbose_name_plural = "notes"
        ordering = ("text",)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notes",
        verbose_name="user",
    )
    schedule_name = models.CharField(verbose_name="schedule name")
    schedule_key = models.CharField(null=True, verbose_name="schedule key")
    day = models.DateField(verbose_name="day")
    lesson_number = models.PositiveSmallIntegerField(
        verbose_name="lesson number",
        validators=[MinValueValidator(1), MaxValueValidator(7)],
    )
    text = models.TextField(verbose_name="text")
    expired_date = models.DateField(verbose_name="expire data")

    def __str__(self):
        return f"Note. ID: {self.pk}"

    def save(self, *args, **kwargs):
        if self.id is None:
            self.expired_date = self.day + timedelta(weeks=1)

        super().save(*args, **kwargs)
