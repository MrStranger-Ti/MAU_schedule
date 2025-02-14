from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from notes.api.serializers import NoteSerializer
from notes.models import Note


class NoteViewSet(ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]
    search_fields = [
        "id",
        "user",
        "schedule_name",
        "group",
        "day",
        "lesson_number",
        "text",
        "expired_date",
    ]
    filterset_fields = [
        "id",
        "user",
        "group",
        "day",
        "lesson_number",
        "text",
        "expired_date",
    ]
    ordering_fields = [
        "pk",
        "user",
        "text",
    ]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)
