import os
from pathlib import Path

from django.urls import reverse_lazy
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    "SECRET_KEY", "django-insecure-k-nlhgsc-7js6kcoy6bijf8zff(t1ebrftyo$7rx_h7yg5%$jc"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "0") == "1"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
] + (os.getenv("ALLOWED_HOSTS").split(","))

INTERNAL_IPS = [
    "127.0.0.1",
    "0.0.0.0",
]

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://147.45.103.191:1337",
]

SECURE_CROSS_ORIGIN_OPENER_POLICY = None

SECURE_SSL_REDIRECT = True

CORS_ALLOWED_ORIGINS = [
    "https://localhost:3000",
    "https://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "PATCH",
    "POST",
    "PUT",
)


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "debug_toolbar",
    "rest_framework",
    "rest_framework.authtoken",
    "django_filters",
    "drf_spectacular",
    "corsheaders",
    "django_extensions",
    "mau_auth.apps.MauAuthConfig",
    "schedule.apps.ScheduleConfig",
    "profiles.apps.ProfilesConfig",
    "notes.apps.NotesConfig",
    "core.apps.CoreConfig",
    "teacher_schedule_bookmarks.apps.BookmarksConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.schedule_data",
            ],
        },
    },
]

WSGI_APPLICATION = "app.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "MauSchedule"),
        "USER": os.getenv("POSTGRES_USER", "MauUser"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "12345"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
        "TEST": {
            "NAME": "test_mau",
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "mau_auth.validators.CustomUserAttributeSimilarityValidator",
    },
    {
        "NAME": "mau_auth.validators.CustomMinimumLengthValidator",
    },
    {
        "NAME": "mau_auth.validators.CustomCommonPasswordValidator",
    },
    {
        "NAME": "mau_auth.validators.CustomNumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = os.getenv("TIME_ZONE", "UTC")

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Authentication

AUTH_USER_MODEL = "mau_auth.MauUser"

LOGIN_URL = reverse_lazy("mau_auth:login")
LOGIN_REDIRECT_URL = reverse_lazy("schedule:group_schedule")
LOGOUT_REDIRECT_URL = reverse_lazy("core:index")
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Email

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DEFAULT_FROM_EMAIL = "mauadmin@mauniver.ru"


# Parsing

SCHEDULE_URL = "https://www.mauniver.ru/student/timetable/new/"

MAU_DOMAINS = [
    "masu.edu.ru",
    "mstu.edu.ru",
    "mauniver.ru",
]

GROUP_SCHEDULE_NAME = "group"
TEACHER_SCHEDULE_NAME = "teacher"

REQUESTS_TIMEOUT = os.getenv("REQUESTS_TIMEOUT", "5")
if REQUESTS_TIMEOUT.isdigit():
    REQUESTS_TIMEOUT = int(REQUESTS_TIMEOUT)
else:
    REQUESTS_TIMEOUT = 5


WEEKDAYS_NAMES = {
    0: "Понедельник",
    1: "Вторник",
    2: "Среда",
    3: "Четверг",
    4: "Пятница",
    5: "Суббота",
    6: "Воскресенье",
}

DEVELOPER_URL = "https://t.me/MrStrangerTi"


# Redis

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")


# Cache

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:6379/0",
    },
    "test": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": f"redis://{REDIS_HOST}:6379/1",
    },
}

SCHEDULE_CACHE_TIME = 60 * 20


# Data Migrations

INSTITUTES = [
    "ЕТИ",
    "ИГ и СН",
    "ИИС и ЦТ",
    "ИКИ и П",
    "ИП и П",
    "ИПАТ",
    "МА",
    "МБИ",
    "ФФК и С",
    "ЮФ",
]


# Celery

CELERY_BROKER_URL = "redis://" + REDIS_HOST + ":" + REDIS_PORT + "/0"
CELERY_BROKER_TRANSPORT_OPTIONS = {
    "visibility_timeout": 3600,
    "max_retries": 3,
}
CELERY_RESULT_BACKEND = "redis://" + REDIS_HOST + ":" + REDIS_PORT + "/0"


# DRF

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "MauSchedule OpenApi documentation",
    "DESCRIPTION": (
        "<p>This API for only frontend part of application.</p>"
        "<p>Almost all endpoints for authenticated users.</p>"
    ),
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "TAGS": [
        {
            "name": "Auth Groups",
            "description": "User groups of permissions",
        },
        {
            "name": "Auth Permissions",
            "description": "User permissions",
        },
        {
            "name": "Auth Admin",
            "description": "Managing users for admin",
        },
        {
            "name": "Auth User",
            "description": "Managing own user account",
        },
        {
            "name": "Auth Register",
            "description": "Registration for users",
        },
        {
            "name": "Auth Token",
            "description": "Managing user token",
        },
        {
            "name": "Auth Password Reset",
            "description": "Password Reset",
        },
        {
            "name": "Notes",
            "description": "Managing own notes",
        },
        {
            "name": "Teacher Schedule Bookmarks",
            "description": "Managing own teacher schedule bookmarks",
        },
        {
            "name": "Schedule",
            "description": "Getting schedule",
        },
    ],
}
