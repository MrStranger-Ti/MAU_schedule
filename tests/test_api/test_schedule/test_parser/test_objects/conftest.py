import os.path
from pathlib import Path
from typing import Callable

import pytest
from bs4 import BeautifulSoup

from schedule.parser.base import WebScraper


@pytest.fixture(scope="package")
def _disable_cache(disable_cache):
    pass


def _get_test_html(html_path: str, valid: bool = True) -> str:
    curr_dir = Path(__file__).parent
    directory = "valid" if valid else "invalid"
    path = os.path.join("testing_html", directory, html_path)
    with open(curr_dir.joinpath(path), "r", encoding="utf-8") as file:
        return file.read()


@pytest.fixture
def mock_scraper(mocker) -> Callable:
    def wrapper(html_file_name: str, valid: bool = True) -> None:
        test_html = _get_test_html(html_file_name, valid=valid)
        mocker.patch.object(
            WebScraper, "get_soup", return_value=BeautifulSoup(test_html)
        )
        response_mock = mocker.Mock()
        response_mock.status_code = 200
        mocker.patch.object(WebScraper, "get_response", return_value=response_mock)

    return wrapper
