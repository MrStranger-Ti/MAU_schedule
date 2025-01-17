import abc
from typing import Any, Sequence

import bs4
import requests
from fake_useragent import UserAgent

from django.conf import settings

from schedule.parser.ext import CacheStorage, PeriodManager
from schedule.parser.ext.response import ParserResponse


class WebScraper:
    """
    Объект для получения response и soup.

    Attributes:
        url (str): путь для запроса
        parser (str): парсер для bs4, по умолчанию lxml
        params (dict): query параметры для запроса
        user_agent_manager (UserAgent): менеджер для предоставления случайного значения User-Agent
    """

    def __init__(
        self,
        url: str,
        parser: str = "lxml",
        params: dict[str, str] | None = None,
    ):
        self.url: str = url
        self.parser: str = parser
        self.params: dict[str, str] = self._change_params(params or {})
        self.user_agent_manager: UserAgent = UserAgent()

    def _change_params(self, params: dict[str, str]) -> dict[str, str]:
        """
        Метод для кастомизации параметров запроса.
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
    Абстрактный парсер.

    В этот объект подмешивается хранилище кэша (CacheStorage).
    Данные parsing_data устанавливаются в атрибуты при инициализации.

    Attributes:
        extra_data (dict[str, Any]): дополнительные данные для парсинга
        required_extra_data (tuple[str, ...] | None): названия атрибутов из parsing_data
    """

    required_extra_data: Sequence[str] | None = None

    def __init__(self, *args, extra_data: dict[str, Any] | None = None, **kwargs):
        self.extra_data: dict[str, Any] = extra_data or {}
        super().__init__(*args, **kwargs)

    def _validate_extra_data(self, data: dict[str, Any]) -> bool:
        """
        Валидатор для extra_data.

        Проверяется что,
        parsing_data имеет корректные названия, такие как в extra_data_names,
        значения parsing_data не None.
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
                error=f"Invalid MAU server response.",
            )

        soup = self.get_soup(response)
        try:
            data = self._parse_data(soup)
        except (AttributeError, TypeError):
            return ParserResponse(
                response=response,
                error="Data didn't get. Please check your profile information.",
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
    Базовый парсер с встроенным хранилищем кэша.

    Attributes:
        base_key (str): базовый ключ, является частью итогового ключа кэша
        unique_cache_key (str): уникальный ключ кэша, который является частью итогового ключа кэша
        cache_storage (CacheStorage): объект хранилища кэша
    """

    base_key: str | None = None

    def __init__(self, url: str, unique_key: str, **kwargs):
        super().__init__(url, **kwargs)
        if self.base_key is None:
            raise AttributeError("Attr 'base_key' must be set.")

        self.unique_cache_key = unique_key
        self.cache_storage: CacheStorage = CacheStorage(self.get_cache_key())

    def get_cache_key(self):
        return self.base_key + "_" + self.unique_cache_key

    def get_data(self) -> ParserResponse:
        """
        Основной метод для получения данных.

        Сначала будет попытка получить данных из кэша.
        Если данных нет, то запускается процесс парсинга.
        Полученные данных сохраняются в кэш.
        """
        data = self.cache_storage.get()
        if data is None:
            parser_response = super().get_data()
            if parser_response.success:
                self.cache_storage.set(parser_response.data)

            return parser_response

        return ParserResponse(data=data)

    @abc.abstractmethod
    def _parse_data(self, soup: bs4.BeautifulSoup) -> Any:
        pass


class ScheduleParser(CacheParser):
    """
    Базовый парсер для расписания.

    Подгружает объект для управления периодом расписания.

    Attributes:
        period_manager (PeriodManger): менеджер периодов
    """

    def __init__(self, *args: Any, period: str = None, **kwargs: Any):
        self.period_manager = PeriodManager(period=period)
        super().__init__(*args, **kwargs)

    def get_cache_key(self):
        return super().get_cache_key() + f"_period_{self.period_manager.period}"

    @abc.abstractmethod
    def _parse_data(self, soup: bs4.BeautifulSoup) -> Any:
        pass
