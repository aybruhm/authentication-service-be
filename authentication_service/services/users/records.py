# Typing Imports
from typing import Tuple

# Account Service Imports
from authentication_service.models import AccountUser

# Django Imports
from django.db import transaction

# Users Timestamps Imports
from authentication_service.services.users.timestamps import get_now

# Third Party Imports
from rest_api_payload import success_response


def user_record_login(*, user: AccountUser) -> AccountUser:
    """
    Set the last login of the user to now
    """
    
    user.last_login = get_now()
    user.save(update_fields=["last_login"])
    return user


def user_create(email, password=None, **extra_fields) -> AccountUser:
    """
    Creates an active user account
    """
    
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
    """
    Get authentication user from Google payload
    """
   
    payload = success_response(
        status=True, 
        message="User authenticated with Google!",
        data = {
            'id': user.id,
            'uuid': user.uuid,
            'name': user.fullname,
            'email': user.email
        }
    )
    return payload


def jwt_response_payload_handler(token, user=None, request=None):
    """
    JWT response payload handler that returns a 
    token with the google authenticated user
    """
    
    return {
        'token': token,
        'me': user_get_me(user=user),
    }


@transaction.atomic
def user_get_or_create(*, email: str, **extra_data) -> Tuple[AccountUser, bool]:
    """
    Get or create a user account
    """
    
    user = AccountUser.objects.filter(email=email).first()

    if user is not None:
        return user, False

    return user_create(email=email, **extra_data), True