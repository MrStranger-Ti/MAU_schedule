from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from django.conf import settings
from mau_auth.forms import UserRegistrationForm, UserLoginForm


class MauRegistrationView(View):
    template_name = 'mau_auth/registration.html'
    form_class = UserRegistrationForm

    def get(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)

        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)

        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()

            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)

        return render(request, self.template_name, context={'form': form})


class MauLoginView(LoginView):
    template_name = 'mau_auth/login.html'
    authentication_form = UserLoginForm
    next_page = reverse_lazy('schedule:index')


class MauPasswordResetView(PasswordResetView):
    template_name = 'mau_auth/password_reset_form.html'
    email_template_name = 'mau_auth/password_reset_email.html'
    success_url = reverse_lazy('mau_auth:password_reset_done')


class MauPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'mau_auth/password_reset_done.html'


class MauPasswordConfirmView(PasswordResetConfirmView):
    template_name = 'mau_auth/password_reset_confirm.html'
    success_url = reverse_lazy('mau_auth:password_reset_complete')


class MauPasswordCompleteView(PasswordResetCompleteView):
    template_name = 'mau_auth/password_reset_complete.html'
