from django.urls import path

from mau_auth.api.views import (
    UserViewSet,
    AdminViewSet,
    RegisterViewSet,
    ObtainAuthToken,
    PasswordResetViewSet,
)

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
        "my/",
        UserViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
            },
        ),
        name="my",
    ),
    path(
        "register/",
        RegisterViewSet.as_view(
            {
                "post": "register",
            },
        ),
        name="register",
    ),
    path(
        "register/confirm/<uidb64>/<token>/",
        RegisterViewSet.as_view(
            {
                "get": "register_confirm",
            },
        ),
        name="register_confirm",
    ),
    path(
        "token/",
        ObtainAuthToken.as_view(),
        name="get_token",
    ),
    path(
        "password-reset/",
        PasswordResetViewSet.as_view({"post": "password_reset"}),
        name="password_reset",
    ),
    path(
        "password-reset/confirm/<uidb64>/<token>/",
        PasswordResetViewSet.as_view({"post": "password_reset_confirm"}),
        name="password_set",
    ),
]
