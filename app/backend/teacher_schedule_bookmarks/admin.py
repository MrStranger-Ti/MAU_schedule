from django.contrib import admin

from teacher_schedule_bookmarks.models import TeacherScheduleBookmark


@admin.register(TeacherScheduleBookmark)
class TeacherScheduleBookmarkAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "teacher_name",
        "teacher_key",
        "created_at",
    )
    list_display_links = (
        "id",
        "teacher_name",
    )
