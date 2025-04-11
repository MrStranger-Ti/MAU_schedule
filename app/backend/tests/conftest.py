import pytest

from django.core.cache import cache
from django.conf import settings


@pytest.fixture(autouse=True)
def disable_https() -> None:
    settings.SECURE_SSL_REDIRECT = False


@pytest.fixture
def conf_cache() -> None:
    default = settings.CACHES["default"]
    settings.CACHES["default"] = settings.CACHES["test"]
    cache.clear()
    yield
    settings.CACHES["default"] = default


@pytest.fixture
def disable_cache(mocker) -> None:
    mocker.patch("django.core.cache.cache.get", return_value=None)
    mocker.patch("django.core.cache.cache.set")
    mocker.patch("django.core.cache.cache.add")
    mocker.patch("django.core.cache.cache.get_or_set", return_value=None)
    mocker.patch("django.core.cache.cache.get_many", return_value={})
    mocker.patch("django.core.cache.cache.set_many")
    mocker.patch("django.core.cache.cache.delete", return_value=True)
    mocker.patch("django.core.cache.cache.delete_many")
    mocker.patch("django.core.cache.cache.clear")
    mocker.patch("django.core.cache.cache.touch")
    mocker.patch("django.core.cache.cache.incr")
    mocker.patch("django.core.cache.cache.decr")
    mocker.patch("django.core.cache.cache.close")
