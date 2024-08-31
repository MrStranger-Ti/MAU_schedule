from django.conf import settings

from mau_auth.exceptions import TagNotFound
from django.conf import settings
from mau_utils.mau_requests import get_query_params, get_group_url, get_schedule_data, get_teachers_urls


class MauScheduleParser:
    def __init__(self, user: settings.AUTH_USER_MODEL):
        self.course = str(user.course)
        self.institute = user.institute
        self.group = user.group
        self.schedule_url = settings.SCHEDULE_URL

    def get_group_schedule(self) -> dict[int, list[str]] | None:
        if not all([self.course, self.institute, self.group]):
            return None

        try:
            perc, facs = get_query_params(self.institute.name)
            group_url = get_group_url(self.group, perc, facs, self.course)

        except TagNotFound:
            return None

        schedule_data = get_schedule_data(group_url)
        return schedule_data

