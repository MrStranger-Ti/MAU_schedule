import re
import urllib
from datetime import date, timedelta

import bs4
import requests

from django.core.cache import cache

from mau_auth.exceptions import TagNotFound
from django.conf import settings

mau_url = settings.SCHEDULE_URL


def get_prepared_group(group: str, spec_symbols: str = None) -> str:
    if not spec_symbols:
        spec_symbols = '()'

    for sym in spec_symbols:
        pattern = fr'\{sym}'
        group = re.sub(pattern, fr'\{sym}', group)

    return group


def get_query_params(institute_name: str) -> tuple[str, str]:
    response = requests.get(mau_url)
    soup = bs4.BeautifulSoup(response.content, 'lxml')

    date_select = soup.find('option', selected=True)
    institute_select = soup.find('option', string=institute_name)

    if date_select is None or institute_select is None:
        raise TagNotFound

    pers = date_select.get('value')
    facs = institute_select.get('value')

    return pers, facs


def get_group_url(group: str, pers: str, facs: str, course: str) -> str:
    group = get_prepared_group(group)

    params = {
        'facs': facs,
        'courses': course,
        'mode': 1,
        'pers': pers,
    }
    response = requests.get(mau_url, params=params)
    soup = bs4.BeautifulSoup(response.content, 'lxml')
    a_tag = soup.find(
        'a',
        string=re.compile(fr'\s*?{group}\s*?'),
        href=lambda url: url and url.startswith('schedule.php'),
    )

    if a_tag is None:
        raise TagNotFound

    group_schedule_url = urllib.parse.urljoin(mau_url, a_tag.get('href'))

    return group_schedule_url


def get_schedule_data(url: str) -> dict[int, list[str]]:
    current_calendar_date = date.today().isocalendar()
    monday = date.fromisocalendar(current_calendar_date[0], current_calendar_date[1], 1)

    data = {}
    for _ in range(4):
        sunday = monday + timedelta(days=6)
        params = {
            'perstart': monday.isoformat(),
            'perend': sunday.isoformat(),
        }

        response = requests.get(url, params=params)
        soup = bs4.BeautifulSoup(response.content, 'lxml')

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


def get_institutes() -> set[str]:
    """Находит и возвращает все имена институтов."""

    response = requests.get(mau_url)
    soup = bs4.BeautifulSoup(response.content, 'lxml')
    select = soup.find('select', attrs={'name': 'facs'})
    options = select.find_all('option', value=lambda val: val != '0')
    institutes = {
        option.text.strip()
        for option in options
    }

    return institutes


def get_groups(facs: str, course: str) -> set[str]:
    params = {
        'facs': facs,
        'course': course,
        'mode': 1,
    }
    response = requests.get(mau_url, params=params)
    soup = bs4.BeautifulSoup(response.content, 'lxml')

    tbody = soup.find('tbody')
    links = tbody.find_all('a', _class='btn btn-default')
    groups = {
        link.text
        for link in links
    }
    return groups