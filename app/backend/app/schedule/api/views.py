from django.conf import settings
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiExample,
    OpenApiParameter,
    extend_schema_view,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from mau_auth.auth_class import CookieTokenAuthentication
from schedule.api.mixins import ParserResponseViewMixin
from schedule.api.serializers import MauInstituteSerializer
from schedule.models import MauInstitute
from schedule.parser import (
    get_group_schedule,
    get_teachers_keys,
    get_teacher_schedule,
    get_periods,
)
from utils.local import get_json


@extend_schema_view(
    list=extend_schema(
        tags=["Schedule"],
        summary="Getting institutes list",
        responses={
            200: OpenApiResponse(
                description="Institutes list",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        "Institutes list example",
                        value=[
                            {"id": 1, "name": "name 1"},
                            {"id": 2, "name": "name 2"},
                            {"id": 3, "name": "name 3"},
                        ],
                    ),
                ],
            ),
        },
    ),
    retrieve=extend_schema(
        tags=["Schedule"],
        summary="Getting institute details",
        responses={
            200: OpenApiResponse(
                description="Institute details",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        "Institute example",
                        value={"id": 3, "name": "name 3"},
                    ),
                ],
            ),
            404: OpenApiResponse(description="Institute not found"),
        },
    ),
)
class InstituteViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = MauInstitute.objects.all()
    serializer_class = MauInstituteSerializer
    authentication_classes = [CookieTokenAuthentication]
    pagination_class = None


class GroupScheduleApiView(APIView, ParserResponseViewMixin):
    authentication_classes = [CookieTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Schedule"],
        summary="Getting group schedule",
        description="User must have institute, course and group.",
        responses={
            200: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        "Group schedule example",
                        value=get_json(
                            settings.BASE_DIR
                            / "schedule/api/swagger_examples/group_schedule.json",
                        ),
                    ),
                ],
            ),
            400: OpenApiResponse(description="Invalid institute, course or group"),
            503: OpenApiResponse(description="Official schedule is unavailable"),
        },
    )
    def get(self, request: Request) -> Response:
        period = request.query_params.get("period")
        parser_response = get_group_schedule(
            institute=request.user.institute.name,
            course=request.user.course,
            group=request.user.group,
            period=period,
        )
        return self.get_response(parser_response)


class TeachersKeysApiView(APIView, ParserResponseViewMixin):
    authentication_classes = [CookieTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Schedule"],
        summary="Getting teachers keys for teacher schedule",
        description="Query param 'name' is required",
        parameters=[
            OpenApiParameter(
                name="name",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=True,
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        "Teachers keys example",
                        value=get_json(
                            settings.BASE_DIR
                            / "schedule/api/swagger_examples/teachers_keys.json",
                        ),
                    ),
                ],
            ),
            503: OpenApiResponse(description="Official schedule is unavailable"),
        },
    )
    def get(self, request: Request) -> Response:
        name = request.query_params.get("name", "")
        parser_response = get_teachers_keys(name=name)
        return self.get_response(parser_response)


class TeacherScheduleApiView(APIView, ParserResponseViewMixin):
    authentication_classes = [CookieTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Schedule"],
        summary="Getting teacher schedule",
        description="Need to get teacher key",
        parameters=[
            OpenApiParameter(
                name="teacher_key",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                required=True,
            )
        ],
        responses={
            200: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        "Teacher schedule example",
                        value=get_json(
                            settings.BASE_DIR
                            / "schedule/api/swagger_examples/teacher_schedule.json",
                        ),
                    ),
                ],
            ),
            400: OpenApiResponse(description="Invalid teacher key"),
            503: OpenApiResponse(description="Official schedule is unavailable"),
        },
    )
    def get(self, request: Request, teacher_key: str) -> Response:
        period = request.query_params.get("period")
        parser_response = get_teacher_schedule(teacher_key=teacher_key, period=period)
        return self.get_response(parser_response)


class SchedulePeriodsApiView(APIView, ParserResponseViewMixin):
    authentication_classes = [CookieTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Schedule"],
        summary="Getting schedule periods",
        responses={
            200: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        "Schedule periods example",
                        value=get_json(
                            settings.BASE_DIR
                            / "schedule/api/swagger_examples/periods.json",
                        ),
                    ),
                ],
            ),
            503: OpenApiResponse(description="Official schedule is unavailable"),
        },
    )
    def get(self, request: Request) -> Response:
        parser_response = get_periods()
        return self.get_response(parser_response)
