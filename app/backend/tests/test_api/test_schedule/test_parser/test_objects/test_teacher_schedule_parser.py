from schedule.parser import TeacherScheduleParser


class TestGroupScheduleParser:
    html = "teacher-schedule.html"
    extra_data = {
        "course": 2,
        "group": "БИВТ-ВП-23",
    }
    period = "27.01.2025-02.02.2025"

    def test_parse_data_success(self, disable_cache, mock_scraper):
        expected_data = {
            "2025-02-01": [["Занятий нет"]],
            "2025-01-27": [
                ["1", "", "", "", ""],
                ["2", "", "", "", ""],
                ["3", "", "", "", ""],
                [
                    "4",
                    "14:45 - 16:20",
                    "Архитектура вычислительных систем и компьютерных сетей "
                    "(Консультация)",
                    "БИВТ-ВТД-22",
                    "310 (Ленина, 57)",
                ],
                ["5", "", "", "", ""],
                ["6", "", "", "", ""],
                ["7", "", "", "", ""],
            ],
            "2025-01-28": [
                [
                    "1",
                    "09:00 - 10:35",
                    "Архитектура вычислительных систем и компьютерных сетей "
                    "(Экзамен)",
                    "БИВТ-ВТД-22",
                    "310 (Ленина, 57)",
                ],
                ["2", "", "", "", ""],
                ["3", "", "", "", ""],
                ["4", "", "", "", ""],
                ["5", "", "", "", ""],
                ["6", "", "", "", ""],
                ["7", "", "", "", ""],
            ],
            "2025-01-29": [["Занятий нет"]],
            "2025-01-30": [
                ["1", "", "", "", ""],
                ["2", "", "", "", ""],
                [
                    "3",
                    "12:40 - 14:15",
                    "Архитектура вычислительных систем и компьютерных сетей "
                    "(Консультация)",
                    "БИВТ-МП-22",
                    "310 (Ленина, 57)",
                ],
                ["4", "", "", "", ""],
                ["5", "", "", "", ""],
                ["6", "", "", "", ""],
                ["7", "", "", "", ""],
            ],
            "2025-01-31": [
                [
                    "1",
                    "09:00 - 10:35",
                    "Архитектура вычислительных систем и компьютерных сетей "
                    "(Экзамен)",
                    "БИВТ-МП-22",
                    "310 (Ленина, 57)",
                ],
                ["2", "", "", "", ""],
                ["3", "", "", "", ""],
                ["4", "", "", "", ""],
                ["5", "", "", "", ""],
                ["6", "", "", "", ""],
                ["7", "", "", "", ""],
            ],
        }
        mock_scraper(self.html)

        parser_response = TeacherScheduleParser(
            extra_data=self.extra_data,
            period=self.period,
        ).get_data()
        assert parser_response.success
        assert parser_response.data == expected_data, parser_response.data

    def test_parse_data_fail(self, disable_cache, mock_scraper):
        mock_scraper(self.html, valid=False)

        parser_response = TeacherScheduleParser(
            extra_data=self.extra_data,
            period=self.period,
        ).get_data()
        assert not parser_response.success
