from schedule.parser.extensions import PeriodManager


class ScheduleParserMixin:
    """
    Миксин, который добавляет необходимый функционал для парсинга расписания.

    Attributes:
        user (settings.AUTH_USER_MODEL): экземпляр модели пользователя
        period_manager (PeriodManger): менеджер периодов
    """

    def __init__(self, *args, period: str = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.period_manager = PeriodManager(period=period)
        self.params.update(
            {
                "perstart": self.period_manager.start(),
                "perend": self.period_manager.end(),
            },
        )
