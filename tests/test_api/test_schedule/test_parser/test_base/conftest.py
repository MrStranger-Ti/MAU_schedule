from typing import Any, Callable

import bs4
import pytest

from schedule.parser import Parser, CacheParser, ParserResponse, ScheduleParser


class ParserTest(Parser):
    url = "https://www.google.com/"

    def _parse_data(self, soup: bs4.BeautifulSoup) -> Any:
        pass


@pytest.fixture
def mock_parser(mocker) -> Callable:
    def wrapper(parser: Parser) -> Parser:
        parser._parse_data = mocker.Mock(return_value="test data")
        parser.get_soup = mocker.Mock(return_value="test soup")

        response_mock = mocker.Mock()
        response_mock.status_code = 200
        parser.get_response = mocker.Mock()
        parser.get_response.return_value = response_mock
        return parser

    return wrapper


@pytest.fixture
def get_parser(mock_parser) -> Callable:
    def wrapper(*args, **kwargs) -> ParserTest:
        parser = mock_parser(ParserTest(*args, **kwargs))
        return parser

    return wrapper


class CacheParserTest(CacheParser):
    url = "https://www.google.com/"
    base_key = "test_key"

    def _parse_data(self, soup: bs4.BeautifulSoup) -> Any:
        pass


@pytest.fixture
def mock_cache_parser(mocker, mock_parser) -> Callable:
    def wrapper(parser: CacheParserTest) -> CacheParserTest:
        parser = mock_parser(parser)
        mocker.patch.object(
            Parser,
            "get_data",
            return_value=ParserResponse(data="some data"),
        )
        return parser

    return wrapper


@pytest.fixture
def get_cache_parser(mock_cache_parser) -> Callable:
    def wrapper(*args, **kwargs) -> CacheParserTest:
        parser = mock_cache_parser(CacheParserTest(*args, **kwargs))
        return parser

    return wrapper


class ScheduleParserTest(ScheduleParser):
    url = "https://www.google.com/"
    base_key = "test_key"

    def _parse_data(self, soup: bs4.BeautifulSoup) -> Any:
        pass


@pytest.fixture
def get_schedule_parser(mock_cache_parser) -> Callable:
    def wrapper(*args, **kwargs) -> ScheduleParserTest:
        parser = mock_cache_parser(ScheduleParserTest(*args, **kwargs))
        return parser

    return wrapper
