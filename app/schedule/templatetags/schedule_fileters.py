from datetime import datetime

from django import template
from django.conf import settings

register = template.Library()


@register.filter
def get_weekday(value: datetime) -> str:
    weekday_number = value.weekday()
    return settings.WEEKDAYS_NAMES.get(weekday_number)
