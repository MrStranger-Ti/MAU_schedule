from django.urls import path

from notes.views import NoteChangeCreateView, NoteDeleteView


app_name = 'notes'


urlpatterns = [
    path('<str:day>/<int:lesson_number>', NoteChangeCreateView.as_view(), name='note'),
    path('<str:day>/<int:lesson_number>/delete', NoteDeleteView.as_view(), name='note_delete'),
]
