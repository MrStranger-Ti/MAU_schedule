from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.forms import ModelForm, Form
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.contrib.auth.tokens import default_token_generator

from django.conf import settings
from django.views.generic import TemplateView

from mau_auth.forms import (
    UserRegistrationForm,
    UserLoginForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
)
from utils.helpers import add_error_class

User = get_user_model()


class MauRegistrationView(UserPassesTestMixin, View):
    template_name = "mau_auth/registration/registration.html"
    form_class = UserRegistrationForm

    def get(self, request: HttpRequest) -> HttpResponse:
        form = self.form_class()
        return render(request, self.template_name, context={"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data["password"])
            user.is_active = False
            user.save()

            user.send_email_confirmation(request)
            return redirect(reverse("mau_auth:registration_email_sent"))

        add_error_class(form, all_fields=False)
        return render(request, self.template_name, context={"form": form})

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect(settings.LOGIN_REDIRECT_URL)


class RegistrationEmailSentView(TemplateView):
    template_name = "mau_auth/registration/email_sent.html"


class RegistrationEmailConfirmView(View):
    template_name = "mau_auth/registration/email_confirm.html"

    def get(self, request: HttpRequest, uidb64: str, token: str) -> HttpResponse:
        uid = urlsafe_base64_decode(uidb64).decode()

        user = User.objects.filter(pk=uid).first()
        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            return render(
                request, self.template_name, context={"email_confirmed": True}
            )

        return render(request, self.template_name, context={"email_confirmed": False})


class MauLoginView(LoginView):
    template_name = "mau_auth/login.html"
    authentication_form = UserLoginForm
    next_page = reverse_lazy("schedule:group_schedule")
    redirect_authenticated_user = True

    def post(self, request: HttpRequest) -> HttpResponse:
        response = super().post(request)

        user = self.request.user
        if user.is_authenticated and (
            not user.institute or not user.course or not user.group
        ):
            return redirect(reverse("profiles:profile_update"))

        return response

    def form_invalid(self, form):
        add_error_class(form, all_fields=True)
        return super().form_invalid(form)


class MauPasswordResetView(PasswordResetView):
    template_name = "mau_auth/password_reset/password_reset_form.html"
    email_template_name = "mau_auth/password_reset/password_reset_email.html"
    subject_template_name = "mau_auth/password_reset/password_reset_subject.html"
    success_url = reverse_lazy("mau_auth:password_reset_done")
    form_class = CustomPasswordResetForm


class MauPasswordResetDoneView(PasswordResetDoneView):
    template_name = "mau_auth/password_reset/password_reset_done.html"


class MauPasswordConfirmView(PasswordResetConfirmView):
    template_name = "mau_auth/password_reset/password_reset_confirm.html"
    success_url = reverse_lazy("mau_auth:password_reset_complete")
    form_class = CustomSetPasswordForm

    def form_invalid(self, form):
        add_error_class(form, all_fields=True)
        return super().form_invalid(form)


class MauPasswordCompleteView(PasswordResetCompleteView):
    template_name = "mau_auth/password_reset/password_reset_complete.html"
