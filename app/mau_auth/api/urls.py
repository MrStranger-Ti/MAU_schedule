from django.urls import path

from mau_auth.api.views import UserViewSet, CustomObtainAuthToken, AdminViewSet

app_name = "api_mau_auth"


urlpatterns = [
    path(
        "",
        AdminViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            },
        ),
        name="user_list",
    ),
    path(
        "<int:pk>/",
        AdminViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            },
        ),
        name="user_details",
    ),
    path(
        "register/",
        UserViewSet.as_view(
            {
                "post": "register",
            },
        ),
        name="register",
    ),
    path(
        "register/confirm/",
        UserViewSet.as_view(
            {
                "post": "register_confirm",
            },
        ),
        name="register_confirm",
    ),
    path(
        "my/",
        UserViewSet.as_view(
            {
                "get": "my",
            },
        ),
        name="my",
    ),
    path(
        "token/",
        CustomObtainAuthToken.as_view(),
        name="login",
    ),
]
