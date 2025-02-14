from typing import TypeVar, Any

from django.db.models import Model
from model_bakery import baker

T = TypeVar("T", bound=Model)


class ModelFactory:
    model: type[T] | None = None
    kwargs: dict[str, Any] | None = None

    def __init__(self, quantity: int = 1, prepare: bool = False):
        self.quantity = quantity
        self.prepare = prepare
        self._maker = baker.prepare if prepare else baker.make

    def make(self, **kwargs) -> list[T] | T | dict[str, Any] | list[dict[str, Any]]:
        test_data = self._build(**kwargs)
        prepared_data = self._prepare_data(test_data)
        return prepared_data

    def _build(self, **extra_kwargs):
        kwargs = self.get_kwargs()
        kwargs.update(extra_kwargs)

        try:
            return self._maker(**kwargs)
        except AttributeError:
            raise AttributeError("Attr 'model' must be set.")

    def _prepare_data(
        self,
        test_data: list[T],
    ) -> list[T] | T | dict[str, Any] | list[dict[str, Any]]:
        if self.prepare:
            self._change_prepared_data(test_data)
        else:
            self._change_made_data(test_data)

        if self.quantity == 1:
            return test_data[0]

        return test_data

    def get_kwargs(self) -> dict[str, Any] | None:
        kwargs = self.kwargs or {}
        kwargs["_model"] = self.model
        kwargs["_quantity"] = self.quantity
        return kwargs

    def _change_made_data(self, test_data):
        """
        Change objects after saving in db with baker.make().
        """
        pass

    def _change_prepared_data(self, test_data):
        """
        Change objects after prepared with baker.prepare().
        """
        pass
