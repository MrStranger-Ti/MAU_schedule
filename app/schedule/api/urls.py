from django.urls import path

from schedule.api.views import (
    GroupScheduleApiView,
    TeachersKeysApiView,
    TeacherScheduleApiView,
    SchedulePeriodsApiView,
)

app_name = "api_schedule"

urlpatterns = [
    path("schedule/group/", GroupScheduleApiView.as_view(), name="group-schedule"),
    path(
        "schedule/teachers-keys/",
        TeachersKeysApiView.as_view(),
        name="teachers-keys",
    ),
    path(
        "schedule/teacher/<str:teacher_key>/",
        TeacherScheduleApiView.as_view(),
        name="teacher-schedule",
    ),
    path("schedule/periods/", SchedulePeriodsApiView.as_view(), name="periods"),
]
