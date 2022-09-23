# Rest Framework Imports
from rest_framework.response import Response

# SimpleJWT Imports
from rest_framework_simplejwt.settings import api_settings

# Account Service Models
from authentication_service.models import AccountUser
from authentication_service.services.users.records import user_record_login


def jwt_login(*, response: Response, user: AccountUser) -> Response:
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)

    if api_settings.JWT_AUTH_COOKIE:
        response.set_cookie(
            api_settings.JWT_AUTH_COOKIE,
            token,
            httponly=True
        )

    user_record_login(user=user)

    return response