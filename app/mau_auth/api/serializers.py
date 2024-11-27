from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers

from mau_auth.models import MauUser

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

    def get_no_create_fields(self) -> list[str]:
        return [
            "password",
        ]

    def get_no_update_fields(self) -> list[str]:
        return [
            "email",
            "password",
        ]

    def exclude_fields(self, validate_data: dict, exclude_fields: list[str]) -> dict:
        for field_name in exclude_fields:
            if field_name in validate_data:
                validate_data.pop(field_name)

        return validate_data

    def create(self, validated_data):
        password = validated_data.get("password")
        self.exclude_fields(
            validate_data=validated_data,
            exclude_fields=self.get_no_create_fields(),
        )

        user = super().create(validated_data)
        user.set_password(password)
        user.is_active = False
        user.save()

        request = self.context.get("request")
        user.send_email_confirmation(request)

        return user

    def update(self, instance, validated_data):
        self.exclude_fields(
            validate_data=validated_data,
            exclude_fields=self.get_no_update_fields(),
        )
        user = super().update(instance, validated_data)
        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop("password", None)
        return representation


class ConfirmationEmailSerializer(serializers.Serializer):
    uid = serializers.CharField(
        max_length=256,
        required=True,
    )
    token = serializers.CharField(
        max_length=256,
        required=True,
    )

    def validate(self, attrs: dict) -> dict:
        uidb64 = attrs.get("uid")
        token = attrs.get("token")

        params_exc = serializers.ValidationError(
            detail="Invalid uid or token.",
        )

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
        except ValueError as exc:
            raise params_exc

        user = User.objects.filter(pk=uid).first()
        if user and default_token_generator.check_token(user, token):
            attrs["user"] = user
            return attrs

        raise params_exc

    def save(self) -> User:
        if user := self.validated_data.get("user"):
            user.is_active = True
            user.save()
            return user

        raise ValueError("Context 'user' not found.")


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

    def validate(self, attrs):
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
