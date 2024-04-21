from django.contrib import admin

from notes.models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = 'pk', 'text', 'user', 'schedule_name', 'day', 'lesson_number'
    list_display_links = 'pk', 'text'
