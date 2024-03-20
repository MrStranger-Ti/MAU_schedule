import os
import re

from datetime import date, timedelta

import requests
import bs4

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
from django.core.cache import cache
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from mau_auth.validators import validate_full_name, validate_email
from mau_auth.exceptions import TagNotFound


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
        ordering = 'course', 'full_name'

    full_name = models.CharField(max_length=50, validators=[validate_full_name], verbose_name='ФИО')
    email = models.EmailField(unique=True, validators=[validate_email], verbose_name='Email')
    institute = models.ForeignKey('MauInstitute', null=True, on_delete=models.PROTECT, related_name='mauusers',
                                  verbose_name='Институт')
    course = models.PositiveSmallIntegerField(default=1, verbose_name='Курс')
    group = models.CharField(null=True, max_length=20, verbose_name='Группа')

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
        current_calendar_date = date.today().isocalendar()
        monday = date.fromisocalendar(current_calendar_date[0], current_calendar_date[1], 1)

        data = {}
        for _ in range(4):
            sunday = monday + timedelta(days=6)
            params = {
                'perstart': monday.isoformat(),
                'perend': sunday.isoformat(),
            }

            group_page_response = requests.get(url, params=params)
            soup = bs4.BeautifulSoup(group_page_response.content, 'lxml')

            if not soup.find('table', class_='table table-bordered table-striped table-3'):
                break

            for weekday_num, day in enumerate(soup.find_all('table')):
                title = day.find('th')
                if title and not title.text.startswith('Воскресенье'):
                    curr_date = monday + timedelta(days=weekday_num)
                    curr_date_format = curr_date.strftime('%Y-%m-%d')
                    data.setdefault(curr_date_format, [])
                    for row in day.find_all('tr')[1:]:
                        data[curr_date_format].append(
                            [field.text for field in row.find_all(['th', 'td'])]
                        )

            monday += timedelta(days=7)

        return data

    def _get_query_params(self) -> str:
        base_schedule_url = settings.SCHEDULE_URL
        base_schedule_page_response = requests.get(base_schedule_url)
        soup = bs4.BeautifulSoup(base_schedule_page_response.content, 'lxml')

        date_select = soup.find('option', selected=True)
        institute_select = soup.find('option', string=self.institute.name)

        if date_select is None or institute_select is None:
            raise TagNotFound

        pers = date_select.get('value')
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
        a_tag = soup.find(
            'a',
            string=re.compile(fr'\s*?{group}\s*?'),
            href=lambda url: url and url.startswith('schedule.php'),
        )

        if a_tag is None:
            raise TagNotFound

        group_schedule_url = os.path.join(base_schedule_url, a_tag.get('href'))

        return group_schedule_url

    def _get_confirmation_message(self, request: HttpRequest) -> str:
        current_site = get_current_site(request)
        context = {
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(self.pk)),
            'token': default_token_generator.make_token(self),
        }
        return render_to_string('registration_email/email_message.html', context=context)

    def get_schedule(self) -> dict[int, list[str]] | None:
        if not all([self.course, self.institute, self.group]):
            return None

        schedule_data = cache.get(f'schedule_of_group_{self.group}')
        if not schedule_data:
            try:
                perc, facs, course = self._get_query_params()
                group_url = self._get_group_url(perc, facs, self.course)

            except TagNotFound:
                return None

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

    def send_email_confirmation(self, request: HttpRequest) -> None:
        subject = 'Подтвердите почту в приложении MAU schedule'
        message = self._get_confirmation_message(request)
        send_mail(
            subject=subject,
            from_email=settings.DEFAULT_FROM_EMAIL,
            message=message,
            recipient_list=[self.email],
        )


class MauInstitute(models.Model):
    class Meta:
        verbose_name = 'институт'
        verbose_name_plural = 'институты'
        ordering = 'name',

    name = models.CharField(max_length=20, verbose_name='Название')

    def __str__(self):
        return self.name
