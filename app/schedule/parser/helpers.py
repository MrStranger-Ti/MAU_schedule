import re
import urllib
from datetime import datetime


def clean_date_period(date_period: str) -> str:
    return re.search(r"\d{2}\.\d{2}\.\d{4}-\d{2}\.\d{2}\.\d{4}", date_period).group()


def join_url(first_url: str, second_url: str) -> str:
    return urllib.parse.urljoin(first_url, second_url)


def convert_to_iso_8601(date_string: str) -> str:
    return datetime.strptime(date_string, "%d.%m.%Y").strftime("%Y-%m-%d")


def check_period_for_current_date(date_period: str) -> bool:
    now = datetime.now()

    first_date, last_date = map(
        lambda x: datetime.strptime(x, "%d.%m.%Y"),
        date_period.split("-"),
    )
    return first_date <= now <= last_date
