from django.urls import path

from bookmarks.views import AjaxBookmarksListView, AjaxBookmarkDeleteView, AjaxBookmarkCreate

app_name = 'bookmarks'


urlpatterns = [
    path('display/', AjaxBookmarksListView.as_view(), name='get_bookmarks_list'),
    path('create/', AjaxBookmarkCreate.as_view(), name='create_bookmark'),
    path('delete/', AjaxBookmarkDeleteView.as_view(), name='delete_bookmark'),
]
