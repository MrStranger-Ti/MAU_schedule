from django.contrib import admin

from schedule.models import MauInstitute


@admin.register(MauInstitute)
class MauInstituteAdmin(admin.ModelAdmin):
    list_display = "pk", "name"
    list_display_links = "pk", "name"
