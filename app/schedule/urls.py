from django.urls import path

from schedule.views import GroupScheduleView, TeacherScheduleView

app_name = 'schedule'

urlpatterns = [
    path('group/', GroupScheduleView.as_view(), name='group'),
    path('teacher/', TeacherScheduleView.as_view(), name='teacher')
]
