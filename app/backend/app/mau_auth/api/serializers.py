from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.password_validation import validate_password
from django.template.loader import render_to_string
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse

from mau_auth.models import MauUser, TokenInfo

User: type[MauUser] = get_user_model()


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"
        read_only_fields = ["id"]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"
        read_only_fields = ["id"]


class BaseUserSerializer(serializers.ModelSerializer):
    REQUIRED_FIELDS = [
        "full_name",
        "email",
        "password",
        "institute",
        "course",
        "group",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].required = False

    def get_required_fields_detail(self, attrs: dict) -> dict:
        detail = {}
        for req_field in self.REQUIRED_FIELDS:
            if req_field not in attrs:
                detail[req_field] = self.error_messages["required"]

        return detail

    def validate_required_fields(self, attrs: dict) -> None:
        # check required fields for create and full update (put method)
        if not self.partial:
            for req_field in self.REQUIRED_FIELDS:
                if req_field not in attrs or not attrs[req_field]:
                    raise ValidationError(detail=self.get_required_fields_detail(attrs))

    def exclude_required_fields(self, *fields_names) -> None:
        for field_name in fields_names:
            if field_name in self.REQUIRED_FIELDS:
                self.REQUIRED_FIELDS.remove(field_name)

    def validate(self, attrs: dict) -> dict:
        self.validate_required_fields(attrs)
        return attrs

    def create(self, validated_data: dict) -> User:
        password = validated_data.get("password")
        user = super().create(validated_data)
        user.set_password(password)
        return user

    def save(self, **kwargs):
        user = super().save(**kwargs)
        user.save()
        return user


class AdminUserSerializer(BaseUserSerializer):
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = [
            "id",
            "date_joined",
            "last_login",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def update(self, instance: User, validated_data: dict) -> User:
        # just set password for any user
        if password := validated_data.get("password"):
            validated_data.pop("password", None)
            instance.set_password(password)

        return super().update(instance, validated_data)


class AuthenticatedUserSerializer(BaseUserSerializer):
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = [
            "id",
            "is_superuser",
            "is_staff",
            "is_active",
            "date_joined",
            "last_login",
            "groups",
            "user_permissions",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data: dict) -> User:
        user = super().create(validated_data)
        user.is_active = False
        return user

    def validate(self, attrs: dict) -> dict:
        # if update
        if self.instance:
            self.exclude_required_fields("password", "email")

            if attrs.get("password"):
                raise ValidationError(
                    detail={
                        "password": "You need to go to password reset url to change_password.",
                        "help_url": reverse("api_mau_auth:password-reset"),
                    },
                )

            elif attrs.get("email"):
                raise ValidationError(
                    detail={"email": "You can not change your email."},
                )

        super().validate(attrs)
        return attrs


class ConfirmationOptionsSerializer(serializers.Serializer):
    url = serializers.URLField(
        required=False,
        help_text=(
            "Custom url for confirmation. Format in email message: "
            "your_url/uidb64/token/",
        ),
    )

    def create(self, validated_data: dict) -> User:
        request = self.context.get("request")
        user = self.context.get("user")
        token_type = self.context.get("token_type")
        custom_template_name = self.context.get("custom_template_name")
        local_template_name = self.context.get("local_template_name")

        if url := validated_data.get("url"):
            url = user.get_custom_confirmation_url(url=url)
            message = render_to_string(
                template_name=custom_template_name,
                context={"url": url},
            )
        else:
            url = user.get_local_confirmation_url(
                request=request,
                url_pattern="api_mau_auth:register-confirm",
            )
            message = render_to_string(
                template_name=local_template_name,
                context={
                    "url": url,
                    "doc_url": f"{request.scheme}://{request.get_host()}"
                    + reverse("swagger"),
                },
            )

        user.send_email_confirmation(message=message)
        TokenInfo.objects.get_or_create(user=user, token_type=token_type)
        return user


class RegisterSerializer(serializers.Serializer):
    user = AuthenticatedUserSerializer(write_only=True)
    options = ConfirmationOptionsSerializer(required=False, write_only=True)

    def create(self, validated_data: dict) -> User:
        user_data = validated_data.pop("user")

        user_serializer = AuthenticatedUserSerializer()
        user = user_serializer.create(validated_data=user_data)
        user.save()

        options = validated_data.get("options", {})
        options_serializer = ConfirmationOptionsSerializer(
            context={
                "user": user,
                "request": self.context.get("request"),
                "token_type": "register",
                "custom_template_name": "mau_auth/register/custom_register_message.html",
                "local_template_name": "mau_auth/register/local_register_message.html",
            }
        )
        user = options_serializer.create(validated_data={"url": options.get("url")})
        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation.get("user", {})


class EmailConfirmationSerializer(serializers.Serializer):
    TOKEN_TYPE = None

    uidb64 = serializers.CharField(
        max_length=256,
        required=True,
    )
    token = serializers.CharField(
        max_length=256,
        required=True,
    )

    def validate(self, attrs: dict) -> dict:
        user = User.check_email_confirmation(
            uidb64=attrs.get("uidb64"),
            token=attrs.get("token"),
        )
        if not user or not user.token_info.filter(token_type=self.TOKEN_TYPE).exists():
            raise ValidationError(detail="Invalid uid or token.")

        user.token_info.filter(token_type="register").delete()

        attrs["user"] = user
        return attrs

    def save(self) -> User:
        return self.validated_data.get("user")


class RegisterConfirmationSerializer(EmailConfirmationSerializer):
    TOKEN_TYPE = "register"

    def save(self) -> User:
        user = super().save()
        user.is_active = True
        user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        write_only=True,
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        trim_whitespace=True,
    )

    def save(self, **kwargs) -> str:
        user = self.validated_data.get("user")
        token, _ = Token.objects.get_or_create(user=user)
        return token.key

    def validate(self, attrs: dict) -> dict:
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"),
                email=email,
                password=password,
            )
            if not user:
                raise serializers.ValidationError(detail="Invalid login or password.")
        else:
            raise serializers.ValidationError(detail="No password or login.")

        attrs["user"] = user
        return attrs


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)
    options = ConfirmationOptionsSerializer(required=False, write_only=True)

    def validate_email(self, value: str) -> str:
        if not User.objects.filter(email=value).exists():
            raise ValidationError(detail="Invalid email")

        return value

    def save(self) -> User:
        user = User.objects.filter(email=self.validated_data.get("email")).first()

        options = self.validated_data.get("options", {})
        options_serializer = ConfirmationOptionsSerializer(
            context={
                "user": user,
                "request": self.context.get("request"),
                "token_type": "password-reset",
                "custom_template_name": "mau_auth/password_reset/custom_password_reset_message.html",
                "local_template_name": "mau_auth/password_reset/local_password_reset_message.html",
            }
        )
        user = options_serializer.create(validated_data={"url": options.get("url")})
        return user


class PasswordResetConfirmationSerializer(EmailConfirmationSerializer):
    TOKEN_TYPE = "password-reset"


class PasswordSetSerializer(serializers.Serializer):
    password1 = serializers.CharField(
        required=True,
        write_only=True,
    )
    password2 = serializers.CharField(
        required=True,
        write_only=True,
    )

    def save(self):
        password = self.validated_data.get("password1")
        user = self.context.get("user")
        user.set_password(password)
        user.auth_token.delete()
        user.save()
        return user

    def validate(self, attrs: dict) -> dict:
        password1 = attrs.get("password1")
        password2 = attrs.get("password2")

        validate_password(password=password1, user=self.context.get("user"))

        if password1 != password2:
            raise ValidationError(detail="Passwords do not match.")

        return attrs
