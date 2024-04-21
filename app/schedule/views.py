from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.views.generic import TemplateView
from django.core.cache import cache
from django.conf import settings

from mau_utils.mau_parser import MauScheduleParser
from mau_utils.mau_requests import get_teachers_urls, get_schedule_data


class GroupScheduleView(LoginRequiredMixin, View):
    template_name = 'schedule/group_schedule.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        page = request.GET.get('page', 1)
        return render(request, self.template_name, context={'page': page})


class AjaxGetGroupScheduleView(View):
    template_name = 'schedule/table.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
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
            }

            return render(request, self.template_name, context=context)

        return HttpResponseNotFound()


class SearchTeacherView(LoginRequiredMixin, TemplateView):
    template_name = 'schedule/search_teacher.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query')
        context['query'] = query

        if query:
            teachers_links = cache.get(f'query_{query}')
            if not teachers_links:
                teachers_links = get_teachers_urls(query)
                cache.set(f'query_{query}', teachers_links, settings.SCHEDULE_CACHE_TIME)

            context['teachers_links'] = teachers_links

        return context


class TeacherScheduleView(View):
    template_name = 'schedule/teacher_schedule.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        query = request.GET.get('query')
        if query:
            url = reverse('schedule:teacher_search') + f'?query={query}'
            return redirect(url)

        context = {
            'teacher': request.GET.get('teacher'),
            'page': request.GET.get('page', 1),
        }
        return render(request, self.template_name, context=context)


class AjaxGetTeacherScheduleView(View):
    template_name = 'schedule/table.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            teacher_url = request.GET.get('teacher')
            page = request.GET.get('page', 1)

            schedule_data = cache.get(f'teacher_schedule_{teacher_url}')
            if not schedule_data:
                url = settings.SCHEDULE_URL + f'schedule2.php?key={teacher_url}'
                schedule_data = get_schedule_data(url, tables=True)
                cache.set(f'teacher_schedule_{teacher_url}', schedule_data, settings.SCHEDULE_CACHE_TIME)

            paginator = Paginator(list(schedule_data.items()), 6)
            page_obj = paginator.get_page(page)

            context = {
                'page_obj': page_obj,
                'teacher': teacher_url,
                'table': settings.TEACHER_SCHEDULE_NAME,
            }

            return render(request, self.template_name, context=context)

        return HttpResponseNotFound()
