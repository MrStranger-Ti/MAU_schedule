import pytest
from django.contrib.auth import get_user_model

from model_bakery import baker

User = get_user_model()


@pytest.fixture
def user_factory():
    def wrapper(n: int = 1):
        test_data = baker.make(
            _model=User,
            _quantity=n,
        )
        if n == 1:
            return test_data[0]
        return test_data

    return wrapper
