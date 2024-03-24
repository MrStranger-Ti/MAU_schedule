import os
import re
from datetime import date, timedelta

import bs4
import requests

from django.conf import settings

from mau_auth.exceptions import TagNotFound
from django.core.cache import cache


class MauUserParserMixin:
    @classmethod
    def _get_schedule_data(cls, url: str) -> dict[int, list[str]]:
        current_calendar_date = date.today().isocalendar()
        monday = date.fromisocalendar(current_calendar_date[0], current_calendar_date[1], 1)

        data = {}
        for _ in range(4):
            sunday = monday + timedelta(days=6)
            params = {
                'perstart': monday.isoformat(),
                'perend': sunday.isoformat(),
            }

            group_page_response = requests.get(url, params=params)
            soup = bs4.BeautifulSoup(group_page_response.content, 'lxml')

            if not soup.find('table', class_='table table-bordered table-striped table-3'):
                break

            for weekday_num, day in enumerate(soup.find_all('table')):
                title = day.find('th')
                if title and not title.text.startswith('Воскресенье'):
                    curr_date = monday + timedelta(days=weekday_num)
                    curr_date_format = curr_date.strftime('%Y-%m-%d')
                    data.setdefault(curr_date_format, [])
                    for row in day.find_all('tr')[1:]:
                        data[curr_date_format].append(
                            [field.text for field in row.find_all(['th', 'td'])]
                        )

            monday += timedelta(days=7)

        return data

    def _get_query_params(self) -> str:
        base_schedule_url = settings.SCHEDULE_URL
        base_schedule_page_response = requests.get(base_schedule_url)
        soup = bs4.BeautifulSoup(base_schedule_page_response.content, 'lxml')

        date_select = soup.find('option', selected=True)
        institute_select = soup.find('option', string=self.institute.name)

        if date_select is None or institute_select is None:
            raise TagNotFound

        pers = date_select.get('value')
        facs = institute_select.get('value')

        return pers, facs, self.course

    def _get_group_url(self, pers: str | int, facs: str | int, course: str | int):
        base_schedule_url = settings.SCHEDULE_URL
        group = self.get_prepared_group()

        params = {
            'facs': facs,
            'courses': course,
            'mode': 1,
            'pers': pers,
        }
        r = requests.get(base_schedule_url, params=params)
        soup = bs4.BeautifulSoup(r.content, 'lxml')
        a_tag = soup.find(
            'a',
            string=re.compile(fr'\s*?{group}\s*?'),
            href=lambda url: url and url.startswith('schedule.php'),
        )

        if a_tag is None:
            raise TagNotFound

        group_schedule_url = os.path.join(base_schedule_url, a_tag.get('href'))

        return group_schedule_url

    def get_schedule(self) -> dict[int, list[str]] | None:
        if not all([self.course, self.institute, self.group]):
            return None

        schedule_data = cache.get(f'schedule_of_group_{self.group}')
        if not schedule_data:
            try:
                perc, facs, course = self._get_query_params()
                group_url = self._get_group_url(perc, facs, self.course)

            except TagNotFound:
                return None

            schedule_data = self._get_schedule_data(group_url)
            cache.set(f'schedule_of_group_{self.group}', schedule_data, settings.SCHEDULE_CACHE_TIME)

        return schedule_data

    def get_prepared_group(self, spec_symbols: str = None) -> str:
        if not spec_symbols:
            spec_symbols = '()'

        group = self.group
        for sym in spec_symbols:
            pattern = fr'\{sym}'
            group = re.sub(pattern, fr'\{sym}', group)

        return group
