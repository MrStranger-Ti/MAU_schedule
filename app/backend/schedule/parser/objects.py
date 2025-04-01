from datetime import date, timedelta
from typing import Any
from urllib.parse import parse_qs, urlparse

from django.conf import settings
import bs4

from schedule.parser.base import CacheParser, ScheduleParser


class GroupParamsParser(ScheduleParser):
    """
    Парсер query параметров для группы.
    """

    url = settings.SCHEDULE_URL
    required_extra_data = ("institute",)
    base_key = "schedule_params_data"

    def _parse_data(self, soup: bs4.BeautifulSoup) -> dict[str, Any]:
        return {
            "pers": self._parse_period(soup),
            "facs": self._parse_institute(soup),
        }

    def _parse_period(self, soup: bs4.BeautifulSoup) -> str:
        periods_select = soup.find("select", {"name": "pers"})
        period_option = periods_select.find(
            "option",
            value=lambda x: int(x) > 0,
            string=lambda raw_period: self.period_manager.period in raw_period,
        )
        period_value = period_option.get("value")
        return period_value

    def _parse_institute(self, soup: bs4.BeautifulSoup) -> str:
        institute_select = soup.find("select", attrs={"name": "facs"})
        institute_option = institute_select.find(
            "option",
            string=self.extra_data["institute"],
        )
        institute_value = institute_option.get("value")
        return institute_value


class GroupKeyParser(CacheParser):
    """
    Парсер ключа группы.
    """

    url = settings.SCHEDULE_URL
    required_extra_data = ("course", "group")
    base_key = "group_key"

    def _change_params(self, params: dict[str, str]) -> dict[str, str]:
        params.update(
            {
                "mode": 1,
                "courses": self.extra_data["course"],
            },
        )
        return params

    def _parse_data(self, soup: bs4.BeautifulSoup) -> str:
        group_a = soup.find("a", class_="btn", string=self.extra_data["group"])
        group_href = group_a.get("href")

        parsed_url = urlparse(group_href)
        query_params = parse_qs(parsed_url.query)
        key = query_params.get("key")
        return key[0]


class GroupScheduleParser(ScheduleParser):
    """
    Парсер для расписания.
    """

    url = settings.SCHEDULE_URL + "schedule.php"
    base_key = "group_schedule"

    def _parse_data(self, soup: bs4.BeautifulSoup) -> dict[str, list[list[str]]]:
        week_monday = date.fromisoformat(self.period_manager.start)

        week_schedule = {}
        for weekday_num, day in enumerate(soup.find_all("table")):
            title = day.find("th")
            if title and "Воскресенье" not in title.text:
                curr_date = week_monday + timedelta(days=weekday_num)
                curr_date_string = curr_date.strftime("%d-%m-%Y")
                week_schedule.setdefault(curr_date_string, [])
                for row in day.find_all("tr")[1:]:
                    week_schedule[curr_date_string].append(
                        [field.text.strip() for field in row.find_all(["th", "td"])]
                    )

        return week_schedule


class TeacherScheduleParser(ScheduleParser):
    """
    Парсер для расписания преподавателей.
    """

    url = settings.SCHEDULE_URL + "schedule2.php"
    base_key = "teacher_schedule"

    def _parse_data(self, soup: bs4.BeautifulSoup) -> Any:
        week_monday = date.fromisoformat(self.period_manager.start)

        week_schedule = {}
        trs = soup.select("tr")

        weekday_num = 0
        for tr in trs:
            tr_class = tr.get("class")
            if tr_class and tr_class[0] == "title":
                curr_date = week_monday + timedelta(days=weekday_num)
                curr_date_string = curr_date.strftime("%d-%m-%Y")
                week_schedule.setdefault(curr_date_string, [])
                weekday_num += 1
            else:
                week_schedule[curr_date_string].append(
                    [field.text.strip() for field in tr.find_all("td")]
                )

        return week_schedule


class TeacherKeysParser(CacheParser):
    """
    Парсер для ключей преподавателей.

    Для поиска необходимо передать sstring в параметры запроса.
    """

    url = settings.SCHEDULE_URL
    base_key = "teacher_links"

    def _change_params(self, params: dict[str, str]) -> dict[str, str]:
        params.update(
            {
                "mode2": "1",
                "tab": "2",
                "pers2": "0",
            }
        )
        return params

    def _parse_data(self, soup: bs4.BeautifulSoup) -> dict[str, str]:
        teacher_keys = {}

        links = soup.select("td b a")
        for link in links:
            parsed_url = urlparse(link.get("href"))
            query_params = parse_qs(parsed_url.query)
            key = query_params.get("key")
            teacher_keys[link.text] = key[0]

        return teacher_keys


class PeriodsParser(CacheParser):
    """
    Парсер для списка периодов.
    """

    url = settings.SCHEDULE_URL
    base_key = "periods_list"

    def _parse_data(self, soup: bs4.BeautifulSoup) -> Any:
        periods_select = soup.find("select", attrs={"name": "pers"})
        periods_options = periods_select.find_all("option", value=lambda x: int(x) > 0)
        periods = [option.text.split()[0] for option in periods_options]
        return periods
