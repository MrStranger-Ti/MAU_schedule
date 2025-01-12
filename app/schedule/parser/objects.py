import urllib
from datetime import date, timedelta
from urllib.parse import urlparse

import bs4

from schedule.parser.base import MauParser, MauScheduleParser
from schedule.parser.mixins import ScheduleParserMixin


class GroupParamsParser(MauParser):
    """
    Парсер query параметров для группы.
    """

    def get_cache_key(self) -> str:
        return f"params_data_{self.user.group}"

    def _parse_data(self, soup: bs4.BeautifulSoup):
        return {
            "periods": self._parse_periods(soup),
            "facs": self._parse_institute_value(soup),
        }

    def _parse_periods(self, form_tag: bs4.BeautifulSoup) -> list[str]:
        periods_select = form_tag.find("select", {"name": "pers"})
        periods_options = periods_select.find_all(
            "option",
            value=lambda name: int(name) > 0,
        )
        return [option.text for option in periods_options]

    def _parse_institute(self, soup: bs4.BeautifulSoup) -> str:
        institute_select = soup.find("select", {"name": "facs"})
        institute_option = institute_select.find("option", string=self.user.group)
        return institute_option.get("value")


class GroupUrlParser(MauParser):
    """
    Парсер ключа группы.
    """

    def get_cache_key(self) -> str:
        return f"group_schedule_data_{self.user.group}"

    def _parse_data(self, soup: bs4.BeautifulSoup):
        group_a = soup.find("a", _class="btn", string=self.user.group)
        group_href = group_a.get("href")
        return group_href


class GroupScheduleParser(MauScheduleParser):
    """
    Парсер для расписания.
    """

    def get_cache_key(self) -> str:
        print(dir(self))
        return (
            f"group_schedule_data_{self.user.group}_period_{self.period_manager.period}"
        )

    def _parse_data(self, soup: bs4.BeautifulSoup) -> dict[date, list[list[str]]]:
        week_monday = date.fromisoformat(self.period_manager.start)

        week_schedule = {}
        for weekday_num, day in enumerate(soup.find_all("table")):
            title = day.find("th")
            if title and "Воскресенье" not in title.text:
                curr_date = week_monday + timedelta(days=weekday_num)
                week_schedule.setdefault(curr_date, [])
                for row in day.find_all("tr")[1:]:
                    week_schedule[curr_date].append(
                        [field.text for field in row.find_all(["th", "td"])]
                    )

        return week_schedule


class TeacherKeysParser(MauParser):
    """
    Парсер для ключей преподавателей.
    """

    def get_cache_key(self) -> str:
        return f"teacher_links_data_{self.user.group}"

    def _parse_data(self, soup: bs4.BeautifulSoup):
        query = self.parsing_data.get("query")
        if query is None:
            raise ValueError("No query item.")

        params = {
            "mode2": "1",
            "pers2": "0",
            "sstring": query,
        }
        response = self.get_response(self.base_url, params=params)

        teacher_keys = {}
        if response and response.status_code == 200:
            soup = self.get_soup(response)
            links = soup.select("td b a")

            for link in links:
                query_params = urllib.parse.parse_qs(link.get("href"))
                key = query_params.get("schedule2.php?key")[0]
                teacher_keys[link.text] = key

        return teacher_keys


class TeacherScheduleParser(MauScheduleParser):
    """
    Парсер для расписания преподавателей.
    """

    def get_cache_key(self) -> str:
        return f"teacher_links_data_{self.user.group}"

    def _parse_data(self, soup: bs4.BeautifulSoup):
        week_monday = date.fromisoformat(self.period_manager.start)

        week_schedule = {}
        trs = soup.select("tr")

        weekday_num = 0
        for tr in trs:
            tr_class = tr.get("class")
            if tr_class and tr_class[0] == "title":
                curr_date = week_monday + timedelta(days=weekday_num)
                week_schedule.setdefault(curr_date, [])

                weekday_num += 1
            else:
                week_schedule[curr_date].append(
                    [field.text for field in tr.find_all("td")]
                )

        return week_schedule

    # def _collect_schedule(self, url: str) -> None:
    #     self._define_week_period()
    #     start, end = self._get_start_end()
    #     params = {
    #         "perstart": start,
    #         "perend": end,
    #     }
    #     response = self.get_response(url, params=params)
    #     if response and response.status_code == 200:
    #         soup = self.get_soup(response)
    #         week_monday = date(*map(int, start.split("-")))
    #         schedule_data = self._parse_schedule(soup, week_monday)
    #         if schedule_data:
    #             self.schedule_storage["schedule_data"] = schedule_data

    # def _get_start_end(self) -> Tuple[str, str]:
    #     start, end = self._get_start_end_period(self.period)
    #     return start, end
    #
    # def _define_week_period(self) -> None:
    #     storage_periods = [
    #         period for _, period in self.parsing_storage.get("weeks_options", [])
    #     ]
    #     if self.period not in storage_periods:
    #         self._change_period_by_weeks_options()
    #
    # def _change_period_by_weeks_options(self) -> None:
    #     weeks_options = self.parsing_storage.get("weeks_options", [])
    #     for _, period in weeks_options:
    #         if check_period_for_current_date(period):
    #             self.period = period
    #             return
    #
    #     if weeks_options:
    #         self.period = weeks_options[0][1]
    #
    # @staticmethod
    # def _get_start_end_period(week_period: str) -> Tuple[str, ...]:
    #     return tuple(map(convert_to_iso_8601, week_period.split("-")))
    #
    # def get_current_week_option(self) -> str | None:
    #     for option in self.parsing_storage.get("weeks_options", []):
    #         if self.period == option[1]:
    #             return option[0]
    #
    #     return None
    #
    # def _collect_weeks_options(self, soup: bs4.BeautifulSoup) -> None:
    #     select = soup.select_one("select[name=pers]")
    #     if select:
    #         date_options = select.find_all(
    #             "option",
    #             value=lambda value: int(value) > 0,
    #         )
    #         weeks_options = [
    #             (option.get("value"), clean_date_period(option.text))
    #             for option in date_options
    #         ]
    #         if weeks_options:
    #             self.parsing_storage["weeks_options"] = weeks_options
    #
    # def get_base_soup(self) -> bs4.BeautifulSoup | None:
    #     response = self.get_response(self.base_url)
    #     if response and response.status_code == 200:
    #         soup = self.get_soup(response)
    #         self._collect_weeks_options(soup)
    #         return soup
    #
    #     return None


# class GroupScheduleParser(ScheduleParser):
#     def __init__(self, user: settings.AUTH_USER_MODEL, *args, **kwargs):
#         super().__init__(user, *args, **kwargs)
#         self.user: settings.AUTH_USER_MODEL = user
#         self.schedule_storage: ParserStorage = ParserStorage(
#             cache_key=f"group_schedule_data_{self.user.group}_period_{self.period}",
#         )
#
#     def _get_schedule(self) -> Dict[date, List[List[str]]]:
#         self._collect_parsing_params()
#
#         group_url = self.parsing_storage.get("group_url", settings.SCHEDULE_URL)
#         self._collect_schedule(group_url)
#
#         schedule_data = self.schedule_storage.get("schedule_data")
#         self.schedule_storage.save_db()
#         self.parsing_storage.save_db()
#         return schedule_data
#
#     def _collect_parsing_params(self) -> None:
#         if not self.parsing_storage.get("group_url"):
#             soup = self.get_base_soup()
#             self._collect_institute_value(soup)
#             self._collect_group_url()
#
#     def _collect_institute_value(self, soup: bs4.BeautifulSoup) -> None:
#         select = soup.select_one("select[name=facs]")
#         if select:
#             institute_option = select.find(
#                 "option",
#                 string=self.user.institute,
#             )
#             if institute_option:
#                 self.parsing_storage["institute_value"] = institute_option.get("value")
#
#     def _collect_group_url(self) -> None:
#         weeks_options = self.parsing_storage.get("weeks_options")
#         institute_value = self.parsing_storage.get("institute_value")
#         if not weeks_options or not institute_value:
#             return
#
#         params = {
#             "mode": 1,
#             "pers": weeks_options[0][0],
#             "facs": institute_value,
#             "courses": self.user.course,
#         }
#         response = self.get_response(self.base_url, params=params)
#         if response and response.status_code == 200:
#             soup = self.get_soup(response)
#             group_link = soup.find(
#                 "a",
#                 string=re.compile(rf"\s*{self.user.group}\s*"),
#                 href=lambda url: url and url.startswith("schedule.php"),
#             )
#
#             if group_link:
#                 self.parsing_storage["group_url"] = join_url(
#                     self.base_url, group_link.get("href")
#                 )
#
#     @staticmethod
#     def _parse_schedule(
#         soup: bs4.BeautifulSoup, week_monday: date
#     ) -> Dict[date, List[List[str]]]:
#         week_schedule = {}
#         for weekday_num, day in enumerate(soup.find_all("table")):
#             title = day.find("th")
#             if title and "Воскресенье" not in title.text:
#                 curr_date = week_monday + timedelta(days=weekday_num)
#                 week_schedule.setdefault(curr_date, [])
#                 for row in day.find_all("tr")[1:]:
#                     week_schedule[curr_date].append(
#                         [field.text for field in row.find_all(["th", "td"])]
#                     )
#
#         return week_schedule
#
#
# class TeacherLinksMauParser(MauParser):
#     def __init__(self, user: settings.AUTH_USER_MODEL, **kwargs):
#         super().__init__(user, **kwargs)
#         self.storage: ParserStorage = ParserStorage(
#             cache_key=f"teacher_links_data_{self.user.group}",
#         )
#
#     def get_data(self, query: str) -> Dict[str, str]:
#         params = {
#             "mode2": "1",
#             "pers2": "0",
#             "sstring": query.encode("cp1251"),
#         }
#         response = self.get_response(self.base_url, params=params)
#
#         teacher_keys = {}
#         if response and response.status_code == 200:
#             soup = self.get_soup(response)
#             links = soup.select("td b a")
#
#             for link in links:
#                 query_params = urllib.parse.parse_qs(link.get("href"))
#                 key = query_params.get("schedule2.php?key")[0]
#                 teacher_keys[link.text] = key
#
#         self.storage.save_db()
#         return teacher_keys
#
#
# class TeacherScheduleParser(ScheduleParser):
#     def __init__(self, user: settings.AUTH_USER_MODEL, teacher_key: str, **kwargs):
#         super().__init__(user, **kwargs)
#         self.teacher_url = self.base_url + f"schedule2.php?key={teacher_key}"
#         self.schedule_storage: ParserStorage = ParserStorage(
#             cache_key=f'teacher_schedule_data_{self.user.group}_period_{self.period or "current"}'
#         )
#
#     def _get_schedule(self) -> Dict[Dict, List]:
#         self.get_base_soup()
#         self._collect_schedule(self.teacher_url)
#
#         schedule_data = self.schedule_storage.get("schedule_data")
#         self.schedule_storage.save_db()
#         self.parsing_storage.save_db()
#         return schedule_data
#
#     def _parse_schedule(
#         self, soup: bs4.BeautifulSoup, week_monday: date
#     ) -> Dict[date, List[List[str]]]:
#         week_schedule = {}
#         trs = soup.select("tr")
#
#         weekday_num = 0
#         for tr in trs:
#             tr_class = tr.get("class")
#             if tr_class and tr_class[0] == "title":
#                 curr_date = week_monday + timedelta(days=weekday_num)
#                 week_schedule.setdefault(curr_date, [])
#
#                 weekday_num += 1
#             else:
#                 week_schedule[curr_date].append(
#                     [field.text for field in tr.find_all("td")]
#                 )
#
#         return week_schedule
