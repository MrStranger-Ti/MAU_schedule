from django.urls import path

from schedule.api.views import (
    GroupParserResponseApiView,
    TeacherLinksApiView,
    TeacherParserResponseApiView,
    SchedulePeriodsApiView,
)

app_name = "api_schedule"

urlpatterns = [
    path(
        "schedule/group/", GroupParserResponseApiView.as_view(), name="group-schedule"
    ),
    path(
        "schedule/teachers-keys/", TeacherLinksApiView.as_view(), name="teachers-keys"
    ),
    path(
        "schedule/teacher/<str:teacher_key>/",
        TeacherParserResponseApiView.as_view(),
        name="teacher-schedule",
    ),
    path("schedule/periods/", SchedulePeriodsApiView.as_view(), name="periods"),
]
