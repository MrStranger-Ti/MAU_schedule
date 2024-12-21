from rest_framework import status
from rest_framework.test import APIClient


class PermissionHelper:
    def has_permission(self, client: APIClient, url: str, **kwargs) -> bool:
        response = client.get(url, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            return True

        elif response.status_code in (
            status.HTTP_403_FORBIDDEN,
            status.HTTP_401_UNAUTHORIZED,
        ):
            return False

        else:
            assert False, f"Response has unexpected status ({response.status_code})."


class MatchingJSONHelper:
    def in_expected(self, response_data: dict, expected_data: dict) -> bool:
        for field_name, value in expected_data.items():
            if field_name not in response_data or response_data[field_name] != value:
                return False

        return True


class Helper(MatchingJSONHelper, PermissionHelper):
    pass
