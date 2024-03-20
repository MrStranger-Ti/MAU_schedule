from datetime import datetime, date

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View

from notes.forms import NoteForm
from notes.models import Note


class NoteCreateView(View):
    template_name = 'notes/note_create.html'
    form_class = NoteForm
    success_url = reverse_lazy('schedule:index')

    def get(self, request: HttpRequest, day: str, lesson_number: int) -> HttpResponse:
        day = datetime.strptime(day, '%Y-%m-%d')
        note = request.user.notes.filter(
            user=request.user,
            day=day,
            lesson_number=lesson_number,
        ).first()

        if note:
            form = self.form_class({'text': note.text})
        else:
            form = self.form_class()

        return render(request, self.template_name, context={'form': form})

    def post(self, request: HttpRequest, day: str, lesson_number: int) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            day = datetime.strptime(day, '%Y-%m-%d')
            Note.objects.update_or_create(
                user=request.user,
                day=day,
                lesson_number=lesson_number,
                defaults={
                    'user': request.user,
                    'text': form.cleaned_data.get('text'),
                    'day': day,
                    'lesson_number': lesson_number,
                },
            )
            return redirect(reverse('schedule:index'))

        return render(request, self.template_name, context={'form': self.form_class(form)})
