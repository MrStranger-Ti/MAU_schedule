from django.contrib import admin


class TeacherScheduleVisitingHistoryAdmin(admin.ModelAdmin):
    list_display = 'teacher_name', 'user', 'teacher_key', 'visited_at'
    list_display_links = 'teacher_name',
    ordering = 'visited_at',
