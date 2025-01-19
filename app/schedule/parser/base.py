import abc
from typing import Any, Sequence

import bs4
import requests
from django.core.cache import cache
from fake_useragent import UserAgent

from django.conf import settings

from schedule.parser.ext import PeriodManager
from schedule.parser.ext.response import ParserResponse


class WebScraper:
    """
    Объект для получения response и soup.

    Attributes:
        url (str): путь для запроса, должен быть установлен при инициализации или на дочернем классе
        parser (str): парсер для bs4, по умолчанию lxml
        _params (dict): query параметры для запроса
        user_agent_manager (UserAgent): менеджер для предоставления случайного значения User-Agent
    """

    url: str | None = None

    def __init__(
        self,
        url: str | None = None,
        parser: str = "lxml",
        params: dict[str, str] | None = None,
    ):
        self.url: str = url or self.url
        if self.url is None:
            raise AttributeError("Class attr 'url' must be set.")

        self.parser: str = parser
        self._params: dict[str, str] = params or {}
        self.user_agent_manager: UserAgent = UserAgent()

    @property
    def params(self):
        return self._change_params(self._params)

    def _change_params(self, params: dict[str, str]) -> dict[str, str]:
        """
        Метод для кастомизации параметров запроса.

        Может быть переопределен в дочерних классах.
        """
        return params

    def get_soup(self, response: requests.Response) -> bs4.BeautifulSoup:
        """
        Получение объекта BeautifulSoup.
        """
        return bs4.BeautifulSoup(response.content, self.parser)

    def get_response(self, **kwargs) -> requests.Response | None:
        """
        Получение ответа от сервера.
        """
        kwargs.update(
            {
                "headers": {"User-Agent": self.user_agent_manager.random},
                "params": self.params,
                "timeout": settings.REQUESTS_TIMEOUT,
            },
        )
        try:
            response = requests.get(self.url, **kwargs)
        except requests.exceptions.Timeout:
            return None

        return response


class Parser(WebScraper, abc.ABC):
    """
    Базовый парсер.

    Attributes:
        extra_data (dict[str, Any]): дополнительные данные для парсинга
        required_extra_data (tuple[str, ...] | None): названия атрибутов из extra_data
    """

    required_extra_data: Sequence[str] | None = None

    def __init__(self, extra_data: dict[str, Any] | None = None, **kwargs):
        super().__init__(**kwargs)
        self.extra_data: dict[str, Any] = extra_data or {}

    def _validate_extra_data(self, data: dict[str, Any]) -> bool:
        """
        Валидатор для extra_data.

        Проверяется что,
        extra_data имеет корректные названия, такие как в extra_data_names,
        значения extra_data не None.
        """
        extra_data_names = self.extra_data.keys()
        valid_extra_data = [
            name in extra_data_names for name in self.required_extra_data or tuple()
        ]
        extra_data_values_is_true = [value is not None for value in data.values()]
        return all(valid_extra_data + extra_data_values_is_true)

    def get_data(self) -> ParserResponse:
        """
        Получение ответа от сервера и парсинг данных.

        Будет запущена валидация дополнительных данных для парсинга.
        Возвращает объект ответа (ParserResponse).
        """
        if not self._validate_extra_data(self.extra_data):
            raise ValueError("Invalid extra_data.")

        response = self.get_response()
        if not response or response.status_code != 200:
            return ParserResponse(
                response=response,
                error=f"Invalid server response.",
            )

        soup = self.get_soup(response)
        try:
            data = self._parse_data(soup)
        except (AttributeError, TypeError):
            return ParserResponse(
                response=response,
                error="Data didn't get.",
            )

        return ParserResponse(response=response, data=data)

    @abc.abstractmethod
    def _parse_data(self, soup: bs4.BeautifulSoup) -> Any:
        """
        Парсит и возвращает найденную информацию.
        """
        pass


class CacheParser(Parser):
    """
    Базовый парсер, который кроме парсинга данных
    получает данные из кэша и сохраняет данные в кэш.

    Основное отличие CacheParser`а от обычного в том, что он оборачивает метод get_data
    для получения данных из кэша или установки кэша после получения данных из get_data.

    Attributes:
        base_key (str): базовый ключ, является частью итогового ключа кэша
        unique_cache_key (str): уникальный ключ кэша, который является частью итогового ключа кэша
    """

    base_key: str | None = None

    def __init__(self, unique_key: str | None = None, **kwargs):
        super().__init__(**kwargs)
        if self.base_key is None:
            raise AttributeError("Class attr 'base_key' must be set.")

        self.unique_cache_key = unique_key or ""

    def get_cache_key(self):
        """
        Получение ключа кэша.
        """
        return self.base_key + "_" + self.unique_cache_key

    def get_data(self) -> ParserResponse:
        """
        Основной метод для получения данных.

        Сначала будет попытка получить данных из кэша.
        Если данных нет, то запускается процесс парсинга.
        Полученные данных сохраняются в кэш.
        """
        cache_key = self.get_cache_key()

        data = cache.get(cache_key)
        if data is None:
            parser_response = super().get_data()
            if parser_response.success:
                cache.set(cache_key, parser_response.data)

            return parser_response

        return ParserResponse(data=data)

    @abc.abstractmethod
    def _parse_data(self, soup: bs4.BeautifulSoup) -> Any:
        pass


class ScheduleParser(CacheParser):
    """
    Базовый парсер для расписания.

    Подгружает объект для управления периодом расписания,
    а также добавляет период в ключ кэша и параметры периода.

    Attributes:
        period_manager (PeriodManger): менеджер периодов
    """

    def __init__(self, period: str = None, **kwargs: Any):
        super().__init__(**kwargs)
        self.period_manager = PeriodManager(period=period)

    def get_cache_key(self):
        return super().get_cache_key() + f"_period_{self.period_manager.period}"

    def _change_params(self, params: dict[str, str]) -> dict[str, str]:
        params.update(
            {
                "perstart": self.period_manager.start,
                "perend": self.period_manager.end,
            }
        )
        return params

    @abc.abstractmethod
    def _parse_data(self, soup: bs4.BeautifulSoup) -> Any:
        pass
