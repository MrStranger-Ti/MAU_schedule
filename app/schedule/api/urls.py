from django.urls import path, include
from rest_framework.routers import DefaultRouter

from schedule.api.views import InstituteViewSet

app_name = "api_schedule"

schedule_router = DefaultRouter()
schedule_router.register(
    prefix="",
    viewset=InstituteViewSet,
    basename="institute",
)

urlpatterns = [
    path("", include(schedule_router.urls)),
]
