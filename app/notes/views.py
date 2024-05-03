import json
import urllib.parse

from datetime import datetime, timedelta

from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.core.exceptions import ValidationError

from notes.models import Note


class AjaxNoteDisplayView(View):
    template_name = 'note_block/display.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
            return HttpResponseNotFound()

        note = request.user.notes.filter(
            schedule_name=request.GET.get('schedule_name'),
            group=request.user.group,
            day=request.GET.get('day'),
            lesson_number=request.GET.get('lesson_number'),
        ).first()
        return render(request, self.template_name, context={'note_text': note.text})


class AjaxNoteCreateView(View):
    template_name = 'note_block/create.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
            return HttpResponseNotFound()

        return render(request, self.template_name)

    def post(self, request: HttpRequest) -> HttpResponse:
        if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
            return HttpResponseNotFound()

        data = json.loads(request.body)
        expired_date = datetime.strptime(data['day'], '%Y-%m-%d') + timedelta(weeks=1)
        note = Note(user=request.user, group=request.user.group, expired_date=expired_date, **data)

        try:
            note.clean()
        except ValidationError:
            return HttpResponseBadRequest()

        note.save()
        return redirect(reverse('notes:note_display') + '?' + urllib.parse.urlencode(data))


class AjaxNoteDeleteView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
            return HttpResponseNotFound()

        data = json.loads(request.body)
        note = request.user.notes.filter(group=request.user.group, **data).first()
        if note:
            note.delete()
            return redirect(reverse('notes:note_create'))

        return HttpResponseBadRequest()


class AjaxNoteUpdateView(View):
    template_name = 'note_block/update.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
            return HttpResponseNotFound()

        note = request.user.notes.filter(
            schedule_name=request.GET.get('schedule_name'),
            group=request.user.group,
            day=request.GET.get('day'),
            lesson_number=request.GET.get('lesson_number'),
        ).first()

        return render(request, self.template_name, context={'note_text': note.text})

    def post(self, request: HttpRequest) -> HttpResponse:
        if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
            return HttpResponseNotFound()

        data = json.loads(request.body)

        note = request.user.notes.filter(
            schedule_name=data.get('schedule_name'),
            group=request.user.group,
            day=data.get('day'),
            lesson_number=data.get('lesson_number'),
        ).first()
        note.text = data.get('text')

        try:
            note.clean()
        except ValidationError:
            return HttpResponseBadRequest()

        note.save()

        return redirect(reverse('notes:note_display') + '?' + urllib.parse.urlencode(data))
