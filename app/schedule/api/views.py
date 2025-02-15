from django.conf import settings
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
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

a = get_json(settings.BASE_DIR / "schedule/api/swagger_examples/group_schedule.json")


class GroupScheduleApiView(APIView, ParserResponseViewMixin):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Schedule"],
        summary="Getting group schedule",
        description="User must have institute, course and group.",
        responses={
            200: OpenApiResponse(
                response="",
                examples=[
                    OpenApiExample(
                        "Group schedule example",
                        value=a,
                    )
                ],
            )
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

    def get(self, request: Request) -> Response:
        name = request.query_params.get("name", "")
        parser_response = get_teachers_keys(name=name)
        return self.get_response(parser_response)


class TeacherScheduleApiView(APIView, ParserResponseViewMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, teacher_key: str) -> Response:
        period = request.query_params.get("period")
        parser_response = get_teacher_schedule(teacher_key=teacher_key, period=period)
        return self.get_response(parser_response)


class SchedulePeriodsApiView(APIView, ParserResponseViewMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        parser_response = get_periods()
        return self.get_response(parser_response)
