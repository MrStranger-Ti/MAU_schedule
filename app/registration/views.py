from django.http import HttpRequest
from django.shortcuts import render
from django.views import View


class MauRegistrationView(View):
    form_class = RegisterForm

    def get(self, request: HttpRequest):
        pass
