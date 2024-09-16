import re
import urllib
from datetime import datetime, date, timedelta
from typing import List, Dict, Tuple, Any

import bs4
import requests

from django.core.cache import cache
from django.conf import settings

from mau_utils.mau_requests import get_response


def get_soup(response: requests.Response) -> bs4.BeautifulSoup:
    return bs4.BeautifulSoup(response.content, 'lxml')


def clean_date_period(date_period: str) -> str:
    return re.search(r'\d{2}\.\d{2}\.\d{4}-\d{2}\.\d{2}\.\d{4}', date_period).group()


def join_url(first_url: str, second_url: str) -> str:
    return urllib.parse.urljoin(first_url, second_url)


def convert_to_iso_8601(date_string: str) -> str:
    return datetime.strptime(date_string, '%d.%m.%Y').strftime('%Y-%m-%d')


def check_period_for_current_date(date_period: str) -> bool:
    now = datetime.now()

    first_date, last_date = map(
        lambda x: datetime.strptime(x, '%d.%m.%Y'),
        date_period.split('-'),
    )
    return first_date <= now <= last_date


class ParserStorage:
    def __init__(self, user: settings.AUTH_USER_MODEL):
        self.user: settings.AUTH_USER_MODEL = user
        self.weeks_options: List[str] | None = None
        self.__storage: Dict[str, Any] = {}

        weeks_options = cache.get(f'schedule_group_options_{self.user.group}')
        if weeks_options:
            self.weeks_options = weeks_options

    def __getitem__(self, item):
        return self.__storage[item]

    def __setitem__(self, key, value):
        self.__storage[key] = value

    def save_weeks_options(self, weeks_options: List[Tuple[str, str]]) -> None:
        cache.set(
            f'schedule_group_options_{self.user.group}',
            weeks_options,
            settings.SCHEDULE_CACHE_TIME,
        )

        self.weeks_options = weeks_options


class ScheduleParser:
    def __init__(self, user: settings.AUTH_USER_MODEL, period: str = None, teacher_schedule: bool = False):
        self.user: settings.AUTH_USER_MODEL = user
        self.period = period
        self.base_url: str = settings.SCHEDULE_URL
        self.storage = ParserStorage(user)
        self.teacher_schedule: bool = teacher_schedule
        self.schedule_url: str = settings.SCHEDULE_URL

    def get_group_schedule(self) -> Dict[int, List[str]] | None:
        group_url = cache.get(f'group_schedule_url_{self.user.group}')
        if not group_url:
            group_url = self.__get_group_url()
            cache.set(
                f'group_schedule_url_{self.user.group}',
                group_url,
                settings.SCHEDULE_CACHE_TIME,
            )

        return self.__get_schedule_data(group_url)

    def __get_group_url(self) -> str | None:
        response = get_response(self.base_url)
        if not response:
            return None

        soup = get_soup(response)
        self.__find_weeks_options(soup)
        self.__find_institute_value(soup)

        weeks_options, institute_value

        if not weeks_options or not institute_value:
            return None

        params = {
            'mode': 1,
            'pers': weeks_options[0][0],
            'facs': institute_value,
            'courses': self.user.course,
        }
        response = get_response(self.base_url, params=params)
        soup = get_soup(response)
        group_url = join_url(self.base_url, self.__find_group_url(soup))

        if not group_url:
            return None

        return group_url

    def __find_weeks_options(self, soup: bs4.BeautifulSoup) -> List[Tuple[str, str]]:
        date_options = soup.select_one('select[name=pers]').find_all(
            'option',
            value=lambda value: int(value) > 0,
        )
        weeks_options = [
            (option.get('value'), clean_date_period(option.text))
            for option in date_options
        ]
        self.storage.save_weeks_options(weeks_options)
        return weeks_options

    def __find_institute_value(self, soup: bs4.BeautifulSoup) -> str | None:
        institute_option = soup.select_one('select[name=facs]').find(
            'option',
            string=self.user.institute,
        )
        return institute_option.get('value')

    def __find_group_url(self, soup: bs4.BeautifulSoup) -> str | None:
        group_link = soup.find(
            'a',
            string=re.compile(fr'\s*{self.user.group}\s*'),
            href=lambda url: url and url.startswith('schedule.php'),
        )

        if not group_link:
            return None

        return group_link.get('href')

    def __get_schedule_data(self, url: str) -> dict[dict: list]:
        start, end = self.__get_start_end()
        params = {
            'perstart': start,
            'perend': end,
        }

        response = get_response(url, params=params)
        soup = get_soup(response)

        week_monday = date(*map(int, start.split('-')))
        if self.teacher_schedule:
            schedule_data = self.__parse_teacher_schedule(soup, week_monday)
        else:
            schedule_data = self.__parse_group_schedule(soup, week_monday)

        return schedule_data

    def __get_start_end(self) -> Tuple[str, str]:
        storage_periods = [period for _, period in self.storage.weeks_options]
        if self.period in storage_periods:
            start, end = self.__get_start_end_period(self.period)
        else:
            start, end = self.__define_week_option()

        return start, end

    def __define_week_option(self) -> Tuple[str, str]:
        week_period = None
        for period in self.storage.weeks_options:
            if check_period_for_current_date(period):
                week_period = period
                break

        if week_period:
            start, end = self.__get_start_end_period(week_period)
        else:
            start, end = self.__get_start_end_period(self.storage.weeks_options[0])

        return start, end

    @staticmethod
    def __get_start_end_period(week_period: str) -> Tuple[str, ...]:
        return tuple(map(convert_to_iso_8601, week_period.split('-')))

    @staticmethod
    def __parse_group_schedule(soup: bs4.BeautifulSoup, week_monday: date):
        week_schedule = {}
        for weekday_num, day in enumerate(soup.find_all('table')):
            title = day.find('th')
            if title and 'Воскресенье' not in title.text:
                curr_date = week_monday + timedelta(days=weekday_num)
                week_schedule.setdefault(curr_date, [])
                for row in day.find_all('tr')[1:]:
                    week_schedule[curr_date].append(
                        [field.text for field in row.find_all(['th', 'td'])]
                    )

        return week_schedule

    def __parse_teacher_schedule(self, soup: bs4.BeautifulSoup, week_monday: date):
        pass
