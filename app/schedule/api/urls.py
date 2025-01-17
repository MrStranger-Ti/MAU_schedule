from django.urls import path

from schedule.api.views import (
    GroupScheduleApiView,
    TeacherLinksApiView,
    TeacherScheduleApiView,
)

app_name = "api_schedule"

urlpatterns = [
    path("schedule/group/", GroupScheduleApiView.as_view(), name="group_schedule"),
    path("schedule/teachers/", TeacherLinksApiView.as_view(), name="teachers"),
    path(
        "schedule/teacher/",
        TeacherScheduleApiView.as_view(),
        name="teacher_schedule",
    ),
]
