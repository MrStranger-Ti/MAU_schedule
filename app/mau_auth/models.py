import os
import re

import requests
import bs4

from django.apps import apps
from django.contrib import auth
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.cache import cache

from mau_auth.validators import validate_full_name


class MauUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, full_name, email, password, **extra_fields):
        if not full_name:
            raise ValueError('Full name must be set')
        if not email:
            raise ValueError('Email must be set')
        if not password:
            raise ValueError('Password must be set')
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

    full_name = models.CharField(max_length=256, validators=[validate_full_name])
    email = models.EmailField(unique=True)
    institute = models.CharField()
    course = models.PositiveSmallIntegerField(default=1)
    group = models.CharField()

    objects = MauUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_active = models.BooleanField(
        "active",
        default=True,
        help_text=
        "Designates whether this user should be treated as active. "
        "Unselect this instead of deleting accounts."
        ,
    )
    date_joined = models.DateTimeField("date joined", default=timezone.now)

    @classmethod
    def _get_schedule_data(cls, url: str) -> dict[int, list[str]]:
        group_page_response = requests.get(url)
        soup = bs4.BeautifulSoup(group_page_response.content, 'lxml')

        data = {}
        weekdays = settings.WEEKDAYS
        for day_num, day in enumerate(soup.find_all('table')):
            data.setdefault(weekdays[day_num], [])
            for row_num, row in enumerate(day.find_all('tr')[1:]):
                data[weekdays[day_num]].append(
                    [field.text for field in row.find_all(['th', 'td'])]
                )

        return data

    def _get_query_params(self) -> str:
        base_schedule_url = settings.SCHEDULE_URL
        base_schedule_page_response = requests.get(base_schedule_url)
        soup = bs4.BeautifulSoup(base_schedule_page_response.content, 'lxml')

        date_select = soup.find('option', selected=True)
        pers = date_select.get('value')

        institute_select = soup.find('option', string=self.institute)
        facs = institute_select.get('value')

        return pers, facs, self.course

    def _get_group_url(self, pers: str | int, facs: str | int, course: str | int):
        base_schedule_url = settings.SCHEDULE_URL
        group = self.get_prepared_group()

        params = {
            'facs': facs,
            'courses': course,
            'mode': 1,
            'pers': pers,
        }
        r = requests.get(base_schedule_url, params=params)
        soup = bs4.BeautifulSoup(r.content, 'lxml')
        a_tag = soup.find('a', string=re.compile(fr'\s*?{group}\s*?'))
        group_schedule_url = os.path.join(base_schedule_url, a_tag.get('href'))

        return group_schedule_url

    def get_schedule(self) -> dict[int, list[str]] | None:
        if not all([self.course, self.institute, self.group]):
            return None

        schedule_data = cache.get(f'schedule_of_group_{self.group}')
        if not schedule_data:
            perc, facs, course = self._get_query_params()
            group_url = self._get_group_url(perc, facs, self.course)
            schedule_data = self._get_schedule_data(group_url)
            cache.set(f'schedule_of_group_{self.group}', schedule_data, settings.SCHEDULE_CACHE_TIME)

        return schedule_data

    def get_prepared_group(self, spec_symbols: str = None) -> str:
        if not spec_symbols:
            spec_symbols = '()'

        group = self.group
        for sym in spec_symbols:
            pattern = fr'\{sym}'
            group = re.sub(pattern, fr'\{sym}', group)

        return group

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
