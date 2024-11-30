from mailbox import NotEmptyError

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.db.models import Model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse

from mau_auth.models import MauUser, Token

User: type[MauUser] = get_user_model()


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = [
            "last_login",
        ]
        read_only_fields = [
            "id",
            "is_superuser",
            "is_stuff",
            "is_active",
            "date_joined",
            "last_login",
        ]

    password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password],
    )

    def create(self, validated_data: dict) -> User:
        password = validated_data.get("password")

        user = super().create(validated_data)
        user.set_password(password)
        user.is_active = False
        user.save()

        return user

    def update(self, instance: Model, validated_data: dict) -> User:
        user = super().update(instance, validated_data)
        # ?
        # ?
        # ?
        return user

    def validate(self, attrs: dict) -> dict:
        if attrs.get("password") and self.instance:
            raise ValidationError(
                detail={
                    "detail": "You need to go to this url to change_password.",
                    "help_url": reverse("api_mau_auth:password_reset"),
                },
            )
        elif attrs.get("email") and self.instance:
            raise ValidationError(
                detail="You can not change your email.",
            )

        return attrs


class EmailConfirmationSerializer(serializers.Serializer):
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
        if not user:
            raise ValidationError(
                detail="Invalid uid or token.",
            )

        attrs["user"] = user
        return attrs

    def save(self) -> User:
        return self.validated_data.get("user")


class RegisterConfirmationSerializer(EmailConfirmationSerializer):
    def save(self) -> User:
        user = super().save()
        user.is_active = True
        user.save()
        return user


class PasswordResetConfirmationSerializer(EmailConfirmationSerializer):
    pass


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

    def save(self, **kwargs):
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
                raise serializers.ValidationError(
                    detail="Invalid login or password.",
                )
        else:
            raise serializers.ValidationError(
                detail="No password or login.",
            )

        attrs["user"] = user
        return attrs


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        write_only=True,
    )

    def create(self, validated_data):
        user = get_object_or_404(
            klass=User,
            email=validated_data.get("email"),
        )
        return user


class PasswordSetSerializer(serializers.Serializer):
    password1 = serializers.CharField(
        required=True,
        write_only=True,
    )
    password2 = serializers.CharField(
        required=True,
        write_only=True,
    )

    def get_user_from_context(self) -> User:
        return self.context.get("user")

    def save(self):
        password = self.validated_data.get("password1")
        user = self.get_user_from_context()
        user.set_password(password)
        user.auth_token.delete()
        user.save()
        return user

    def validate(self, attrs):
        password1 = attrs.get("password1")
        password2 = attrs.get("password2")

        validate_password(password=password1, user=self.get_user_from_context())

        if password1 != password2:
            raise ValidationError(detail="Passwords do not match.")

        return attrs
