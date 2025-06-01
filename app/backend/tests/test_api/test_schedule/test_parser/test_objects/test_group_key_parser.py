from schedule.parser import GroupKeyParser


class TestGroupKeyParser:
    html = "groups-list.html"
    extra_data = {
        "course": 2,
        "group": "БИВТ-ВП-23",
    }

    def test_parse_data_success(self, disable_cache, mock_scraper):
        expected_data = "6f54eeb0-54ce-11ee-b017-1cc1de6f817c"
        mock_scraper(self.html)

        parser_response = GroupKeyParser(extra_data=self.extra_data).get_data()
        assert parser_response.success
        assert parser_response.data == expected_data

    def test_parse_data_fail(self, disable_cache, mock_scraper):
        mock_scraper(self.html, valid=False)

        parser_response = GroupKeyParser(extra_data=self.extra_data).get_data()
        assert not parser_response.success
