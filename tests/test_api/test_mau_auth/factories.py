from typing import Callable, Any
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
        return {
            "_fill_optional": True,
            "full_name": "Petrov Petr Petrovich",
            "institute": self._maker(MauInstitute),
            "groups": self._maker(Group, _quantity=5),
            "user_permissions": self._maker(Permission, _quantity=5),
        }

    def _change_made_data(self, users_data: list[User]) -> None:
        for instance in users_data:
            instance.email = instance.email.split("@")[0] + "@mauniver.ru"
            instance.set_password(instance.password)

        User.objects.bulk_update(users_data, ["email", "password"])

    def serialize(self, obj: User, **kwargs) -> dict[str, Any]:
        json_data = super().serialize(obj, **kwargs)

        if obj.last_login:
            last_login = obj.date_joined.astimezone(tz=ZoneInfo("Europe/Moscow"))
            json_data["last_login"] = last_login.isoformat()

        if obj.date_joined:
            date_joined = obj.last_login.astimezone(tz=ZoneInfo("Europe/Moscow"))
            json_data["date_joined"] = date_joined.isoformat()

        if obj.id:
            json_data["groups"] = [instance.id for instance in obj.groups.all()]
            json_data["user_permissions"] = [
                instance.id for instance in obj.user_permissions.all()
            ]

        return json_data
