from django.urls import path

from schedule.views import GroupScheduleView, TeacherScheduleView, get_teacher_schedule_view

app_name = 'schedule'

urlpatterns = [
    path('group/', GroupScheduleView.as_view(), name='group'),
    path('teacher/', TeacherScheduleView.as_view(), name='teacher'),
    path('get_schedule/', get_teacher_schedule_view, name='get_schedule'),
]
