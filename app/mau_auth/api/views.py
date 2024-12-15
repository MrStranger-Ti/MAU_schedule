from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ViewSet
from rest_framework import status
from rest_framework import mixins

from mau_auth.api.permissions import IsOwner
from mau_auth.models import MauUser
from mau_auth.api.serializers import (
    AuthTokenSerializer,
    AdminUserSerializer,
    PasswordResetSerializer,
    PasswordSetSerializer,
    RegisterConfirmationSerializer,
    PasswordResetConfirmationSerializer,
    AuthenticatedUserSerializer,
    GroupSerializer,
    PermissionSerializer,
)

User: type[MauUser] = get_user_model()


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]


class PermissionViewSet(ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAdminUser]


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


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = User.objects.all()
    serializer_class = AuthenticatedUserSerializer

    def get_object(self):
        return self.request.user


class RegisterAPIView(GenericAPIView):
    serializer_class = AuthenticatedUserSerializer

    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data={"message": "Check your email to confirm register."},
            status=status.HTTP_201_CREATED,
            headers={"Location": reverse("api_mau_auth:me")},
        )


class RegisterConfirmAPIView(GenericAPIView):
    serializer_class = RegisterConfirmationSerializer

    def get(self, request: Request, uidb64: str, token: str) -> Response:
        confirm_serializer = self.get_serializer(
            data={"uidb64": uidb64, "token": token},
        )
        confirm_serializer.is_valid(raise_exception=True)
        user = confirm_serializer.save()
        user_serializer = AuthenticatedUserSerializer(instance=user)
        return Response(data=user_serializer.data, status=status.HTTP_200_OK)


class ObtainAuthTokenAPIView(APIView):
    def post(self, request: Request) -> Response:
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.save()
        return Response(data={"token": token}, status=status.HTTP_200_OK)


class PasswordResetViewSet(ViewSet):
    def password_reset(self, request: Request) -> Response:
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        user.send_email_confirmation(
            request=request,
            confirmation_url_pattern="api_mau_auth:password-set",
        )
        return Response(
            data={"message": "Check your email to set the new password."},
            status=status.HTTP_200_OK,
        )

    def password_reset_confirm(
        self,
        request: Request,
        uidb64: str,
        token: str,
    ) -> Response:
        user = self.get_user_by_uidb64_and_token(uidb64=uidb64, token=token)
        self.check_password(user=user)

        return Response(
            data={
                "message": (
                    "Your password was successfully changed. "
                    "You need to get a new token."
                ),
                "help_url": reverse("api_mau_auth:get-token"),
            },
            status=status.HTTP_200_OK,
        )

    def get_user_by_uidb64_and_token(
        self,
        uidb64: str,
        token: str,
    ) -> User:
        serializer = PasswordResetConfirmationSerializer(
            data={"uidb64": uidb64, "token": token},
        )
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    def check_password(self, user: User) -> None:
        serializer = PasswordSetSerializer(
            data=self.request.data,
            context={"user": user},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
