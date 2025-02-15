from schedule.parser import PeriodsParser


class TestPeriodsParser:
    html = "searching-group.html"

    def test_parse_data_success(self, disable_cache, mock_scraper):
        expected_data = [
            "02.09.2024-08.09.2024",
            "09.09.2024-15.09.2024",
            "16.09.2024-22.09.2024",
            "23.09.2024-29.09.2024",
            "30.09.2024-06.10.2024",
            "07.10.2024-13.10.2024",
            "14.10.2024-20.10.2024",
            "21.10.2024-27.10.2024",
            "28.10.2024-03.11.2024",
            "04.11.2024-10.11.2024",
            "11.11.2024-17.11.2024",
            "18.11.2024-24.11.2024",
            "25.11.2024-01.12.2024",
            "02.12.2024-08.12.2024",
            "09.12.2024-15.12.2024",
            "16.12.2024-22.12.2024",
            "23.12.2024-29.12.2024",
            "30.12.2024-05.01.2025",
            "06.01.2025-12.01.2025",
            "13.01.2025-19.01.2025",
            "20.01.2025-26.01.2025",
            "27.01.2025-02.02.2025",
            "03.02.2025-09.02.2025",
            "10.02.2025-16.02.2025",
            "17.02.2025-23.02.2025",
            "24.02.2025-02.03.2025",
            "03.03.2025-09.03.2025",
            "10.03.2025-16.03.2025",
            "17.03.2025-23.03.2025",
            "24.03.2025-30.03.2025",
        ]
        mock_scraper(self.html)

        parser_response = PeriodsParser().get_data()
        assert parser_response.success
        assert expected_data == parser_response.data

    def test_parse_data_fail(self, disable_cache, mock_scraper):
        mock_scraper(self.html, valid=False)

        parser_response = PeriodsParser().get_data()
        assert not parser_response.success
