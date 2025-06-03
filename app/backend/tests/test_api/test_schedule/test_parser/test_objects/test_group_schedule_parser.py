from schedule.parser import GroupScheduleParser


class TestGroupScheduleParser:
    html = "group-schedule.html"
    period = "27.01.2025-02.02.2025"

    def test_parse_data_success(self, disable_cache, mock_scraper):
        expected_data = {
            "2025-01-27": [["Занятий нет"]],
            "2025-01-28": [
                [
                    "1",
                    "09:00 - 10:35",
                    "Военная подготовка\xa0 (Практ.)",
                    "—",
                    "Корпус М (Советская,17)",
                ],
                [
                    "2",
                    "10:45 - 12:20",
                    "Военная подготовка\xa0 (Практ.)",
                    "—",
                    "Корпус М (Советская,17)",
                ],
                [
                    "3",
                    "12:40 - 14:15",
                    "Военная подготовка\xa0 (Практ.)",
                    "—",
                    "Корпус М (Советская,17)",
                ],
                [
                    "4",
                    "14:45 - 16:20",
                    "Военная подготовка\xa0 (Практ.)",
                    "—",
                    "Корпус М (Советская,17)",
                ],
                ["5", "", "", "", ""],
                ["6", "", "", "", ""],
                ["7", "", "", "", ""],
            ],
            "2025-01-29": [["Занятий нет"]],
            "2025-01-30": [["Занятий нет"]],
            "2025-01-31": [["Занятий нет"]],
            "2025-02-01": [["Занятий нет"]],
        }
        mock_scraper(self.html)

        parser_response = GroupScheduleParser(period=self.period).get_data()
        assert parser_response.success
        assert parser_response.data == expected_data

    def test_parse_data_fail(self, disable_cache, mock_scraper):
        mock_scraper(self.html, valid=False)

        parser_response = GroupScheduleParser(period=self.period).get_data()
        assert not parser_response.success
