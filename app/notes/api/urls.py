from django.urls import path, include
from rest_framework.routers import DefaultRouter

from notes.api.views import NoteViewSet

app_name = "api_notes"

notes_router = DefaultRouter()
notes_router.register(
    prefix="notes",
    viewset=NoteViewSet,
    basename="note",
)


urlpatterns = [
    path("", include(notes_router.urls)),
]
