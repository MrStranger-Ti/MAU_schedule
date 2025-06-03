from django.urls import path, include
from rest_framework.routers import DefaultRouter

from teacher_schedule_bookmarks.views import TeacherScheduleBookmarkViewSet

app_name = "api_teacher_schedule_bookmarks"

teacher_schedule_bookmarks_router = DefaultRouter()
teacher_schedule_bookmarks_router.register(
    prefix="teacher-schedule-bookmarks",
    viewset=TeacherScheduleBookmarkViewSet,
    basename="bookmark",
)


urlpatterns = [
    path("", include(teacher_schedule_bookmarks_router.urls)),
]
