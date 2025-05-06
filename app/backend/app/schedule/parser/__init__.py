__all__ = [
    "get_group_schedule",
    "get_teachers_keys",
    "get_teacher_schedule",
    "get_periods",
    "Parser",
    "CacheParser",
    "ScheduleParser",
    "ParserResponse",
    "PeriodManager",
    "GroupParamsParser",
    "GroupKeyParser",
    "GroupScheduleParser",
    "TeacherKeysParser",
    "TeacherScheduleParser",
    "PeriodsParser",
]

from schedule.parser.ext import PeriodManager, ParserResponse
from schedule.parser.base import Parser, CacheParser, ScheduleParser
from schedule.parser.objects import (
    GroupParamsParser,
    GroupKeyParser,
    GroupScheduleParser,
    TeacherKeysParser,
    TeacherScheduleParser,
    PeriodsParser,
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
    extra_data = {
        "institute": institute,
        "course": course,
        "group": group,
    }

    response = GroupParamsParser(
        unique_key=group,
        period=period,
        extra_data=extra_data,
    ).get_data()
    if not response.success:
        return response

    response = GroupKeyParser(
        unique_key=group,
        params=response.data,
        extra_data=extra_data,
    ).get_data()
    if not response.success:
        return response

    response = GroupScheduleParser(
        unique_key=group,
        params={"key": response.data},
        period=period,
        extra_data=extra_data,
    ).get_data()
    return response


def get_teachers_keys(name: str) -> ParserResponse:
    """
    Функция для получения ссылок преподавателей.

    :param name: имя преподавателя
    """
    response = TeacherKeysParser(unique_key=name, params={"sstring": name}).get_data()
    return response


def get_teacher_schedule(teacher_key: str, period: str | None = None) -> ParserResponse:
    """
    Функция для получения расписания преподавателя.

    :param teacher_key: ключ преподавателя.
    :param period: период расписания в формате DD.MM.YYYY-DD.MM.YYYY
    """
    response = TeacherScheduleParser(
        unique_key=teacher_key,
        params={"key": teacher_key},
        period=period,
    ).get_data()
    return response


def get_periods() -> ParserResponse:
    """
    Функция для получения списка всех периодов расписания.
    """
    response = PeriodsParser().get_data()
    return response
