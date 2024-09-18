from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView


class IndexView(UserPassesTestMixin, TemplateView):
    template_name = "core/index.html"

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect(reverse("schedule:group_schedule"))
