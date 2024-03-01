from django.contrib.auth.views import LogoutView
from django.contrib import admin
from django.urls import path

from mau_auth.views import (
    MauRegistrationView,
    MauLoginView,
    MauPasswordResetView,
    MauPasswordResetDoneView,
    MauPasswordConfirmView,
    MauPasswordCompleteView,
)

app_name = 'mau_auth'

urlpatterns = [
    path('registration/', MauRegistrationView.as_view(), name='registration'),
    path('login/', MauLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('password_reset/', MauPasswordResetView.as_view(), name='password_reset_form'),
    path('password_reset/done/', MauPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>', MauPasswordConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', MauPasswordCompleteView.as_view(), name='password_reset_complete'),
]
