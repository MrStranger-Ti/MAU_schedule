from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from mau_auth.models import MauUser


@admin.register(MauUser)
class MauUserAdmin(UserAdmin):
    list_display = (
        "full_name",
        "email",
        "institute",
        "course",
        "group",
    )
    list_display_links = ("full_name",)
    ordering = ["full_name", "course"]
    fieldsets = (
        ("Главная информация", {"fields": ("full_name", "email", "password")}),
        ("Данные об учащимся", {"fields": ("institute", "course", "group")}),
        (
            "Дополнительная информация",
            {"fields": ("is_staff", "is_active", "date_joined", "last_login")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "fields": ("email", "password", "full_name"),
            },
        ),
    )
