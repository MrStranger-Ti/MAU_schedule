import re
import urllib
from datetime import date, timedelta
from typing import Dict, List

import bs4
from django.conf import settings

from schedule.parser.abstract import ScheduleParser, Parser
from schedule.parser.storage import ParserStorage
from schedule.parser.helpers import join_url


class GroupScheduleParser(ScheduleParser):
    def __init__(self, user: settings.AUTH_USER_MODEL, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.user: settings.AUTH_USER_MODEL = user
        self.schedule_storage: ParserStorage = ParserStorage(
            cache_key=f"group_schedule_data_{self.user.group}_period_{self.period}",
        )

    def _get_schedule(self) -> Dict[date, List[List[str]]]:
        self._collect_parsing_params()

        group_url = self.parsing_storage.get("group_url", settings.SCHEDULE_URL)
        self._collect_schedule(group_url)

        schedule_data = self.schedule_storage.get("schedule_data")
        self.schedule_storage.save_db()
        self.parsing_storage.save_db()
        return schedule_data

    def _collect_parsing_params(self) -> None:
        if not self.parsing_storage.get("group_url"):
            soup = self.get_base_soup()
            self._collect_institute_value(soup)
            self._collect_group_url()

    def _collect_institute_value(self, soup: bs4.BeautifulSoup) -> None:
        select = soup.select_one("select[name=facs]")
        if select:
            institute_option = select.find(
                "option",
                string=self.user.institute,
            )
            if institute_option:
                self.parsing_storage["institute_value"] = institute_option.get("value")

    def _collect_group_url(self) -> None:
        weeks_options = self.parsing_storage.get("weeks_options")
        institute_value = self.parsing_storage.get("institute_value")
        if not weeks_options or not institute_value:
            return

        params = {
            "mode": 1,
            "pers": weeks_options[0][0],
            "facs": institute_value,
            "courses": self.user.course,
        }
        response = self.get_response(self.base_url, params=params)
        if response and response.status_code == 200:
            soup = self.get_soup(response)
            group_link = soup.find(
                "a",
                string=re.compile(rf"\s*{self.user.group}\s*"),
                href=lambda url: url and url.startswith("schedule.php"),
            )

            if group_link:
                self.parsing_storage["group_url"] = join_url(
                    self.base_url, group_link.get("href")
                )

    @staticmethod
    def _parse_schedule(
        soup: bs4.BeautifulSoup, week_monday: date
    ) -> Dict[date, List[List[str]]]:
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


class TeacherLinksParser(Parser):
    def __init__(self, user: settings.AUTH_USER_MODEL, **kwargs):
        super().__init__(user, **kwargs)
        self.storage: ParserStorage = ParserStorage(
            cache_key=f"teacher_links_data_{self.user.group}",
        )

    def get_data(self, query: str) -> Dict[str, str]:
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

        self.storage.save_db()
        return teacher_keys


class TeacherScheduleParser(ScheduleParser):
    def __init__(self, user: settings.AUTH_USER_MODEL, teacher_key: str, **kwargs):
        super().__init__(user, **kwargs)
        self.teacher_url = self.base_url + f"schedule2.php?key={teacher_key}"
        self.schedule_storage: ParserStorage = ParserStorage(
            cache_key=f'teacher_schedule_data_{self.user.group}_period_{self.period or "current"}'
        )

    def _get_schedule(self) -> Dict[Dict, List]:
        self.get_base_soup()
        self._collect_schedule(self.teacher_url)

        schedule_data = self.schedule_storage.get("schedule_data")
        self.schedule_storage.save_db()
        self.parsing_storage.save_db()
        return schedule_data

    def _parse_schedule(
        self, soup: bs4.BeautifulSoup, week_monday: date
    ) -> Dict[date, List[List[str]]]:
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
