from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from schedule.api.mixins import ScheduleViewMixin
from schedule.parser import get_group_schedule, get_teacher_links, get_teacher_schedule


class GroupScheduleApiView(APIView, ScheduleViewMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        period = request.query_params.get("period")
        parser_response = get_group_schedule(
            institute=request.user.institute.name,
            course=request.user.course,
            group=request.user.group,
            period=period,
        )
        return self.get_response(parser_response)


class TeacherLinksApiView(APIView, ScheduleViewMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        name = request.query_params.get("name", "")
        parser_response = get_teacher_links(name=name)
        return self.get_response(parser_response)


class TeacherScheduleApiView(APIView, ScheduleViewMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, teacher_key: str) -> Response:
        period = request.query_params.get("period")
        parser_response = get_teacher_schedule(teacher_key=teacher_key, period=period)
        return self.get_response(parser_response)
