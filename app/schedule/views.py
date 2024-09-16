import re

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect, reverse
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView
from django.core.cache import cache
from django.conf import settings

from mau_utils.mau_parser import ScheduleParser
from mau_utils.mau_requests import get_teachers_urls, get_schedule_data
from schedule.forms import WeeksForm


class GroupScheduleView(LoginRequiredMixin, View):
    template_name = 'schedule/group/group_schedule.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            'page': request.GET.get('page', 1),
        }
        return render(request, self.template_name, context=context)


class AjaxGetGroupScheduleView(View):
    template_name = 'schedule/ajax/table.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
            return HttpResponseNotFound()

        user = request.user
        period = request.GET.get('period')
        if week and week.isdigit():
            week = int(week)
        else:
            week = None

        mau_parser = ScheduleParser(user, teacher_schedule=False)
        schedule_data = cache.get(f'schedule_group_{user.group}_week_{week or "current"}')
        if not schedule_data:
            schedule_data = mau_parser.get_group_schedule(week)
            cache.set(
                f'schedule_group_{user.group}_week_{week}',
                schedule_data,
                settings.SCHEDULE_CACHE_TIME,
            )

        form = WeeksForm()
        form.fields['weeks_periods'].choices = mau_parser.storage.weeks_options

        context = {
            'form': form,
            'schedule_data': schedule_data,
            'table': settings.GROUP_SCHEDULE_NAME,
            'original_schedule_url': settings.SCHEDULE_URL,
        }

        response = JsonResponse({
            'html': render_to_string(self.template_name, context=context, request=request),
            'notes': [
                {
                    'location': note.location,
                    'text': note.text,
                }
                for note in request.user.notes.defer('location')
            ],
        })
        return response


class SearchTeacherView(LoginRequiredMixin, TemplateView):
    template_name = 'schedule/teacher/search_teacher.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bookmarks'] = self.request.user.bookmarks.all()
        context['original_schedule_url'] = settings.SCHEDULE_URL
        return context


class AjaxTeachersListView(View):
    template_name = 'schedule/ajax/teachers.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
            return HttpResponseNotFound()

        query = self.request.GET.get('query')
        teachers_links = cache.get(f'query_{query}')
        if not teachers_links:
            teachers_links = get_teachers_urls(query)
            cache.set(f'query_{query}', teachers_links, settings.SCHEDULE_CACHE_TIME)

        return render(request, self.template_name, context={'teachers_links': teachers_links})


class TeacherScheduleView(View):
    template_name = 'schedule/teacher/teacher_schedule.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            'teacher_key': request.GET.get('key'),
            'teacher_name': request.GET.get('name'),
            'page': request.GET.get('page', 1),
            'table_type': 'teacher',
            'bookmarks': request.user.bookmarks.all(),
        }
        return render(request, self.template_name, context=context)


class AjaxGetTeacherScheduleView(View):
    template_name = 'schedule/ajax/table.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
            return HttpResponseNotFound()

        teacher_name = request.GET.get('name')
        teacher_key = request.GET.get('key')
        page = request.GET.get('page', 1)

        if not re.fullmatch(r'[1-3]', page):
            page = 1
        else:
            page = int(page)

        schedule_data = cache.get(f'teacher_schedule_{teacher_key}_page_{page}')
        if not schedule_data:
            url = settings.SCHEDULE_URL + f'schedule2.php?key={teacher_key}'
            schedule_data = get_schedule_data(url, teacher_schedule=True, week_step=page - 1)
            cache.set(
                f'teacher_schedule_{teacher_key}_page_{page}',
                schedule_data,
                settings.SCHEDULE_CACHE_TIME,
            )

        context = {
            'schedule_data': schedule_data,
            'current_page': page,
            'teacher_name': teacher_name,
            'teacher_key': teacher_key,
            'table': settings.TEACHER_SCHEDULE_NAME,
            'bookmarks':  self.request.user.bookmarks.all(),
        }

        return JsonResponse({
            'html': render_to_string(self.template_name, context=context, request=request),
            'notes': [
                {
                    'location': note.location,
                    'text': note.text,
                }
                for note in request.user.notes.defer('location')
            ],
        })
