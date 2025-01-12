import abc
from typing import Any

import bs4
import requests
from fake_useragent import UserAgent

from django.conf import settings

from schedule.parser.extensions import CacheStorage, PeriodManager
from schedule.parser.mixins import ScheduleParserMixin


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
        self.params = params
        self.user_agent_manager: UserAgent = UserAgent()

    def get_soup(self, response: requests.Response) -> bs4.BeautifulSoup:
        """
        Получение объекта BeautifulSoup.
        """
        return bs4.BeautifulSoup(response.content, self.parser)

    def get_response(self, **kwargs: Any) -> requests.Response | None:
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


class MauParser(abc.ABC, WebScraper):
    """
    Базовый парсер.

    В этот объект встроено хранилище кэша (CacheStorage).

    Attributes:
        user (settings.AUTH_USER_MODEL): объект пользователя
        parsing_data (dict): дополнительные данные для парсинга
        cache_storage (CacheStorage): объект хранилища кэша
    """

    def __init__(
        self,
        user: settings.AUTH_USER_MODEL,
        *args,
        parsing_data: dict | None = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.user = user
        self.parsing_data = parsing_data
        self.cache_storage = CacheStorage(self.get_cache_key())

    def get_data(self) -> Any:
        """
        Основной метод для получения данных.

        Сначала будет попытка получить данных из кэша.
        Если данных нет, то запускает процесс парсинга.
        Полученные данных сохраняются в кэш.
        """
        data = self.cache_storage.get()
        if data is None:
            data = self._get_data()
            if data:
                self.cache_storage.set(data)

        return data

    def _get_data(self) -> Any:
        """
        Получение ответа от сервера и парсинг данных.
        """
        response = self.get_response()
        if response and response.status_code == 200:
            soup = self.get_soup(response)
            try:
                data = self._parse_data(soup)
            except AttributeError:
                return None

            return data

    @abc.abstractmethod
    def get_cache_key(self) -> str:
        """
        Возвращает ключ кэша.
        """
        pass

    @abc.abstractmethod
    def _parse_data(self, soup: bs4.BeautifulSoup):
        """
        Парсит и возвращает найденную информацию.
        """
        pass


class MauScheduleParser(abc.ABC, MauParser):
    """

    Attributes:
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

    @abc.abstractmethod
    def get_cache_key(self) -> str:
        pass

    @abc.abstractmethod
    def _parse_data(self, soup: bs4.BeautifulSoup):
        pass
