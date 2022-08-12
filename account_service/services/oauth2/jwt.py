from django.http import HttpResponse

from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.compat import set_cookie_with_token

from account_service.models import AccountUser
from users.services import user_record_login


def jwt_login(*, response: HttpResponse, user: AccountUser) -> HttpResponse:
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)

    if api_settings.JWT_AUTH_COOKIE:
        set_cookie_with_token(response, api_settings.JWT_AUTH_COOKIE, token)

    user_record_login(user=user)

    return response