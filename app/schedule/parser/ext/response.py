from typing import Any

from requests import Response


class ParserResponse:
    """
    Ответ от парсера.

    Содержит распарсенную информацию и дополнительные данных, которые получил парсер.

    Attributes:
        data (Any): распарсенные данные
        response (Response): объект ответа библиотеки requests
        success (bool): успешно ли парсеру удалось спарсить данные
        error (str | None): текст ошибки
    """

    def __init__(
        self,
        data: Any = None,
        response: Response | None = None,
        error: str | Exception | None = None,
    ):
        self.data: Any = data
        self.response: Response | None = response
        self.success: bool = True
        self.error: str | None = None

        # Если передан error или data is None, то результат неуспешный
        if error or self.data is None:
            self.success = False

        if isinstance(error, Exception):
            self.error = str(error)
        else:
            self.error = error
