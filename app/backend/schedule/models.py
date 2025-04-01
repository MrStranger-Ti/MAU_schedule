from django.db import models


class MauInstitute(models.Model):
    class Meta:
        verbose_name = "институт"
        verbose_name_plural = "институты"
        ordering = ("name",)

    name = models.CharField(max_length=20, verbose_name="Название")

    def __str__(self):
        return self.name
