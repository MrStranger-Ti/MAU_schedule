from django.contrib.auth import get_user_model
from django.http import HttpRequest
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from mau_auth.models import MauUser

User: MauUser = get_user_model()


class CookieTokenAuthentication(TokenAuthentication):
    def authenticate(self, request: HttpRequest) -> tuple[User, str] | None:
        token = request.COOKIES.get("auth_token")
        if token is None:
            return None

        user = User.objects.filter(auth_token__key=token).first()
        if user is None:
            raise AuthenticationFailed("Invalid authorization token.")

        return user, token
