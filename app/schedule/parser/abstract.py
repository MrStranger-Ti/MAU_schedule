import abc
from abc import ABC
from datetime import date
from typing import Any, Tuple

import bs4
import requests
from django.conf import settings
from fake_useragent import UserAgent

from schedule.parser.helpers import (
    check_period_for_current_date,
    convert_to_iso_8601,
    clean_date_period,
)
from schedule.parser.storage import ParserStorage


class Parser(ABC):
    def __init__(self, user: settings.AUTH_USER_MODEL, parser: str = "lxml"):
        self.user: settings.AUTH_USER_MODEL = user
        self.base_url: str = settings.SCHEDULE_URL
        self.parser: str = parser
        self.user_agent_manager = UserAgent()

    @abc.abstractmethod
    def get_data(self):
        pass

    def get_soup(self, response: requests.Response) -> bs4.BeautifulSoup:
        return bs4.BeautifulSoup(response.content, self.parser)

    def get_response(self, url: str, **kwargs: Any) -> requests.Response | None:
        try:
            response = requests.get(
                url,
                headers={"User-Agent": self.user_agent_manager.random},
                timeout=5,
                **kwargs,
            )
        except requests.exceptions.Timeout:
            return None

        return response


class ScheduleParser(Parser, ABC):
    def __init__(self, user: settings.AUTH_USER_MODEL, period: str = None, **kwargs):
        super().__init__(user, **kwargs)
        self.user: settings.AUTH_USER_MODEL = user
        self.period = period
        if not self.period:
            self._set_default_period()

        self.schedule_storage: ParserStorage | None = None
        self.parsing_storage: ParserStorage = ParserStorage(
            cache_key=f"group_parsing_data_{self.user.group}",
        )

    @abc.abstractmethod
    def _get_schedule(self):
        pass

    @abc.abstractmethod
    def _parse_schedule(self):
        pass

    def get_data(self):
        schedule_data = self.schedule_storage.get("schedule_data")
        if not schedule_data:
            schedule_data = self._get_schedule()

        self._collect_current_week_option()
        return schedule_data

    def _set_default_period(self):
        current_week = date(2024, 7, 2).isocalendar()
        monday = date.fromisocalendar(current_week[0], current_week[1], 1)
        sunday = date.fromisocalendar(current_week[0], current_week[1], 7)
        self.period = monday.strftime("%d.%m.%Y") + "-" + sunday.strftime("%d.%m.%Y")

    def _collect_schedule(self, url: str) -> None:
        self._define_week_period()
        start, end = self._get_start_end()
        params = {
            "perstart": start,
            "perend": end,
        }
        response = self.get_response(url, params=params)
        if response and response.status_code == 200:
            soup = self.get_soup(response)
            week_monday = date(*map(int, start.split("-")))
            schedule_data = self._parse_schedule(soup, week_monday)
            if schedule_data:
                self.schedule_storage["schedule_data"] = schedule_data

    def _get_start_end(self) -> Tuple[str, str]:
        start, end = self._get_start_end_period(self.period)
        return start, end

    def _define_week_period(self) -> None:
        storage_periods = [
            period for _, period in self.parsing_storage.get("weeks_options", [])
        ]
        if self.period not in storage_periods:
            self._change_period_by_weeks_options()

        self._collect_current_week_option()

    def _change_period_by_weeks_options(self) -> None:
        weeks_options = self.parsing_storage.get("weeks_options", [])
        for _, period in weeks_options:
            if check_period_for_current_date(period):
                self.period = period
                return

        if weeks_options:
            self.period = weeks_options[0][1]

    @staticmethod
    def _get_start_end_period(week_period: str) -> Tuple[str, ...]:
        return tuple(map(convert_to_iso_8601, week_period.split("-")))

    def _collect_current_week_option(self) -> None:
        for option in self.parsing_storage.get("weeks_options", []):
            if self.period == option[1]:
                self.parsing_storage["current_week_value"] = option[0]
                break

    def _collect_weeks_options(self, soup: bs4.BeautifulSoup) -> None:
        select = soup.select_one("select[name=pers]")
        if select:
            date_options = select.find_all(
                "option",
                value=lambda value: int(value) > 0,
            )
            weeks_options = [
                (option.get("value"), clean_date_period(option.text))
                for option in date_options
            ]
            if weeks_options:
                self.parsing_storage["weeks_options"] = weeks_options
