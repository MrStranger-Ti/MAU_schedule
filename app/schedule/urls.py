from django.urls import path

from schedule.views import IndexPageView

app_name = 'schedule'

urlpatterns = [
    path('', IndexPageView.as_view(), name='index'),
]
