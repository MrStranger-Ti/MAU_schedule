from datetime import date, datetime


def convert_to_iso_8601(date_string: str) -> str:
    """
    Конвертирует дату формата DD.MM.YYYY в формат YYYY-MM-DD.
    """
    return datetime.strptime(date_string, "%d.%m.%Y").strftime("%Y-%m-%d")


class PeriodManager:
    """
    Класс для управления периодом расписания.

    Attributes:
        period (str | None): Период в формате DD.MM.YYYY-DD.MM.YYYY
    """

    def __init__(self, period: str | None = None):
        self.period = period or self.get_current_period()

    @staticmethod
    def get_current_period() -> str:
        """
        Возвращает текущий период.
        """
        current_week = date.today().isocalendar()
        monday = date.fromisocalendar(current_week[0], current_week[1], 1)
        sunday = date.fromisocalendar(current_week[0], current_week[1], 7)
        return monday.strftime("%d.%m.%Y") + "-" + sunday.strftime("%d.%m.%Y")

    def get_limit(self, limit: int) -> str:
        """
        Получение первого или последнего дня периода.
        """
        if self.period is None:
            raise ValueError("Limit must be 0 or 1.")

        return self.period.split("-")[limit]

    @property
    def start(self) -> str:
        """
        Первый день периода.
        """
        raw_start = self.get_limit(0)
        return self.convert_to_iso_8601(raw_start)

    @property
    def end(self) -> str:
        """
        Последний день периода.
        """
        raw_end = self.get_limit(1)
        return self.convert_to_iso_8601(raw_end)
