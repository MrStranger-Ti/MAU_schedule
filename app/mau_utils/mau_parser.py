from django.conf import settings
from django.core.cache import cache

from mau_auth.exceptions import TagNotFound
from django.conf import settings
from mau_utils.mau_requests import get_query_params, get_group_url, get_schedule_data, get_teachers_urls


class MauScheduleParser:
    def __init__(self, user: settings.AUTH_USER_MODEL):
        self.course = str(user.course)
        self.institute = user.institute
        self.group = user.group
        self.schedule_url = settings.SCHEDULE_URL

    def get_group_schedule(self, page: int = 1) -> dict[int, list[str]] | None:
        if not all([self.course, self.institute, self.group]):
            return None

        group_url = cache.get(f'group_schedule_url_{self.group}')
        if not group_url:
            try:
                perc, facs = get_query_params(self.institute.name)
                group_url = get_group_url(self.group, perc, facs, self.course)
            except TagNotFound:
                return None

            cache.set(
                f'group_schedule_url_{self.group}',
                group_url,
                settings.SCHEDULE_CACHE_TIME,
            )

        return get_schedule_data(group_url, week_step=page - 1)

