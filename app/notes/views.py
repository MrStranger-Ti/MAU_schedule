import json
import urllib.parse

from datetime import datetime, timedelta

from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
    JsonResponse,
)
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from notes.models import Note
from notes.serializers import NoteSerializer


class AjaxNoteDisplayView(View):
    template_name = "notes/display.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        if request.headers.get("X-Requested-With") != "XMLHttpRequest":
            return HttpResponseNotFound()

        note = request.user.notes.filter(location=request.GET.get("location")).first()
        return JsonResponse(
            {
                "form": render_to_string(self.template_name, request=request),
                "value": note.text,
            }
        )


class AjaxNoteCreateView(View):
    template_name = "notes/create.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        if request.headers.get("X-Requested-With") != "XMLHttpRequest":
            return HttpResponseNotFound()

        return render(request, self.template_name)

    def post(self, request: HttpRequest) -> HttpResponse:
        if request.headers.get("X-Requested-With") != "XMLHttpRequest":
            return HttpResponseNotFound()

        data = json.loads(request.body)
        location = data.get("location")
        text = data.get("text")
        note = Note(user=request.user, location=location, text=text)

        try:
            note.clean()
        except ValidationError:
            return HttpResponseBadRequest()

        expired_date = datetime.strptime(
            location.split(":")[2], "%Y-%m-%d"
        ) + timedelta(weeks=1)
        note.expired_date = expired_date
        note.save()
        return redirect(
            reverse("notes:note_display")
            + "?"
            + f"location={urllib.parse.quote(location)}"
        )


class AjaxNoteDeleteView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        if request.headers.get("X-Requested-With") != "XMLHttpRequest":
            return HttpResponseNotFound()

        data = json.loads(request.body)
        location = data.get("location")

        note = request.user.notes.filter(location=location).first()
        if note:
            note.delete()
            return redirect(reverse("notes:note_create"))

        return HttpResponseBadRequest()


class AjaxNoteUpdateView(View):
    template_name = "notes/update.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        if request.headers.get("X-Requested-With") != "XMLHttpRequest":
            return HttpResponseNotFound()

        note = request.user.notes.filter(location=request.GET.get("location")).first()
        return JsonResponse(
            {
                "form": render_to_string(self.template_name, request=request),
                "value": note.text,
            }
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        if request.headers.get("X-Requested-With") != "XMLHttpRequest":
            return HttpResponseNotFound()

        data = json.loads(request.body)

        note = request.user.notes.filter(location=data.get("location")).first()
        note.text = data.get("text")

        try:
            note.clean()
        except ValidationError:
            return HttpResponseBadRequest()

        note.save()

        return redirect(
            reverse("notes:note_display") + "?" + urllib.parse.urlencode(data)
        )


# RestAPI views


class NoteViewSet(ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]
    search_fields = [
        "location",
        "text",
    ]
    filterset_fields = [
        "user",
        "location",
        "text",
        "expired_date",
    ]
    ordering_fields = [
        "pk",
        "user",
        "text",
    ]
