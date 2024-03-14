from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView


class IndexPageView(LoginRequiredMixin, TemplateView):
    template_name = 'schedule/index.html'

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        context = self.get_context_data(*args, **kwargs)

        schedule = self.request.user.get_schedule()
        paginator = Paginator(list(schedule.items()), 6)

        page = request.GET.get('page', 1)
        page_obj = paginator.get_page(page)
        context['page_obj'] = page_obj

        return render(request, self.template_name, context=context)
