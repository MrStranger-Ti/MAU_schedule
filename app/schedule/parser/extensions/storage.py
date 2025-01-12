from typing import Any

from django.core.cache import cache


class CacheStorage:
    """
    Объект хранилища кэша.

    Основная задача этого класса хранить, получать и устанавливать кэш.

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
        self.__data[self.key] = value
        cache.set(self.key, value)


# class StorageManager:
#     """
#     Менеджер, который управляет получением кэша и хранит ключи кэша.
#
#     Основная задача этого класса управлять хранилищем кэша
#     с помощью коротких названий для ключей кэша.
#
#     Attributes:
#         cache_keys: ключи кэша с их короткими названиями
#         __cache_storage: объект хранилища кэша
#     """
#
#     def __init__(self, cache_keys: dict[str, str]):
#         self.cache_keys = cache_keys
#         self.__cache_storage = CacheStorage(list(cache_keys.values()))
#
#     def get(self, key_name: str) -> dict[str, Any] | None:
#         """
#         Получение данных по имени ключа кэша.
#         """
#         key = self.cache_keys.get(key_name)
#         return self.cache_storage.get(key)
#
#     def set(self, key_name: str, value: Any) -> None:
#         """
#         Установка данных по имени ключа кэша.
#         """
#         key = self.cache_keys.get(key_name)
#         self.cache_storage.set(key, value)
#
#     @property
#     def cache_storage(self):
#         """
#         Геттер для cache_storage.
#         """
#         return self.__cache_storage
