import re
import urllib.parse

import bs4
import requests

from datetime import date, timedelta, datetime

from fake_useragent import UserAgent

from mau_auth.exceptions import TagNotFound
from django.conf import settings

ua = UserAgent()


def get_prepared_group(group: str, spec_symbols: str = None) -> str:
    if not spec_symbols:
        spec_symbols = '()'

    for sym in spec_symbols:
        pattern = fr'\{sym}'
        group = re.sub(pattern, fr'\{sym}', group)

    return group


# def filter_by_current_date(date_range: str) -> bool:
#     now = datetime.now()
#
#     clean_date_range = re.search(r'\d{2}\.\d{2}\.\d{4}-\d{2}\.\d{2}\.\d{4}', date_range).group()
#     first_date, last_date = map(
#         lambda x: datetime.strptime(x, '%d.%m.%Y'),
#         clean_date_range.split('-'),
#     )
#     return first_date <= now <= last_date


def get_query_params(institute_name: str) -> tuple[str, str]:
    response = requests.get(settings.SCHEDULE_URL, headers={'User-Agent': ua.random})
    soup = bs4.BeautifulSoup(response.content, 'lxml')

    date_option = soup.select_one('select[name=pers]').find(
        'option',
        value=lambda x: int(x) > 0,
    )
    institute_option = soup.select_one('select[name=facs]').find(
        'option',
        string=institute_name,
    )

    if date_option is None or institute_option is None:
        raise TagNotFound

    pers = date_option.attrs.get('value')
    facs = institute_option.attrs.get('value')

    return pers, facs


def get_group_url(group: str, pers: str, facs: str, course: str) -> str:
    group = get_prepared_group(group)

    params = {
        'mode': 1,
        'pers': pers,
        'facs': facs,
        'courses': course,
    }
    response = requests.get(settings.SCHEDULE_URL, params=params, headers={'User-Agent': ua.random})
    soup = bs4.BeautifulSoup(response.content, 'lxml')
    a_tag = soup.find(
        'a',
        string=lambda text: re.fullmatch(fr'\s*{group}\s*', text),
        href=lambda url: url and url.startswith('schedule.php'),
    )

    if a_tag is None:
        raise TagNotFound

    return urllib.parse.urljoin(settings.SCHEDULE_URL, a_tag.get('href'))


def parse_group_schedule(soup: bs4.BeautifulSoup, curr_week_monday: date) -> dict[int, list[str]]:
    week_schedule = {}
    for weekday_num, day in enumerate(soup.find_all('table')):
        title = day.find('th')
        if title and 'Воскресенье' not in title.text:
            curr_date = curr_week_monday + timedelta(days=weekday_num)
            week_schedule.setdefault(curr_date, [])
            for row in day.find_all('tr')[1:]:
                week_schedule[curr_date].append(
                    [field.text for field in row.find_all(['th', 'td'])]
                )

    return week_schedule


def parse_teacher_schedule(soup: bs4.BeautifulSoup, curr_week_monday: date) -> dict[int, list[str]]:
    week_schedule = {}
    trs = soup.select('tr')

    weekday_num = 0
    for tr in trs:
        tr_class = tr.get('class')
        if tr_class and tr_class[0] == 'title':
            curr_date = curr_week_monday + timedelta(days=weekday_num)
            week_schedule.setdefault(curr_date, [])

            weekday_num += 1

        else:
            week_schedule[curr_date].append(
                [field.text for field in tr.find_all('td')]
            )

    return week_schedule


def get_schedule_data(url: str, teacher_schedule: bool = False, week_step: int = 0) -> dict[dict: list]:
    schedule_date = date.today()
    if week_step:
        schedule_date += timedelta(weeks=week_step)

    current_calendar_date = schedule_date.isocalendar()
    monday = date.fromisocalendar(current_calendar_date[0], current_calendar_date[1], 1)

    sunday = monday + timedelta(days=6)
    params = {
        'perstart': monday.isoformat(),
        'perend': sunday.isoformat(),
    }

    response = requests.get(url, params=params, headers={'User-Agent': ua.random})
    soup = bs4.BeautifulSoup(response.content, 'lxml')

    if teacher_schedule:
        schedule_data = parse_teacher_schedule(soup, monday)
    else:
        schedule_data = parse_group_schedule(soup, monday)

    return schedule_data


# def get_institutes() -> set[str]:
#     """Находит и возвращает все имена институтов."""
#
#     response = requests.get(settings.SCHEDULE_URL, headers={'User-Agent': ua.random})
#     soup = bs4.BeautifulSoup(response.content, 'lxml')
#     select = soup.find('select', attrs={'name': 'facs'})
#     options = select.find_all('option', value=lambda val: val != '0')
#     institutes = {
#         option.text.strip()
#         for option in options
#     }
#
#     return institutes
#
#
# def get_groups(facs: str, course: str) -> set[str]:
#     params = {
#         'facs': facs,
#         'course': course,
#         'mode': 1,
#     }
#     response = requests.get(settings.SCHEDULE_URL, params=params, headers={'User-Agent': ua.random})
#     soup = bs4.BeautifulSoup(response.content, 'lxml')
#
#     tbody = soup.find('tbody')
#     links = tbody.find_all('a', _class='btn btn-default')
#     groups = {
#         link.text
#         for link in links
#     }
#     return groups


def get_teachers_urls(query: str) -> dict[str: str] | None:
    params = {'mode2': '1', 'pers2': '0', 'sstring': query.encode('cp1251')}
    response = requests.get(settings.SCHEDULE_URL, params=params, headers={'User-Agent': ua.random})
    soup = bs4.BeautifulSoup(response.content, 'lxml')
    links = soup.select('td b a')

    if not links:
        return None

    teacher_keys = {}
    for link in links:
        query_params = urllib.parse.parse_qs(link.get('href'))
        key = query_params.get('schedule2.php?key')[0]
        teacher_keys[link.text] = key

    return teacher_keys
