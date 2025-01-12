from schedule.parser.extensions import PeriodManager


class ScheduleParserMixin:
    """
    Миксин, который добавляет необходимый функционал для парсинга расписания.

    Attributes:
        period_manager (PeriodManger): менеджер периодов
    """

    def __init__(self, period: str = None):
        self.period_manager = PeriodManager(period=period)
        self.params.update(
            {
                "perstart": self.period_manager.start(),
                "perend": self.period_manager.end(),
            },
        )
