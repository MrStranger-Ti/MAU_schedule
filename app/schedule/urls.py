from django.urls import path

from schedule.views import (
    GroupScheduleView,
    SearchTeacherView,
    TeacherScheduleView,
    ajax_get_teacher_schedule_view,
    ajax_get_group_schedule_view,
)

app_name = 'schedule'

urlpatterns = [
    path('group/', GroupScheduleView.as_view(), name='group_schedule'),

    path('teacher-search/', SearchTeacherView.as_view(), name='teacher_search'),
    path('teacher-search/teacher/', TeacherScheduleView.as_view(), name='teacher_schedule'),

    path('get-group-schedule/', ajax_get_group_schedule_view, name='get_group_schedule'),
    path('get-teacher-schedule/', ajax_get_teacher_schedule_view, name='get_teacher_schedule'),
]
