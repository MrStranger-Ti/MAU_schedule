from typing import Any

from django.core.cache import cache


class CacheStorage:
    """
    Объект хранилища кэша.

    Основная задача этого класса хранить, получать и устанавливать кэш.
    Используется Django cache framework.

    Attributes:
        key (str): ключ кэша
        __data (Any | None): кэш
    """

    def __init__(self, key: str):
        self.key: str = key
        self.__data: Any | None = None

    def get(self) -> Any | None:
        """
        Получение данных по ключу.

        Если в __data нет данных, то будет выполнен запрос к базе по ключу.
        Подгруженный кэш сохранятся в __data.
        """
        if not self.__data:
            data = cache.get(self.key)
            self.__data = data

        return data

    def set(self, value) -> None:
        """
        Установка данных по ключу кэша.
        """
        self.__data = value
        cache.set(self.key, value)
