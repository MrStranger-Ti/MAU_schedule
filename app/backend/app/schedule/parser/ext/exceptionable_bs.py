import functools
from typing import Callable, Any

from bs4 import BeautifulSoup

from schedule.parser.exceptions import ParserError


def _raise_parse_error_instead_none(func: Callable) -> Callable:
    """
    Декоратор для методов BeautifulSoup.

    Если метод возвращает None, то возбуждается исключение ParserError.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        result = func(*args, **kwargs)
        if result is None:
            raise ParserError
        return result

    return wrapper


def _raise_parse_error_instead_none_class(
    cls: type[BeautifulSoup],
) -> type[BeautifulSoup]:
    """
    Декоратор класса для BeautifulSoup.

    Декорирует все методы поиска с помощью декоратора
    _raise_parse_error_instead_none, которые могут вернуть None.
    """

    methods_for_decorate = [
        "find",
        "find_all",
        "find_all_next",
        "find_all_previous",
        "find_next",
        "find_previous",
        "find_next_sibling",
        "find_previous_sibling",
        "find_parent",
        "select",
        "select_one",
    ]

    for attr in dir(cls):
        if attr in methods_for_decorate:
            method_for_decorate = getattr(cls, attr)
            decorated_method = _raise_parse_error_instead_none(method_for_decorate)
            setattr(cls, attr, decorated_method)

    return cls


ExceptionableBeautifulSoup = _raise_parse_error_instead_none_class(BeautifulSoup)
