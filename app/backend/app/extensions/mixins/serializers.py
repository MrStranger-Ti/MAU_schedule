from typing import Any


class ContextMixin:
    def get_context(self, key: str) -> Any:
        value = self.context.get(key)
        if value is None:
            raise ValueError(f"Context param {key!r} not set.")

        return value
