from django.urls import path, re_path
from rest_framework.routers import DefaultRouter

from teacher_schedule_bookmarks.views import (
    AjaxBookmarksListView,
    AjaxBookmarkDeleteView,
    AjaxBookmarkCreate,
)

from teacher_schedule_bookmarks.views import (
    BookmarkViewSet,
)

app_name = "bookmarks"

router = DefaultRouter()
router.register(
    prefix="bookmarks",
    viewset=BookmarkViewSet,
)


urlpatterns = [
    path("display/", AjaxBookmarksListView.as_view(), name="get_bookmarks_list"),
    path("create/", AjaxBookmarkCreate.as_view(), name="create_bookmark"),
    path("delete/", AjaxBookmarkDeleteView.as_view(), name="delete_bookmark"),
    # api
    # path("", BookmarkList.as_view(), name="list"),
    # re_path(r"^(?P<pk>\d+)/?$", BookmarkDetails.as_view(), name="details"),
]
