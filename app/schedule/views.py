from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView

from schedule.tasks import get_schedule_data


class IndexPageView(LoginRequiredMixin, TemplateView):
    template_name = 'schedule/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['schedule'] = self.request.user.get_schedule()
        return context
