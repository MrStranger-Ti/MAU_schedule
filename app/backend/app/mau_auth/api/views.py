from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
    OpenApiParameter,
)
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status
from rest_framework import mixins

from mau_auth.auth_class import CookieTokenAuthentication
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
    RegisterSerializer,
)

User: type[MauUser] = get_user_model()


@extend_schema_view(
    list=extend_schema(
        tags=["Auth Groups"],
        summary="Get list of groups",
    ),
    create=extend_schema(
        tags=["Auth Groups"],
        summary="Create and get new group",
        responses={
            201: GroupSerializer,
            400: OpenApiResponse(description="Validation error"),
        },
    ),
    retrieve=extend_schema(
        tags=["Auth Groups"],
        summary="Get group by id",
        responses={
            200: GroupSerializer,
            404: None,
        },
    ),
    update=extend_schema(
        tags=["Auth Groups"],
        summary="Completely update group by id",
        responses={
            200: GroupSerializer,
            400: OpenApiResponse(description="Validation error"),
            404: None,
        },
    ),
    partial_update=extend_schema(
        tags=["Auth Groups"],
        summary="Partially update group by id",
        responses={
            200: GroupSerializer,
            400: OpenApiResponse(description="Validation error"),
            404: None,
        },
    ),
    destroy=extend_schema(
        tags=["Auth Groups"],
        summary="Delete group by id",
        responses={
            204: OpenApiResponse(description="No content"),
            404: None,
        },
    ),
)
class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    authentication_classes = [CookieTokenAuthentication]
    permission_classes = [IsAdminUser]


@extend_schema_view(
    list=extend_schema(
        tags=["Auth Permissions"],
        summary="Get list of permissions",
    ),
    create=extend_schema(
        tags=["Auth Permissions"],
        summary="Create and get new permission",
        responses={
            201: PermissionSerializer,
            400: OpenApiResponse(description="Validation error"),
        },
    ),
    retrieve=extend_schema(
        tags=["Auth Permissions"],
        summary="Get permission by id",
        responses={
            200: PermissionSerializer,
            404: None,
        },
    ),
    update=extend_schema(
        tags=["Auth Permissions"],
        summary="Completely update permission by id",
        responses={
            200: PermissionSerializer,
            400: OpenApiResponse(description="Validation error"),
            404: None,
        },
    ),
    partial_update=extend_schema(
        tags=["Auth Permissions"],
        summary="Partially update permission by id",
        responses={
            200: PermissionSerializer,
            400: OpenApiResponse(description="Validation error"),
            404: None,
        },
    ),
    destroy=extend_schema(
        tags=["Auth Permissions"],
        summary="Delete permission by id",
        responses={
            204: OpenApiResponse(description="No content"),
            404: None,
        },
    ),
)
class PermissionViewSet(ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    authentication_classes = [CookieTokenAuthentication]
    permission_classes = [IsAdminUser]


@extend_schema_view(
    list=extend_schema(
        tags=["Auth Admin"],
        summary="Get list of all users",
    ),
    create=extend_schema(
        tags=["Auth Admin"],
        summary="Create and get new user",
        responses={
            201: AdminUserSerializer,
            400: OpenApiResponse(description="Validation error"),
        },
    ),
    retrieve=extend_schema(
        tags=["Auth Admin"],
        summary="Get user by id",
        responses={
            200: AdminUserSerializer,
            404: None,
        },
    ),
    update=extend_schema(
        tags=["Auth Admin"],
        summary="Completely update user by id",
        responses={
            200: AdminUserSerializer,
            400: OpenApiResponse(description="Validation error"),
            404: None,
        },
    ),
    partial_update=extend_schema(
        tags=["Auth Admin"],
        summary="Partially update user by id",
        responses={
            200: AdminUserSerializer,
            400: OpenApiResponse(description="Validation error"),
            404: None,
        },
    ),
    destroy=extend_schema(
        tags=["Auth Admin"],
        summary="Delete user by id",
        responses={
            204: OpenApiResponse(description="No content"),
            404: None,
        },
    ),
)
class AdminViewSet(ModelViewSet):
    queryset = User.objects.prefetch_related("groups", "user_permissions")
    serializer_class = AdminUserSerializer
    authentication_classes = [CookieTokenAuthentication]
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


@extend_schema_view(
    retrieve=extend_schema(
        tags=["Auth User"],
        summary="Get own user data by id",
        responses={
            200: AuthenticatedUserSerializer,
            404: None,
        },
    ),
    update=extend_schema(
        tags=["Auth User"],
        summary="Completely update own user data by id",
        responses={
            200: AuthenticatedUserSerializer,
            400: OpenApiResponse(description="Validation error"),
            404: None,
        },
    ),
    partial_update=extend_schema(
        tags=["Auth User"],
        summary="Partially update own user data by id",
        responses={
            200: AuthenticatedUserSerializer,
            400: OpenApiResponse(description="Validation error"),
            404: None,
        },
    ),
)
class UserViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = AuthenticatedUserSerializer
    authentication_classes = [CookieTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer

    @extend_schema(
        tags=["Auth Register"],
        summary="Sending credentials and extra data for registration",
        responses={
            200: OpenApiResponse(description="Success"),
            400: OpenApiResponse(description="Validation error"),
        },
    )
    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data={"message": "Check your email to confirm register."},
            status=status.HTTP_201_CREATED,
        )


class RegisterConfirmAPIView(GenericAPIView):
    serializer_class = RegisterConfirmationSerializer

    @extend_schema(
        tags=["Auth Register"],
        summary="Confirmation registration via url in email message",
        responses={
            200: OpenApiResponse(description="Success"),
            400: OpenApiResponse(description="Validation error"),
        },
    )
    def get(self, request: Request, uidb64: str, token: str) -> Response:
        confirm_serializer = self.get_serializer(
            data={"uidb64": uidb64, "token": token},
        )
        confirm_serializer.is_valid(raise_exception=True)
        confirm_serializer.save()
        return Response(
            data={"message": "You have been successfully registered."},
            headers={"Location": reverse("api_mau_auth:me-detail")},
            status=status.HTTP_200_OK,
        )


class SetAuthTokenAPIView(GenericAPIView):
    serializer_class = AuthTokenSerializer

    @extend_schema(
        tags=["Auth Token"],
        summary="Setting token in httponly cookie by credentials",
        responses={
            200: OpenApiResponse(description="Success"),
            400: OpenApiResponse(description="Validation error"),
        },
    )
    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.save()
        response = Response(
            data={"message": "Success obtaining token"},
            status=status.HTTP_200_OK,
        )
        response.set_cookie(
            key="auth_token",
            value=token,
            max_age=60 * 60 * 24 * 7,
            httponly=True,
            secure=True,
            samesite=None,
        )
        return response


class DeleteTokenAPIView(APIView):
    authentication_classes = [CookieTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Auth Token"],
        summary="Deleting token from httponly cookie",
        responses={
            200: OpenApiResponse(description="Success"),
        },
    )
    def post(self, request: Request) -> Response:
        response = Response(
            data={"message": "Success deleted token"},
            status=status.HTTP_200_OK,
        )
        response.delete_cookie(key="auth_token", samesite=None)
        return response


class PasswordResetAPIView(GenericAPIView):
    serializer_class = PasswordResetSerializer

    @extend_schema(
        tags=["Auth Password Reset"],
        summary="Sending email address to confirm password reset",
        responses={
            200: OpenApiResponse(description="Success"),
            400: OpenApiResponse(description="Validation error"),
        },
    )
    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data={"message": "Check your email to set the new password."},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmAPIView(APIView):
    @extend_schema(
        tags=["Auth Password Reset"],
        summary="Changing password",
        parameters=[
            OpenApiParameter(
                name="uidb64",
                type=str,
                required=True,
                location=OpenApiParameter.PATH,
            ),
            OpenApiParameter(
                name="token",
                type=str,
                required=True,
                location=OpenApiParameter.PATH,
            ),
        ],
        request=PasswordSetSerializer,
        responses={
            200: OpenApiResponse(description="Success"),
            400: OpenApiResponse(description="Validation error"),
        },
    )
    def post(
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
                "help_url": reverse("api_mau_auth:set-token"),
            },
            status=status.HTTP_200_OK,
        )

    def get_user_by_uidb64_and_token(self, uidb64: str, token: str) -> User:
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
