from typing import Any
from zoneinfo import ZoneInfo

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

from mau_auth.models import MauUser
from schedule.models import MauInstitute
from tests.test_api.factories import ModelFactory

User: type[MauUser] = get_user_model()


class UserFactory(ModelFactory):
    model = User

    def get_kwargs(self) -> dict[str:Any]:
        kwargs = super().get_kwargs()
        kwargs.update(
            {
                "_fill_optional": True,
                "full_name": "Petrov Petr Petrovich",
                "institute": self._maker(MauInstitute),
                "groups": self._maker(Group, _quantity=5),
                "user_permissions": self._maker(Permission, _quantity=5),
            }
        )
        return kwargs

    def _change_made_data(self, users_data: list[User]) -> None:
        for instance in users_data:
            instance.email = instance.email.split("@")[0] + "@mauniver.ru"
            instance.set_password(instance.password)

        User.objects.bulk_update(users_data, ["email", "password"])
