import pytest
from django.conf import settings
from django.core.cache import cache

from schedule.parser import ParserResponse, Parser
from tests.test_api.test_schedule.test_parser.test_base.conftest import (
    CacheParserTest,
)


class TestCacheParser:
    def test_base_key_is_correct(self):
        class CacheParserTestBaseKey(CacheParserTest):
            base_key = "some_key"

        parser = CacheParserTestBaseKey()
        assert parser

    def test_base_key_is_none_fail(self):
        class CacheParserTestBaseKey(CacheParserTest):
            base_key = None

        with pytest.raises(AttributeError, match="Class attr 'base_key' must be set."):
            CacheParserTestBaseKey()

    def test_get_cache_key(self, get_cache_parser):
        unique_key = "some_unique_key"
        parser = get_cache_parser(unique_key=unique_key)
        assert parser.get_cache_key() == parser.base_key + "_" + unique_key

    def test_cache_found(self, mocker, get_cache_parser):
        cache_data = "some_data"
        mocker.patch("django.core.cache.cache.get", return_value=cache_data)
        parser_response = get_cache_parser().get_data()
        assert isinstance(parser_response, ParserResponse)
        assert parser_response.success
        assert parser_response.data == cache_data

    def test_cache_not_found_response_successful(self, mocker, get_cache_parser):
        mock_get = mocker.patch("django.core.cache.cache.get", return_value=None)
        mock_set = mocker.patch("django.core.cache.cache.set")

        parser = get_cache_parser()
        parser_response = parser.get_data()
        assert parser_response.success

        cache_key = parser.get_cache_key()
        mock_get.assert_called_with(cache_key)
        mock_set.assert_called_with(
            cache_key,
            parser_response.data,
            settings.SCHEDULE_CACHE_TIME,
        )

    def test_cache_not_found_response_unsuccessful(self, mocker, get_cache_parser):
        parser = get_cache_parser()
        mocker.patch.object(
            Parser,
            "get_data",
            return_value=ParserResponse(error="some error"),
        )
        mock_get = mocker.patch("django.core.cache.cache.get", return_value=None)
        mock_set = mocker.patch("django.core.cache.cache.set")

        parser_response = parser.get_data()
        assert not parser_response.success

        cache_key = parser.get_cache_key()
        mock_get.assert_called_with(cache_key)
        mock_set.assert_not_called()
