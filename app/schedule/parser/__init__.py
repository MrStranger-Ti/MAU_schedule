__all__ = [
    "get_group_schedule",
    "get_teacher_links",
    "get_teacher_schedule",
    "Parser",
    "CacheParser",
    "ScheduleParser",
    "ParserResponse",
]

from django.conf import settings

from schedule.parser.ext import PeriodManager, ParserResponse
from schedule.parser.base import Parser, CacheParser, ScheduleParser
from schedule.parser.objects import (
    GroupParamsParser,
    GroupKeyParser,
    GroupScheduleParser,
    TeacherKeysParser,
    TeacherScheduleParser,
)


def get_group_schedule(
    institute: str,
    course: str | int,
    group: str,
    period: str | None = None,
) -> ParserResponse:
    """
    Функция для получения расписания группы.

    :param institute: институт
    :param course: курс
    :param group: группа
    :param period: период расписания в формате DD.MM.YYYY-DD.MM.YYYY
    """
    group_url = settings.SCHEDULE_URL + "schedule.php"
    parsing_data = {
        "institute": institute,
        "course": course,
        "group": group,
    }

    response = GroupParamsParser(
        url=settings.SCHEDULE_URL,
        unique_key=group,
        period=period,
        extra_data=parsing_data,
    ).get_data()
    response = GroupKeyParser(
        url=settings.SCHEDULE_URL,
        unique_key=group,
        params=response.data,
        extra_data=parsing_data,
    ).get_data()
    response = GroupScheduleParser(
        url=group_url,
        unique_key=group,
        params={"key": response.data},
        period=period,
        extra_data=parsing_data,
    ).get_data()
    return response


def get_teacher_links(name: str) -> ParserResponse:
    """
    Функция для получения ссылок преподавателей.

    :param name: имя преподавателя
    """
    response = TeacherKeysParser(
        url=settings.SCHEDULE_URL,
        unique_key=name,
        extra_data={"name": name},
    ).get_data()
    return response


def get_teacher_schedule(teacher_key: str, period: str | None = None) -> ParserResponse:
    """
    Функция для получения расписания преподавателя.

    :param teacher_key: ключ преподавателя.
    :param period: период расписания в формате DD.MM.YYYY-DD.MM.YYYY
    """
    teacher_url = settings.SCHEDULE_URL + "schedule2.php"
    response = TeacherScheduleParser(
        url=teacher_url,
        unique_key=teacher_key,
        params={"key": teacher_key},
        period=period,
    ).get_data()
    return response
