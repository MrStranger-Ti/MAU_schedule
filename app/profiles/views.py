from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from profiles.forms import ProfileUpdateForm
from utils.helpers import add_error_class

User = get_user_model()


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profiles/profile.html'


class ProfileUpdateView(LoginRequiredMixin, FormView):
    template_name = 'profiles/profile_update.html'
    form_class = ProfileUpdateForm
    success_url = reverse_lazy('profiles:profile')

    def form_valid(self, form):
        user = self.request.user
        user.full_name = form.cleaned_data['full_name']
        user.institute = form.cleaned_data['institute']
        user.course = form.cleaned_data['course']
        user.group = form.cleaned_data['group']
        user.save()

        return super().form_valid(form)
    
    def form_invalid(self, form):
        add_error_class(form)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = context.get('form')
        if not form.errors:
            user = self.request.user
            prepared_user_data = {
                'full_name': user.full_name,
                'institute': user.institute,
                'course': user.course,
                'group': user.group,
            }
            form = self.form_class(prepared_user_data)
            context['form'] = form

        return context
