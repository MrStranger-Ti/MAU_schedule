from typing import TypeVar, Any

from django.db.models import Model
from model_bakery import baker

T = TypeVar("T", bound=Model)


class ModelFactory:
    model: type[T] | None = None
    kwargs: dict[str, Any] | None = None

    def __init__(self, quantity: int = 1, prepare: bool = False):
        if self.model is None:
            raise AttributeError("Attr 'model' must be set.")

        self.quantity = quantity
        self.prepare = prepare
        self.maker = baker.prepare if prepare else baker.make

    def make(self, **kwargs) -> list[T] | T:
        test_data = self._get_factory(**kwargs)
        prepared_data = self._prepare_data(test_data)
        return prepared_data

    def _get_factory(self, **extra_kwargs):
        kwargs = self.get_kwargs() or {}
        kwargs.update(extra_kwargs)
        return self.maker(_model=self.model, _quantity=self.quantity, **kwargs)

    def _prepare_data(self, test_data: list[T]) -> list[T] | T:
        if self.prepare:
            self._change_prepared_data(test_data)
        else:
            self._change_made_data(test_data)

        if self.quantity == 1:
            return test_data[0]

        return test_data

    def get_kwargs(self) -> dict[str:Any] | None:
        return self.kwargs

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
