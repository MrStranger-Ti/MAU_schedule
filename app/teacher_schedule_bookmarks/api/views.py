from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from teacher_schedule_bookmarks.api.serializers import TeacherScheduleBookmarkSerializer
from teacher_schedule_bookmarks.models import TeacherScheduleBookmark


class TeacherScheduleBookmarkViewSet(ModelViewSet):
    serializer_class = TeacherScheduleBookmarkSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = [
        "id",
        "teacher_name",
        "teacher_key",
        "user",
    ]
    filterset_set = [
        "id",
        "teacher_name",
        "teacher_key",
        "user",
    ]
    ordering_fields = [
        "id",
        "teacher_name",
    ]

    def get_queryset(self):
        return TeacherScheduleBookmark.objects.filter(user=self.request.user)
