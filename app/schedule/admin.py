from django.contrib import admin


class TeacherScheduleBookmarkAdmin(admin.ModelAdmin):
    list_display = 'teacher_name', 'user', 'teacher_key', 'created_at'
    list_display_links = 'teacher_name',
    ordering = 'created_at',
