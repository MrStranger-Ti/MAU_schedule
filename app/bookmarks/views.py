import json

from django.core.serializers import serialize
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseNotFound,
    HttpResponseBadRequest,
    Http404,
)
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from bookmarks.models import TeacherScheduleBookmark
from bookmarks.serializers import BookmarkSerializer


class AjaxBookmarksListView(View):
    template_name = "bookmarks/bookmarks.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        if request.headers.get("X-Requested-With") != "XMLHttpRequest":
            return HttpResponseNotFound()

        return render(
            request,
            self.template_name,
            context={
                "bookmarks": request.user.bookmarks.all(),
            },
        )


class AjaxBookmarkCreate(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        if request.headers.get("X-Requested-With") != "XMLHttpRequest":
            return HttpResponseNotFound()

        data = json.loads(request.body)
        bookmark, created = TeacherScheduleBookmark.objects.get_or_create(
            user=request.user,
            teacher_name=data.get("name"),
            teacher_key=data.get("key"),
        )

        if created:
            return redirect(reverse("bookmarks:get_bookmarks_list"))

        return HttpResponseBadRequest()


class AjaxBookmarkDeleteView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        if request.headers.get("X-Requested-With") != "XMLHttpRequest":
            return HttpResponseNotFound()

        data = json.loads(request.body)
        bookmark = request.user.bookmarks.filter(
            teacher_name=data.get("name"),
            teacher_key=data.get("key"),
        ).first()

        if bookmark:
            bookmark.delete()
            return redirect(reverse("bookmarks:get_bookmarks_list"))

        return HttpResponseBadRequest()


# RestAPI views


class BookmarkViewSet(ModelViewSet):
    queryset = TeacherScheduleBookmark.objects.all()
    serializer_class = BookmarkSerializer
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]
    filterset_fields = [
        "id",
        "user",
        "teacher_name",
        "teacher_key",
        "created_at",
    ]
    search_fields = [
        "id",
        "user",
        "teacher_name",
        "teacher_key",
        "created_at",
    ]
    ordering = [
        "id",
        "user",
        "teacher_name",
        "created_at",
    ]


# class BookmarkList(APIView):
#     model = TeacherScheduleBookmark
#     serializer = BookmarkSerializer
#
#     def get(self, request: Request) -> Response:
#         bookmarks = self.model.objects.all()
#         serializer = self.serializer(bookmarks, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request: Request) -> Response:
#         serializer = self.serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class BookmarkDetails(APIView):
#     model = TeacherScheduleBookmark
#     serializer = BookmarkSerializer
#
#     def get_object(self, pk: int) -> TeacherScheduleBookmark:
#         try:
#             return self.model.objects.get(pk=pk)
#         except self.model.DoesNotExist:
#             raise Http404(f"Bookmark {pk} not found")
#
#     def get(self, request: Request, pk: int) -> Response:
#         bookmark = self.get_object(pk=pk)
#         serializer = self.serializer(bookmark)
#         return Response(serializer.data)
#
#     def put(self, request: Request, pk: int) -> Response:
#         bookmark = self.get_object(pk=pk)
#         serializer = self.serializer(bookmark, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def patch(self, request: Request, pk: int) -> Response:
#         bookmark = self.get_object(pk=pk)
#         serializer = self.serializer(bookmark, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request: Request, pk: int) -> Response:
#         bookmark = self.get_object(pk=pk)
#         bookmark.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
