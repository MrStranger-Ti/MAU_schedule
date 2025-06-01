import re

from datetime import date, datetime


def convert_to_iso_8601(date_string: str) -> str:
    """
    Конвертирует дату формата DD.MM.YYYY в формат YYYY-MM-DD.
    """
    return datetime.strptime(date_string, "%d.%m.%Y").strftime("%Y-%m-%d")


class PeriodManager:
    """
    Класс для управления периодом расписания.

    Периодом считается строка в формате DD.MM.YYYY-DD.MM.YYYY.
    Первая часть (start) - понедельник,
    Вторая часть (end) - воскресенье.

    Attributes:
        period (str): Период в формате DD.MM.YYYY-DD.MM.YYYY
    """

    def __init__(self, period: str | None = None):
        self.period: str = period
        if not period or not self.validate(period):
            self.period = self.__get_current_period()

    @staticmethod
    def validate(period: str) -> bool:
        """
        Валидация формата переданного периода.

        Если валидация не прошла, то будет установлен текущий период.
        """
        date_regex = r"[0-3][0-9]\.[01][0-9]\.\d{4}"
        return bool(re.fullmatch(rf"{date_regex}-{date_regex}", period))

    @staticmethod
    def __get_current_period() -> str:
        """
        Получение текущего периода.

        Текущим периодом будет являться промежуток времени от
        понедельника до воскресенья текущей недели.
        """
        current_week = date.today().isocalendar()
        monday = date.fromisocalendar(current_week[0], current_week[1], 1)
        sunday = date.fromisocalendar(current_week[0], current_week[1], 7)
        return monday.strftime("%d.%m.%Y") + "-" + sunday.strftime("%d.%m.%Y")

    def _get_limit(self, limit: int) -> str:
        """
        Получение первого или последнего дня периода.
        """
        if limit not in range(2):
            raise ValueError("Limit must be 0 or 1.")

        limit = self.period.split("-")[limit]
        return convert_to_iso_8601(limit)

    @property
    def start(self) -> str:
        """
        Первый день периода.
        """
        return self._get_limit(0)

    @property
    def end(self) -> str:
        """
        Последний день периода.
        """
        return self._get_limit(1)
