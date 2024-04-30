from django.urls import path

from notes.views import AjaxNoteDisplayView, AjaxNoteCreateView, AjaxNoteDeleteView, AjaxNoteUpdateView

app_name = 'notes'


urlpatterns = [
    path('display/', AjaxNoteDisplayView.as_view(), name='note_display'),
    path('create/', AjaxNoteCreateView.as_view(), name='note_create'),
    path('delete/', AjaxNoteDeleteView.as_view(), name='note_delete'),
    path('update/', AjaxNoteUpdateView.as_view(), name='note_update'),
]
