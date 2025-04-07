from typing import Any

from requests import Response


class ParserResponse:
    """
    Ответ от парсера.

    Содержит распарсенную информацию и дополнительные данные, которые получил парсер.

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
        self.data: Any = data or None
        self.response: Response | None = response
        self.success: bool = True
        self.error: str | None = None

        # Если передан error или data is None, то результат неуспешный
        if error or not self.data:
            self.success = False

        self.error = str(error)
