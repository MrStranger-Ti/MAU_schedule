from django.urls import path

from notes.views import NoteCreateView


app_name = 'notes'


urlpatterns = [
    path('add/<str:day>/<int:lesson_number>', NoteCreateView.as_view(), name='note_create'),
]
