from django.conf import settings
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiExample,
    OpenApiRequest,
    OpenApiParameter,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from schedule.api.mixins import ParserResponseViewMixin
from schedule.parser import (
    get_group_schedule,
    get_teachers_keys,
    get_teacher_schedule,
    get_periods,
)
from utils.local import get_json


class GroupScheduleApiView(APIView, ParserResponseViewMixin):
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
                    )
                ],
            ),
            400: OpenApiResponse(description="Invalid institute, course or group"),
            503: OpenApiResponse(description="Official schedule is unavailable now"),
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
            )
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
                    )
                ],
            ),
            503: OpenApiResponse(description="Official schedule is unavailable now"),
        },
    )
    def get(self, request: Request) -> Response:
        name = request.query_params.get("name", "")
        parser_response = get_teachers_keys(name=name)
        return self.get_response(parser_response)


class TeacherScheduleApiView(APIView, ParserResponseViewMixin):
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
                    )
                ],
            ),
            400: OpenApiResponse(description="Invalid teacher key"),
            503: OpenApiResponse(description="Official schedule is unavailable now"),
        },
    )
    def get(self, request: Request, teacher_key: str) -> Response:
        period = request.query_params.get("period")
        parser_response = get_teacher_schedule(teacher_key=teacher_key, period=period)
        return self.get_response(parser_response)


class SchedulePeriodsApiView(APIView, ParserResponseViewMixin):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Schedule"],
        summary="Getting schedule periods",
        responses={
            200: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        "Teacher schedule example",
                        value=get_json(
                            settings.BASE_DIR
                            / "schedule/api/swagger_examples/teachers_keys.json",
                        ),
                    )
                ],
            ),
            503: OpenApiResponse(description="Official schedule is unavailable now"),
        },
    )
    def get(self, request: Request) -> Response:
        parser_response = get_periods()
        return self.get_response(parser_response)
