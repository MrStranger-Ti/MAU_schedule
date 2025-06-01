import pytest

from schedule.parser.base import WebScraper

URL = "https://www.google.com/"


class TestWebScraper:
    def test_url_is_correct(self):
        scraper = WebScraper(url=URL)
        assert scraper

    def test_url_is_none_fail(self):
        with pytest.raises(AttributeError, match="Class attr 'url' must be set."):
            WebScraper()

    def test_change_params_method(self, mocker):
        test_params = {"test_param_1": "value_1", "test_param_2": "value_2"}

        class WebScraperTest(WebScraper):
            url = URL

            def _change_params(self, params: dict[str, str]) -> dict[str, str]:
                params.update(test_params)
                return params

        scraper = WebScraperTest()
        spy = mocker.spy(scraper, "_change_params")
        for param_name, value in test_params.items():
            scraper_params = scraper.params

            assert param_name in scraper_params
            assert scraper_params[param_name] == value

        assert spy.call_count == len(test_params)
