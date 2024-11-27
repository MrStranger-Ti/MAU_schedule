from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework import status

from mau_auth.api.permissions import IsOwner
from mau_auth.models import MauUser
from mau_auth.api.serializers import (
    UserSerializer,
    ConfirmationEmailSerializer,
    AuthTokenSerializer,
    AdminUserSerializer,
)

User: type[MauUser] = get_user_model()


class AdminViewSet(ModelViewSet):
    queryset = User.objects.prefetch_related("groups", "user_permissions")
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
    ]
    filterset_fields = [
        "full_name",
        "email",
        "institute",
        "course",
        "group",
        "is_staff",
        "is_active",
    ]
    search_fields = [
        "full_name",
        "email",
        "institute",
        "course",
        "group",
        "is_staff",
        "is_active",
    ]


class UserViewSet(ViewSet):
    serializer_class = UserSerializer

    def my(self, request: Request) -> Response:
        serializer = self.serializer_class(request.user)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )

    def register(self, request: Request) -> Response:
        serializer = self.serializer_class(request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def register_confirm(self, request: Request) -> Response:
        confirm_serializer = ConfirmationEmailSerializer(
            data={
                "uid": request.data.get("uid"),
                "token": request.data.get("token"),
            },
        )
        confirm_serializer.is_valid(raise_exception=True)

        user = confirm_serializer.save()
        user_serializer = self.serializer_class(user)
        return Response(
            data=user_serializer.data,
            status=status.HTTP_200_OK,
        )

    def get_permissions(self):
        if self.action == "my":
            permission_classes = [IsAuthenticated, IsOwner]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
