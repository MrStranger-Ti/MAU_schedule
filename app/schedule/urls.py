from django.urls import path

from schedule.views import (
    GroupScheduleView,
    SearchTeacherView,
    TeacherScheduleView,
    AjaxGetGroupScheduleView,
    AjaxGetTeacherScheduleView,
    AjaxTeachersListView,
)

app_name = 'schedule'

urlpatterns = [
    path('group/', GroupScheduleView.as_view(), name='group_schedule'),

    path('teacher-search/', SearchTeacherView.as_view(), name='teacher_search'),
    path('teacher-search/teacher/', TeacherScheduleView.as_view(), name='teacher_schedule'),

    path('get-group-schedule/', AjaxGetGroupScheduleView.as_view(), name='get_group_schedule'),
    path('get-teacher-schedule/', AjaxGetTeacherScheduleView.as_view(), name='get_teacher_schedule'),
    path('get-teachers-links/', AjaxTeachersListView.as_view(), name='get_teachers_links'),
]
