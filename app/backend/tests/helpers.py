import json
from typing import Any, TypeVar
from zoneinfo import ZoneInfo

from django.conf import settings
from django.db.models import Model, DateField, DateTimeField
from django.forms import model_to_dict
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

T = TypeVar("T", bound=Model)


class PermissionHelper:
    def has_permission(self, client: APIClient, url: str, **kwargs) -> bool:
        response = client.get(url, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            return True
        return False


class ResponseDataHelper:
    def get_results(self, response: Response) -> list[dict[str, Any]]:
        response_data = json.loads(response.content)
        results = response_data.get("results", response_data)
        return results

    def in_response(self, expected_data: dict, response: Response) -> bool:
        response_data = self.get_results(response)
        for field_name, value in expected_data.items():
            if field_name not in response_data or response_data[field_name] != value:
                return False

        return True

    def equals_expected_and_response(
        self,
        expected_data: Any,
        response: Response,
    ) -> bool:
        results = self.get_results(response)
        return expected_data == results


class SerializeHelper:
    def serialize_all(self, test_data: list[T]) -> list[dict[str, Any]]:
        serialized_data = []
        for obj in test_data:
            serialized_obj = self.serialize(obj)
            serialized_data.append(serialized_obj)

        return serialized_data

    def serialize(self, obj: T, **kwargs) -> dict[str, Any]:
        """
        Convert obj to dict if 'serialize' is True.

        Serialize DateField manually because model_to_dict function
        just ignore this field if param auto_now_add=True. It sets editable=False on field.
        """
        serialized = model_to_dict(obj, **kwargs)
        tp: type[T] = type(obj)
        for field in tp._meta.fields:
            obj_field_value = getattr(obj, field.name)
            if obj_field_value is None:
                continue

            if isinstance(field, DateTimeField):
                date_time_field_tz = obj_field_value.astimezone(
                    tz=ZoneInfo(settings.TIME_ZONE)
                )
                serialized[field.name] = date_time_field_tz.isoformat()

            elif isinstance(field, DateField):
                serialized[field.name] = obj_field_value.isoformat()

        # getting ids for relationships instead instances
        if obj.id is not None:
            for field in tp._meta.many_to_many:
                if obj_m2m_field_value := getattr(obj, field.name):
                    serialized[field.name] = [
                        relative.id for relative in obj_m2m_field_value.all()
                    ]

        return serialized


class Helper(
    PermissionHelper,
    ResponseDataHelper,
    SerializeHelper,
):
    pass
