from django.conf import settings
from django.core.cache import cache

from mau_auth.exceptions import TagNotFound
from mau_utils.mau_requests import get_query_params, get_group_url, get_schedule_data


class MauScheduleParser:
    def __init__(self, user: settings.AUTH_USER_MODEL):
        self.course = str(user.course)
        self.institute = user.institute
        self.group = user.group
        self.schedule_url = settings.SCHEDULE_URL

    def get_schedule(self) -> dict[int, list[str]] | None:
        if not all([self.course, self.institute, self.group]):
            return None

        schedule_data = cache.get(f'schedule_of_group_{self.group}')
        if not schedule_data:
            try:
                perc, facs = get_query_params(self.institute.name)
                group_url = get_group_url(self.group, perc, facs, self.course)

            except TagNotFound:
                return None

            schedule_data = get_schedule_data(group_url)
            cache.set(f'schedule_of_group_{self.group}', schedule_data, settings.SCHEDULE_CACHE_TIME)

        return schedule_data
