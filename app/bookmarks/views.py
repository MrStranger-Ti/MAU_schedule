import json

from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import render, redirect, reverse
from django.views import View

from bookmarks.models import TeacherScheduleBookmark


class AjaxBookmarksListView(View):
    template_name = 'bookmarks/bookmarks.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
            return HttpResponseNotFound()

        return render(request, self.template_name, context={
            'bookmarks': request.user.bookmarks.all(),
        })


class AjaxBookmarkCreate(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
            return HttpResponseNotFound()

        data = json.loads(request.body)
        bookmark, created = TeacherScheduleBookmark.objects.get_or_create(
            user=request.user,
            teacher_name=data.get('name'),
            teacher_key=data.get('key'),
        )

        if created:
            return redirect(reverse('bookmarks:get_bookmarks_list'))

        return HttpResponseBadRequest()


class AjaxBookmarkDeleteView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
            return HttpResponseNotFound()

        data = json.loads(request.body)
        bookmark = request.user.bookmarks.filter(
            teacher_name=data.get('name'),
            teacher_key=data.get('key'),
        ).first()

        if bookmark:
            bookmark.delete()
            return HttpResponse()

        return HttpResponseBadRequest()
