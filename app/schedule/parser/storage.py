from typing import Dict, Any

from django.conf import settings
from django.core.cache import cache


class ParserStorage:
    def __init__(self, cache_key: str):
        self.cache_key: str = cache_key
        self.__data: Dict[str, Any] = {}

        self.load_data()

    def __getitem__(self, item):
        return self.__data[item]

    def __setitem__(self, key, value):
        self.__data[key] = value

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        self.__data = value

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def save_db(self) -> None:
        cache.add(
            self.cache_key,
            self.data,
            settings.SCHEDULE_CACHE_TIME,
        )

    def load_data(self):
        data = cache.get(self.cache_key)
        if data and isinstance(data, dict):
            self.data = data
