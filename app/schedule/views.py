from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseForbidden
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView
from django.conf import settings

from schedule.parser import (
    GroupScheduleParser,
    TeacherScheduleParser,
    TeacherLinksMauParser,
)
from schedule.forms import WeeksForm


class GroupScheduleView(LoginRequiredMixin, TemplateView):
    template_name = "schedule/group/group_schedule.html"


class SearchTeacherView(LoginRequiredMixin, TemplateView):
    template_name = "schedule/teacher/search_teacher.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bookmarks"] = self.request.user.bookmarks.all()
        context["original_schedule_url"] = settings.SCHEDULE_URL
        return context


class TeacherScheduleView(View):
    template_name = "schedule/teacher/teacher_schedule.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "teacher_key": request.GET.get("key"),
            "teacher_name": request.GET.get("name"),
            "table_type": "teacher",
            "bookmarks": request.user.bookmarks.all(),
        }
        return render(request, self.template_name, context=context)


class AjaxView(UserPassesTestMixin, View):
    def test_func(self) -> bool:
        if self.request.headers.get("X-Requested-With") != "XMLHttpRequest":
            return False
        return True

    def handle_no_permission(self):
        return HttpResponseForbidden()


class AjaxGetGroupScheduleView(AjaxView):
    template_name = "schedule/ajax/table.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        user = request.user
        period = request.GET.get("period")

        parser = GroupScheduleParser(user, period=period)
        schedule_data = parser.get_data()

        form = WeeksForm({"periods": parser.get_current_week_option()})
        form.set_period_choices(parser.parsing_storage.get("weeks_options", []))

        context = {
            "form": form,
            "schedule_data": schedule_data,
            "table": settings.GROUP_SCHEDULE_NAME,
            "original_schedule_url": settings.SCHEDULE_URL,
        }

        response = JsonResponse(
            {
                "html": render_to_string(
                    self.template_name, context=context, request=request
                ),
                "notes": [
                    {
                        "location": note.location,
                        "text": note.text,
                    }
                    for note in request.user.notes.defer("location")
                ],
            }
        )
        return response


class AjaxTeachersListView(AjaxView):
    template_name = "schedule/ajax/teachers.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        query = self.request.GET.get("query")
        parser = TeacherLinksMauParser(request.user)
        teachers_links = parser.get_data(query)
        return render(
            request, self.template_name, context={"teachers_links": teachers_links}
        )


class AjaxGetTeacherScheduleView(AjaxView):
    template_name = "schedule/ajax/table.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        teacher_name = request.GET.get("name")
        teacher_key = request.GET.get("key")
        period = request.GET.get("period")

        parser = TeacherScheduleParser(request.user, teacher_key, period=period)
        schedule_data = parser.get_data()

        form = WeeksForm({"periods": parser.get_current_week_option()})
        form.set_period_choices(parser.parsing_storage.get("weeks_options", []))

        context = {
            "form": form,
            "schedule_data": schedule_data,
            "teacher_name": teacher_name,
            "teacher_key": teacher_key,
            "table": settings.TEACHER_SCHEDULE_NAME,
            "bookmarks": self.request.user.bookmarks.all(),
        }

        return JsonResponse(
            {
                "html": render_to_string(
                    self.template_name, context=context, request=request
                ),
                "notes": [
                    {
                        "location": note.location,
                        "text": note.text,
                    }
                    for note in request.user.notes.defer("location")
                ],
            }
        )
