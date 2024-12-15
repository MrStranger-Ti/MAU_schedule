from django.urls import path, include
from rest_framework.routers import DefaultRouter

from mau_auth.api.views import (
    UserViewSet,
    AdminViewSet,
    ObtainAuthTokenAPIView,
    PasswordResetViewSet,
    GroupViewSet,
    PermissionViewSet,
    RegisterAPIView,
    RegisterConfirmAPIView,
)

app_name = "api_mau_auth"

auth_router = DefaultRouter()
auth_router.register(
    prefix="users",
    viewset=AdminViewSet,
    basename="user",
)
auth_router.register(
    prefix="groups",
    viewset=GroupViewSet,
    basename="group",
)
auth_router.register(
    prefix="permissions",
    viewset=PermissionViewSet,
    basename="permission",
)

urlpatterns = [
    path("", include(auth_router.urls)),
    path(
        "me/",
        UserViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
            },
        ),
        name="me",
    ),
    path("register/", RegisterAPIView.as_view(), name="register"),
    path(
        "register/confirm/<uidb64>/<token>/",
        RegisterConfirmAPIView.as_view(),
        name="register-confirm",
    ),
    path(
        "token/",
        ObtainAuthTokenAPIView.as_view(),
        name="get-token",
    ),
    path(
        "password-reset/",
        PasswordResetViewSet.as_view({"post": "password_reset"}),
        name="password-reset",
    ),
    path(
        "password-reset/confirm/<uidb64>/<token>/",
        PasswordResetViewSet.as_view({"post": "password_reset_confirm"}),
        name="password-set",
    ),
]
