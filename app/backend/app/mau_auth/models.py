from __future__ import annotations

import urllib.parse

from django.apps import apps
from django.contrib import auth
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.request import Request
from rest_framework.reverse import reverse

from mau_auth.validators import validate_full_name, validate_email
from schedule.models import MauInstitute


class MauUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, full_name, email, password, **extra_fields):
        if not full_name:
            raise ValueError("Full name must be set")
        if not email:
            raise ValueError("Email must be set")
        if not password:
            raise ValueError("Password must be set")
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        full_name = GlobalUserModel.normalize_username(full_name)
        user = self.model(full_name=full_name, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, full_name, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(full_name, email, password, **extra_fields)

    def create_superuser(self, full_name, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(full_name, email, password, **extra_fields)

    def with_perm(
        self,
        perm,
        is_active=True,
        include_superusers=True,
        backend=None,
        obj=None,
    ):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class EmailConfirmationMixin:
    EMAIL_SUBJECT = "Подтвердите почту в приложении MAU schedule"

    def get_custom_confirmation_url(self, url: str) -> str:
        uidb64, token = self.get_uidb64_and_token()
        return urllib.parse.urljoin(url, uidb64 + "/" + token)

    def get_local_confirmation_url(self, request: Request, url_pattern: str) -> str:
        uidb64, token = self.get_uidb64_and_token()
        return urllib.parse.urljoin(
            f"{request.scheme}://{request.get_host()}",
            reverse(
                url_pattern,
                kwargs={
                    "uidb64": uidb64,
                    "token": token,
                },
            ),
        )

    def get_uidb64_and_token(self) -> tuple[str, str]:
        uidb64 = urlsafe_base64_encode(force_bytes(self.pk))
        token = default_token_generator.make_token(self)
        return uidb64, token

    def send_email_confirmation(
        self,
        message: str,
        subject: str = EMAIL_SUBJECT,
    ) -> None:
        send_mail(
            subject=subject,
            from_email=settings.DEFAULT_FROM_EMAIL,
            message=message,
            recipient_list=[self.email],
        )

    @classmethod
    def check_email_confirmation(cls, uidb64: str, token: str) -> MauUser | None:
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
        except ValueError:
            return None

        user = cls.objects.filter(pk=uid).first()
        if user and default_token_generator.check_token(user, token):
            return user


class MauUser(AbstractBaseUser, PermissionsMixin, EmailConfirmationMixin):
    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = "course", "full_name"

    full_name = models.CharField(
        max_length=50,
        validators=[validate_full_name],
        verbose_name="full name",
    )
    email = models.EmailField(
        unique=True,
        validators=[validate_email],
        verbose_name="email",
    )
    institute = models.ForeignKey(
        MauInstitute,
        null=True,
        on_delete=models.PROTECT,
        related_name="mauusers",
        verbose_name="institute",
    )
    course = models.PositiveSmallIntegerField(
        null=True,
        verbose_name="course",
    )
    group = models.CharField(
        null=True,
        max_length=20,
        verbose_name="group",
    )

    objects = MauUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "full_name",
        "institute",
        "course",
        "group",
    ]

    is_staff = models.BooleanField(
        verbose_name="staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_active = models.BooleanField(
        "active",
        default=True,
        help_text="Designates whether this user should be treated as active. "
        "Unselect this instead of deleting accounts.",
    )
    date_joined = models.DateTimeField(
        "date joined",
        default=timezone.now,
    )

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)


class TokenInfo(models.Model):
    user = models.ForeignKey(
        MauUser,
        related_name="token_info",
        on_delete=models.CASCADE,
    )
    token_type = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "token_type"],
                name="unique_user_token_type",
            ),
        ]
