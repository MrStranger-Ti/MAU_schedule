from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from mau_auth.auth_class import CookieTokenAuthentication
from teacher_schedule_bookmarks.api.serializers import TeacherScheduleBookmarkSerializer
from teacher_schedule_bookmarks.models import TeacherScheduleBookmark


@extend_schema_view(
    list=extend_schema(
        tags=["Teacher Group Bookmarks"],
        summary="Get list of own teacher schedule bookmarks",
    ),
    create=extend_schema(
        tags=["Teacher Group Bookmarks"],
        summary="Create and get new teacher schedule bookmark",
        responses={
            201: TeacherScheduleBookmarkSerializer,
            400: OpenApiResponse(description="Validation error"),
        },
    ),
    retrieve=extend_schema(
        tags=["Teacher Group Bookmarks"],
        summary="Get teacher schedule bookmark by id",
        responses={
            200: TeacherScheduleBookmarkSerializer,
            404: None,
        },
    ),
    update=extend_schema(
        tags=["Teacher Group Bookmarks"],
        summary="Completely update teacher schedule bookmark by id",
        responses={
            200: TeacherScheduleBookmarkSerializer,
            400: OpenApiResponse(description="Validation error"),
            404: None,
        },
    ),
    partial_update=extend_schema(
        tags=["Teacher Group Bookmarks"],
        summary="Partially update teacher schedule bookmark by id",
        responses={
            200: TeacherScheduleBookmarkSerializer,
            400: OpenApiResponse(description="Validation error"),
            404: None,
        },
    ),
    destroy=extend_schema(
        tags=["Teacher Group Bookmarks"],
        summary="Delete teacher schedule bookmark by id",
        responses={
            204: OpenApiResponse(description="No content"),
            404: None,
        },
    ),
)
class TeacherScheduleBookmarkViewSet(ModelViewSet):
    serializer_class = TeacherScheduleBookmarkSerializer
    authentication_classes = [CookieTokenAuthentication]
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
