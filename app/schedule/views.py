from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.cache import cache
from django.conf import settings

from mau_utils.mau_parser import MauScheduleParser
from mau_utils.mau_requests import get_teachers_urls, get_schedule_data


class GroupScheduleView(LoginRequiredMixin, TemplateView):
    template_name = 'schedule/group.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        page = self.request.GET.get('page', 1)

        schedule_data = cache.get(f'schedule_of_group_{user.group}')
        if not schedule_data:
            mau_parser = MauScheduleParser(user)
            schedule_data = mau_parser.get_group_schedule()
            cache.set(
                f'schedule_of_group_{user.group}',
                schedule_data or 'null',
                settings.SCHEDULE_CACHE_TIME,
            )

        obj_list = list(schedule_data.items()) if isinstance(schedule_data, dict) else list()
        paginator = Paginator(obj_list, self.paginate_by)
        page_obj = paginator.get_page(page)
        context['page_obj'] = page_obj

        return context


class TeacherScheduleView(LoginRequiredMixin, TemplateView):
    template_name = 'schedule/teacher.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query')
        context['query'] = query

        if query:
            teachers_links = cache.get(f'query_{query}')
            if not teachers_links:
                teachers_links = get_teachers_urls(query)

            context['teachers_links'] = teachers_links

        return context


def get_teacher_schedule_view(request: HttpRequest) -> HttpResponse:
    teacher_url = request.GET.get('teacher')
    page = request.GET.get('page', 1)

    schedule_data = cache.get(f'teacher_schedule_{teacher_url}')
    if not schedule_data:
        schedule_data = get_schedule_data(teacher_url)
        cache.set(f'teacher_schedule_{teacher_url}', schedule_data, settings.SCHEDULE_CACHE_TIME)

    paginator = Paginator(schedule_data.items(), 6)
    page_obj = paginator.get_page(page)

    return render(request, 'schedule/schedule.html', context={'page_obj': page_obj})
