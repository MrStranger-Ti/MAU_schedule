from schedule.parser import GroupParamsParser


class TestGroupParamsParser:
    html = "searching-group.html"
    extra_data = {
        "institute": "ИГ и СН",
    }
    period = "27.01.2025-02.02.2025"

    def test_parse_data_success(self, disable_cache, mock_scraper):
        expected_data = {
            "pers": "321",
            "facs": "4",
        }
        mock_scraper(self.html)

        response = GroupParamsParser(
            extra_data=self.extra_data,
            period=self.period,
        ).get_data()
        assert response.success
        assert response.data == expected_data

    def test_parse_data_fail(self, disable_cache, mock_scraper):
        mock_scraper(self.html, valid=False)

        response = GroupParamsParser(
            extra_data=self.extra_data,
            period=self.period,
        ).get_data()
        assert not response.success
