# Typing Imports
from typing import Tuple

# Account Service Imports
from account_service.models import AccountUser

# Django Imports
from django.db import transaction
from django.core.management.utils import get_random_secret_key

# Users Timestamps Imports
from account_service.services.users.timestamps import get_now

# Third Party Imports
from rest_api_payload import success_response


def user_record_login(*, user: AccountUser) -> AccountUser:
    user.last_login = get_now()
    user.save()

    return user


def user_create(email, password=None, **extra_fields) -> AccountUser:
    extra_fields = {
        'is_staff': False,
        'is_superuser': False,
        'is_active': True,
        'is_email_active': True,
        **extra_fields
    }

    user = AccountUser(email=email, **extra_fields)

    if password:
        user.set_password(password)
    else:
        user.set_unusable_password()

    user.full_clean()
    user.save()

    return user


def user_get_me(*, user: AccountUser):
    payload = success_response(
        status="success", message="User authenticated with Google!",
        data = {
            'id': user.id,
            'uuid': user.uuid,
            'name': user.fullname,
            'email': user.email
        }
    )
    return payload


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'me': user_get_me(user=user),
    }


@transaction.atomic
def user_get_or_create(*, email: str, **extra_data) -> Tuple[AccountUser, bool]:
    user = AccountUser.objects.filter(email=email).first()

    if user:
        return user, False

    return user_create(email=email, **extra_data), True