from django.urls import path, include
from rest_framework.routers import DefaultRouter

from mau_auth.api import views

app_name = "api_mau_auth"

router = DefaultRouter()
router.register(prefix="users", viewset=views.AdminViewSet, basename="user")
router.register(prefix="groups", viewset=views.GroupViewSet, basename="group")
router.register(
    prefix="permissions", viewset=views.PermissionViewSet, basename="permission"
)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "me/",
        views.UserViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
            }
        ),
        name="me-detail",
    ),
    path(
        "register/",
        views.RegisterAPIView.as_view(),
        name="register",
    ),
    path(
        "register/confirm/<uidb64>/<token>/",
        views.RegisterConfirmAPIView.as_view(),
        name="register-confirm",
    ),
    path(
        "token/",
        views.ObtainAuthTokenAPIView.as_view(),
        name="get-token",
    ),
    path(
        "password/reset/",
        views.PasswordResetAPIView.as_view(),
        name="password-reset",
    ),
    path(
        "password/reset/confirm/<uidb64>/<token>/",
        views.PasswordResetConfirmAPIView.as_view(),
        name="password-set",
    ),
]
