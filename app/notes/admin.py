from django.contrib import admin

from notes.models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = 'pk', 'text', 'user', 'location'
    list_display_links = 'pk', 'text'
