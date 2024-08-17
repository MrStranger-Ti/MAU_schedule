from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.views.generic import TemplateView
from django.core.cache import cache
from django.conf import settings

from mau_utils.mau_parser import MauScheduleParser
from mau_utils.mau_requests import get_teachers_urls, get_schedule_data


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
        page = request.GET.get('page', 1)

        schedule_data = cache.get(f'schedule_of_group_{user.group}')
        if not schedule_data:
            mau_parser = MauScheduleParser(user)
            schedule_data = mau_parser.get_group_schedule()
            cache.set(
                f'schedule_of_group_{user.group}',
                schedule_data,
                settings.SCHEDULE_CACHE_TIME,
            )

        paginator_data = schedule_data or dict()
        paginator = Paginator(list(paginator_data.items()), 6)
        page_obj = paginator.get_page(page)

        context = {
            'page_obj': page_obj,
            'table': settings.GROUP_SCHEDULE_NAME,
            'original_schedule_url': settings.SCHEDULE_URL
        }

        return render(request, self.template_name, context=context)


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

        schedule_data = cache.get(f'teacher_schedule_{teacher_key}')
        if not schedule_data:
            url = settings.SCHEDULE_URL + f'schedule2.php?key={teacher_key}'
            schedule_data = get_schedule_data(url, tables=True)
            cache.set(f'teacher_schedule_{teacher_key}', schedule_data, settings.SCHEDULE_CACHE_TIME)

        paginator = Paginator(list(schedule_data.items()), 6)
        page_obj = paginator.get_page(page)

        context = {
            'page_obj': page_obj,
            'teacher_name': teacher_name,
            'teacher_key': teacher_key,
            'table': settings.TEACHER_SCHEDULE_NAME,
            'bookmarks':  self.request.user.bookmarks.all(),
        }

        return render(request, self.template_name, context=context)
