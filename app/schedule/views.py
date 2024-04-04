from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from mau_utils.mau_parser import MauScheduleParser


class IndexPageView(LoginRequiredMixin, TemplateView):
    template_name = 'schedule/index.html'
    paginate_by = 6

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        context = self.get_context_data(*args, **kwargs)

        mau_parser = MauScheduleParser(request.user)
        schedule = mau_parser.get_schedule()
        if schedule:
            obj_list = list(schedule.items())
        else:
            obj_list = list()

        paginator = Paginator(obj_list, self.paginate_by)

        page = request.GET.get('page', 1)
        page_obj = paginator.get_page(page)
        context['page_obj'] = page_obj

        return render(request, self.template_name, context=context)
