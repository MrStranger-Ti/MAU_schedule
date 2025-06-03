from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from mau_auth.auth_class import CookieTokenAuthentication
from notes.serializers import NoteSerializer
from notes.models import Note


@extend_schema_view(
    list=extend_schema(
        tags=["Notes"],
        summary="Get list of own notes",
    ),
    create=extend_schema(
        tags=["Notes"],
        summary="Create and get new note",
        responses={
            201: NoteSerializer,
            400: OpenApiResponse(description="Validation error"),
        },
    ),
    retrieve=extend_schema(
        tags=["Notes"],
        summary="Get note by id",
        responses={
            200: NoteSerializer,
            404: None,
        },
    ),
    update=extend_schema(
        tags=["Notes"],
        summary="Completely update note by id",
        responses={
            200: NoteSerializer,
            400: OpenApiResponse(description="Validation error"),
            404: None,
        },
    ),
    partial_update=extend_schema(
        tags=["Notes"],
        summary="Partially update note by id",
        responses={
            200: NoteSerializer,
            400: OpenApiResponse(description="Validation error"),
            404: None,
        },
    ),
    destroy=extend_schema(
        tags=["Notes"],
        summary="Delete note by id",
        responses={
            204: OpenApiResponse(description="No content"),
            404: None,
        },
    ),
)
class NoteViewSet(ModelViewSet):
    serializer_class = NoteSerializer
    authentication_classes = [CookieTokenAuthentication]
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
        "schedule_key",
        "day",
        "lesson_number",
        "text",
        "expired_date",
    ]
    filterset_fields = [
        "id",
        "user",
        "schedule_key",
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
