from typing import Dict, Any

from django.conf import settings
from django.core.cache import cache


class ParserStorage:
    """
    Объект хранилища данных для парсинга.

    Основная задача этого класса подгружать, сохранять и возвращать
    данные из базы данных для кэша.
    """

    def __init__(self, keys: list[str]):
        """
        Установка всех ключей в __data.

        Значения изначально равны None.
        """
        self.__data = {}
        for key in keys:
            self.__data.setdefault(key, None)

    def get(self, key):
        """
        Получение данных по ключу кэша.

        Если в __data нет данных, то будет выполнен запрос к базе по ключу кэша.
        Подгруженные данные сохранятся на объекте.
        """
        data = self.__data.get(key)
        if not data:
            data = cache.get(key)
            self.__data[key]

        return data

    def set(self, key, value):
        """
        Установка данных по ключу кэша.
        """
        pass

    def save(self):
        """
        Сохранение всех данных по их ключам.
        """
