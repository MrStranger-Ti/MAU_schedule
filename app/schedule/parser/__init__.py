__all__ = [
    "get_group_schedule",
    "get_teacher_links",
    "get_teacher_schedule",
]


from datetime import date

from django.conf import settings

from mau_auth.models import MauUser
from schedule.parser.objects import (
    GroupParamsParser,
    GroupUrlParser,
    GroupScheduleParser,
    TeacherKeysParser,
    TeacherScheduleParser,
)


def get_group_schedule(user: settings.AUTH_USER_MODEL) -> dict[date, list[list[str]]]:
    group_params = GroupParamsParser(user=user, url=settings.SCHEDULE_URL).get_data()
    group_url = GroupUrlParser(user=user, url=settings.SCHEDULE_URL).get_data()
    schedule = GroupScheduleParser(
        user=user,
        url=group_url,
        params=group_params,
    ).get_data()
    return schedule


def get_teacher_links(user: settings.AUTH_USER_MODEL) -> dict[str, str]:
    teacher_links = TeacherKeysParser(
        user=user,
        url=settings.SCHEDULE_URL,
    ).get_data()
    return teacher_links


def get_teacher_schedule(user: settings.AUTH_USER_MODEL) -> dict[date, list[list[str]]]:
    teacher_schedule = TeacherScheduleParser(
        user=user,
        url=settings.SCHEDULE_URL,
    ).get_data()
    return teacher_schedule
