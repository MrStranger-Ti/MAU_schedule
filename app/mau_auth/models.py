from __future__ import annotations

from django.apps import apps
from django.contrib import auth
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db import models
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
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
        self, perm, is_active=True, include_superusers=True, backend=None, obj=None
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


class MauUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = "course", "full_name"

    full_name = models.CharField(
        max_length=50,
        validators=[validate_full_name],
        verbose_name="ФИО",
    )
    email = models.EmailField(
        unique=True,
        validators=[validate_email],
        verbose_name="Email",
    )
    institute = models.ForeignKey(
        MauInstitute,
        null=True,
        on_delete=models.PROTECT,
        related_name="mauusers",
        verbose_name="Институт",
    )
    course = models.PositiveSmallIntegerField(
        null=True,
        verbose_name="Курс",
    )
    group = models.CharField(
        null=True,
        max_length=20,
        verbose_name="Группа",
    )

    objects = MauUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "full_name",
    ]

    is_staff = models.BooleanField(
        "staff status",
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

    def get_confirmation_message(
        self,
        request: HttpRequest,
        confirmation_url_pattern: str,
    ) -> str:
        current_site = get_current_site(request)
        context = {
            "domain": current_site.domain,
            "url": self.get_confirmation_url(base_url=confirmation_url_pattern),
        }
        return render_to_string(
            "mau_auth/registration/email_message.html",
            context=context,
        )

    def get_confirmation_url(self, base_url: str) -> str:
        uidb64, token = self.get_uidb64_and_token()
        return reverse(base_url, args=[uidb64, token])

    def get_uidb64_and_token(self) -> tuple[str, str]:
        uidb64 = urlsafe_base64_encode(force_bytes(self.pk))
        token = default_token_generator.make_token(self)
        return uidb64, token

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def send_email_confirmation(
        self,
        request: HttpRequest,
        confirmation_url_pattern: str,
    ) -> None:
        subject = "Подтвердите почту в приложении MAU schedule"
        message = self.get_confirmation_message(
            request=request,
            confirmation_url_pattern=confirmation_url_pattern,
        )
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
        except ValueError as exc:
            return

        user = cls.objects.filter(pk=uid).first()
        if user and default_token_generator.check_token(user, token):
            return user
